#!/usr/bin/env python3
"""Generate generic CHIRP CSV files from RadioPack France JSON datasets.

No third-party dependency is required.
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

def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def validate_channel(channel: dict[str, Any], index: int) -> None:
    required = {"name", "frequency_mhz", "mode", "step_khz", "tx_policy", "comment"}
    missing = sorted(required.difference(channel))
    if missing:
        raise ValueError(f"Canal {index}: champs manquants: {', '.join(missing)}")
    if len(str(channel["name"])) > 10:
        raise ValueError(f"Canal {index}: nom trop long pour l'écran UV-K5: {channel['name']}")
    if channel["mode"] not in {"FM", "NFM", "AM"}:
        raise ValueError(f"Canal {index}: mode non pris en charge: {channel['mode']}")
    frequency = float(channel["frequency_mhz"])
    if not 18 <= frequency <= 1300:
        raise ValueError(f"Canal {index}: fréquence hors plage raisonnable: {frequency}")
    if float(channel["step_khz"]) <= 0:
        raise ValueError(f"Canal {index}: pas invalide")

def chirp_row(location: int, channel: dict[str, Any]) -> dict[str, Any]:
    validate_channel(channel, location)
    # Public releases are safety-first. Only an explicitly licensed dataset
    # can leave TX enabled; all current Sprint 3 public datasets are RX-only.
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

def write_csv(channels: Iterable[dict[str, Any]], output: Path) -> int:
    channel_list = list(channels)
    names = [str(channel["name"]) for channel in channel_list]
    if len(names) != len(set(names)):
        duplicates = sorted({name for name in names if names.count(name) > 1})
        raise ValueError(f"Noms de mémoires dupliqués: {', '.join(duplicates)}")
    rows = [chirp_row(i, channel) for i, channel in enumerate(channel_list)]
    if len(rows) > 200:
        raise ValueError(f"Le pack contient {len(rows)} mémoires; maximum UV-K5 configuré: 200")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHIRP_COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)

def generate_dataset(root: Path, dataset_path: Path, output: Path) -> int:
    dataset = load_json(root / dataset_path)
    return write_csv(dataset["channels"], output)

def generate_pack(root: Path, pack_path: Path, output: Path) -> int:
    pack = load_json(root / pack_path)
    channels: list[dict[str, Any]] = []
    for dataset_path in pack.get("datasets", []):
        channels.extend(load_json(root / dataset_path)["channels"])
    channels.extend(pack.get("local_channels", []))
    if len(channels) > int(pack.get("max_memories", 200)):
        raise ValueError("Le pack dépasse sa limite de mémoires")
    return write_csv(channels, output)

def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur CSV CHIRP — RadioPack France")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    jobs = [
        ("dataset", Path("data/national/pmr446.json"),
         root / "website/public/downloads/national/radiopack-france-pmr446-rx.csv"),
        ("dataset", Path("data/national/marine-vhf-rx.json"),
         root / "website/public/downloads/national/radiopack-france-marine-vhf-rx.csv"),
        ("dataset", Path("data/national/amateur-listening-rx.json"),
         root / "website/public/downloads/national/radiopack-france-amateur-listening-rx.csv"),
        ("pack", Path("data/regions/normandie/pack.json"),
         root / "website/public/downloads/normandie/radiopack-france-normandie-v0.2.csv"),
    ]

    for kind, source, output in jobs:
        count = (
            generate_dataset(root, source, output)
            if kind == "dataset"
            else generate_pack(root, source, output)
        )
        print(f"OK: {output.relative_to(root)} ({count} mémoires)")

if __name__ == "__main__":
    main()
