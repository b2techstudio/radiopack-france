#!/usr/bin/env python3
"""Record one RX-only F5ZHA/Mortain diagnostic observation safely."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIELD_PATH = Path("research/normandie-v0.4/f5zha-mortain-validation.json")
ACCEPTED_CONFIDENCE = {"none", "low", "medium", "high", "unmistakable", "confirmed"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_observation(root: Path, observation: dict[str, Any]) -> dict[str, Any]:
    field = load_json(root / FIELD_PATH)
    allowed = {
        round(float(item["frequency_mhz"]), 6)
        for item in field["memories"]
    }
    frequency = round(float(observation["frequency_mhz"]), 6)
    if frequency not in allowed:
        raise ValueError(f"Frequency {frequency:.6f} MHz is not in the F5ZHA diagnostic pack")

    intelligibility = int(observation["intelligibility_0_to_5"])
    if not 0 <= intelligibility <= 5:
        raise ValueError("intelligibility_0_to_5 must be between 0 and 5")

    confidence = str(observation["identification_confidence"]).strip().lower()
    if confidence not in ACCEPTED_CONFIDENCE:
        raise ValueError(f"Unsupported identification confidence: {confidence}")

    signal = bool(observation["signal_detected"])
    if not signal and (intelligibility != 0 or confidence != "none"):
        raise ValueError("No-signal observations require intelligibility 0 and confidence none")

    if not str(observation.get("date_local", "")).strip():
        raise ValueError("date_local is required")
    if not str(observation.get("time_local", "")).strip():
        raise ValueError("time_local is required")
    if not str(observation.get("location_description", "")).strip():
        raise ValueError("location_description is required")

    normalized = dict(observation)
    normalized["frequency_mhz"] = frequency
    normalized["intelligibility_0_to_5"] = intelligibility
    normalized["identification_confidence"] = confidence
    normalized["signal_detected"] = signal
    normalized["diagnostic_only"] = frequency == round(float(field["validation"]["legacy_conflict_probe_mhz"]), 6)
    normalized["can_close_source_conflict"] = False
    return normalized


def append_observation(root: Path, observation: dict[str, Any]) -> int:
    path = root / FIELD_PATH
    field = load_json(path)
    normalized = validate_observation(root, observation)
    field.setdefault("observations", []).append(normalized)

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(field, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return len(field["observations"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--date", required=True, dest="date_local")
    parser.add_argument("--time", required=True, dest="time_local")
    parser.add_argument("--location", required=True, dest="location_description")
    parser.add_argument("--frequency", required=True, type=float, dest="frequency_mhz")
    parser.add_argument("--signal", choices=["yes", "no"], required=True)
    parser.add_argument("--confidence", required=True, choices=sorted(ACCEPTED_CONFIDENCE), dest="identification_confidence")
    parser.add_argument("--intelligibility", required=True, type=int, dest="intelligibility_0_to_5")
    parser.add_argument("--receiver", default="Quansheng UV-K5", dest="receiver_model")
    parser.add_argument("--antenna", default="", dest="antenna_description")
    parser.add_argument("--signal-strength", default="", dest="signal_strength_observation")
    parser.add_argument("--notes", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    observation = {
        "date_local": args.date_local,
        "time_local": args.time_local,
        "location_description": args.location_description,
        "receiver_model": args.receiver_model,
        "antenna_description": args.antenna_description,
        "frequency_mhz": args.frequency_mhz,
        "signal_detected": args.signal == "yes",
        "identification_confidence": args.identification_confidence,
        "intelligibility_0_to_5": args.intelligibility_0_to_5,
        "signal_strength_observation": args.signal_strength_observation,
        "notes": args.notes,
    }
    count = append_observation(root, observation)
    print(f"F5ZHA observation recorded safely; total observations={count}; source_conflict_closed=false")


if __name__ == "__main__":
    main()
