#!/usr/bin/env python3
"""Check age of current Normandie v0.4 revalidation evidence without changing any promotion gate."""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = Path("research/normandie-v0.4/source-freshness-policy.json")
REVALIDATION_PATH = Path("research/normandie-v0.4/blocked-station-revalidation.json")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_day(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def evaluate(root: Path, as_of: date | None = None) -> dict[str, Any]:
    policy = load_json(root / POLICY_PATH)
    revalidation = load_json(root / REVALIDATION_PATH)
    if policy["rules"]["public_export_allowed"] is not False:
        raise ValueError("Source freshness policy must remain non-public")
    if revalidation["public_export_allowed"] is not False:
        raise ValueError("Revalidation snapshot must remain non-public")

    as_of = as_of or date.today()
    classes = policy["classes"]
    station_policy = policy["station_policy"]
    station_rows = {item["id"]: item for item in revalidation["stations"]}
    if set(station_rows) != set(station_policy):
        raise ValueError("Freshness policy station set differs from revalidation snapshot")

    results: dict[str, Any] = {}
    stale_ids: list[str] = []
    for station_id, config in station_policy.items():
        row = station_rows[station_id]
        checked_on = parse_day(row["checked_on"])
        freshness_class = config["revalidation_class"]
        maximum_age = int(classes[freshness_class]["maximum_age_days"])
        age_days = (as_of - checked_on).days
        if age_days < 0:
            raise ValueError(f"Future checked_on date for {station_id}")
        fresh = age_days <= maximum_age
        if not fresh:
            stale_ids.append(station_id)
        results[station_id] = {
            "checked_on": checked_on.isoformat(),
            "freshness_class": freshness_class,
            "maximum_age_days": maximum_age,
            "age_days": age_days,
            "fresh": fresh,
            "stale_state_is_negative_operational_evidence": False,
        }

    return {
        "schema_version": "1.0",
        "status": "source_freshness_check_not_public",
        "as_of": as_of.isoformat(),
        "all_revalidations_fresh": not stale_ids,
        "stale_station_count": len(stale_ids),
        "stale_station_ids": stale_ids,
        "stations": results,
        "release_review_freshness_gate_passed": not stale_ids,
        "public_export_allowed": False,
        "rules": policy["rules"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--as-of", help="Override date as YYYY-MM-DD for deterministic checks.")
    args = parser.parse_args()
    as_of = parse_day(args.as_of) if args.as_of else None
    result = evaluate(args.root.resolve(), as_of)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["all_revalidations_fresh"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
