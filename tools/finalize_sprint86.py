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


# Annecy v0.3 plan.
plan_path = ROOT / "research/annecy-alpes-leman-v0.3/pack-plan.json"
plan = json.loads(plan_path.read_text(encoding="utf-8"))
plan["schema_version"] = "1.2"
plan["updated"] = "2026-08-15"
plan["latest_revalidation"] = {
    "sprint": 86,
    "checked_on": "2026-08-15",
    "evidence": "research/annecy-alpes-leman-v0.3/paired-rx-expansion.json",
    "builder": "tools/build_annecy_v03_internal_candidate.py",
    "candidate_full_memory_count": 76,
    "candidate_without_aviation_memory_count": 59,
    "new_unique_rf_memory_count": 11,
    "potential_ceiling_if_f1zth_50m_clears": 77,
    "public_export_allowed": False,
}
plan["memory_plan"] = {
    "status": "sprint86_internal_candidate_defined_not_public",
    "published_base_memory_count": 65,
    "published_base_memory_count_without_aviation": 48,
    "expected_memory_count": 76,
    "expected_memory_count_without_aviation": 59,
    "new_unique_rf_memory_count": 11,
    "potential_ceiling_if_f1zth_50m_clears": 77,
    "new_blocks": [
        {"id": "satellite_split_uplinks", "unique_rf_memory_count": 2},
        {"id": "paired_rx_france", "unique_rf_memory_count": 7},
        {"id": "paired_rx_switzerland", "unique_rf_memory_count": 2},
    ],
    "deferred": ["F1ZTH 50.5375 MHz pending project device/firmware RX compatibility baseline"],
}
plan["publication"]["public_export_allowed"] = False
plan["publication"]["public_registry_allowed"] = False
plan["publication"]["public_routes_allowed"] = False
plan["publication"]["review_required"] = True
plan["publication"]["review_completed"] = False
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Annecy v0.3 README.
annecy_readme = ROOT / "research/annecy-alpes-leman-v0.3/README.md"
annecy_readme.write_text(
    '# Annecy–Alpes–Léman v0.3 — recherche\n\n'
    'État : **Sprint 86 / 0.21.75 — premier candidat interne à 76 mémoires RX, 59 sans aviation, +11 RF uniques, aucune publication**.\n\n'
    'La base publique **v0.2 reste immuable à 65 mémoires / 48 sans aviation**. Le candidat v0.3 applique désormais la politique paired RX aux liaisons split/duplex déjà sélectionnées et aux nouveaux cas publics validés.\n\n'
    '## Candidat Sprint 86\n\n'
    '- base v0.2 complète : **65 RX** ;\n'
    '- base v0.2 sans aviation : **48 RX** ;\n'
    '- candidat v0.3 complet : **76 RX** ;\n'
    '- candidat v0.3 sans aviation : **59 RX** ;\n'
    '- delta : **+11 RF uniques** ;\n'
    '- plafond conditionnel : **77** si F1ZTH 50.5375 MHz franchit le gate de compatibilité UV-K5/firmware ;\n'
    '- `Duplex=off`, `Offset=0.000000`, aucune émission ;\n'
    '- aucune route ni entrée de registre v0.3.\n\n'
    'Preuve structurée : `paired-rx-expansion.json`. Builder : `tools/build_annecy_v03_internal_candidate.py`.\n\n'
    '## Satellites paired RX\n\n'
    'La v0.2 publique conserve les descentes historiques. La v0.3 ajoute **145.850 MHz** comme montée RX partagée SO-50/AO-123 et **435.250 MHz** comme montée RX AO-91. La fréquence 145.850 n’est mémorisée qu’une fois. Les descentes restent déjà présentes : SO-50 436.795, AO-91 145.960, AO-123 435.400 MHz.\n\n'
    'Le statut opérationnel AMSAT doit être recontrôlé avant toute publication v0.3.\n\n'
    '## Relais France\n\n'
    'Nouvelles entrées RX de relais dont les sorties étaient déjà sélectionnées :\n\n'
    '- F1ZOH Crozet : **439.625 MHz** ;\n'
    '- F6ZJD Nurieux : **145.0375 MHz** ;\n'
    '- F1ZCQ Échirolles : **145.050 MHz** ;\n'
    '- F1ZCR Chamrousse : **430.325 MHz** ;\n'
    '- F1ZDC Échirolles : **431.425 MHz**.\n\n'
    'F1ZPY/F1ZWY et les transpondeurs F5ZDT, F1ZFX, F1ZIC, F1ZHE, F1ZHG, F5ZGT et F5ZLV n’ajoutent aucune RF après déduplication : leurs deux côtés sont déjà représentés dans la base.\n\n'
    '## Haute-Savoie / ADRASEC public\n\n'
    'F1ZJV Pointe des Brasses et F1ZYT Semnoz partagent la paire analogique VHF publique **145.1875 / 145.7875 MHz**. Deux mémoires RF suffisent aux deux sites.\n\n'
    'La source locale mentionne un lien/transpondeur UHF ADRASEC mais n’en publie pas la fréquence : aucune fréquence UHF n’est inférée, recherchée dans des données privées ou ajoutée au candidat.\n\n'
    '## Suisse HB9G\n\n'
    'Les sorties HB9G 145.725 et 439.100 MHz étant déjà présentes, le paired RX ajoute leurs entrées **145.125 MHz** et **431.500 MHz**.\n\n'
    '## F1ZTH 50 MHz différé\n\n'
    'Le REF publie **50.5375 MHz** comme côté analogique supplémentaire de F1ZTH. Les deux autres côtés, 431.275 et 145.2125 MHz, sont déjà présents. La RF 50.5375 représente donc un potentiel +1, mais reste hors candidat tant que RadioPack n’a pas défini et vérifié une base de compatibilité récepteur/firmware UV-K5 permettant de la garantir aux utilisateurs. Aucun firmware tiers n’est supposé.\n\n'
    '## Génération\n\n'
    '```bash\npython tools/build_annecy_v03_internal_candidate.py --output-dir annecy-v03\npython tools/build_annecy_v03_internal_candidate.py --no-aviation --output-dir annecy-v03-no-air\n```\n\n'
    'Le builder repart du candidat v0.2 validé, conserve ses lignes à l’identique et ajoute uniquement les 11 RF de `paired-rx-expansion.json`.\n\n'
    'Règles permanentes : v0.2 immuable, RX-only, fréquence identique dédupliquée, données non publiées jamais inférées, réseaux professionnels privés/PPDR exclus, revue humaine obligatoire avant publication.\n',
    encoding="utf-8",
)

# Machine-readable project state.
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated"] = "2026-08-15"
state["current_sprint"] = 86
state["state_version"] = "0.21.75"
state["active_work"] = {
    "pack": "Annecy–Alpes–Léman",
    "target_version": "0.3",
    "status": "paired_rx_internal_candidate_76_new11_not_public",
    "published_base_version": "0.2",
    "published_base_memory_count": 65,
    "published_base_without_aviation_memory_count": 48,
    "published_base_is_immutable": True,
    "internal_candidate_memory_count": 76,
    "internal_candidate_without_aviation_memory_count": 59,
    "internal_candidate_new_memory_count": 11,
    "known_potential_ceiling_if_f1zth_50m_clears": 77,
    "paired_rx_expansion": "research/annecy-alpes-leman-v0.3/paired-rx-expansion.json",
    "pack_plan": "research/annecy-alpes-leman-v0.3/pack-plan.json",
    "internal_candidate_builder": "tools/build_annecy_v03_internal_candidate.py",
    "sprint_guard": "tests/test_sprint86_annecy_v03_paired_rx_expansion.py",
    "new_satellite_uplink_unique_rf_count": 2,
    "new_france_paired_rx_unique_rf_count": 7,
    "new_switzerland_paired_rx_unique_rf_count": 2,
    "f1zth_50m_frequency_mhz": 50.5375,
    "f1zth_50m_promoted": False,
    "f1zth_50m_gate": "device_firmware_rx_compatibility_not_project_verified",
    "unpublished_adrasec_frequency_inferred": False,
    "public_export_allowed": False,
    "public_registry_allowed": False,
    "public_routes_allowed": False,
    "public_release_ready": False,
    "published": False,
    "review_completed": False,
}
state["latest_sprint86_annecy_v0_3_paired_rx"] = {
    "sprint": 86,
    "state_version": "0.21.75",
    "checked_on": "2026-08-15",
    "base_full_memory_count": 65,
    "base_without_aviation_memory_count": 48,
    "candidate_full_memory_count": 76,
    "candidate_without_aviation_memory_count": 59,
    "new_unique_rf_memory_count": 11,
    "potential_ceiling_if_f1zth_50m_clears": 77,
    "f1zth_50m_promoted": False,
    "public_export_allowed": False,
}
for item in [
    "research/annecy-alpes-leman-v0.3/paired-rx-expansion.json",
    "research/annecy-alpes-leman-v0.3/pack-plan.json",
    "research/sprint-86-summary.md",
]:
    if item not in state.setdefault("sources_of_truth", []):
        state["sources_of_truth"].append(item)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Generic file guard.
site = ROOT / "tests/test_site_files.py"
insert_before(
    site,
    '    "tests/test_normandie_v04_public_release.py",\n',
    '    "research/annecy-alpes-leman-v0.3/paired-rx-expansion.json",\n'
    '    "tools/build_annecy_v03_internal_candidate.py",\n'
    '    "tests/test_sprint86_annecy_v03_paired_rx_expansion.py",\n'
    '    "research/sprint-86-summary.md",\n',
)

# README.
readme = ROOT / "README.md"
replace_once(
    readme,
    '**État courant : Sprint 85 / 0.21.74 — Normandie v0.5 reste à 142 mémoires RX ; le journal terrain R3/F5ZHA peut maintenant être évalué automatiquement sans aucune promotion ni publication automatique.**',
    '**État courant : Sprint 86 / 0.21.75 — Annecy–Alpes–Léman v0.3 dispose d’un premier candidat interne à 76 mémoires RX (59 sans aviation), soit +11 RF uniques, sans publication.**',
)
replace_once(readme, '## État actuel — Sprint 85 / 0.21.74', '## État actuel — Sprint 86 / 0.21.75')
replace_once(
    readme,
    'Recherche : Normandie v0.5 reste à **142 mémoires RX**, delta 0. Le mini-pack terrain de **6 sondes RX-only** et son journal disposent maintenant d’un évaluateur reproductible qui classe R3 et F5ZHA en `satisfied`, `insufficient` ou `indeterminate` sans jamais modifier le candidat automatiquement. Le plafond potentiel reste **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
    'Recherche : **Annecy–Alpes–Léman v0.3 = 76 mémoires RX / 59 sans aviation, +11 RF uniques**, premier candidat interne paired RX non public ; plafond conditionnel 77 si F1ZTH 50.5375 MHz franchit le gate de compatibilité UV-K5/firmware. Normandie v0.5 reste à **142 RX**, delta 0, en attente de terrain R3/F5ZHA et de nouvelles sources F1ZOV/F6ZES. Bretagne v0.3 reste à **151 RX**, delta 0 ; sa prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
)
replace_once(
    readme,
    '`research/sprint-84-summary.md` et `research/sprint-85-summary.md`.',
    '`research/sprint-84-summary.md`, `research/sprint-85-summary.md` et `research/sprint-86-summary.md`.',
)
insert_before(
    readme,
    '## Sprint 85 — évaluateur du journal terrain Normandie v0.5\n',
    '## Sprint 86 — Annecy–Alpes–Léman v0.3 paired RX\n\n'
    'Premier candidat interne exact : **65 → 76 mémoires RX**, ou **48 → 59 sans aviation**, soit **+11 RF uniques**. La v0.2 publique reste immuable.\n\n'
    '- satellites : 145.850 MHz partagée SO-50/AO-123 et 435.250 MHz AO-91 ;\n'
    '- France : nouvelles entrées RX F1ZOH, F6ZJD, F1ZCQ, F1ZCR et F1ZDC ;\n'
    '- Haute-Savoie : paire publique F1ZJV/F1ZYT 145.1875 / 145.7875 MHz, dédupliquée entre les deux sites ;\n'
    '- Suisse : entrées HB9G 145.125 et 431.500 MHz ;\n'
    '- F1ZTH 50.5375 MHz reste un +1 conditionnel hors candidat tant que la compatibilité récepteur/firmware UV-K5 n’est pas définie ;\n'
    '- aucune fréquence UHF ADRASEC non publiée n’est inférée ; aucune route publique v0.3.\n\n'
    'Preuve : `research/annecy-alpes-leman-v0.3/paired-rx-expansion.json`. Builder : `tools/build_annecy_v03_internal_candidate.py`. Garde-fou : `tests/test_sprint86_annecy_v03_paired_rx_expansion.py`.\n\n',
)

# PROJECT_STATUS.
status = ROOT / "PROJECT_STATUS.md"
replace_once(status, 'Sprint courant : **85**\nÉtat logique : **0.21.74**', 'Sprint courant : **86**\nÉtat logique : **0.21.75**')
replace_once(status, 'Résumé courant : `research/sprint-85-summary.md`.', 'Résumé courant : `research/sprint-86-summary.md`.')
insert_before(
    status,
    '## Sprint 85 — évaluateur terrain Normandie v0.5\n',
    '## Sprint 86 — Annecy–Alpes–Léman v0.3 paired RX\n\n'
    'Premier candidat v0.3 : **76 RX / 59 sans aviation**, à partir de la v0.2 publique immuable **65 / 48**. Delta : **+11 RF uniques**.\n\n'
    '- +2 montées satellites dédupliquées : 145.850 et 435.250 MHz ;\n'
    '- +7 RF paired RX France, dont la paire F1ZJV/F1ZYT partagée 145.1875 / 145.7875 MHz ;\n'
    '- +2 entrées HB9G : 145.125 et 431.500 MHz ;\n'
    '- F1ZTH 50.5375 MHz reste différé, plafond conditionnel 77 ;\n'
    '- aucun UHF ADRASEC non publié, aucune publication v0.3.\n\n'
    'Preuve : `research/annecy-alpes-leman-v0.3/paired-rx-expansion.json`. Builder : `tools/build_annecy_v03_internal_candidate.py`. Test : `tests/test_sprint86_annecy_v03_paired_rx_expansion.py`.\n\n',
)

# CHANGELOG.
changelog = ROOT / "CHANGELOG.md"
insert_before(
    changelog,
    '## 0.21.74 - 2026-08-15\n',
    '## 0.21.75 - 2026-08-15\n\n'
    '- **Sprint 86** : premier candidat interne Annecy–Alpes–Léman v0.3, **76 mémoires RX / 59 sans aviation**, soit **+11 RF uniques** depuis la v0.2 immuable 65/48.\n'
    '- Paired RX : ajout des montées satellites 145.850/435.250, de cinq entrées de relais France, de la paire VHF partagée F1ZJV/F1ZYT et des deux entrées HB9G.\n'
    '- Déduplication explicite des paires déjà entièrement représentées ; aucune duplication RF par site ou fonction.\n'
    '- F1ZTH 50.5375 MHz reste différé jusqu’à définition d’une base de compatibilité UV-K5/firmware ; plafond conditionnel **77**.\n'
    '- Aucune fréquence ADRASEC non publiée n’est inférée, aucune route/registre public v0.3 n’est créé.\n'
    '- Ajout de `paired-rx-expansion.json`, du builder v0.3 et du garde-fou Sprint 86.\n\n',
)

print("Sprint 86 finalization complete")
