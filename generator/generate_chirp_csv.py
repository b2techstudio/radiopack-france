#!/usr/bin/env python3
"""Generate generic CHIRP CSV files from RadioPack France JSON datasets.

CSV generation has no third-party dependency.

Published versioned regional packs are intentionally not overwritten here:
- Annecy–Alpes–Léman v0.2 is built by the Astro pack library;
- Normandie v0.3.1 is a frozen published artifact and must only change through
  an explicit new regional version and review.

By default, generic generated files are written to their normal repository
locations. Tests pass --output-root to recreate the same relative paths in an
isolated temporary directory without touching tracked public files.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable

CHIRP_COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
    "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
    "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]

OUTPUT_JOBS = [
    (
        "dataset",
        Path("data/national/pmr446.json"),
        Path("website/public/downloads/national/radiopack-france-pmr446-rx.csv"),
    ),
    (
        "dataset",
        Path("data/national/marine-vhf-rx.json"),
        Path("website/public/downloads/national/radiopack-france-marine-vhf-rx.csv"),
    ),
    (
        "dataset",
        Path("data/national/amateur-listening-rx.json"),
        Path("website/public/downloads/national/radiopack-france-amateur-listening-rx.csv"),
    ),
    (
        "dataset",
        Path("data/national/amateur-calls-rx.json"),
        Path("website/public/downloads/national/radiopack-france-amateur-calls-rx.csv"),
    ),
    (
        "dataset",
        Path("data/regions/normandie/repeaters-analog-rx.json"),
        Path("website/public/downloads/normandie/radiopack-france-normandie-repeaters-rx.csv"),
    ),
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_channel(channel: dict[str, Any], location: int) -> None:
    required = {"name", "frequency_mhz", "mode", "step_khz", "tx_policy", "comment"}
    missing = sorted(required.difference(channel))
    if missing:
        raise ValueError(f"Memoire {location}: champs manquants: {', '.join(missing)}")
    if len(str(channel["name"])) > 10:
        raise ValueError(f"Memoire {location}: nom trop long pour l'ecran UV-K5: {channel['name']}")
    if channel["mode"] not in {"FM", "NFM", "AM"}:
        raise ValueError(f"Memoire {location}: mode non pris en charge: {channel['mode']}")
    if not 0 <= location <= 199:
        raise ValueError(f"Numero de memoire hors limite UV-K5: {location}")
    if float(channel["step_khz"]) <= 0:
        raise ValueError(f"Memoire {location}: pas invalide")


def chirp_row(location: int, channel: dict[str, Any]) -> dict[str, Any]:
    validate_channel(channel, location)
    duplex = "" if channel.get("tx_policy") == "licensed_only" else "off"
    return {
        "Location": location,
        "Name": channel["name"],
        "Frequency": f"{float(channel['frequency_mhz']):.6f}",
        "Duplex": duplex,
        "Offset": "0.000000",
        "Tone": "",
        "rToneFreq": "88.5",
        "cToneFreq": "88.5",
        "DtcsCode": "023",
        "DtcsPolarity": "NN",
        "RxDtcsCode": "023",
        "CrossMode": "Tone->Tone",
        "Mode": channel["mode"],
        "TStep": f"{float(channel['step_khz']):.2f}",
        "Skip": channel.get("skip", ""),
        "Power": "",
        "Comment": channel["comment"],
        "URCALL": "",
        "RPT1CALL": "",
        "RPT2CALL": "",
        "DVCODE": "",
    }


def validate_placed(placed: list[tuple[int, dict[str, Any]]]) -> None:
    locations = [location for location, _ in placed]
    names = [str(channel["name"]) for _, channel in placed]
    if len(locations) != len(set(locations)):
        duplicates = sorted({str(loc) for loc in locations if locations.count(loc) > 1})
        raise ValueError(f"Memoires en conflit: {', '.join(duplicates)}")
    if len(names) != len(set(names)):
        duplicates = sorted({name for name in names if names.count(name) > 1})
        raise ValueError(f"Noms de memoires dupliques: {', '.join(duplicates)}")
    if len(placed) > 200:
        raise ValueError(f"Le pack contient {len(placed)} memoires; maximum UV-K5: 200")


def write_csv(placed: Iterable[tuple[int, dict[str, Any]]], output: Path) -> int:
    items = sorted(list(placed), key=lambda item: item[0])
    validate_placed(items)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHIRP_COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for location, channel in items:
            writer.writerow(chirp_row(location, channel))
    return len(items)


def dataset_items(root: Path, dataset_path: Path, start_location: int = 0):
    dataset = load_json(root / dataset_path)
    return [(start_location + index, channel) for index, channel in enumerate(dataset["channels"])]


def generate_dataset(root: Path, dataset_path: Path, output: Path) -> int:
    return write_csv(dataset_items(root, dataset_path), output)


def generate_pack(root: Path, pack_path: Path, output: Path) -> int:
    """Build a pack explicitly when called by version/review tooling.

    The generic CLI does not schedule frozen published regional packs.
    """
    pack = load_json(root / pack_path)
    placed: list[tuple[int, dict[str, Any]]] = []
    next_location = 0

    for entry in pack.get("datasets", []):
        if isinstance(entry, str):
            path = Path(entry)
            start = next_location
        else:
            path = Path(entry["path"])
            start = int(entry.get("start_location", next_location))
        items = dataset_items(root, path, start)
        placed.extend(items)
        if items:
            next_location = max(location for location, _ in items) + 1

    for source_channel in pack.get("local_channels", []):
        channel = dict(source_channel)
        location = int(channel.pop("location", next_location))
        placed.append((location, channel))
        next_location = max(next_location, location + 1)

    return write_csv(placed, output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generateur CSV CHIRP - RadioPack France")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help="Racine de sortie alternative; conserve les chemins relatifs sans modifier le dépôt source.",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output_root = args.output_root.resolve() if args.output_root is not None else root

    for kind, source, output_relative in OUTPUT_JOBS:
        output = output_root / output_relative
        count = (
            generate_dataset(root, source, output)
            if kind == "dataset"
            else generate_pack(root, source, output)
        )
        print(f"OK: {output_relative} ({count} memoires)")

    if output_root != root:
        print(f"INFO: sortie isolée: {output_root}")
    print("INFO: Annecy–Alpes–Léman v0.2 est généré par website/src/lib/annecyPack.ts")
    print("INFO: Normandie v0.3.1 est un artefact publié figé; une évolution exige une nouvelle version")


if __name__ == "__main__":
    main()
