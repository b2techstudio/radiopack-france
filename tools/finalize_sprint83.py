#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Anchor not found in {path}: {old[:120]!r}")
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
state["current_sprint"] = 83
state["state_version"] = "0.21.72"
state["active_work"] = {
    "pack": "Normandie",
    "target_version": "0.5",
    "status": "current_blockers_revalidated_zero_delta_142_not_public",
    "public_export_allowed": False,
    "public_registry_allowed": False,
    "public_release_ready": False,
    "published_base_version": "0.4",
    "published_base_memory_count": 142,
    "published_base_is_immutable": True,
    "published_base_sha256": "3da26f18cefbf7ec1dfb6a991101d07f6a8ce9fb921015a7202870fc9b9db66d",
    "internal_candidate_memory_count": 142,
    "internal_candidate_new_memory_count": 0,
    "known_potential_ceiling_excluding_f6zes": 147,
    "internal_candidate_builder": "tools/build_normandie_v05_internal_candidate.py",
    "pack_plan": "research/normandie-v0.5/pack-plan.json",
    "backlog": "research/normandie-v0.5/backlog.json",
    "current_blocker_revalidation": "research/normandie-v0.5/current-blocker-revalidation.json",
    "backlog_item_count": 4,
    "backlog_ids": [
        "R3_MORTAIN_RX",
        "F5ZHA_SOURCE_AND_COVERAGE",
        "F1ZOV_OPERATIONAL_STATUS",
        "F6ZES_RESOLVED",
    ],
    "last_revalidated_on": "2026-08-15",
    "last_revalidation_memory_delta": 0,
    "last_revalidation_promoted_item_count": 0,
    "r3_current_operator_status": "operational",
    "r3_field_reception_from_mortain_validated": False,
    "r3_minimum_independent_rx_sessions_required": 2,
    "f5zha_current_ref_pair_mhz": [145.4675, 432.575],
    "f5zha_secondary_stale_conflict_frequency_mhz": 431.4125,
    "f5zha_useful_mortain_coverage_verified": False,
    "f1zov_local_operator_status": "maintenance",
    "f1zov_ref_directory_status": "active",
    "f6zes_usable_frequency_published": False,
    "f6zes_mode_published": False,
    "f6zes_operational_state_published": False,
    "published": False,
    "scope_frozen": False,
    "prepublication_ready": False,
}
state["latest_sprint83_normandie_v0_5_revalidation"] = {
    "sprint": 83,
    "state_version": "0.21.72",
    "checked_on": "2026-08-15",
    "candidate_memory_count_before": 142,
    "candidate_memory_count_after": 142,
    "candidate_memory_delta": 0,
    "promoted_item_count": 0,
    "known_potential_ceiling_excluding_f6zes": 147,
    "r3_field_gate_open": True,
    "f5zha_field_coverage_gate_open": True,
    "f1zov_maintenance_gate_open": True,
    "f6zes_frequency_mode_state_unresolved": True,
}
for item in [
    "research/normandie-v0.5/current-blocker-revalidation.json",
    "research/sprint-83-summary.md",
]:
    if item not in state.setdefault("sources_of_truth", []):
        state["sources_of_truth"].append(item)
field_tools = state.get("field_tools")
if isinstance(field_tools, dict):
    field_tools["build_normandie_v05_internal_candidate"] = "tools/build_normandie_v05_internal_candidate.py"
    field_tools["test_sprint83_normandie_v05_revalidation"] = "tests/test_sprint83_normandie_v05_revalidation.py"
elif isinstance(field_tools, list):
    for item in ["tools/build_normandie_v05_internal_candidate.py", "tests/test_sprint83_normandie_v05_revalidation.py"]:
        if item not in field_tools:
            field_tools.append(item)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Generic repository guard.
site = ROOT / "tests/test_site_files.py"
insert_before(
    site,
    '    "tests/test_normandie_v04_public_release.py",\n',
    '    "research/normandie-v0.5/current-blocker-revalidation.json",\n'
    '    "tools/build_normandie_v05_internal_candidate.py",\n'
    '    "tests/test_sprint83_normandie_v05_revalidation.py",\n'
    '    "research/sprint-83-summary.md",\n',
)

# README.
readme = ROOT / "README.md"
replace_once(
    readme,
    '**État courant : Sprint 82 / 0.21.71 — Bretagne v0.3 reste à 151 mémoires RX après revalidation publique ciblée de six dossiers ; delta RF 0, aucune publication.**',
    '**État courant : Sprint 83 / 0.21.72 — Normandie v0.5 reste à 142 mémoires RX après revalidation actuelle des quatre dossiers différés ; delta RF 0, plafond potentiel 147 hors F6ZES, aucune publication.**',
)
replace_once(readme, '## État actuel — Sprint 82 / 0.21.71', '## État actuel — Sprint 83 / 0.21.72')
replace_once(
    readme,
    'Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 : les six dossiers non-AIRAC ouverts ont été revalidés le 15 août 2026 sans promotion ; la prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
    'Recherche : Normandie v0.5 reste à **142 mémoires RX**, delta 0, après revalidation le 15 août 2026 des quatre dossiers différés ; le plafond potentiel reste **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
)
replace_once(
    readme,
    '`research/sprint-81-summary.md` et `research/sprint-82-summary.md`.',
    '`research/sprint-81-summary.md`, `research/sprint-82-summary.md` et `research/sprint-83-summary.md`.',
)
insert_before(
    readme,
    '## Sprint 82 — revalidation publique ciblée Bretagne v0.3\n',
    '## Sprint 83 — revalidation ciblée Normandie v0.5\n\n'
    'Les quatre dossiers différés de Normandie v0.5 ont été recontrôlés le **15 août 2026**. Résultat : **142 → 142 mémoires RX, delta RF 0, zéro promotion**. Le plafond potentiel reste **147** hors F6ZES.\n\n'
    '- **R3 F1ZBX** : opérateur actuel confirmé, paire `145.075 / 145.675 MHz`, mais deux sessions RX indépendantes depuis Mortain restent obligatoires ;\n'
    '- **F5ZHA Laval** : le REF courant et une seconde liste convergent sur `145.4675 / 432.575 MHz`; RepeaterBook conserve `431.4125 MHz` avec une vérification 2017, classée conflit secondaire ancien ; la couverture Mortain reste non démontrée ;\n'
    '- **F1ZOV** : toujours `En Maintenance` chez F6KFW malgré le REF actif ; le statut opérateur local prime ;\n'
    '- **F6ZES Sourdeval** : site toujours listé mais sans fréquence, mode ni état opérationnel exploitables ; rien n’est deviné.\n\n'
    'Builder : `tools/build_normandie_v05_internal_candidate.py`. Preuve : `research/normandie-v0.5/current-blocker-revalidation.json`. Garde-fou : `tests/test_sprint83_normandie_v05_revalidation.py`.\n\n',
)
if '`research/sprint-61-summary.md` à `research/sprint-82-summary.md`' in readme.read_text(encoding='utf-8'):
    replace_once(readme, '`research/sprint-61-summary.md` à `research/sprint-82-summary.md`', '`research/sprint-61-summary.md` à `research/sprint-83-summary.md`')

# PROJECT_STATUS.
status = ROOT / "PROJECT_STATUS.md"
replace_once(status, 'Sprint courant : **82**\nÉtat logique : **0.21.71**', 'Sprint courant : **83**\nÉtat logique : **0.21.72**')
replace_once(status, 'Résumé courant : `research/sprint-82-summary.md`.', 'Résumé courant : `research/sprint-83-summary.md`.')
insert_before(
    status,
    '## Sprint 82 — Bretagne v0.3 revalidée, delta 0\n',
    '## Sprint 83 — Normandie v0.5 revalidée, delta 0\n\n'
    'Revalidation actuelle des quatre dossiers différés : **candidat 142, delta RF 0, zéro promotion**, plafond potentiel **147** hors F6ZES.\n\n'
    '- R3 F1ZBX : paramètres opérateur actuels confirmés, gate terrain Mortain toujours ouvert ;\n'
    '- F5ZHA : paire REF `145.4675 / 432.575 MHz` renforcée, conflit RepeaterBook 2017 classé secondaire ancien, couverture terrain toujours requise ;\n'
    '- F1ZOV : maintenance locale reconfirmée, donc pas de promotion malgré le REF actif ;\n'
    '- F6ZES : site confirmé sans fréquence/mode/état utilisables ; aucune hypothèse.\n\n'
    'Builder : `tools/build_normandie_v05_internal_candidate.py`. Preuve : `research/normandie-v0.5/current-blocker-revalidation.json`. Test : `tests/test_sprint83_normandie_v05_revalidation.py`.\n\n',
)

# Normandie v0.5 README.
v05 = ROOT / "research/normandie-v0.5/README.md"
v05.write_text(
    '# Normandie v0.5 — recherche\n\n'
    'État : **Sprint 83 / 0.21.72 — candidat interne 142 mémoires RX, delta 0 après revalidation des quatre dossiers différés**.\n\n'
    'Base publique immuable : **Normandie v0.4, 142 mémoires RX**. Le plafond potentiel connu reste **147 mémoires** hors F6ZES.\n\n'
    '## Sprint 83 — revalidation actuelle\n\n'
    '- R3 F1ZBX : `145.075 / 145.675 MHz`, opérationnel chez l’ARA35, mais deux sessions RX indépendantes depuis Mortain restent requises ;\n'
    '- F5ZHA Laval : paire REF actuelle `145.4675 / 432.575 MHz`; conflit secondaire RepeaterBook `431.4125 MHz` daté 2017 ; couverture Mortain non validée ;\n'
    '- F1ZOV : toujours en maintenance selon F6KFW, malgré REF actif ;\n'
    '- F6ZES : Sourdeval confirmé sans fréquence, mode ni état opérationnel exploitables.\n\n'
    'Aucun de ces dossiers n’est promu : **142 → 142, delta 0**.\n\n'
    'Le builder `tools/build_normandie_v05_internal_candidate.py` vérifie le record de publication v0.4, son SHA-256, le contrat RX-only et l’unicité des positions, noms et RF, puis reproduit exactement le CSV v0.4 comme candidat interne v0.5.\n\n'
    'Preuve : `current-blocker-revalidation.json`.\n\n'
    'Règles : RX-only, `Duplex=off`, `Offset=0.000000`, pas de fréquence devinée, deux mémoires RX pour une paire distincte vérifiée, géométrie ≠ preuve de réception, et un gate terrain ne peut pas être satisfait par une recherche web.\n',
    encoding='utf-8',
)

# CHANGELOG.
changelog = ROOT / "CHANGELOG.md"
insert_before(
    changelog,
    '## 0.21.71 - 2026-08-15\n',
    '## 0.21.72 - 2026-08-15\n\n'
    '- **Sprint 83** : revalidation actuelle des quatre dossiers différés de Normandie v0.5 ; candidat maintenu à **142 mémoires RX**, delta RF **0**, plafond potentiel **147** hors F6ZES.\n'
    '- R3 F1ZBX opérationnel et paire `145.075 / 145.675 MHz` reconfirmés, mais gate terrain Mortain toujours ouvert.\n'
    '- F5ZHA : paire REF `145.4675 / 432.575 MHz` renforcée ; conflit RepeaterBook `431.4125 MHz` daté 2017 conservé comme conflit secondaire ancien ; couverture Mortain toujours requise.\n'
    '- F1ZOV reste en maintenance chez l’opérateur local ; F6ZES reste sans fréquence/mode/état exploitables.\n'
    '- Ajout du builder interne v0.5, de `current-blocker-revalidation.json` et du garde-fou Sprint 83 ; aucune publication v0.5.\n\n',
)

print("Sprint 83 finalization complete")
