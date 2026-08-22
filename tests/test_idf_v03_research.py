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

    def test_second_pass_closes_attribution_and_dedup_decisions(self):
        pass2 = load_json("radio-validation-pass2-2026-08-21.json")
        decisions = pass2["decisions"]
        self.assertEqual({item["call"] for item in decisions["validated_existing_rf_replacement"]}, {"F6ZEE"})
        self.assertEqual({item["call"] for item in decisions["validated_deduplicated_extension"]}, {"F5ZNN-crossband"})
        replacement = decisions["validated_existing_rf_replacement"][0]
        self.assertEqual(set(replacement["frequencies_mhz"]), {145.1, 145.7})
        self.assertEqual(replacement["net_new_rf_memory_count_vs_v0_2"], 0)
        extension = decisions["validated_deduplicated_extension"][0]
        self.assertEqual(extension["already_present_rf_mhz"], [145.65])
        self.assertEqual(extension["unique_new_frequencies_mhz"], [430.65])
        self.assertEqual(extension["memory_count"], 1)

    def test_third_radio_pass_finalizes_current_release_scope(self):
        pass3 = load_json("radio-validation-pass3-2026-08-21.json")
        excluded = {item["call"] for item in pass3["scope_decisions"]["not_carried_in_v0_3_candidate_scope"]}
        self.assertEqual(excluded, {"F1ZTC", "F5ZDR", "F5ZBK", "F1ZDL"})
        accounting = pass3["final_radio_memory_accounting_assuming_aviation_unchanged"]
        expected = (
            accounting["published_v0_2_total"]
            - accounting["removed_v0_2_station_pair_memories"]
            + accounting["replacement_existing_rf_memories"]
            + accounting["direct_new_promoted_rf_memories_from_pass1"]
            + accounting["deduplicated_extension_new_rf_memories"]
        )
        self.assertEqual(expected, 57)
        self.assertEqual(accounting["working_total_with_aviation_18"], 57)
        self.assertTrue(accounting["radio_memory_accounting_final"])
        self.assertIsNone(accounting["release_candidate_memory_count"])
        self.assertTrue(pass3["result"]["radio_source_conflicts_closed_for_current_release_scope"])
        self.assertTrue(pass3["result"]["radio_memory_accounting_final"])
        self.assertFalse(pass3["result"]["aviation_revalidation_complete"])
        self.assertFalse(pass3["result"]["publication_ready"])

    def test_third_radio_pass_contract_remains_rx_only(self):
        pass3 = load_json("radio-validation-pass3-2026-08-21.json")
        self.assertTrue(pass3["rules"]["rx_only"])
        self.assertTrue(pass3["rules"]["paired_rx"])
        self.assertTrue(pass3["rules"]["same_rf_deduplicated"])
        self.assertTrue(pass3["rules"]["no_artificial_fill"])
        self.assertEqual(pass3["rules"]["chirp_duplex"], "off")
        self.assertEqual(pass3["rules"]["chirp_offset"], "0.000000")

    def test_second_aviation_pass_revalidates_lfpg_without_expansion(self):
        aviation = load_json("aviation-validation-pass2-2026-08-21.json")
        lfpg = aviation["aerodromes"]["LFPG"]
        self.assertTrue(lfpg["current_direct_sia_ad2_18_checked"])
        self.assertTrue(lfpg["published_v0_2_subset_revalidated"])
        self.assertEqual(lfpg["published_v0_2_subset_mhz"], [118.155, 119.855, 121.155, 124.355])
        self.assertFalse(lfpg["additional_candidates_promoted"])
        self.assertEqual(aviation["provisional_aviation_decision"]["working_memory_count"], 18)
        self.assertEqual(aviation["provisional_aviation_decision"]["memory_delta_promoted"], 0)
        self.assertFalse(aviation["gates"]["publication_allowed"])

    def test_third_aviation_pass_preserves_prior_caution(self):
        aviation = load_json("aviation-validation-pass3-2026-08-21.json")
        self.assertEqual(aviation["current_airac"], "08/26")
        self.assertTrue(aviation["aerodromes"]["LFPG"]["current_airac08_direct_subset_revalidated"])
        self.assertTrue(aviation["aerodromes"]["LFPO"]["official_sia_recent_com_material_matches_published_subset"])
        self.assertTrue(aviation["aerodromes"]["LFPB"]["official_sia_june_july_2026_material_matches_published_subset"])
        self.assertFalse(aviation["sup_aip_review"]["147/2026"]["full_pdf_visual_review_completed"])
        self.assertFalse(aviation["gates"]["publication_allowed"])

    def test_fourth_aviation_pass_closes_scoped_gate_without_expansion(self):
        aviation = load_json("aviation-validation-pass4-2026-08-21.json")
        self.assertEqual(aviation["current_airac"], "08/26")
        self.assertEqual(aviation["airac_valid_through_inclusive"], "2026-09-02")
        self.assertEqual(aviation["final_aviation_decision"]["memory_count"], 18)
        self.assertEqual(aviation["final_aviation_decision"]["memory_delta"], 0)
        self.assertFalse(aviation["final_aviation_decision"]["additional_frequencies_promoted"])
        self.assertTrue(aviation["gates"]["aviation_revalidation_complete"])
        self.assertTrue(aviation["gates"]["notam_sup_review_complete_for_retained_subset"])
        self.assertTrue(aviation["gates"]["frequency_delta_validated"])
        self.assertTrue(aviation["gates"]["publication_allowed_before_airac09_boundary"])
        self.assertEqual(aviation["freshness_boundary"]["airac09_revalidation_required_on_or_after"], "2026-09-03")

    def test_release_scope_is_published_immutable(self):
        scope = load_json("release-scope.json")
        self.assertEqual(scope["status"], "published_immutable")
        self.assertEqual(scope["published_base"]["version"], "0.2")
        self.assertEqual(scope["published_base"]["memory_count"], 58)
        self.assertTrue(scope["published_base"]["immutable"])
        self.assertEqual(scope["research_evidence"]["candidate_memory_count"], 57)
        self.assertEqual(scope["research_evidence"]["candidate_aviation_memory_count"], 18)
        self.assertEqual(scope["research_evidence"]["candidate_regional_radio_memory_count"], 15)
        self.assertEqual(scope["research_evidence"]["candidate_sha256"], scope["research_evidence"]["public_csv_sha256"])
        self.assertEqual(
            scope["research_evidence"]["latest_aviation_pass"],
            "research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json",
        )
        for key in [
            "radio_source_conflicts_closed", "radio_memory_accounting_final", "aviation_revalidation_complete",
            "deterministic_candidate_built", "rx_only_validation_passed", "rf_deduplication_passed",
            "memory_limit_passed", "review_checklist_complete", "publication_gates_zero_blockers",
            "publication_record_frozen", "public_csv_matches_candidate", "public_registry_updated",
        ]:
            self.assertTrue(scope["publication_gates"][key])
        self.assertTrue(scope["publication_ready"])
        self.assertTrue(scope["published"])
        self.assertTrue(scope["public_mutation_performed"])
        self.assertTrue(scope["published_version_is_immutable"])


if __name__ == "__main__":
    unittest.main()
