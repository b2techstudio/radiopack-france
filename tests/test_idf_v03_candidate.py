import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "ile-de-france-v0.3"
CANDIDATE = RESEARCH / "generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv"
MANIFEST = RESEARCH / "generated/release-candidate/candidate-manifest.json"


class IleDeFranceV03CandidateTests(unittest.TestCase):
    def test_deterministic_builder_matches_frozen_candidate(self):
        subprocess.run(
            [sys.executable, str(ROOT / "tools/build_idf_v03_candidate.py"), "--root", str(ROOT), "--check"],
            check=True,
        )

    def test_candidate_manifest_and_hash(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["candidate_memory_count"], 57)
        self.assertEqual(manifest["candidate_aviation_memory_count"], 18)
        self.assertEqual(manifest["candidate_regional_radio_memory_count"], 15)
        self.assertEqual(
            manifest["published_base_sha256"],
            "dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d",
        )
        self.assertEqual(
            manifest["candidate_sha256"],
            hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
        )
        self.assertFalse(manifest["public_export_allowed"])

    def test_candidate_contract_and_scope(self):
        with CANDIDATE.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 57)
        self.assertTrue(all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows))
        self.assertEqual(len({row["Frequency"] for row in rows}), 57)
        self.assertEqual(len({row["Name"] for row in rows}), 57)
        self.assertEqual(len({row["Location"] for row in rows}), 57)
        self.assertLessEqual(max(int(row["Location"]) for row in rows), 199)
        self.assertEqual(sum(40 <= int(row["Location"]) <= 57 for row in rows), 18)
        self.assertEqual(sum(int(row["Location"]) >= 70 for row in rows), 15)

        frequencies = {round(float(row["Frequency"]), 6) for row in rows}
        for required in [145.625, 145.025, 145.65, 145.05, 145.7, 145.1, 145.7375, 145.1375,
                         145.7625, 145.1625, 431.525, 439.125, 145.325, 430.325, 430.65]:
            self.assertIn(round(required, 6), frequencies)
        self.assertNotIn(145.6, frequencies)

    def test_aviation_pass4_closes_current_scope_only(self):
        aviation = json.loads((RESEARCH / "aviation-validation-pass4-2026-08-21.json").read_text(encoding="utf-8"))
        self.assertEqual(aviation["current_airac"], "08/26")
        self.assertEqual(aviation["final_aviation_decision"]["memory_count"], 18)
        self.assertEqual(aviation["final_aviation_decision"]["memory_delta"], 0)
        self.assertFalse(aviation["final_aviation_decision"]["additional_frequencies_promoted"])
        self.assertTrue(aviation["gates"]["aviation_revalidation_complete"])
        self.assertTrue(aviation["gates"]["frequency_delta_validated"])
        self.assertTrue(aviation["gates"]["publication_allowed_before_airac09_boundary"])
        self.assertEqual(aviation["freshness_boundary"]["publication_allowed_through_inclusive"], "2026-09-02")
        self.assertEqual(aviation["freshness_boundary"]["airac09_revalidation_required_on_or_after"], "2026-09-03")

    def test_prepublication_bundle_is_frozen_but_not_public(self):
        scope = json.loads((RESEARCH / "release-scope.json").read_text(encoding="utf-8"))
        checklist = json.loads((RESEARCH / "review-checklist.json").read_text(encoding="utf-8"))
        gates_file = json.loads((RESEARCH / "publication-gates.json").read_text(encoding="utf-8"))
        record = json.loads((RESEARCH / "publication-record.json").read_text(encoding="utf-8"))

        self.assertEqual(scope["status"], "prepublication_ready_not_published")
        self.assertTrue(scope["publication_ready"])
        self.assertFalse(scope["published"])
        self.assertFalse(scope["public_mutation_performed"])
        for key in [
            "radio_source_conflicts_closed", "radio_memory_accounting_final", "aviation_revalidation_complete",
            "deterministic_candidate_built", "rx_only_validation_passed", "rf_deduplication_passed",
            "memory_limit_passed", "review_checklist_complete", "publication_gates_zero_blockers",
            "publication_record_frozen",
        ]:
            self.assertTrue(scope["publication_gates"][key])

        self.assertEqual(checklist["status"], "completed_prepublication_not_published")
        self.assertEqual(checklist["item_count"], 12)
        self.assertEqual(checklist["reviewed_count"], 12)
        self.assertTrue(all(item["reviewed"] for item in checklist["items"]))
        self.assertFalse(checklist["public_mutation_performed"])

        self.assertEqual(gates_file["status"], "prepublication_zero_blockers_not_published")
        self.assertEqual(gates_file["blocker_count"], 0)
        self.assertTrue(all(item["pass"] for item in gates_file["checks"]))
        self.assertFalse(gates_file["public_mutation_performed"])

        self.assertEqual(record["status"], "prepublication_frozen_not_published")
        self.assertEqual(record["memory_count"], 57)
        self.assertEqual(record["candidate_csv_sha256"], hashlib.sha256(CANDIDATE.read_bytes()).hexdigest())
        self.assertEqual(record["base_public_csv_sha256"], manifest_sha := json.loads(MANIFEST.read_text(encoding="utf-8"))["published_base_sha256"])
        self.assertEqual(manifest_sha, "dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d")
        self.assertFalse(record["public_csv_created"])
        self.assertFalse(record["public_registry_updated"])
        self.assertFalse(record["published"])
        self.assertFalse(record["published_version_is_immutable"])


if __name__ == "__main__":
    unittest.main()
