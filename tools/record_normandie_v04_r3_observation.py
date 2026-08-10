#!/usr/bin/env python3
"""Append one RX-only R3/Mortain field observation to the research log."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIELD_PATH = Path("research/normandie-v0.4/r3-mortain-field-validation.json")
PACK_PATH = Path("research/normandie-v0.4/r3-validation-pack.json")
ALLOWED_CONFIDENCE = {"none", "low", "medium", "high", "unmistakable", "confirmed"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_observation(root: Path, observation: dict[str, Any]) -> None:
    pack = load_json(root / PACK_PATH)
    allowed_frequencies = {round(float(item["frequency_mhz"]), 6) for item in pack["memories"]}
    frequency = round(float(observation["frequency_mhz"]), 6)
    if frequency not in allowed_frequencies:
        raise ValueError(f"Frequency {frequency:.6f} MHz is not in the R3 validation mini-pack")

    intelligibility = int(observation["intelligibility_0_to_5"])
    if not 0 <= intelligibility <= 5:
        raise ValueError("intelligibility_0_to_5 must be between 0 and 5")

    confidence = str(observation["identification_confidence"]).lower()
    if confidence not in ALLOWED_CONFIDENCE:
        raise ValueError(f"Unsupported identification confidence: {confidence}")

    for key in ("date_local", "time_local", "location_description", "receiver_model", "antenna_description"):
        if not str(observation.get(key, "")).strip():
            raise ValueError(f"{key} is required")

    if observation["signal_detected"] is False and intelligibility != 0:
        raise ValueError("A no-signal observation must use intelligibility 0")
    if observation["signal_detected"] is False and confidence != "none":
        raise ValueError("A no-signal observation must use identification confidence 'none'")


def append_observation(root: Path, observation: dict[str, Any]) -> int:
    validate_observation(root, observation)
    field_path = root / FIELD_PATH
    field = load_json(field_path)
    if field["rules"]["public_export_allowed"] is not False or field["rules"]["no_tx_test_required_or_allowed"] is not True:
        raise ValueError("R3 field log must remain RX-only and non-public")

    observations = field.setdefault("observations", [])
    observations.append(observation)

    temp_path = field_path.with_suffix(field_path.suffix + ".tmp")
    temp_path.write_text(json.dumps(field, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp_path.replace(field_path)
    return len(observations)


def build_observation(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "date_local": args.date,
        "time_local": args.time,
        "location_description": args.location,
        "receiver_model": args.receiver,
        "antenna_description": args.antenna,
        "frequency_mhz": float(args.frequency),
        "signal_detected": bool(args.signal_detected),
        "identification_confidence": args.confidence,
        "intelligibility_0_to_5": int(args.intelligibility),
        "signal_strength_observation": args.strength,
        "notes": args.notes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--date", required=True, help="Local date, YYYY-MM-DD")
    parser.add_argument("--time", required=True, help="Local time, HH:MM")
    parser.add_argument("--location", required=True)
    parser.add_argument("--receiver", required=True)
    parser.add_argument("--antenna", required=True)
    parser.add_argument("--frequency", required=True, type=float)
    signal = parser.add_mutually_exclusive_group(required=True)
    signal.add_argument("--signal-detected", action="store_true")
    signal.add_argument("--no-signal", dest="signal_detected", action="store_false")
    parser.add_argument("--confidence", choices=sorted(ALLOWED_CONFIDENCE), required=True)
    parser.add_argument("--intelligibility", type=int, required=True)
    parser.add_argument("--strength", default="")
    parser.add_argument("--notes", default="")
    parser.set_defaults(signal_detected=None)
    args = parser.parse_args()

    root = args.root.resolve()
    observation = build_observation(args)
    count = append_observation(root, observation)
    print(f"R3 FIELD OBSERVATION RECORDED: {count} total observations")
    print(root / FIELD_PATH)


if __name__ == "__main__":
    main()
