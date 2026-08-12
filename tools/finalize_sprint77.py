#!/usr/bin/env python3
"""Finalize Sprint 77 project state and documentation, then remove this helper."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --- project-resume-state.json -------------------------------------------------
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["current_sprint"] = 77
state["state_version"] = "0.21.66"

active = state["active_work"]
active.update({
    "status": "internal_candidate_151_airac08_amateur_adrasec_revalidated_not_public",
    "adrasec_revalidation": "research/bretagne-v0.2/adrasec-public-revalidation.json",
    "adrasec_revalidation_checked_on": "2026-08-12",
    "adrasec_revalidation_candidate_memory_delta": 0,
    "adrasec_departments_reviewed": [22, 29, 35, 56],
    "adrasec_membership_confirmed_for_all_departments": True,
    "adrasec29_public_role_frequency_validated": True,
    "adrasec29_frequency_mhz": 144.8,
    "adrasec29_frequency_already_present_nationally": True,
    "f1zug_adrasec_transponder_frequency_published": False,
    "adrasec56_service_specific_frequency_promoted": False,
})

for source in (
    "research/bretagne-v0.2/adrasec-public-revalidation.json",
    "research/sprint-77-summary.md",
):
    if source not in state["sources_of_truth"]:
        state["sources_of_truth"].append(source)

state["field_tools"]["run_sprint77_test"] = "python tests/test_sprint77_bretagne_adrasec_public_revalidation.py"

if not state["recent_sprints"] or state["recent_sprints"][0].get("sprint") != 77:
    state["recent_sprints"].insert(0, {
        "sprint": 77,
        "state_version": "0.21.66",
        "summary": "Bretagne v0.2 public ADRASEC revalidation confirmed FNRASEC membership for departments 22/29/35/56; the only current public role-frequency cross-check at 144.800 MHz is already nationally deduplicated, so candidate remains 151 with zero RF delta.",
        "summary_file": "research/sprint-77-summary.md",
    })

state["resume_rules"].update({
    "organisation_membership_does_not_publish_frequency": True,
    "geography_does_not_prove_adrasec_role": True,
    "aprs_role_does_not_imply_other_service_frequency": True,
    "historical_role_does_not_equal_current_role": True,
    "private_ppdr_operational_data_excluded": True,
})

state["latest_sprint77_adrasec_revalidation"] = {
    "file": "research/sprint-77-summary.md",
    "evidence": "research/bretagne-v0.2/adrasec-public-revalidation.json",
    "test": "tests/test_sprint77_bretagne_adrasec_public_revalidation.py",
    "candidate_memory_count_before": 151,
    "candidate_memory_count_after": 151,
    "candidate_memory_delta": 0,
    "departments_reviewed": [22, 29, 35, 56],
    "all_memberships_confirmed": True,
    "department29_current_public_role_frequency_validated": True,
    "department29_frequency_mhz": 144.8,
    "department29_frequency_already_present_nationally": True,
    "department35_f1zug_transponder_frequency_published": False,
    "department56_service_specific_frequency_promoted": False,
    "private_ppdr_operational_data_excluded": True,
    "public_export_allowed": False,
    "public_registry_allowed": False,
}
write_json(state_path, state)


# --- README.md ----------------------------------------------------------------
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = readme.replace(
    "**État courant : Sprint 76 / 0.21.65 — Bretagne v0.2 reste à 151 mémoires RX après revalidation radioamateur, delta RF 0.**",
    "**État courant : Sprint 77 / 0.21.66 — Bretagne v0.2 reste à 151 mémoires RX après revalidation publique ADRASEC, delta RF 0.**",
    1,
)
readme = readme.replace("## État actuel — Sprint 76 / 0.21.65", "## État actuel — Sprint 77 / 0.21.66", 1)
readme = readme.replace(
    "Point de reprise : `PROJECT_STATUS.md`, `research/project-resume-state.json`, `research/sprint-75-summary.md` et `research/sprint-76-summary.md`.",
    "Point de reprise : `PROJECT_STATUS.md`, `research/project-resume-state.json`, `research/sprint-75-summary.md`, `research/sprint-76-summary.md` et `research/sprint-77-summary.md`.",
    1,
)
section77 = """## Sprint 77 — revalidation publique ADRASEC Bretagne v0.2

`research/bretagne-v0.2/adrasec-public-revalidation.json` revalide uniquement les données publiquement accessibles des ADRASEC 22, 29, 35 et 56. Le candidat reste à **151 mémoires RX**, avec un **delta RF de 0**.

- **ADRASEC 29** : F1ZBH-3 et F1ZGQ-3 sont publiquement recoupés comme rôles ADRASEC-29 sur l'APRS 144.800 MHz ; cette RF est déjà présente dans le bloc APRS national, donc aucune duplication.
- **ADRASEC 35** : F1ZUG reste publiquement identifié en APRS sur 144.800 MHz, tandis que la fréquence de sa fonction de transpondeur ADRASEC 35 n'est pas publiée. Elle n'est jamais déduite de l'APRS.
- **ADRASEC 56** : l'activité départementale publique est confirmée, ainsi que des métadonnées APRS publiques, mais aucune fréquence de service ADRASEC actuelle distincte n'est promue. Une association historique de F1ZKU ne devient pas un rôle courant par inférence.
- **ADRASEC 22** : appartenance FNRASEC confirmée, sans fréquence ADRASEC actuelle explicitement attribuée dans les sources publiques retenues.

Garde-fous : appartenance associative ≠ fréquence publiée ; géographie ≠ rôle ADRASEC ; rôle historique ≠ rôle courant ; APRS ≠ fréquence d'un autre service ; données opérationnelles privées PPDR exclues.

Test : `tests/test_sprint77_bretagne_adrasec_public_revalidation.py`.

"""
if "## Sprint 77 — revalidation publique ADRASEC Bretagne v0.2" not in readme:
    readme = readme.replace("## Sprint 76 — revalidation radioamateur Bretagne v0.2", section77 + "## Sprint 76 — revalidation radioamateur Bretagne v0.2", 1)
readme = readme.replace("`research/sprint-61-summary.md` à `research/sprint-76-summary.md`", "`research/sprint-61-summary.md` à `research/sprint-77-summary.md`", 1)
if "python tests\\test_sprint77_bretagne_adrasec_public_revalidation.py" not in readme:
    readme = readme.replace(
        "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_bretagne_public_release.py",
        "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_sprint77_bretagne_adrasec_public_revalidation.py\npython tests\\test_bretagne_public_release.py",
        1,
    )
    readme = readme.replace(
        "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_site_files.py",
        "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_sprint77_bretagne_adrasec_public_revalidation.py\npython tests\\test_site_files.py",
        1,
    )
readme_path.write_text(readme, encoding="utf-8")


# --- PROJECT_STATUS.md ---------------------------------------------------------
status_path = ROOT / "PROJECT_STATUS.md"
status = status_path.read_text(encoding="utf-8")
status = status.replace("Sprint courant : **76**", "Sprint courant : **77**", 1)
status = status.replace("État logique : **0.21.65**", "État logique : **0.21.66**", 1)
status = status.replace("Résumé courant : `research/sprint-76-summary.md`.", "Résumé courant : `research/sprint-77-summary.md`.", 1)
section_status77 = """## Sprint 77 — ADRASEC public, candidat toujours 151

La revalidation publique des ADRASEC 22, 29, 35 et 56 produit un **delta candidat 0**. Le candidat Bretagne v0.2 reste à **151 mémoires RX**.

- ADRASEC 29 : F1ZBH-3 et F1ZGQ-3 sont recoupés publiquement sur APRS 144.800 MHz, déjà présent nationalement ;
- ADRASEC 35 : F1ZUG APRS 144.800 MHz reste distinct de la fonction transpondeur ADRASEC 35 dont la fréquence n'est pas publiée ;
- ADRASEC 56 : activité publique confirmée, aucune fréquence de service ADRASEC actuelle distincte promue ;
- ADRASEC 22 : appartenance confirmée, aucune fréquence actuelle explicitement attribuée dans le périmètre public retenu ;
- aucune fréquence opérationnelle privée ni donnée PPDR n'est recherchée ou inférée.

Test : `tests/test_sprint77_bretagne_adrasec_public_revalidation.py`.

"""
if "## Sprint 77 — ADRASEC public, candidat toujours 151" not in status:
    status = status.replace("## Sprint 76 — Bretagne v0.2 reste à 151", section_status77 + "## Sprint 76 — Bretagne v0.2 reste à 151", 1)
status = status.replace(
    "- ADRASEC publiquement vérifiable pour 22 / 29 / 35 / 56 ;\n- F1ZUG / ADRASEC 35 sans inférer de fréquence depuis APRS ;",
    "- F1ZUG / ADRASEC 35 reste sans fréquence de transpondeur publiée ;\n- ADRASEC 29 est résolu à delta RF 0 sur APRS 144.800 MHz déjà national ;",
    1,
)
if "python tests\\test_sprint77_bretagne_adrasec_public_revalidation.py" not in status:
    status = status.replace(
        "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_sprint74_bretagne_v02_initialization.py",
        "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_sprint77_bretagne_adrasec_public_revalidation.py\npython tests\\test_sprint74_bretagne_v02_initialization.py",
        1,
    )
status_path.write_text(status, encoding="utf-8")


# --- Bretagne v0.2 README ------------------------------------------------------
bretagne_readme_path = ROOT / "research/bretagne-v0.2/README.md"
bretagne = bretagne_readme_path.read_text(encoding="utf-8")
bretagne = bretagne.replace("## État Sprint 76", "## État Sprint 77", 1)
bretagne = bretagne.replace(
    "Le candidat interne reste à **151 mémoires RX** : base v0.1=135 + **16 mémoires aviation AIRAC 08/26**. La revalidation des infrastructures radioamateur du Sprint 76 produit un **delta RF de 0**. Aucun export public v0.2 n'existe et le registre public reste sur Bretagne v0.1.",
    "Le candidat interne reste à **151 mémoires RX** : base v0.1=135 + **16 mémoires aviation AIRAC 08/26**. Les revalidations radioamateur du Sprint 76 et ADRASEC publique du Sprint 77 produisent chacune un **delta RF de 0**. Aucun export public v0.2 n'existe et le registre public reste sur Bretagne v0.1.",
    1,
)
adrasec_section = """### ADRASEC — revalidation publique Sprint 77

`adrasec-public-revalidation.json` traite uniquement les informations publiquement vérifiables des ADRASEC 22, 29, 35 et 56 :

- les quatre associations sont confirmées dans l'agrément FNRASEC courant ; cette appartenance ne publie aucune fréquence ;
- ADRASEC 29 est recoupée publiquement avec F1ZBH-3 / F1ZGQ-3 sur APRS 144.800 MHz, déjà présent nationalement : **delta 0** ;
- F1ZUG conserve APRS 144.800 MHz, mais la fréquence de sa fonction transpondeur ADRASEC 35 reste non publiée et n'est pas inférée ;
- ADRASEC 56 publie son activité et des rôles APRS, sans fréquence de service ADRASEC actuelle distincte promue ;
- ADRASEC 22 ne reçoit aucune fréquence par simple géographie ou appartenance.

Les données opérationnelles privées PPDR restent hors périmètre.

"""
if "### ADRASEC — revalidation publique Sprint 77" not in bretagne:
    bretagne = bretagne.replace("## Backlog restant", adrasec_section + "## Backlog restant", 1)
bretagne = bretagne.replace(
    "Restent ouverts : données ADRASEC publiquement vérifiables, cas F1ZUG / ADRASEC 35, attribution locale CROSS Étel Ch64, attribution locale CROSS Corsen Ch79, ainsi que les futures revalidations de F5ZPV, F5ZZH et F5ZZC-4.",
    "Restent ouverts : fréquence de la fonction transpondeur F1ZUG / ADRASEC 35 non publiée, attribution locale CROSS Étel Ch64, attribution locale CROSS Corsen Ch79, ainsi que les futures revalidations de F5ZPV, F5ZZH et F5ZZC-4. La revalidation publique générale ADRASEC 22/29/35/56 est close à delta RF 0.",
    1,
)
bretagne_readme_path.write_text(bretagne, encoding="utf-8")


# --- CHANGELOG.md --------------------------------------------------------------
changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
if "## 0.21.66 - 2026-08-12" not in changelog:
    entries = """## 0.21.66 - 2026-08-12

- **Sprint 77** : revalidation publique ADRASEC Bretagne (22/29/35/56), candidat Bretagne v0.2 maintenu à **151 mémoires RX**, delta RF **0**.
- ADRASEC 29 : F1ZBH-3 et F1ZGQ-3 recoupés publiquement sur APRS 144.800 MHz, déjà présent dans le bloc national ; aucune duplication.
- ADRASEC 35 : F1ZUG APRS 144.800 MHz reste distinct du transpondeur ADRASEC 35 dont la fréquence n'est pas publiée.
- ADRASEC 56 : activité publique confirmée sans fréquence de service ADRASEC actuelle distincte promue ; association historique de F1ZKU non transformée en rôle courant.
- ADRASEC 22 : appartenance FNRASEC confirmée, sans fréquence actuelle explicitement attribuée dans le périmètre public retenu.
- Données opérationnelles privées et PPDR explicitement exclues ; ajout du garde-fou Sprint 77 à la CI.

## 0.21.65 - 2026-08-12

- **Sprint 76** : revalidation des infrastructures radioamateur Bretagne v0.2, candidat maintenu à **151 mémoires RX**, delta RF **0**.
- F1ZBZ résolu sans nouvelle RF car les cinq valeurs utiles sont déjà représentées ; F5ZPV/F5ZZH restent arrêtés selon l'opérateur local ; F5ZZC-4 reste sans fréquence actuelle validée.
- Ajout de `amateur-infrastructure-revalidation.json` et du garde-fou Sprint 76.

## 0.21.64 - 2026-08-12

- **Sprint 75** : Bretagne v0.2 passe de 135 à **151 mémoires RX** avec **16 mémoires aviation** AIRAC 08/26 aux positions 130–145.
- Rennes, Brest, Dinard, Quimper et 121.500 MHz urgence sont intégrés au candidat interne RX-only ; positions 146–149 laissées libres.
- Aucun CSV public v0.2 ni changement de registre ; Bretagne v0.1 reste immuable à 135.

## 0.21.63 - 2026-08-12

- **Sprint 74** : initialisation de Bretagne v0.2 en recherche à partir de Bretagne v0.1 immuable = **135 mémoires RX**.
- Six dossiers de backlog créés : aviation, ADRASEC public, F1ZUG/ADRASEC35, CROSS Étel Ch64, CROSS Corsen Ch79 et infrastructures radioamateur ambiguës/arrêtées.
- Candidat initial 135, delta 0, aucune publication v0.2.

"""
    changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + entries, 1)
changelog_path.write_text(changelog, encoding="utf-8")


# Remove temporary trigger/helper/workflow from the final commit.
for relative in (
    "research/sprint-77-finalize-trigger.txt",
    "tools/finalize_sprint77.py",
    ".github/workflows/finalize-sprint77.yml",
):
    path = ROOT / relative
    if path.exists():
        path.unlink()

print("Sprint 77 finalization files updated; temporary helper removed from working tree.")
