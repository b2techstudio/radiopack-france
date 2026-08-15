#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Anchor not found in {path}: {old[:140]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before(path: Path, anchor: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if block.strip() in text:
        return
    if anchor not in text:
        raise RuntimeError(f"Insert anchor not found in {path}: {anchor!r}")
    path.write_text(text.replace(anchor, block + anchor, 1), encoding="utf-8")


# Machine state.
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated"] = "2026-08-15"
state["current_sprint"] = 84
state["state_version"] = "0.21.73"
active = state["active_work"]
active["status"] = "field_validation_kit_prepared_zero_delta_142_not_public"
active["internal_candidate_memory_count"] = 142
active["internal_candidate_new_memory_count"] = 0
active["field_validation_kit"] = "research/normandie-v0.5/field-validation-kit.json"
active["field_validation_kit_builder"] = "tools/build_normandie_v05_field_validation_kit.py"
active["field_validation_kit_guard"] = "tests/test_sprint84_normandie_v05_field_validation_kit.py"
active["field_validation_probe_memory_count"] = 6
active["field_validation_session_template_generated"] = True
active["field_validation_changes_candidate"] = False
active["r3_field_reception_from_mortain_validated"] = False
active["f5zha_useful_mortain_coverage_verified"] = False
active["public_export_allowed"] = False
active["public_registry_allowed"] = False
active["public_release_ready"] = False
state["latest_sprint84_normandie_v0_5_field_kit"] = {
    "sprint": 84,
    "state_version": "0.21.73",
    "prepared_on": "2026-08-15",
    "candidate_memory_count": 142,
    "candidate_memory_delta": 0,
    "field_probe_memory_count": 6,
    "probe_names": ["R3-OUT", "R3-IN", "ZHA-VHF", "ZHA-UHF", "ZHA-OLD", "CTRL-ZHY"],
    "r3_minimum_independent_sessions": 2,
    "f5zha_minimum_independent_sessions": 2,
    "f5zha_minimum_intelligibility_0_to_5": 3,
    "legacy_f5zha_probe_diagnostic_only": True,
    "public_export_allowed": False,
}
for item in [
    "research/normandie-v0.5/field-validation-kit.json",
    "research/sprint-84-summary.md",
]:
    if item not in state.setdefault("sources_of_truth", []):
        state["sources_of_truth"].append(item)
field_tools = state.get("field_tools")
if isinstance(field_tools, dict):
    field_tools["build_normandie_v05_field_validation_kit"] = "tools/build_normandie_v05_field_validation_kit.py"
    field_tools["test_sprint84_normandie_v05_field_validation_kit"] = "tests/test_sprint84_normandie_v05_field_validation_kit.py"
elif isinstance(field_tools, list):
    for item in [
        "tools/build_normandie_v05_field_validation_kit.py",
        "tests/test_sprint84_normandie_v05_field_validation_kit.py",
    ]:
        if item not in field_tools:
            field_tools.append(item)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Generic repository guard.
site = ROOT / "tests/test_site_files.py"
insert_before(
    site,
    '    "tests/test_normandie_v04_public_release.py",\n',
    '    "research/normandie-v0.5/field-validation-kit.json",\n'
    '    "tools/build_normandie_v05_field_validation_kit.py",\n'
    '    "tests/test_sprint84_normandie_v05_field_validation_kit.py",\n'
    '    "research/sprint-84-summary.md",\n',
)

# README.
readme = ROOT / "README.md"
replace_once(
    readme,
    '**État courant : Sprint 83 / 0.21.72 — Normandie v0.5 reste à 142 mémoires RX après revalidation actuelle des quatre dossiers différés ; delta RF 0, plafond potentiel 147 hors F6ZES, aucune publication.**',
    '**État courant : Sprint 84 / 0.21.73 — Normandie v0.5 reste à 142 mémoires RX ; un kit terrain RX-only de 6 sondes prépare la validation R3/F5ZHA sans modifier le candidat ni publier v0.5.**',
)
replace_once(readme, '## État actuel — Sprint 83 / 0.21.72', '## État actuel — Sprint 84 / 0.21.73')
replace_once(
    readme,
    'Recherche : Normandie v0.5 reste à **142 mémoires RX**, delta 0, après revalidation le 15 août 2026 des quatre dossiers différés ; le plafond potentiel reste **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
    'Recherche : Normandie v0.5 reste à **142 mémoires RX**, delta 0. Un mini-pack terrain de **6 sondes RX-only** est maintenant prêt pour produire des observations reproductibles sur R3 F1ZBX et F5ZHA depuis Mortain ; ces six sondes ne sont pas des mémoires candidates. Le plafond potentiel reste **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
)
replace_once(
    readme,
    '`research/sprint-82-summary.md` et `research/sprint-83-summary.md`.',
    '`research/sprint-82-summary.md`, `research/sprint-83-summary.md` et `research/sprint-84-summary.md`.',
)
insert_before(
    readme,
    '## Sprint 83 — revalidation ciblée Normandie v0.5\n',
    '## Sprint 84 — kit terrain Normandie v0.5\n\n'
    'Le candidat reste à **142 mémoires RX**. Un kit de validation non public regroupe désormais six sondes : `R3-OUT`, `R3-IN`, `ZHA-VHF`, `ZHA-UHF`, `ZHA-OLD` et `CTRL-ZHY`.\n\n'
    '- R3 : deux sessions RX indépendantes et identifiées sur 145.675 MHz restent nécessaires ;\n'
    '- F5ZHA : deux sessions indépendantes sur la paire actuelle 145.4675 / 432.575 MHz restent nécessaires, avec intelligibilité minimale 3/5 ;\n'
    '- 431.4125 MHz reste une sonde diagnostique historique et ne peut jamais promouvoir F5ZHA à elle seule ;\n'
    '- un modèle CSV de journal terrain est généré avec date, lieu, matériel, fréquence, identification, intelligibilité et notes ;\n'
    '- aucune mémoire publique ni candidate n’est ajoutée.\n\n'
    'Kit : `research/normandie-v0.5/field-validation-kit.json`. Builder : `tools/build_normandie_v05_field_validation_kit.py`. Garde-fou : `tests/test_sprint84_normandie_v05_field_validation_kit.py`.\n\n',
)

# PROJECT_STATUS.
status = ROOT / "PROJECT_STATUS.md"
replace_once(status, 'Sprint courant : **83**\nÉtat logique : **0.21.72**', 'Sprint courant : **84**\nÉtat logique : **0.21.73**')
replace_once(status, 'Résumé courant : `research/sprint-83-summary.md`.', 'Résumé courant : `research/sprint-84-summary.md`.')
insert_before(
    status,
    '## Sprint 83 — Normandie v0.5 revalidée, delta 0\n',
    '## Sprint 84 — kit terrain Normandie v0.5\n\n'
    'Le candidat reste à **142 RX, delta 0**. Le travail de terrain R3/F5ZHA est désormais préparé sous forme d’un mini-pack CHIRP non public de **6 sondes** et d’un journal de sessions vide généré automatiquement.\n\n'
    '- R3 : `R3-OUT` 145.675 et `R3-IN` 145.075 ;\n'
    '- F5ZHA actuel : `ZHA-VHF` 145.4675 et `ZHA-UHF` 432.575 ;\n'
    '- diagnostic seulement : `ZHA-OLD` 431.4125 ;\n'
    '- contrôle facultatif : `CTRL-ZHY` 145.6875 ;\n'
    '- aucune promotion, aucun CSV public v0.5, aucun changement du registre.\n\n'
    'Kit : `research/normandie-v0.5/field-validation-kit.json`. Builder : `tools/build_normandie_v05_field_validation_kit.py`. Test : `tests/test_sprint84_normandie_v05_field_validation_kit.py`.\n\n',
)

# Normandie research README.
v05 = ROOT / "research/normandie-v0.5/README.md"
replace_once(
    v05,
    'État : **Sprint 83 / 0.21.72 — candidat interne 142 mémoires RX, delta 0 après revalidation des quatre dossiers différés**.',
    'État : **Sprint 84 / 0.21.73 — candidat interne 142 mémoires RX, delta 0 ; kit terrain R3/F5ZHA prêt sans publication**.',
)
insert_before(
    v05,
    '## Sprint 83 — revalidation actuelle\n',
    '## Sprint 84 — kit terrain R3 / F5ZHA\n\n'
    'Le fichier `field-validation-kit.json` regroupe six sondes RX-only et les gates associés. Le builder `tools/build_normandie_v05_field_validation_kit.py` génère un CSV CHIRP de diagnostic, un journal de sessions vide et un manifeste machine.\n\n'
    'Ce kit ne modifie pas le candidat : **142 → 142, delta 0**. Les sessions terrain sont des preuves, jamais des mémoires supplémentaires.\n\n',
)

# CHANGELOG.
changelog = ROOT / "CHANGELOG.md"
insert_before(
    changelog,
    '## 0.21.72 - 2026-08-15\n',
    '## 0.21.73 - 2026-08-15\n\n'
    '- **Sprint 84** : préparation d’un kit terrain Normandie v0.5 pour R3 F1ZBX et F5ZHA ; candidat maintenu à **142 mémoires RX**, delta **0**.\n'
    '- Mini-pack CHIRP non public de **6 sondes** : R3 sortie/entrée, paire F5ZHA actuelle, ancienne valeur F5ZHA strictement diagnostique et contrôle F5ZHY facultatif.\n'
    '- Génération d’un modèle CSV de journal de sessions reproductible ; les sessions restent des preuves et ne créent aucune mémoire.\n'
    '- Ajout du builder `build_normandie_v05_field_validation_kit.py`, du manifeste `field-validation-kit.json` et du garde-fou Sprint 84 ; aucune publication v0.5.\n\n',
)

print("Sprint 84 finalization complete")
