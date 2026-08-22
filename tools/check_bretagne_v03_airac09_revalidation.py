#!/usr/bin/env python3
"""Validate Bretagne v0.3 AIRAC 09/26 evidence without publishing or mutating a candidate."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = Path("research/bretagne-v0.3/airac09-readiness.json")
TEMPLATE_PATH = Path("research/bretagne-v0.3/airac09-revalidation-template.json")

EXPECTED_BASELINE = [
    (130, "AIR-EMERG", 121.500),
    (131, "RNS-COT-A", 120.350),
    (132, "RNS-NORD", 126.950),
    (133, "RNS-SUD", 134.000),
    (134, "RNS-COT-B", 134.200),
    (135, "RNS-GND", 121.730),
    (136, "RNS-TWR", 120.505),
    (137, "RNS-ATIS", 136.405),
    (138, "BES-IRO1", 119.575),
    (139, "BES-IRO2", 135.830),
    (140, "BES-APP", 125.860),
    (141, "BES-TWR", 120.105),
    (142, "BES-ATIS", 129.355),
    (143, "DIN-TWR", 120.155),
    (144, "DIN-ATIS", 124.580),
    (145, "QUIM-TWR", 118.625),
]
ALLOWED_DECISIONS = {"unchanged", "changed", "removed"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_iso_date(value: str | None, label: str, errors: list[str]) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} is not a valid ISO date: {value!r}")
        return None


def same_frequency(left: Any, right: float) -> bool:
    try:
        return abs(float(left) - right) <= 0.000001
    except (TypeError, ValueError):
        return False


def validate_configuration(readiness: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("status") != "future_cycle_source_available_not_current_readiness_prepared":
        errors.append("unexpected readiness status")
    if readiness.get("pack") != "Bretagne" or readiness.get("target_version") != "0.3":
        errors.append("unexpected readiness pack/version")
    if readiness.get("public_base", {}).get("version") != "0.2":
        errors.append("unexpected public base version")
    if readiness.get("public_base", {}).get("memory_count") != 151:
        errors.append("unexpected public base memory count")
    if readiness.get("candidate", {}).get("memory_count") != 151:
        errors.append("unexpected candidate memory count")
    if readiness.get("candidate", {}).get("aviation_memory_count") != 16:
        errors.append("unexpected aviation memory count")
    if readiness.get("candidate", {}).get("public_export_allowed") is not False:
        errors.append("readiness must not allow public export")
    if readiness.get("candidate", {}).get("public_release_allowed") is not False:
        errors.append("readiness must not allow public release")

    if evidence.get("pack") != "Bretagne" or evidence.get("target_version") != "0.3":
        errors.append("unexpected evidence pack/version")
    if evidence.get("cycle") != "AIRAC 09/26":
        errors.append("evidence cycle must be AIRAC 09/26")
    if evidence.get("effective_from") != "2026-09-03":
        errors.append("AIRAC 09/26 effective_from drift")
    if evidence.get("effective_until_inclusive") != "2026-09-30":
        errors.append("AIRAC 09/26 effective_until drift")
    if evidence.get("direct_xml_field_match_claimed") is not False and evidence.get("xml_export_bytes_extracted") is not True:
        errors.append("direct XML field-match claim requires extracted XML bytes")

    memories = evidence.get("memories")
    if not isinstance(memories, list) or len(memories) != 16:
        errors.append("evidence must contain exactly 16 aviation memories")
        return errors

    seen_locations: set[int] = set()
    seen_names: set[str] = set()
    for item, (location, name, frequency) in zip(memories, EXPECTED_BASELINE, strict=True):
        if item.get("location") != location:
            errors.append(f"location drift at expected {location}")
        if item.get("name") != name:
            errors.append(f"name drift at location {location}")
        if not same_frequency(item.get("baseline_frequency_mhz"), frequency):
            errors.append(f"baseline frequency drift for {name}")
        if location in seen_locations:
            errors.append(f"duplicate location {location}")
        if name in seen_names:
            errors.append(f"duplicate name {name}")
        seen_locations.add(location)
        seen_names.add(name)
    return errors


def evaluate(root: Path, evidence_path: Path, as_of: date) -> dict[str, Any]:
    readiness = load_json(root / READINESS_PATH)
    evidence = load_json(evidence_path)
    errors = validate_configuration(readiness, evidence)

    cycle_start = date.fromisoformat("2026-09-03")
    cycle_end = date.fromisoformat("2026-09-30")
    cycle_is_current = cycle_start <= as_of <= cycle_end
    if as_of < cycle_start:
        cycle_phase = "future_not_current"
    elif as_of > cycle_end:
        cycle_phase = "expired_require_newer_cycle"
    else:
        cycle_phase = "current"

    primary_verified = evidence.get("current_cycle_primary_source_verified") is True
    primary_verified_on = parse_iso_date(
        evidence.get("current_cycle_primary_source_verified_on"),
        "current_cycle_primary_source_verified_on",
        errors,
    )
    primary_verification_valid = (
        primary_verified
        and primary_verified_on is not None
        and cycle_start <= primary_verified_on <= as_of
        and cycle_is_current
        and bool(evidence.get("current_cycle_primary_source_url"))
    )
    if primary_verified and not primary_verification_valid:
        errors.append("current-cycle primary verification date is outside the effective/current window")

    resolved_count = 0
    unresolved_names: list[str] = []
    changed_names: list[str] = []
    removed_names: list[str] = []

    for item, (_, name, baseline_frequency) in zip(evidence["memories"], EXPECTED_BASELINE, strict=True):
        decision = item.get("decision")
        if decision is None:
            unresolved_names.append(name)
            continue
        if decision not in ALLOWED_DECISIONS:
            errors.append(f"invalid decision for {name}: {decision!r}")
            continue

        source_cycle = item.get("source_cycle")
        source_effective_from = item.get("source_effective_from")
        source_url = item.get("source_url")
        evidence_note = item.get("evidence_note")
        if source_cycle != "AIRAC 09/26":
            errors.append(f"{name}: resolved decision requires source_cycle AIRAC 09/26")
        if source_effective_from != "2026-09-03":
            errors.append(f"{name}: resolved decision requires AIRAC 09/26 effective date")
        if not source_url:
            errors.append(f"{name}: resolved decision requires source_url")
        if not evidence_note:
            errors.append(f"{name}: resolved decision requires evidence_note")

        current_frequency = item.get("current_frequency_mhz")
        if decision == "unchanged":
            if not same_frequency(current_frequency, baseline_frequency):
                errors.append(f"{name}: unchanged decision must retain baseline frequency")
        elif decision == "changed":
            if current_frequency is None:
                errors.append(f"{name}: changed decision requires current_frequency_mhz")
            elif same_frequency(current_frequency, baseline_frequency):
                errors.append(f"{name}: changed decision must differ from baseline frequency")
            else:
                changed_names.append(name)
        elif decision == "removed":
            if current_frequency is not None:
                errors.append(f"{name}: removed decision requires current_frequency_mhz=null")
            removed_names.append(name)
        resolved_count += 1

    human_review = evidence.get("human_review", {})
    human_reviewed = human_review.get("completed") is True
    reviewed_on = parse_iso_date(human_review.get("reviewed_on"), "human_review.reviewed_on", errors)
    human_review_valid = (
        human_reviewed
        and reviewed_on is not None
        and cycle_start <= reviewed_on <= as_of
        and cycle_is_current
        and bool(human_review.get("reviewer_note"))
    )
    if human_reviewed and not human_review_valid:
        errors.append("human review date/note is not valid for the current AIRAC 09/26 window")

    all_memories_resolved = resolved_count == 16 and not unresolved_names
    candidate_rebuild_allowed = (
        cycle_is_current
        and primary_verification_valid
        and all_memories_resolved
        and human_review_valid
        and not errors
    )

    return {
        "schema_version": "1.0",
        "status": "airac09_revalidation_readiness_evaluation_not_public",
        "pack": "Bretagne",
        "target_version": "0.3",
        "as_of": as_of.isoformat(),
        "cycle": "AIRAC 09/26",
        "cycle_phase": cycle_phase,
        "cycle_is_current": cycle_is_current,
        "primary_cycle_source_verified": primary_verified,
        "primary_cycle_source_verification_valid": primary_verification_valid,
        "aviation_memory_count": 16,
        "resolved_memory_count": resolved_count,
        "unresolved_memory_count": len(unresolved_names),
        "unresolved_memory_names": unresolved_names,
        "changed_memory_names": changed_names,
        "removed_memory_names": removed_names,
        "human_review_completed": human_reviewed,
        "human_review_valid": human_review_valid,
        "validation_errors": errors,
        "candidate_rebuild_allowed": candidate_rebuild_allowed,
        "candidate_rebuild_is_publication": False,
        "automatic_candidate_mutation_allowed": False,
        "automatic_publication_allowed": False,
        "public_release_allowed": False,
        "next_action": (
            "wait_until_2026_09_03"
            if as_of < cycle_start
            else "use_newer_current_cycle"
            if as_of > cycle_end
            else "complete_current_airac09_primary_revalidation_and_human_review"
            if not candidate_rebuild_allowed
            else "rebuild_internal_candidate_then_run_separate_prepublication_gates"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--evidence", type=Path, default=TEMPLATE_PATH)
    parser.add_argument("--as-of", required=True, help="Explicit YYYY-MM-DD evaluation date")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-candidate-rebuild-ready", action="store_true")
    args = parser.parse_args()

    try:
        as_of = date.fromisoformat(args.as_of)
    except ValueError as exc:
        raise SystemExit(f"invalid --as-of date: {args.as_of!r}") from exc

    root = args.root.resolve()
    evidence_path = args.evidence if args.evidence.is_absolute() else root / args.evidence
    report = evaluate(root, evidence_path.resolve(), as_of)
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output_path = args.output if args.output.is_absolute() else root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    print(text, end="")

    if args.require_candidate_rebuild_ready and not report["candidate_rebuild_allowed"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
