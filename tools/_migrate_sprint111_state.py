#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
README = ROOT / "README.md"
STATUS = ROOT / "PROJECT_STATUS.md"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] == 110
assert state["state_version"] == "0.21.98"
assert state["updated"] == "2026-08-22"
assert state["active_work"]["pack"] == "Normandie"
assert state["active_work"]["target_version"] == "0.5"
assert state["active_work"]["candidate_memory_count"] == 142
assert state["active_work"]["candidate_memory_delta"] == 0
assert state["next_priority"]["pack"] == "Normandie"
assert state["next_priority"]["status"] == "collect_real_mortain_bocage_field_sessions"

state["current_sprint"] = 111
state["state_version"] = "0.21.99"

handoff = state["bretagne_v0_3_airac_handoff"]
assert handoff["public_base_version"] == "0.2"
assert handoff["public_base_memory_count"] == 151
assert handoff["candidate_memory_count"] == 151
assert handoff["candidate_memory_delta"] == 0
assert handoff["airac_current_until_inclusive"] == "2026-09-02"
assert handoff["airac_next_effective_from"] == "2026-09-03"
handoff.update({
    "status": "airac09_future_source_available_readiness_prepared_waiting_effective_date",
    "future_cycle_source_available": True,
    "future_cycle_source_observed_on": "2026-08-22",
    "future_cycle_source_is_current_evidence": False,
    "airac_next_effective_until_inclusive": "2026-09-30",
    "baseline_aviation_memory_count": 16,
    "required_explicit_memory_decision_count": 16,
    "candidate_rebuild_allowed_before_effective_date": False,
    "automatic_candidate_mutation_allowed": False,
    "automatic_publication_allowed": False,
    "readiness": "research/bretagne-v0.3/airac09-readiness.json",
    "revalidation_template": "research/bretagne-v0.3/airac09-revalidation-template.json",
    "validator": "tools/check_bretagne_v03_airac09_revalidation.py",
    "summary": "research/sprint-111-summary.md",
})

state["latest_sprint111_bretagne_airac09_readiness"] = {
    "sprint": 111,
    "state_version": "0.21.99",
    "completed_on": "2026-08-22",
    "status": "bretagne_v03_airac09_readiness_prepared_future_cycle_not_current",
    "public_base_version": "0.2",
    "public_base_memory_count": 151,
    "candidate_memory_count": 151,
    "candidate_memory_delta": 0,
    "baseline_aviation_cycle": "AIRAC 08/26",
    "baseline_aviation_memory_count": 16,
    "baseline_locations": [130, 145],
    "required_cycle": "AIRAC 09/26",
    "future_sia_product_available": True,
    "future_sia_product_observed_on": "2026-08-22",
    "future_sia_product_is_current_evidence": False,
    "effective_from": "2026-09-03",
    "effective_until_inclusive": "2026-09-30",
    "explicit_memory_decision_count_required": 16,
    "candidate_rebuild_allowed_before_effective_date": False,
    "automatic_candidate_mutation_allowed": False,
    "automatic_publication_allowed": False,
    "public_csv_mutation": False,
    "rf_data_mutation": False,
    "public_v0_3_created": False,
    "readiness": "research/bretagne-v0.3/airac09-readiness.json",
    "revalidation_template": "research/bretagne-v0.3/airac09-revalidation-template.json",
    "validator": "tools/check_bretagne_v03_airac09_revalidation.py",
    "summary": "research/sprint-111-summary.md",
}

for source in [
    "research/bretagne-v0.3/airac09-readiness.json",
    "research/bretagne-v0.3/airac09-revalidation-template.json",
    "tools/check_bretagne_v03_airac09_revalidation.py",
    "tests/test_sprint111_bretagne_airac09_readiness.py",
    ".github/workflows/sprint111-bretagne-airac09-readiness.yml",
    "research/sprint-111-summary.md",
]:
    if source not in state["sources_of_truth"]:
        state["sources_of_truth"].append(source)

state["recent_sprints"] = [item for item in state["recent_sprints"] if item["sprint"] != 111]
state["recent_sprints"].insert(0, {
    "sprint": 111,
    "state_version": "0.21.99",
    "summary": "Bretagne v0.3 AIRAC 09/26 readiness prepared with a 16-memory aviation revalidation matrix and a deterministic date-aware validator; future SIA AIRAC 09/26 availability is recorded but cannot be treated as current evidence before 2026-09-03; no RF or public CSV mutation.",
    "summary_file": "research/sprint-111-summary.md",
})
state["resume_rules"]["future_airac_source_availability_is_not_current_evidence"] = True
state["resume_rules"]["candidate_rebuild_after_airac_revalidation_is_not_publication"] = True
state["resume_rules"]["airac_revalidation_requires_explicit_decision_for_every_scoped_aviation_memory"] = True

STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

readme = README.read_text(encoding="utf-8")
old_state = "**État courant : Sprint 110 / 0.21.98 — Normandie v0.5 reste un candidat interne à 142 RX / delta 0 après revalidation des sources ; R3/F1ZBX et F5ZHA restent soumis aux gates terrain.**"
new_state = "**État courant : Sprint 111 / 0.21.99 — Bretagne v0.3 est préparée pour AIRAC 09/26 avec une matrice de 16 mémoires et un validateur temporel ; Normandie v0.5 reste la priorité terrain à 142 RX / delta 0.**"
assert old_state in readme
readme = readme.replace(old_state, new_state, 1)
marker = "## Sprint 110 — Normandie v0.5 : sources revalidées, handoff terrain\n"
assert marker in readme
section = """## Sprint 111 — Bretagne v0.3 : readiness AIRAC 09/26\n\nLe produit SIA AIRAC 09/26 est déjà disponible au 22 août 2026, mais il n'entre en vigueur que le **3 septembre 2026**. Sa disponibilité anticipée est enregistrée comme source future uniquement et ne peut fermer aucun gate avant cette date.\n\nLa préparation couvre exactement les **16 mémoires aviation** Bretagne héritées d'AIRAC 08/26, positions **130–145**. `research/bretagne-v0.3/airac09-revalidation-template.json` exige une décision explicite `unchanged`, `changed` ou `removed` pour chaque mémoire. `tools/check_bretagne_v03_airac09_revalidation.py` refuse la reconstruction avant le 3 septembre, après l'expiration du cycle, si une mémoire reste non résolue, ou sans vérification primaire et revue humaine.\n\nMême après un verdict positif, seule la **reconstruction d'un candidat interne** est autorisée : aucune mutation automatique et aucune publication automatique. Bretagne publique reste **v0.2 / 151 RX** immuable et le candidat v0.3 reste **151 RX / delta 0**. Référence : `research/sprint-111-summary.md`.\n\n"""
readme = readme.replace(marker, section + marker, 1)
old_work = "- **Bretagne v0.3** : 151 RX, delta 0, publication bloquée jusqu'à la revalidation AIRAC 09/26 à partir du **3 septembre 2026**."
new_work = "- **Bretagne v0.3** : 151 RX, delta 0 ; Sprint 111 a préparé la matrice de 16 mémoires et le validateur AIRAC 09/26. Le produit futur est déjà disponible mais ne devient source courante qu'à partir du **3 septembre 2026**."
assert old_work in readme
readme = readme.replace(old_work, new_work, 1)
README.write_text(readme, encoding="utf-8")

status = STATUS.read_text(encoding="utf-8")
assert "Sprint courant : **110**" in status
assert "État logique : **0.21.98**" in status
assert "Résumé courant : `research/sprint-110-summary.md`." in status
status = status.replace("Sprint courant : **110**", "Sprint courant : **111**", 1)
status = status.replace("État logique : **0.21.98**", "État logique : **0.21.99**", 1)
status = status.replace("Résumé courant : `research/sprint-110-summary.md`.", "Résumé courant : `research/sprint-111-summary.md`.", 1)
marker_status = "## Sprint 110 — Normandie v0.5 revalidée, zéro delta\n"
assert marker_status in status
section_status = """## Sprint 111 — Bretagne v0.3 AIRAC 09/26 prête pour revalidation\n\nLe produit SIA AIRAC 09/26 est disponible en avance mais n'est **pas courant avant le 3 septembre 2026**. Sprint 111 prépare une matrice de **16 mémoires aviation** (positions 130–145) et un validateur qui exige une décision explicite pour chaque mémoire, une source primaire courante et une revue humaine.\n\nBretagne v0.2 reste publique et immuable à **151 RX** ; le candidat v0.3 reste **151 RX / delta 0**. Aucun CSV v0.3 n'est créé. Un verdict AIRAC positif autorisera seulement une reconstruction interne, jamais une publication automatique.\n\nLa priorité immédiatement actionnable reste **Normandie v0.5 terrain**.\n\n"""
status = status.replace(marker_status, section_status + marker_status, 1)
old_bretagne = "Candidat **151 RX, delta 0**. Publication bloquée jusqu'à la revalidation AIRAC 09/26 à partir du **3 septembre 2026** ; avant cette date, AIRAC 08/26 reste la référence applicable."
new_bretagne = "Candidat **151 RX, delta 0**. Sprint 111 a préparé la matrice de 16 mémoires et le validateur. AIRAC 09/26 est disponible comme source future mais ne devient courant qu'à partir du **3 septembre 2026** ; avant cette date, AIRAC 08/26 reste la référence applicable."
assert old_bretagne in status
status = status.replace(old_bretagne, new_bretagne, 1)
STATUS.write_text(status, encoding="utf-8")

print("Sprint 111 state migration complete: canonical 0.21.99, Bretagne AIRAC readiness recorded, Normandie field priority preserved")
