#!/usr/bin/env python3
"""Build an internal Annecy–Alpes–Léman candidate without publishing it."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

CHIRP_COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
    "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
    "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = Path("research/annecy-alpes-leman-v0.2")

BLOCKS = [
    {
        "label": "PMR446 national RX",
        "path": Path("data/national/pmr446.json"),
        "start": 0,
        "selector": "all",
    },
    {
        "label": "APRS et ISS",
        "path": Path("data/national/amateur-listening-rx.json"),
        "start": 20,
        "selector": "all",
    },
    {
        "label": "Satellites FM analogiques",
        "path": RESEARCH / "satellites-fm-inventory.json",
        "start": 26,
        "selector": "satellites",
    },
    {
        "label": "Canaux d'appel",
        "path": Path("data/national/amateur-calls-rx.json"),
        "start": 30,
        "selector": "all",
    },
    {
        "label": "Radioamateur France",
        "path": RESEARCH / "radioamateur-france-inventory.json",
        "start": 40,
        "selector": "france_verified",
    },
    {
        "label": "Radioamateur Suisse",
        "path": RESEARCH / "radioamateur-switzerland-candidates.json",
        "start": 90,
        "selector": "switzerland_verified",
    },
]

SATELLITE_ALLOWED = {
    "verified_current",
    "verified_current_limited",
    "current_amsat_list",
}
FRANCE_ALLOWED = {"verified", "verified_merged"}
SWITZERLAND_ALLOWED = {"verified_current"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def select_channels(dataset: dict[str, Any], selector: str) -> list[dict[str, Any]]:
    channels = dataset.get("channels", [])
    if selector == "all":
        return [dict(channel) for channel in channels]
    if selector == "satellites":
        return [
            dict(channel)
            for channel in channels
            if channel.get("verification") in SATELLITE_ALLOWED
        ]
    if selector == "france_verified":
        return [
            dict(channel)
            for channel in channels
            if channel.get("verification") in FRANCE_ALLOWED
        ]
    if selector == "switzerland_verified":
        return [
            dict(channel)
            for channel in channels
            if channel.get("verification") in SWITZERLAND_ALLOWED
        ]
    raise ValueError(f"Sélecteur inconnu: {selector}")


def normalize_channel(channel: dict[str, Any], source_path: Path, label: str) -> dict[str, Any]:
    normalized = dict(channel)
    normalized["tx_policy"] = "rx_only"
    normalized["source_dataset"] = source_path.as_posix()
    normalized["candidate_block"] = label
    return normalized


def chirp_row(location: int, channel: dict[str, Any]) -> dict[str, Any]:
    if len(str(channel["name"])) > 10:
        raise ValueError(f"Nom trop long: {channel['name']}")
    if channel["mode"] not in {"FM", "NFM", "AM"}:
        raise ValueError(f"Mode non pris en charge: {channel['mode']}")
    if channel.get("tx_policy") != "rx_only":
        raise ValueError(f"Politique TX interdite: {channel['name']}")
    return {
        "Location": location,
        "Name": channel["name"],
        "Frequency": f"{float(channel['frequency_mhz']):.6f}",
        "Duplex": "off",
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


def build_candidate(root: Path) -> dict[str, Any]:
    plan = load_json(root / RESEARCH / "memory-plan.json")
    placed: list[dict[str, Any]] = []

    for block in BLOCKS:
        dataset = load_json(root / block["path"])
        channels = select_channels(dataset, block["selector"])
        for index, source_channel in enumerate(channels):
            location = int(block["start"]) + index
            channel = normalize_channel(source_channel, block["path"], block["label"])
            placed.append({"location": location, "channel": channel})

    locations = [item["location"] for item in placed]
    names = [item["channel"]["name"] for item in placed]
    frequencies = [float(item["channel"]["frequency_mhz"]) for item in placed]

    if len(locations) != len(set(locations)):
        raise ValueError("Conflit de numéros de mémoire")
    if len(names) != len(set(names)):
        raise ValueError("Noms de mémoire dupliqués")
    if len(frequencies) != len(set(frequencies)):
        raise ValueError("Fréquences descendantes dupliquées dans le candidat interne")
    if len(placed) != int(plan["internal_candidate"]["expected_memory_count"]):
        raise ValueError(
            f"Total inattendu: {len(placed)} au lieu de "
            f"{plan['internal_candidate']['expected_memory_count']}"
        )

    forbidden_sources = {
        (RESEARCH / "aviation-france-pre-airac-08.json").as_posix(),
        (RESEARCH / "navigation-lakes-findings.json").as_posix(),
    }
    if forbidden_sources.intersection(
        {item["channel"]["source_dataset"] for item in placed}
    ):
        raise ValueError("Une source aviation ou lacustre a été intégrée avant validation")

    return {
        "pack": "Annecy–Alpes–Léman",
        "target_version": "0.2.0",
        "status": "internal_candidate_not_for_publication",
        "public_export_allowed": False,
        "updated": "2026-08-04",
        "memory_count": len(placed),
        "rules": [
            "Ce candidat est stocké hors du répertoire public du site.",
            "Aucune ligne aviation pre_airac_recheck n'est intégrée.",
            "Aucune fréquence lacustre n'est intégrée.",
            "Seules les lignes suisses verified_current sont intégrées.",
            "Toutes les mémoires sont en réception seule avec Duplex=off.",
            "Les montantes ISS et satellites restent des métadonnées, jamais des mémoires séparées.",
        ],
        "memories": placed,
    }


def write_candidate(candidate: dict[str, Any], json_path: Path, csv_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(candidate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHIRP_COLUMNS)
        writer.writeheader()
        for item in sorted(candidate["memories"], key=lambda row: row["location"]):
            writer.writerow(chirp_row(item["location"], item["channel"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=RESEARCH / "generated",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = root / output_dir

    candidate = build_candidate(root)
    json_path = output_dir / "annecy-alpes-leman-v0.2-internal.json"
    csv_path = output_dir / "annecy-alpes-leman-v0.2-internal.csv"
    write_candidate(candidate, json_path, csv_path)
    print(f"Internal candidate only: {candidate['memory_count']} memories")
    print(json_path)
    print(csv_path)


if __name__ == "__main__":
    main()
