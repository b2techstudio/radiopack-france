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
state["current_sprint"] = 82
state["state_version"] = "0.21.71"
active = state["active_work"]
active.update({
    "pack": "Bretagne",
    "target_version": "0.3",
    "status": "public_revalidation_zero_rf_delta_151_not_public",
    "public_export_allowed": False,
    "public_registry_allowed": False,
    "public_release_ready": False,
    "internal_candidate_memory_count": 151,
    "internal_candidate_new_memory_count": 0,
    "public_service_revalidation": "research/bretagne-v0.3/public-service-revalidation.json",
    "public_service_revalidation_checked_on": "2026-08-15",
    "public_service_revalidation_reviewed_count": 6,
    "public_service_revalidation_candidate_memory_delta": 0,
    "public_service_revalidation_promoted_item_count": 0,
    "f1zug_aprs_frequency_mhz": 144.8,
    "f1zug_aprs_frequency_already_present_nationally": True,
    "f1zug_adrasec35_transponder_frequency_published": False,
    "f5zzc4_current_service_frequency_validated": False,
    "f5zpv_local_operator_still_stopped": True,
    "f5zzh_local_operator_still_stopped": True,
    "etel_channel64_primary_source_conflict_open": True,
    "corsen_channel79_primary_current_transmitter_site_confirmed": False,
    "published": False,
    "scope_frozen": False,
    "prepublication_ready": False,
})
state["latest_sprint82_bretagne_v0_3_public_revalidation"] = {
    "sprint": 82,
    "state_version": "0.21.71",
    "checked_on": "2026-08-15",
    "reviewed_non_airac_item_count": 6,
    "candidate_memory_count_before": 151,
    "candidate_memory_count_after": 151,
    "candidate_memory_delta": 0,
    "promoted_item_count": 0,
    "public_v0_3_exists": False,
    "f1zug_aprs_frequency_mhz": 144.8,
    "f1zug_transponder_frequency_published": False,
    "f5zzc4_current_service_frequency_validated": False,
    "f5zpv_local_operator_still_stopped": True,
    "f5zzh_local_operator_still_stopped": True,
    "etel_channel64_primary_conflict_open": True,
    "corsen_channel79_primary_site_mapping_confirmed": False,
}
for item in [
    "research/bretagne-v0.3/public-service-revalidation.json",
    "research/sprint-82-summary.md",
]:
    if item not in state.setdefault("sources_of_truth", []):
        state["sources_of_truth"].append(item)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Require Sprint 82 files in the generic repository guard.
site = ROOT / "tests/test_site_files.py"
insert_before(
    site,
    '    "research/normandie-v0.4/README.md",\n',
    '    "research/bretagne-v0.3/public-service-revalidation.json",\n'
    '    "research/sprint-82-summary.md",\n'
    '    "tests/test_sprint82_bretagne_v03_public_revalidation.py",\n',
)

# README.
readme = ROOT / "README.md"
replace_once(
    readme,
    '**État courant : Sprint 81 / 0.21.70 — Bretagne v0.3 est initialisée en recherche à 151 mémoires RX depuis la v0.2 publique immuable ; delta initial 0.**',
    '**État courant : Sprint 82 / 0.21.71 — Bretagne v0.3 reste à 151 mémoires RX après revalidation publique ciblée de six dossiers ; delta RF 0, aucune publication.**',
)
replace_once(readme, '## État actuel — Sprint 81 / 0.21.70', '## État actuel — Sprint 82 / 0.21.71')
replace_once(
    readme,
    'Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.3 démarre à **151 mémoires RX**, delta 0, comme copie interne exacte de la v0.2 publique immuable ; la prochaine transition aviation est AIRAC 09/26 au 3 septembre 2026.',
    'Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.3 reste à **151 mémoires RX**, delta 0 : les six dossiers non-AIRAC ouverts ont été revalidés le 15 août 2026 sans promotion ; la prochaine transition aviation reste AIRAC 09/26 au 3 septembre 2026.',
)
replace_once(
    readme,
    '`research/sprint-80-summary.md` et `research/sprint-81-summary.md`.',
    '`research/sprint-80-summary.md`, `research/sprint-81-summary.md` et `research/sprint-82-summary.md`.',
)
insert_before(
    readme,
    '## Sprint 81 — initialisation Bretagne v0.3\n',
    '## Sprint 82 — revalidation publique ciblée Bretagne v0.3\n\n'
    'Les six dossiers non-AIRAC encore ouverts ont été recontrôlés le **15 août 2026**. Résultat : **151 → 151 mémoires RX, delta RF 0, zéro promotion**.\n\n'
    '- F1ZUG-4 reste publiquement documenté en APRS sur **144.800 MHz**, déjà présent nationalement ; la fréquence de son transpondeur ADRASEC35 n’est toujours pas publiée ;\n'
    '- F5ZZC-4 reste sans fréquence de service actuelle validée : l’ancienne attribution APRS/ADRASEC35 n’est pas transformée en preuve courante ;\n'
    '- F5ZPV est toujours déclaré temporairement arrêté par l’ARA35 malgré un annuaire général qui le marque actif ;\n'
    '- F5ZZH est toujours arrêté et en recherche de nouveau site ;\n'
    '- CROSS Étel : conflit primaire Ch64 toujours ouvert, Étel restant explicitement mappé sur Ch63 dans la page opérationnelle ;\n'
    '- CROSS Corsen : réseau VHF/MHF actuel confirmé sans mapping primaire Ch79 → site précis.\n\n'
    'Preuve : `research/bretagne-v0.3/public-service-revalidation.json`. Garde-fou : `tests/test_sprint82_bretagne_v03_public_revalidation.py`.\n\n',
)
replace_once(readme, '`research/sprint-61-summary.md` à `research/sprint-81-summary.md`', '`research/sprint-61-summary.md` à `research/sprint-82-summary.md`')

# PROJECT_STATUS.
status = ROOT / "PROJECT_STATUS.md"
replace_once(status, 'Dernière mise à jour : **12 août 2026**', 'Dernière mise à jour : **15 août 2026**')
replace_once(status, 'Sprint courant : **81**\nÉtat logique : **0.21.70**', 'Sprint courant : **82**\nÉtat logique : **0.21.71**')
replace_once(status, 'Résumé courant : `research/sprint-81-summary.md`.', 'Résumé courant : `research/sprint-82-summary.md`.')
insert_before(
    status,
    '## Sprint 81 — Bretagne v0.3 initialisée à 151\n',
    '## Sprint 82 — Bretagne v0.3 revalidée, delta 0\n\n'
    'Revalidation publique des six dossiers non-AIRAC encore ouverts : **candidat 151, delta RF 0, zéro promotion**.\n\n'
    '- F1ZUG : APRS 144.800 MHz confirmé et déjà présent ; fréquence du transpondeur ADRASEC35 toujours non publiée ;\n'
    '- F5ZZC-4 : aucune fréquence de service actuelle publiquement validée ; absence de trace récente ≠ preuve d’arrêt ;\n'
    '- F5ZPV : opérateur local toujours « temporairement arrêté », malgré le statut actif de l’annuaire général ;\n'
    '- F5ZZH : toujours arrêté, recherche de site en cours ;\n'
    '- Étel Ch64 : conflit primaire non résolu, aucune attribution locale ;\n'
    '- Corsen Ch79 : réseau actuel confirmé, aucun mapping primaire canal → station.\n\n'
    'Preuve : `research/bretagne-v0.3/public-service-revalidation.json`. Test : `tests/test_sprint82_bretagne_v03_public_revalidation.py`.\n\n',
)

# Bretagne v0.3 README.
v03 = ROOT / "research/bretagne-v0.3/README.md"
replace_once(
    v03,
    'État : **Sprint 81 / 0.21.70 — initialisée depuis la Bretagne v0.2 publique immuable à 151 mémoires RX**.',
    'État : **Sprint 82 / 0.21.71 — six dossiers non-AIRAC revalidés, candidat toujours 151 mémoires RX, delta RF 0**.',
)
insert_before(
    v03,
    '## Base\n',
    '## Sprint 82 — revalidation publique ciblée\n\n'
    '`public-service-revalidation.json` recontrôle F1ZUG, F5ZZC-4, F5ZPV, F5ZZH et les mappings CROSS Étel Ch64 / Corsen Ch79. Aucun dossier ne produit de nouvelle RF : **delta 0**.\n\n'
    '- F1ZUG APRS 144.800 MHz reste déjà couvert nationalement ; le transpondeur ADRASEC35 reste sans fréquence publique ;\n'
    '- F5ZZC-4 reste non résolu faute de source actuelle de fréquence ;\n'
    '- F5ZPV et F5ZZH restent arrêtés selon l’opérateur local ;\n'
    '- Ch64 et Ch79 restent des paires génériques sans attribution locale non prouvée.\n\n',
)

# CHANGELOG.
changelog = ROOT / "CHANGELOG.md"
insert_before(
    changelog,
    '## 0.21.70 - 2026-08-12\n',
    '## 0.21.71 - 2026-08-15\n\n'
    '- **Sprint 82** : revalidation publique ciblée des six dossiers non-AIRAC ouverts de Bretagne v0.3 ; candidat maintenu à **151 mémoires RX**, delta RF **0**, aucune promotion.\n'
    '- F1ZUG APRS 144.800 MHz confirmé comme déjà couvert ; fréquence du transpondeur ADRASEC35 toujours non publiée. F5ZZC-4 reste sans fréquence actuelle validée.\n'
    '- F5ZPV et F5ZZH restent arrêtés selon l’ARA35 ; le statut local prime sur l’annuaire général.\n'
    '- CROSS Étel Ch64 et Corsen Ch79 restent sans attribution locale primaire exploitable ; les paires génériques déjà présentes ne sont pas dupliquées.\n'
    '- Ajout de `public-service-revalidation.json`, du garde-fou Sprint 82 et adaptation forward-compatible du test Sprint 81.\n\n',
)

print("Sprint 82 finalization complete")
