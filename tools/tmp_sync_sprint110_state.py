#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
README = ROOT / "README.md"
STATUS = ROOT / "PROJECT_STATUS.md"
SITE_TEST = ROOT / "tests/test_site_files.py"
S109_TEST = ROOT / "tests/test_sprint109_state_sync.py"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] == 109
assert state["state_version"] == "0.21.97"
assert state["public_packs"]["normandie"]["version"] == "0.4"
assert state["public_packs"]["normandie"]["memory_count"] == 142
assert state["public_packs"]["auvergne_rhone_alpes"]["version"] == "0.3"
assert state["public_packs"]["auvergne_rhone_alpes"]["memory_count"] == 71
assert state["latest_sprint109_ara_v03_publication"]["published"] is True

state["updated"] = "2026-08-22"
state["current_sprint"] = 110
state["state_version"] = "0.21.98"
state["active_work"] = {
    "pack": "Normandie",
    "target_version": "0.5",
    "status": "current_sources_refreshed_zero_delta_field_blocked",
    "public_base_version": "0.4",
    "public_base_memory_count": 142,
    "candidate_memory_count": 142,
    "candidate_memory_delta": 0,
    "known_potential_ceiling_excluding_f6zes": 147,
    "field_required": ["R3_F1ZBX", "F5ZHA"],
    "source_watch": ["F1ZOV", "F6ZES"],
    "r3_minimum_independent_sessions": 2,
    "f5zha_minimum_independent_sessions": 2,
    "field_validation_kit": "research/normandie-v0.5/field-validation-kit.json",
    "field_evaluation_policy": "research/normandie-v0.5/field-evaluation-policy.json",
    "field_evaluator": "tools/evaluate_normandie_v05_field_sessions.py",
    "latest_source_refresh": "research/normandie-v0.5/sprint110-source-field-refresh.json",
    "summary": "research/sprint-110-summary.md",
    "field_gate_can_be_evaluated_automatically": True,
    "automatic_candidate_mutation_allowed": False,
    "automatic_publication_allowed": False,
    "public_export_allowed": False,
    "public_release_ready": False,
    "published": False,
    "public_mutation_performed": False,
    "rf_data_mutation": False,
    "published_v0_4_immutable": True,
}
state["next_priority"] = {
    "pack": "Normandie",
    "target_version": "0.5",
    "status": "collect_real_mortain_bocage_field_sessions",
    "public_base_version": "0.4",
    "public_base_memory_count": 142,
    "candidate_memory_count": 142,
    "candidate_memory_delta": 0,
    "field_required": ["R3_F1ZBX", "F5ZHA"],
    "required_independent_sessions_per_target": 2,
    "source_watch": ["F1ZOV", "F6ZES"],
    "field_validation_kit": "research/normandie-v0.5/field-validation-kit.json",
    "field_evaluator": "tools/evaluate_normandie_v05_field_sessions.py",
    "latest_evidence": "research/normandie-v0.5/sprint110-source-field-refresh.json",
}
state["latest_sprint110_normandie_v05_refresh"] = {
    "sprint": 110,
    "state_version": "0.21.98",
    "completed_on": "2026-08-22",
    "status": "normandie_v05_sources_refreshed_zero_delta_field_handoff",
    "public_base_version": "0.4",
    "public_base_memory_count": 142,
    "candidate_memory_count": 142,
    "candidate_memory_delta": 0,
    "known_potential_ceiling_excluding_f6zes": 147,
    "field_required": ["R3_F1ZBX", "F5ZHA"],
    "source_watch": ["F1ZOV", "F6ZES"],
    "r3_public_pair_mhz": [145.675, 145.075],
    "f5zha_public_pair_mhz": [145.4675, 432.575],
    "f1zov_operator_status": "maintenance",
    "f6zes_frequency_resolved": False,
    "f6zes_mode_resolved": False,
    "promotion_count": 0,
    "public_csv_mutation": False,
    "rf_data_mutation": False,
    "public_v0_4_immutable": True,
    "refresh": "research/normandie-v0.5/sprint110-source-field-refresh.json",
    "field_validation_kit": "research/normandie-v0.5/field-validation-kit.json",
    "field_evaluation_policy": "research/normandie-v0.5/field-evaluation-policy.json",
    "field_evaluator": "tools/evaluate_normandie_v05_field_sessions.py",
    "summary": "research/sprint-110-summary.md",
}

for source in [
    "research/normandie-v0.5/sprint110-source-field-refresh.json",
    "research/normandie-v0.5/field-validation-kit.json",
    "research/normandie-v0.5/field-evaluation-policy.json",
    "tools/evaluate_normandie_v05_field_sessions.py",
    "tests/test_sprint110_normandie_v05_refresh.py",
    "research/sprint-110-summary.md",
]:
    if source not in state["sources_of_truth"]:
        state["sources_of_truth"].append(source)

recent = state["recent_sprints"]
if not recent or recent[0].get("sprint") != 110:
    recent.insert(0, {
        "sprint": 110,
        "state_version": "0.21.98",
        "summary": "Normandie v0.5 sources revalidated with zero promotion and zero public/RF mutation; candidate remains 142 RX, R3/F1ZBX and F5ZHA remain field-gated, F1ZOV remains in operator maintenance, and F6ZES RF/mode remain unresolved.",
        "summary_file": "research/sprint-110-summary.md",
    })

STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

readme = README.read_text(encoding="utf-8")
old = "**État courant : Sprint 109 / 0.21.97 — Auvergne-Rhône-Alpes v0.3 est publiée et immuable à 71 RX, dont 18 aviation et 9 VHF de navigation intérieure.**"
new = "**État courant : Sprint 110 / 0.21.98 — Normandie v0.5 reste un candidat interne à 142 RX / delta 0 après revalidation des sources ; R3/F1ZBX et F5ZHA restent soumis aux gates terrain.**"
assert old in readme
readme = readme.replace(old, new, 1)
anchor = "## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée"
section = """## Sprint 110 — Normandie v0.5 : sources revalidées, handoff terrain\n\nLa revalidation du 22 août 2026 maintient le candidat Normandie v0.5 à **142 RX / delta 0**, sans mutation RF ni publique. Le plafond potentiel connu reste **147 RX hors F6ZES**, mais aucune addition ne franchit actuellement ses gates.\n\n**R3/F1ZBX** reste conditionné à deux sessions RX indépendantes et identifiées depuis Mortain-Bocage sur 145.675 MHz. **F5ZHA** reste conditionné à deux sessions RX indépendantes sur la paire actuelle 145.4675 / 432.575 MHz avec les critères du Sprint 85. **F1ZOV** reste en maintenance selon l'opérateur local et **F6ZES** reste sans fréquence/mode publics exploitables.\n\nLe kit Sprint 84 et l'évaluateur Sprint 85 sont suffisants : aucune nouvelle sonde n'est nécessaire et aucun verdict terrain ne peut muter automatiquement le candidat ou publier une version. Référence : `research/sprint-110-summary.md`.\n\n"""
assert anchor in readme
readme = readme.replace(anchor, section + anchor, 1)
readme = readme.replace("python tests\\test_sprint109_state_sync.py", "python tests\\test_sprint110_state_sync.py", 1)
README.write_text(readme, encoding="utf-8")

status = STATUS.read_text(encoding="utf-8")
status = status.replace("Sprint courant : **109**", "Sprint courant : **110**", 1)
status = status.replace("État logique : **0.21.97**", "État logique : **0.21.98**", 1)
status = status.replace("Résumé courant : `research/sprint-109-summary.md`.", "Résumé courant : `research/sprint-110-summary.md`.", 1)
anchor = "## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée"
section = """## Sprint 110 — Normandie v0.5 revalidée, zéro delta\n\nNormandie v0.5 reste **interne et non publiée à 142 RX / delta 0**. Le rafraîchissement source du 22 août 2026 ne justifie aucune promotion.\n\n- R3/F1ZBX : paramètres publics confirmés, mais **2 sessions terrain Mortain-Bocage** restent requises ;\n- F5ZHA : paire actuelle **145.4675 / 432.575 MHz**, mais **2 sessions terrain** restent requises ;\n- F1ZOV : statut opérateur local toujours **en maintenance** ;\n- F6ZES : site Sourdeval connu, mais fréquence et mode publics toujours non résolus.\n\nLe kit Sprint 84 et l'évaluateur Sprint 85 restent les outils de référence. Aucune mutation automatique du candidat ni publication automatique n'est autorisée. La prochaine action est la collecte de vraies sessions terrain.\n\n"""
assert anchor in status
status = status.replace(anchor, section + anchor, 1)
STATUS.write_text(status, encoding="utf-8")

site = SITE_TEST.read_text(encoding="utf-8")
site = site.replace('"research/sprint-109-summary.md",', '"research/sprint-109-summary.md", "research/sprint-110-summary.md",', 1)
site = site.replace('"Sprint 109 / 0.21.97",', '"Sprint 110 / 0.21.98",\n    "## Sprint 110 — Normandie v0.5 : sources revalidées, handoff terrain",', 1)
site = site.replace('for expected in ["Sprint courant : **109**", "État logique : **0.21.97**",', 'for expected in ["Sprint courant : **110**", "État logique : **0.21.98**",', 1)
site = site.replace('print("Tests RadioPack repository/site: canonical Sprint 109 / ARA v0.3 71 RX synchronized, historical releases preserved, RX-only guards OK")', 'print("Tests RadioPack repository/site: canonical Sprint 110 / Normandie v0.5 zero-delta field handoff synchronized, public releases preserved, RX-only guards OK")', 1)
SITE_TEST.write_text(site, encoding="utf-8")

s109 = S109_TEST.read_text(encoding="utf-8")
s109 = s109.replace('assert state["current_sprint"] == 109', 'assert state["current_sprint"] >= 109', 1)
s109 = s109.replace('assert state["state_version"] == "0.21.97"', 'assert state["state_version"].startswith("0.21.")', 1)
start = s109.index('active = state["active_work"]')
end = s109.index('s108 = state["latest_sprint108_ara_v03_candidate"]')
s109 = s109[:start] + '# Current active work may advance after Sprint 109; the ARA publication snapshot below is historical.\n\n' + s109[end:]
s109 = s109.replace('assert state["recent_sprints"][0]["sprint"] == 109\nassert state["recent_sprints"][0]["state_version"] == "0.21.97"\nassert state["recent_sprints"][1]["sprint"] == 108\nassert state["recent_sprints"][1]["state_version"] == "0.21.96"', 'recent_by_sprint = {item["sprint"]: item for item in state["recent_sprints"]}\nassert recent_by_sprint[109]["state_version"] == "0.21.97"\nassert recent_by_sprint[108]["state_version"] == "0.21.96"', 1)
s109 = s109.replace('    "Sprint 109 / 0.21.97",\n', '', 1)
s109 = s109.replace('    "Sprint courant : **109**",\n    "État logique : **0.21.97**",\n', '    "## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée",\n', 1)
s109 = s109.replace('print("Sprint 109 state sync: ARA v0.3=71 immutable, v0.2=62 historical, byte identity SHA frozen, next priority Normandie v0.5 OK")', 'print("Sprint 109 historical guard: ARA v0.3=71 immutable, v0.2=62 historical, byte identity SHA frozen after later state advances OK")', 1)
S109_TEST.write_text(s109, encoding="utf-8")

print("Sprint 110 canonical state migration complete")
