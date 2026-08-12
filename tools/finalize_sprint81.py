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


# Forward-compatible Sprint 80 state guard.
s80 = ROOT / "tests/test_sprint80_bretagne_v02_publication.py"
replace_once(
    s80,
    'assert state["current_sprint"] == 80\nassert state["state_version"] == "0.21.69"\n',
    'assert state["current_sprint"] >= 80\nassert tuple(map(int, state["state_version"].split("."))) >= (0, 21, 69)\n',
)
replace_once(
    s80,
    'print("Sprint 80: Bretagne v0.2 published immutable at 151 RX memories with AIRAC 08/26 boundary preserved OK")',
    'print("Sprint 80: Bretagne v0.2 immutable publication remains auditable after later Bretagne version initialization OK")',
)

# CI: add Sprint 81 guard after publication guard.
ci = ROOT / ".github/workflows/ci.yml"
insert_before(
    ci,
    '      - name: Test CROSS Etel network research\n',
    '      - name: Test Sprint 81 Bretagne v0.3 initialization\n'
    '        run: python tests/test_sprint81_bretagne_v03_initialization.py\n\n',
)

# Site-file guard: require the Sprint 81 source-of-truth files.
site = ROOT / "tests/test_site_files.py"
insert_before(
    site,
    '    "research/normandie-v0.4/README.md",\n',
    '    "research/bretagne-v0.3/README.md",\n'
    '    "research/bretagne-v0.3/pack-plan.json",\n'
    '    "research/bretagne-v0.3/backlog.json",\n'
    '    "research/bretagne-v0.3/airac-transition-policy.json",\n'
    '    "research/sprint-81-summary.md",\n'
    '    "tools/build_bretagne_v03_internal_candidate.py",\n'
    '    "tests/test_sprint81_bretagne_v03_initialization.py",\n',
)
insert_before(
    site,
    '    "Normandie v0.4",\n',
    '    "Bretagne v0.3",\n',
)

# Project state.
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated"] = "2026-08-12"
state["current_sprint"] = 81
state["state_version"] = "0.21.70"
state["completed_bretagne_v0_2_release"] = {
    "pack": "Bretagne",
    "version": "0.2",
    "memory_count": 151,
    "new_memory_count_vs_v0_1": 16,
    "immutable": True,
    "aviation_memory_count": 16,
    "aviation_cycle": "AIRAC 08/26",
    "aviation_valid_through_inclusive": "2026-09-02",
    "publication_sprint": 80,
    "published_on": "2026-08-12",
    "publication_record": "research/bretagne-v0.2/publication-record.json",
    "public_csv": "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
    "public_csv_sha256": "73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4",
}
state["active_work"] = {
    "pack": "Bretagne",
    "target_version": "0.3",
    "status": "initialized_from_immutable_public_v0_2_151_not_public",
    "public_export_allowed": False,
    "public_registry_allowed": False,
    "public_release_ready": False,
    "published_base_version": "0.2",
    "published_base_memory_count": 151,
    "published_base_is_immutable": True,
    "published_base_sha256": "73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4",
    "internal_candidate_memory_count": 151,
    "internal_candidate_new_memory_count": 0,
    "internal_candidate_builder": "tools/build_bretagne_v03_internal_candidate.py",
    "pack_plan": "research/bretagne-v0.3/pack-plan.json",
    "backlog": "research/bretagne-v0.3/backlog.json",
    "airac_transition_policy": "research/bretagne-v0.3/airac-transition-policy.json",
    "backlog_item_count": 7,
    "backlog_ids": [
        "AIRAC_09_BRETAGNE_REVALIDATION",
        "F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY",
        "CROSS_ETEL_CH64_LOCAL_MAPPING",
        "CROSS_CORSEN_CH79_LOCAL_MAPPING",
        "F5ZPV_RESTART_REVALIDATION",
        "F5ZZH_RESTART_REVALIDATION",
        "F5ZZC4_CURRENT_APRS_FREQUENCY",
    ],
    "current_sia_cycle": "AIRAC 08/26",
    "current_sia_valid_through": "2026-09-02",
    "next_airac_cycle": "AIRAC 09/26",
    "next_airac_valid_from": "2026-09-03",
    "next_airac_valid_through": "2026-09-30",
    "post_transition_aviation_revalidation_required": True,
    "current_sia_xml_export_bytes_extracted": False,
    "current_xml_field_match_claimed": False,
    "channel64_generic_pair_in_published_base": True,
    "channel79_generic_pair_in_published_base": True,
    "channel64_local_site_claimed": False,
    "channel79_local_site_claimed": False,
    "private_ppdr_operational_data_excluded": True,
    "resolved_v0_2_items_not_reopened": [
        "ADRASEC_PUBLIC_DATA_REVALIDATION",
        "F1ZBZ_RF_DIRECTION_REVIEW",
    ],
    "published": False,
    "scope_frozen": False,
    "prepublication_ready": False,
}
state["latest_sprint81_bretagne_v0_3_initialization"] = {
    "sprint": 81,
    "state_version": "0.21.70",
    "initialized_on": "2026-08-12",
    "base_version": "0.2",
    "base_memory_count": 151,
    "candidate_memory_count": 151,
    "candidate_memory_delta": 0,
    "public_v0_3_exists": False,
    "airac08_valid_through_inclusive": "2026-09-02",
    "airac09_effective_from": "2026-09-03",
    "airac09_effective_through_inclusive": "2026-09-30",
    "carried_open_dossier_count": 6,
    "scheduled_transition_dossier_count": 1,
}
sources = state.setdefault("sources_of_truth", [])
for item in [
    "research/bretagne-v0.2/publication-record.json",
    "research/bretagne-v0.3/pack-plan.json",
    "research/bretagne-v0.3/backlog.json",
    "research/bretagne-v0.3/airac-transition-policy.json",
    "research/bretagne-v0.3/README.md",
    "research/sprint-81-summary.md",
]:
    if item not in sources:
        sources.append(item)
field_tools = state.get("field_tools")
if isinstance(field_tools, dict):
    field_tools["build_bretagne_v03_internal_candidate"] = "tools/build_bretagne_v03_internal_candidate.py"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# README.
readme = ROOT / "README.md"
replace_once(
    readme,
    '**État courant : Sprint 80 / 0.21.69 — Bretagne v0.2 est publiée et immuable à 151 mémoires RX, avec 16 mémoires aviation AIRAC 08/26.**',
    '**État courant : Sprint 81 / 0.21.70 — Bretagne v0.3 est initialisée en recherche à 151 mémoires RX depuis la v0.2 publique immuable ; delta initial 0.**',
)
replace_once(readme, '## État actuel — Sprint 80 / 0.21.69', '## État actuel — Sprint 81 / 0.21.70')
replace_once(
    readme,
    'Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.2 est désormais **publique à 151 mémoires RX** : base historique v0.1=135 + 16 mémoires aviation AIRAC 08/26.',
    'Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.3 démarre à **151 mémoires RX**, delta 0, comme copie interne exacte de la v0.2 publique immuable ; la prochaine transition aviation est AIRAC 09/26 au 3 septembre 2026.',
)
replace_once(
    readme,
    '`research/sprint-79-summary.md` et `research/sprint-80-summary.md`.',
    '`research/sprint-79-summary.md`, `research/sprint-80-summary.md` et `research/sprint-81-summary.md`.',
)
insert_before(
    readme,
    '## Sprint 80 — publication Bretagne v0.2\n',
    '## Sprint 81 — initialisation Bretagne v0.3\n\n'
    'Bretagne v0.3 est initialisée en recherche depuis la **v0.2 publique immuable à 151 mémoires RX**. Le candidat interne initial reproduit exactement le CSV v0.2 : **151 → 151, delta 0**, sans CSV public v0.3 ni changement de registre.\n\n'
    '- base SHA-256 : `73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4` ;\n'
    '- builder : `tools/build_bretagne_v03_internal_candidate.py` ;\n'
    '- backlog limité aux dossiers réellement ouverts : AIRAC 09/26, F1ZUG public uniquement, CROSS Ch64/Ch79, F5ZPV, F5ZZH et F5ZZC-4 ;\n'
    '- ADRASEC général déjà résolu à delta 0 et F1ZBZ déjà représenté ne sont pas rouverts sans nouvelle preuve ;\n'
    '- AIRAC 08/26 reste la base aviation courante jusqu’au 2 septembre 2026 inclus ; toute publication v0.3 à partir du 3 septembre exige une revalidation AIRAC 09/26.\n\n'
    'Garde-fou : `tests/test_sprint81_bretagne_v03_initialization.py`.\n\n',
)
replace_once(readme, '`research/sprint-61-summary.md` à `research/sprint-80-summary.md`', '`research/sprint-61-summary.md` à `research/sprint-81-summary.md`')
insert_before(
    readme,
    'python tests\\test_bretagne_public_release.py\n',
    'python tests\\test_sprint81_bretagne_v03_initialization.py\n',
)
insert_before(
    readme,
    'python tests\\test_site_files.py\n',
    'python tools\\build_bretagne_v03_internal_candidate.py\npython tests\\test_sprint81_bretagne_v03_initialization.py\n',
)

# PROJECT_STATUS.
status = ROOT / "PROJECT_STATUS.md"
replace_once(status, 'Sprint courant : **80**\nÉtat logique : **0.21.69**', 'Sprint courant : **81**\nÉtat logique : **0.21.70**')
replace_once(status, 'Résumé courant : `research/sprint-80-summary.md`.', 'Résumé courant : `research/sprint-81-summary.md`.')
insert_before(
    status,
    '## Sprint 80 — Bretagne v0.2 publiée à 151\n',
    '## Sprint 81 — Bretagne v0.3 initialisée à 151\n\n'
    'La prochaine version Bretagne démarre depuis la v0.2 publique immuable, sans ajout automatique : **151 mémoires RX, delta 0**. Le builder v0.3 recopie exactement la v0.2 et vérifie son SHA-256.\n\n'
    '- aucune v0.3 publique ni bascule de registre ;\n'
    '- AIRAC 08/26 reste courant jusqu’au 2 septembre 2026 inclus ; AIRAC 09/26 commence le 3 septembre ;\n'
    '- toute future publication v0.3 après cette transition doit revalider l’aviation ;\n'
    '- seuls F1ZUG public, CROSS Ch64/Ch79, F5ZPV, F5ZZH et F5ZZC-4 restent reportés, plus la transition AIRAC ;\n'
    '- les revues ADRASEC générales à delta 0 et F1ZBZ ne sont pas rouvertes sans nouvelle preuve.\n\n'
    'Test : `tests/test_sprint81_bretagne_v03_initialization.py`.\n\n',
)
insert_before(
    status,
    'python tests\\test_sprint74_bretagne_v02_initialization.py\n',
    'python tools\\build_bretagne_v03_internal_candidate.py\npython tests\\test_sprint81_bretagne_v03_initialization.py\n',
)

# CHANGELOG.
changelog = ROOT / "CHANGELOG.md"
insert_before(
    changelog,
    '## 0.21.69 - 2026-08-12\n',
    '## 0.21.70 - 2026-08-12\n\n'
    '- **Sprint 81** : initialisation de Bretagne v0.3 à partir de la v0.2 publique immuable = **151 mémoires RX**.\n'
    '- Candidat interne initial **151, delta 0**, copie exacte du CSV public v0.2 contrôlée par SHA-256 ; aucune publication v0.3 ni changement de registre.\n'
    '- Politique de transition AIRAC : 08/26 valable jusqu’au 2 septembre 2026 inclus, 09/26 effectif le 3 septembre ; revalidation aviation obligatoire avant toute publication v0.3 post-transition.\n'
    '- Backlog réduit aux dossiers encore ouverts : F1ZUG public uniquement, CROSS Ch64/Ch79, F5ZPV, F5ZZH, F5ZZC-4 et transition AIRAC 09/26.\n'
    '- Ajout du builder v0.3, du garde-fou Sprint 81 et adaptation forward-compatible du test de publication Sprint 80.\n\n',
)

# Remove temporary finalizer assets from the final tree.
for rel in [
    "tools/finalize_sprint81.py",
    ".github/workflows/finalize-sprint81.yml",
    ".github/sprint81-finalize-trigger",
]:
    path = ROOT / rel
    if path.exists():
        path.unlink()

print("Sprint 81 finalization complete")
