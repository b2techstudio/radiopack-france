#!/usr/bin/env python3
"""Run the focused local validation suite for the active Normandie v0.4 work."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOCUSED_TESTS = [
    "tests/test_normandie_v04_candidate_delta.py",
    "tests/test_normandie_v04_internal_candidate.py",
    "tests/test_normandie_v04_promotion_gates.py",
    "tests/test_normandie_v04_field_tools.py",
    "tests/test_normandie_v04_readiness.py",
    "tests/test_normandie_v04_evidence_pipeline.py",
    "tests/test_normandie_v04_decision_pipeline.py",
    "tests/test_normandie_v04_prepublication_audit.py",
]

EXTENDED_TESTS = [
    "tests/test_paired_rx_policy.py",
    "tests/test_paired_rx_memory_plan.py",
    "tests/test_site_files.py",
    "tests/test_pack_registry.py",
]


def run_test(relative_path: str) -> None:
    path = ROOT / relative_path
    if not path.is_file():
        raise FileNotFoundError(path)
    print(f"\n=== {relative_path} ===", flush=True)
    subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extended", action="store_true", help="Also run paired-RX and public-site guard tests.")
    args = parser.parse_args()
    tests = list(FOCUSED_TESTS)
    if args.extended:
        tests.extend(EXTENDED_TESTS)
    for test in tests:
        run_test(test)
    print(f"\nNORMANDIE V0.4 LOCAL CHECKS: {len(tests)} test scripts passed (extended={str(args.extended).lower()})")


if __name__ == "__main__":
    main()
