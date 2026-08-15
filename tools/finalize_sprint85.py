#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Anchor not found in {path}: {old[:160]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before(path: Path, anchor: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if block.strip() in text:
        return
    if anchor not in text:
        raise RuntimeError(f"Insert anchor not found in {path}: {anchor!r}")
    path.write_text(text.replace(anchor, block + anchor, 1), encoding="utf-8")


# Machine-readable state.
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated"] = "2026-08-15"
state["current_sprint"] = 85
state["state_version"] = "0.21.74"
active = state["active_work"]
active["status"] = "field_session_evaluator_ready_zero_delta_142_not_public"
active["field_evaluation_policy"] = "research/normandie-v0.5/field-evaluation-policy.json"
active["field_evaluator"] = "tools/evaluate_normandie_v05_field_sessions.py"
active["field_evaluator_guard"] = "tests/test_sprint85_normandie_v05_field_evaluator.py"
active["field_evaluator_verdicts"] = ["satisfied", "insufficient", "indeterminate"]
active["field_evaluator_independence_unit"] = "session_id"
active["field_evaluator_minimum_independent_sessions_per_gate"] = 2
active["field_evaluator_legacy_f5zha_probe_counts_for_gate"] = False
active["field_evaluator_non_reception_is_operational_negative_evidence"] = False
active["field_evaluator_automatic_candidate_mutation_allowed"] = False
active["field_evaluator_automatic_publication_allowed"] = False
active["field_evaluator_promotion_ready"] = False
active["internal_candidate_memory_count"] = 142
active["internal_candidate_new_memory_count"] = 0
active["public_export_allowed"] = False
active["public_registry_allowed"] = False
active["public_release_ready"] = False
active["published"] = False
state["latest_sprint85_normandie_v0_5_field_evaluator"] = {
    "sprint": 85,
    "state_version": "0.21.74",
    "updated": "2026-08-15",
    "candidate_memory_count_before": 142,
    "candidate_memory_count_after": 142,
    "candidate_memory_delta": 0,
    "verdicts": ["satisfied", "insufficient", "indeterminate"],
    "independent_session_unit": "session_id",
    "minimum_independent_sessions_per_gate": 2,
    "r3_primary_frequency_mhz": 145.675,
    "r3_optional_input_counts_for_gate": False,
    "f5zha_current_pair_mhz": [145.4675, 432.575],
    "f5zha_legacy_probe_mhz": 431.4125,
    "f5zha_legacy_probe_counts_for_gate": False,
    "non_reception_is_operational_negative_evidence": False,
    "automatic_candidate_mutation_allowed": False,
    "automatic_publication_allowed": False,
    "promotion_ready": False,
}
for item in [
    "research/normandie-v0.5/field-evaluation-policy.json",
    "research/sprint-85-summary.md",
]:
    if item not in state.setdefault("sources_of_truth", []):
        state["sources_of_truth"].append(item)
field_tools = state.get("field_tools")
new_tools = {
    "evaluate_normandie_v05_field_sessions": "tools/evaluate_normandie_v05_field_sessions.py",
    "test_sprint85_normandie_v05_field_evaluator": "tests/test_sprint85_normandie_v05_field_evaluator.py",
}
if isinstance(field_tools, dict):
    field_tools.update(new_tools)
elif isinstance(field_tools, list):
    for value in new_tools.values():
        if value not in field_tools:
            field_tools.append(value)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Generic repository guard.
site = ROOT / "tests/test_site_files.py"
insert_before(
    site,
    '    "tests/test_normandie_v04_public_release.py",\n',
    '    "research/normandie-v0.5/field-evaluation-policy.json",\n'
    '    "tools/evaluate_normandie_v05_field_sessions.py",\n'
    '    "tests/test_sprint85_normandie_v05_field_evaluator.py",\n'
    '    "research/sprint-85-summary.md",\n',
)

# README.
readme = ROOT / "README.md"
replace_once(
    readme,
    '**État courant : Sprint 84 / 0.21.73 — Normandie v0.5 reste à 142 mémoires RX ; un kit terrain RX-only de 6 sondes prépare la validation R3/F5ZHA sans modifier le candidat ni publier v0.5.**',
    '**État courant : Sprint 85 / 0.21.74 — Normandie v0.5 reste à 142 mémoires RX ; le journal terrain R3/F5ZHA peut maintenant être évalué automatiquement sans aucune promotion ni publication automatique.**',
)
replace_once(readme, '## État actuel — Sprint 84 / 0.21.73', '## État actuel — Sprint 85 / 0.21.74')
replace_once(
    readme,
    'Recherche : Normandie v0.5 reste à **142 mémoires RX**, delta 0. Un mini-pack terrain de **6 sondes RX-only** est maintenant prêt pour produire des observations reproductibles sur R3 F1ZBX et F5ZHA depuis Mortain ; ces six sondes ne sont pas des mémoires candidates. Le plafond potentiel reste **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
    'Recherche : Normandie v0.5 reste à **142 mémoires RX**, delta 0. Le mini-pack terrain de **6 sondes RX-only** et son journal disposent maintenant d’un évaluateur reproductible qui classe R3 et F5ZHA en `satisfied`, `insufficient` ou `indeterminate` sans jamais modifier le candidat automatiquement. Le plafond potentiel reste **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
)
replace_once(
    readme,
    '`research/sprint-83-summary.md` et `research/sprint-84-summary.md`.',
    '`research/sprint-83-summary.md`, `research/sprint-84-summary.md` et `research/sprint-85-summary.md`.',
)
insert_before(
    readme,
    '## Sprint 84 — kit terrain Normandie v0.5\n',
    '## Sprint 85 — évaluateur du journal terrain Normandie v0.5\n\n'
    'Le candidat reste à **142 mémoires RX, delta 0**. Le journal CSV du Sprint 84 peut maintenant être évalué par `tools/evaluate_normandie_v05_field_sessions.py`.\n\n'
    '- verdicts : `satisfied`, `insufficient`, `indeterminate` ;\n'
    '- l’indépendance est comptée par `session_id` : plusieurs lignes d’une même session ne deviennent jamais plusieurs preuves ;\n'
    '- R3 : seule la sortie **145.675 MHz** compte, avec deux sessions indépendantes identifiées ; l’entrée 145.075 MHz reste facultative ;\n'
    '- F5ZHA : deux sessions indépendantes qualifiantes sur **145.4675 ou 432.575 MHz**, confiance reconnue et intelligibilité ≥ 3/5 ; les deux côtés n’ont pas besoin d’être entendus pour le seul gate terrain ;\n'
    '- **431.4125 MHz** et `CTRL-ZHY` restent diagnostiques et ne comptent jamais pour un gate ;\n'
    '- une non-réception n’est jamais interprétée comme preuve d’arrêt ;\n'
    '- même avec un gate `satisfied`, `promotion_ready=false`, aucune mutation du candidat et aucune publication automatique.\n\n'
    'Politique : `research/normandie-v0.5/field-evaluation-policy.json`. Évaluateur : `tools/evaluate_normandie_v05_field_sessions.py`. Garde-fou : `tests/test_sprint85_normandie_v05_field_evaluator.py`.\n\n',
)

# PROJECT_STATUS.
status = ROOT / "PROJECT_STATUS.md"
replace_once(status, 'Sprint courant : **84**\nÉtat logique : **0.21.73**', 'Sprint courant : **85**\nÉtat logique : **0.21.74**')
replace_once(status, 'Résumé courant : `research/sprint-84-summary.md`.', 'Résumé courant : `research/sprint-85-summary.md`.')
insert_before(
    status,
    '## Sprint 84 — kit terrain Normandie v0.5\n',
    '## Sprint 85 — évaluateur terrain Normandie v0.5\n\n'
    'Le candidat reste à **142 RX, delta 0**. L’évaluateur du journal terrain classe désormais séparément les gates R3 et F5ZHA en `satisfied`, `insufficient` ou `indeterminate`.\n\n'
    '- deux sessions indépendantes sont nécessaires pour chaque gate ;\n'
    '- `session_id` est l’unité d’indépendance ;\n'
    '- R3 145.675 MHz compte, 145.075 MHz reste facultative ;\n'
    '- F5ZHA 145.4675 / 432.575 MHz compte ; 431.4125 MHz reste diagnostic seulement ;\n'
    '- non-réception ≠ arrêt du relais ;\n'
    '- verdict terrain ≠ promotion : aucune modification ou publication automatique.\n\n'
    'Politique : `research/normandie-v0.5/field-evaluation-policy.json`. Outil : `tools/evaluate_normandie_v05_field_sessions.py`. Test : `tests/test_sprint85_normandie_v05_field_evaluator.py`.\n\n',
)

# Normandie v0.5 README.
v05 = ROOT / "research/normandie-v0.5/README.md"
v05.write_text(
    '# Normandie v0.5 — recherche\n\n'
    'État : **Sprint 85 / 0.21.74 — candidat interne 142 mémoires RX, delta 0 ; kit terrain et évaluateur R3/F5ZHA prêts, aucune publication**.\n\n'
    'Base publique immuable : **Normandie v0.4, 142 mémoires RX**. Le plafond potentiel connu reste **147 mémoires** hors F6ZES.\n\n'
    '## Chaîne terrain\n\n'
    '1. Générer le kit RX-only et le journal vide :\n\n'
    '```bash\npython tools/build_normandie_v05_field_validation_kit.py --output-dir field-kit\n```\n\n'
    '2. Renseigner `field-kit/normandie-v0.5-field-session-template.csv` pendant ou après les écoutes.\n\n'
    '3. Évaluer le journal :\n\n'
    '```bash\npython tools/evaluate_normandie_v05_field_sessions.py --input observations.csv --output evaluation.json\n```\n\n'
    'Le rapport distingue `satisfied`, `insufficient` et `indeterminate`, compte les sessions indépendantes par `session_id`, signale les lignes invalides et n’effectue jamais de promotion automatique.\n\n'
    '## Gates\n\n'
    '- **R3 F1ZBX** : 145.675 MHz est la sonde principale ; deux sessions indépendantes identifiées sont nécessaires. 145.075 MHz est facultative.\n'
    '- **F5ZHA Laval** : deux sessions indépendantes qualifiantes sur 145.4675 ou 432.575 MHz, intelligibilité ≥ 3/5 et confiance reconnue. Les deux côtés de la paire n’ont pas besoin d’être entendus pour le seul gate de couverture terrain.\n'
    '- **431.4125 MHz** : diagnostic historique uniquement, ne compte jamais pour le gate et ne ferme jamais le conflit de source.\n'
    '- **CTRL-ZHY 145.6875 MHz** : contrôle facultatif du matériel, ne compte pour aucun gate.\n\n'
    'Une non-réception n’est jamais une preuve d’arrêt. Même si un gate terrain est satisfait, `promotion_ready` reste faux : une revue humaine et des sources courantes restent nécessaires.\n\n'
    'Fichiers : `field-validation-kit.json`, `field-evaluation-policy.json`, `current-blocker-revalidation.json`.\n\n'
    'Règles : RX-only, `Duplex=off`, `Offset=0.000000`, aucune fréquence devinée, géométrie ≠ réception, aucune mutation automatique du candidat, aucune publication automatique, Normandie v0.4 immuable.\n',
    encoding='utf-8',
)

# CHANGELOG.
changelog = ROOT / "CHANGELOG.md"
insert_before(
    changelog,
    '## 0.21.73 - 2026-08-15\n',
    '## 0.21.74 - 2026-08-15\n\n'
    '- **Sprint 85** : ajout d’un évaluateur reproductible du journal terrain Normandie v0.5 ; candidat maintenu à **142 mémoires RX**, delta **0**.\n'
    '- Verdicts `satisfied` / `insufficient` / `indeterminate`, indépendance par `session_id`, lignes invalides et sessions incohérentes signalées.\n'
    '- R3 : 145.675 MHz compte pour le gate ; F5ZHA : 145.4675 / 432.575 MHz comptent, 431.4125 MHz reste diagnostic uniquement.\n'
    '- Une non-réception ne vaut jamais preuve d’arrêt et aucun verdict ne déclenche une promotion, une mutation du candidat ou une publication automatique.\n'
    '- Ajout de `field-evaluation-policy.json`, `evaluate_normandie_v05_field_sessions.py` et du garde-fou Sprint 85.\n\n',
)

print("Sprint 85 finalization complete")
