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

    def test_initial_checkpoint_conflicts_are_not_silently_promoted(self):
        radio = load_json("radio-validation-2026-08-21.json")
        promoted = {item["call"] for item in radio["promoted_for_working_candidate"]}
        deferred = {item["call"] for item in radio["deferred"]}
        removed = {item["call"] for item in radio["not_carried_forward_from_v0_2"]}

        self.assertTrue({"F5ZMR", "F5ZSY"}.issubset(promoted))
        self.assertTrue({"F1ZSY", "F5ZEQ", "F5ZDR", "F5ZNN-crossband"}.issubset(deferred))
        self.assertTrue({"F5ZAD", "F1ZUX"}.issubset(removed))
        self.assertTrue(promoted.isdisjoint(deferred))
        self.assertTrue(promoted.isdisjoint(removed))

    def test_second_pass_closes_attribution_and_dedup_decisions(self):
        pass2 = load_json("radio-validation-pass2-2026-08-21.json")
        decisions = pass2["decisions"]

        keep = {item["call"] for item in decisions["closed_keep_gate"]}
        replacements = {item["call"] for item in decisions["validated_existing_rf_replacement"]}
        extensions = {item["call"] for item in decisions["validated_deduplicated_extension"]}
        not_carried = {item["call"] for item in decisions["not_carried_forward_now"]}
        deferred = {item["call"] for item in decisions["still_deferred"]}
        pending = {item["call"] for item in decisions["pending_independent_current_corroboration"]}

        self.assertIn("F1ZHK", keep)
        self.assertEqual(replacements, {"F6ZEE"})
        self.assertEqual(extensions, {"F5ZNN-crossband"})
        self.assertEqual(not_carried, {"F1ZSY", "F5ZEQ"})
        self.assertEqual(deferred, {"F1ZTC", "F5ZDR"})
        self.assertEqual(pending, {"F5ZBK", "F1ZDL"})

        replacement = decisions["validated_existing_rf_replacement"][0]
        self.assertEqual(set(replacement["frequencies_mhz"]), {145.1, 145.7})
        self.assertEqual(replacement["replaces_v0_2_attribution"], "F1ZSY")
        self.assertEqual(replacement["net_new_rf_memory_count_vs_v0_2"], 0)

        extension = decisions["validated_deduplicated_extension"][0]
        self.assertEqual(extension["already_present_rf_mhz"], [145.65])
        self.assertEqual(extension["unique_new_frequencies_mhz"], [430.65])
        self.assertEqual(extension["memory_count"], 1)

    def test_second_pass_provisional_memory_arithmetic_is_explicit(self):
        pass2 = load_json("radio-validation-pass2-2026-08-21.json")
        accounting = pass2["provisional_memory_accounting"]

        expected = (
            accounting["published_v0_2_total"]
            - accounting["removed_v0_2_station_pair_memories"]
            + accounting["replacement_existing_rf_memories"]
            + accounting["direct_new_promoted_rf_memories_from_pass1"]
            + accounting["deduplicated_extension_new_rf_memories"]
        )
        self.assertEqual(expected, 57)
        self.assertEqual(
            accounting["provisional_working_memory_count_if_aviation_and_national_blocks_unchanged"],
            57,
        )
        self.assertIsNone(accounting["release_candidate_memory_count"])
        self.assertFalse(pass2["result"]["radio_source_conflicts_closed"])
        self.assertFalse(pass2["result"]["radio_memory_accounting_final"])
        self.assertFalse(pass2["result"]["publication_ready"])

    def test_second_pass_contract_remains_rx_only(self):
        pass2 = load_json("radio-validation-pass2-2026-08-21.json")
        self.assertTrue(pass2["rules"]["rx_only"])
        self.assertTrue(pass2["rules"]["paired_rx"])
        self.assertTrue(pass2["rules"]["same_rf_deduplicated"])
        self.assertTrue(pass2["rules"]["no_artificial_fill"])
        self.assertTrue(pass2["rules"]["source_conflict_blocks_promotion"])
        self.assertTrue(pass2["rules"]["local_operator_status_overrides_general_directory_for_current_state"])
        self.assertEqual(pass2["rules"]["chirp_duplex"], "off")
        self.assertEqual(pass2["rules"]["chirp_offset"], "0.000000")

    def test_promoted_initial_working_candidate_has_no_duplicate_rf(self):
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

    def test_second_aviation_pass_revalidates_lfpg_without_premature_expansion(self):
        aviation = load_json("aviation-validation-pass2-2026-08-21.json")
        self.assertEqual(aviation["current_airac"], "08/26")
        self.assertEqual(aviation["airac_effective_from"], "2026-08-06")
        self.assertEqual(aviation["airac_valid_through_inclusive"], "2026-09-02")

        lfpg = aviation["aerodromes"]["LFPG"]
        self.assertTrue(lfpg["current_direct_sia_ad2_18_checked"])
        self.assertTrue(lfpg["published_v0_2_subset_revalidated"])
        self.assertEqual(
            lfpg["published_v0_2_subset_mhz"],
            [118.155, 119.855, 121.155, 124.355],
        )
        self.assertEqual(
            lfpg["additional_current_app_frequencies_observed_mhz"],
            [125.83, 126.43, 126.58, 131.205, 133.38, 136.28],
        )
        self.assertFalse(lfpg["additional_candidates_promoted"])

        self.assertFalse(aviation["aerodromes"]["LFPO"]["current_direct_sia_ad2_18_checked"])
        self.assertFalse(aviation["aerodromes"]["LFPB"]["current_direct_sia_ad2_18_checked"])
        self.assertEqual(aviation["provisional_aviation_decision"]["working_memory_count"], 18)
        self.assertEqual(aviation["provisional_aviation_decision"]["memory_delta_promoted"], 0)
        self.assertFalse(aviation["provisional_aviation_decision"]["working_count_is_final"])
        self.assertTrue(aviation["gates"]["lfpg_published_subset_revalidated"])
        self.assertFalse(aviation["gates"]["full_scoped_ad2_18_recheck_complete"])
        self.assertFalse(aviation["gates"]["notam_sup_review_complete"])
        self.assertFalse(aviation["gates"]["frequency_delta_validated"])
        self.assertFalse(aviation["gates"]["publication_allowed"])

    def test_release_scope_is_explicitly_not_ready(self):
        scope = load_json("release-scope.json")
        self.assertEqual(scope["published_base"]["version"], "0.2")
        self.assertEqual(scope["published_base"]["memory_count"], 58)
        self.assertTrue(scope["published_base"]["immutable"])
        self.assertEqual(scope["research_evidence"]["provisional_working_memory_count"], 57)
        self.assertEqual(scope["research_evidence"]["provisional_aviation_memory_count"], 18)
        self.assertEqual(
            scope["research_evidence"]["latest_aviation_pass"],
            "research/ile-de-france-v0.3/aviation-validation-pass2-2026-08-21.json",
        )
        self.assertFalse(scope["research_evidence"]["provisional_count_is_release_candidate"])
        self.assertFalse(scope["publication_ready"])
        self.assertTrue(all(value is False for value in scope["publication_gates"].values()))


if __name__ == "__main__":
    unittest.main()
