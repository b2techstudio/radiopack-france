import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "ile-de-france-v0.3"


def load_json(name: str):
    return json.loads((RESEARCH / name).read_text(encoding="utf-8"))


class IleDeFranceV03ResearchTests(unittest.TestCase):
    def test_radio_checkpoint_preserves_public_base_and_contract(self):
        radio = load_json("radio-validation-2026-08-21.json")
        self.assertEqual(radio["published_base_version"], "0.2")
        self.assertEqual(radio["published_base_memory_count"], 58)
        self.assertFalse(radio["result"]["publication_ready"])
        self.assertTrue(radio["rules"]["rx_only"])
        self.assertTrue(radio["rules"]["paired_rx"])
        self.assertEqual(radio["rules"]["chirp_duplex"], "off")
        self.assertEqual(radio["rules"]["chirp_offset"], "0.000000")
        self.assertTrue(radio["rules"]["same_rf_deduplicated"])
        self.assertTrue(radio["rules"]["no_artificial_fill"])
        self.assertTrue(radio["rules"]["source_conflict_blocks_promotion"])

    def test_known_conflicts_are_not_silently_promoted(self):
        radio = load_json("radio-validation-2026-08-21.json")
        promoted = {item["call"] for item in radio["promoted_for_working_candidate"]}
        deferred = {item["call"] for item in radio["deferred"]}
        removed = {item["call"] for item in radio["not_carried_forward_from_v0_2"]}

        self.assertTrue({"F5ZMR", "F5ZSY"}.issubset(promoted))
        self.assertTrue({"F1ZSY", "F5ZEQ", "F5ZDR", "F5ZNN-crossband"}.issubset(deferred))
        self.assertTrue({"F5ZAD", "F1ZUX"}.issubset(removed))
        self.assertTrue(promoted.isdisjoint(deferred))
        self.assertTrue(promoted.isdisjoint(removed))

    def test_promoted_working_candidate_has_no_duplicate_rf(self):
        radio = load_json("radio-validation-2026-08-21.json")
        frequencies = [
            frequency
            for item in radio["promoted_for_working_candidate"]
            for frequency in item["frequencies_mhz"]
        ]
        self.assertEqual(len(frequencies), len(set(frequencies)))

    def test_aviation_gate_stays_closed_for_release(self):
        aviation = load_json("aviation-airac08-2026-08-21.json")
        self.assertEqual(aviation["current_airac"], "08/26")
        self.assertEqual(aviation["airac_valid_through_inclusive"], "2026-09-02")
        self.assertEqual(aviation["next_airac"]["cycle"], "09/26")
        self.assertEqual(aviation["next_airac"]["effective_from"], "2026-09-03")
        self.assertFalse(aviation["gates"]["publication_allowed"])
        self.assertFalse(aviation["gates"]["full_scoped_ad2_18_recheck_complete"])
        self.assertFalse(aviation["gates"]["notam_sup_review_complete"])
        self.assertFalse(aviation["gates"]["frequency_delta_validated"])

    def test_release_scope_is_explicitly_not_ready(self):
        scope = load_json("release-scope.json")
        self.assertEqual(scope["published_base"]["version"], "0.2")
        self.assertEqual(scope["published_base"]["memory_count"], 58)
        self.assertTrue(scope["published_base"]["immutable"])
        self.assertFalse(scope["publication_ready"])
        self.assertTrue(all(value is False for value in scope["publication_gates"].values()))


if __name__ == "__main__":
    unittest.main()
