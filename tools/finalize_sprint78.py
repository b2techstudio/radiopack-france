import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


# Machine-readable resume state.
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
if state["current_sprint"] != 77 or state["state_version"] != "0.21.66":
    raise RuntimeError("Unexpected resume state before Sprint 78 finalization")
state["current_sprint"] = 78
state["state_version"] = "0.21.67"
aw = state["active_work"]
if aw["internal_candidate_memory_count"] != 151:
    raise RuntimeError("Bretagne v0.2 candidate must remain 151")
aw["status"] = "internal_candidate_151_airac08_amateur_adrasec_cross_revalidated_not_public"
aw["cross_revalidation"] = "research/bretagne-v0.2/cross-local-mapping-revalidation.json"
aw["cross_revalidation_checked_on"] = "2026-08-12"
aw["cross_revalidation_candidate_memory_delta"] = 0
aw["cross_local_site_metadata_promoted_count"] = 0
aw["etel_channel63_current_local_mapping_confirmed"] = True
aw["etel_channel64_current_brittany_site_confirmed"] = False
aw["etel_channel64_primary_source_conflict_open"] = True
aw["corsen_current_cross_network_confirmed"] = True
aw["corsen_channel79_primary_current_transmitter_site_confirmed"] = False
aw["corsen_secondary_site_chain_promoted"] = False
aw["guide_marine_2026_identified_but_not_extracted"] = True

for item in (
    "research/bretagne-v0.2/cross-local-mapping-revalidation.json",
    "research/sprint-78-summary.md",
):
    if item not in state["sources_of_truth"]:
        state["sources_of_truth"].append(item)
state["field_tools"]["run_sprint78_test"] = "python tests/test_sprint78_bretagne_cross_mapping_revalidation.py"

if not any(item.get("sprint") == 78 for item in state["recent_sprints"]):
    state["recent_sprints"].insert(0, {
        "sprint": 78,
        "state_version": "0.21.67",
        "summary": "Bretagne v0.2 CROSS Etel Ch64 and Corsen Ch79 local mapping revalidation produced zero RF delta and no promoted site metadata; candidate stays 151.",
        "summary_file": "research/sprint-78-summary.md",
    })

state["resume_rules"].update({
    "regional_channel_statement_does_not_name_transmitter_site": True,
    "current_cross_network_does_not_map_channel_to_station": True,
    "secondary_site_clue_is_not_primary_validation": True,
    "unread_primary_pdf_is_not_negative_evidence": True,
    "cross_site_assignment_must_not_be_guessed": True,
    "generic_rf_pair_must_not_be_duplicated_for_site_metadata": True,
})
state["latest_sprint78_cross_revalidation"] = {
    "file": "research/sprint-78-summary.md",
    "evidence": "research/bretagne-v0.2/cross-local-mapping-revalidation.json",
    "test": "tests/test_sprint78_bretagne_cross_mapping_revalidation.py",
    "candidate_memory_count_before": 151,
    "candidate_memory_count_after": 151,
    "candidate_memory_delta": 0,
    "local_site_metadata_promoted_count": 0,
    "channel64_pair_mhz": [156.225, 160.825],
    "channel79_pair_mhz": [156.975, 161.575],
    "etel_channel63_current_local_mapping_confirmed": True,
    "etel_channel64_current_brittany_site_confirmed": False,
    "etel_channel64_primary_source_conflict_open": True,
    "corsen_current_cross_network_confirmed": True,
    "corsen_channel79_primary_current_transmitter_site_confirmed": False,
    "guide_marine_2026_identified_but_not_extracted": True,
    "public_export_allowed": False,
    "public_registry_allowed": False,
}
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Global README.
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = replace_once(
    readme,
    "**État courant : Sprint 77 / 0.21.66 — Bretagne v0.2 reste à 151 mémoires RX après revalidation publique ADRASEC, delta RF 0.**",
    "**État courant : Sprint 78 / 0.21.67 — Bretagne v0.2 reste à 151 mémoires RX après revalidation CROSS Ch64/Ch79, delta RF 0 et aucun site local promu.**",
    "README current state",
)
readme = replace_once(readme, "## État actuel — Sprint 77 / 0.21.66", "## État actuel — Sprint 78 / 0.21.67", "README heading")
readme = replace_once(
    readme,
    "`research/sprint-75-summary.md`, `research/sprint-76-summary.md` et `research/sprint-77-summary.md`.",
    "`research/sprint-75-summary.md`, `research/sprint-76-summary.md`, `research/sprint-77-summary.md` et `research/sprint-78-summary.md`.",
    "README resume files",
)
section78 = """## Sprint 78 — revalidation CROSS Bretagne v0.2

`research/bretagne-v0.2/cross-local-mapping-revalidation.json` revalide les mappings locaux **CROSS Étel Ch64** et **CROSS Corsen Ch79** sans ajouter de mémoire ni promouvoir d'attribution locale.

- **Étel Ch64** : le ministère conserve une affirmation régionale 63/64 dans le Morbihan, tandis que la documentation opérationnelle actuelle du CROSS Étel mappe explicitement Étel sur Ch63. Le conflit primaire reste ouvert ; aucun site Ch64 n'est deviné.
- **Corsen Ch79** : le réseau VHF/MHF actuel est confirmé mais aucune source primaire actuelle exploitée ne mappe Ch79 vers Cap Fréhel, Bodic, Batz, Stiff ou Pointe du Raz. Les pistes secondaires restent des indices uniquement.
- Le **Guide Marine 2026** est identifié comme référence primaire pertinente mais son PDF n'est pas extractible dans le workflow courant ; aucune conclusion n'est tirée de cette indisponibilité.
- Les paires Ch64 `156.225 / 160.825 MHz` et Ch79 `156.975 / 161.575 MHz` sont déjà présentes génériquement : **delta RF 0**, candidat toujours **151**.

Garde-fou : `tests/test_sprint78_bretagne_cross_mapping_revalidation.py`.

"""
readme = replace_once(readme, "## Sprint 77 — revalidation publique ADRASEC Bretagne v0.2\n", section78 + "## Sprint 77 — revalidation publique ADRASEC Bretagne v0.2\n", "README Sprint 78 insertion")
readme = replace_once(readme, "`research/sprint-61-summary.md` à `research/sprint-76-summary.md`", "`research/sprint-61-summary.md` à `research/sprint-78-summary.md`", "README history range")
readme = replace_once(readme, "python tests\\test_sprint77_bretagne_adrasec_public_revalidation.py\n", "python tests\\test_sprint77_bretagne_adrasec_public_revalidation.py\npython tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\n", "README tests")
readme = replace_once(readme, "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_site_files.py", "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tests\\test_site_files.py", "README sync")
readme_path.write_text(readme, encoding="utf-8")

# PROJECT_STATUS.
status_path = ROOT / "PROJECT_STATUS.md"
status = status_path.read_text(encoding="utf-8")
status = replace_once(status, "Sprint courant : **77**", "Sprint courant : **78**", "status sprint")
status = replace_once(status, "État logique : **0.21.66**", "État logique : **0.21.67**", "status version")
status = replace_once(status, "Résumé courant : `research/sprint-77-summary.md`.", "Résumé courant : `research/sprint-78-summary.md`.", "status summary")
status78 = """## Sprint 78 — CROSS Ch64 / Ch79, candidat toujours 151

La revalidation primaire des mappings locaux CROSS produit un **delta candidat 0** et aucune attribution de site.

- Étel Ch64 : l'affirmation ministérielle régionale 63/64 dans le Morbihan ne nomme pas de site ; la documentation opérationnelle actuelle mappe Étel sur Ch63. Le conflit primaire reste ouvert et Ch64 n'est ni déclaré arrêté ni attribué à un site précis.
- Corsen Ch79 : le réseau côtier actuel est confirmé, mais aucun mapping primaire actuel Ch79 → émetteur précis n'est exploitable. Fréhel/Bodic/Batz/Stiff/Raz restent des pistes secondaires ou historiques, pas des attributions promues.
- Le Guide Marine 2026 est identifié mais son PDF n'est pas extrait dans le workflow courant ; son indisponibilité ne vaut pas preuve négative.
- Les deux paires RF sont déjà présentes génériquement : aucune duplication mémoire.

Test : `tests/test_sprint78_bretagne_cross_mapping_revalidation.py`.

"""
status = replace_once(status, "## Sprint 77 — ADRASEC public, candidat toujours 151\n", status78 + "## Sprint 77 — ADRASEC public, candidat toujours 151\n", "status Sprint 78 insertion")
status = replace_once(status, "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_sprint74_bretagne_v02_initialization.py", "python tests\\test_sprint76_bretagne_amateur_revalidation.py\npython tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tests\\test_sprint74_bretagne_v02_initialization.py", "status commands")
status_path.write_text(status, encoding="utf-8")

# Bretagne v0.2 research README.
bzh_path = ROOT / "research/bretagne-v0.2/README.md"
bzh = bzh_path.read_text(encoding="utf-8")
bzh = replace_once(bzh, "## État Sprint 77", "## État Sprint 78", "Bretagne heading")
bzh = replace_once(
    bzh,
    "Les revalidations radioamateur du Sprint 76 et ADRASEC publique du Sprint 77 produisent chacune un **delta RF de 0**.",
    "Les revalidations radioamateur du Sprint 76, ADRASEC publique du Sprint 77 et CROSS Ch64/Ch79 du Sprint 78 produisent chacune un **delta RF de 0**.",
    "Bretagne current state",
)
cross_section = """### CROSS Étel Ch64 / Corsen Ch79 — Sprint 78

`cross-local-mapping-revalidation.json` confirme que les paires RF Ch64 et Ch79 restent génériques et déjà dédupliquées.

- Étel : le site est explicitement associé à Ch63 dans la documentation opérationnelle actuelle ; l'affirmation régionale Ch64 dans le Morbihan ne suffit pas à nommer un émetteur Ch64.
- Corsen : le réseau radio côtier actuel est confirmé mais Ch79 n'est toujours pas mappé par une source primaire actuelle vers Fréhel, Bodic, Batz, Stiff ou Pointe du Raz.
- Les indices secondaires ne sont pas promus et les PDF primaires identifiés mais non extraits ne produisent aucune conclusion négative.

Résultat : **151 mémoires RX, delta 0, 0 attribution locale promue**.

"""
bzh = replace_once(bzh, "## Backlog restant\n", cross_section + "## Backlog restant\n", "Bretagne CROSS insertion")
bzh_path.write_text(bzh, encoding="utf-8")

# Changelog.
changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
entry = """## 0.21.67 - 2026-08-12

- **Sprint 78** : revalidation des mappings locaux CROSS Étel Ch64 et Corsen Ch79 ; Bretagne v0.2 reste à **151 mémoires RX**, delta RF **0**.
- Étel : affirmation ministérielle régionale 63/64 conservée, mais la documentation opérationnelle actuelle associe explicitement Étel à Ch63 ; aucun site Ch64 n'est promu et le conflit primaire reste ouvert.
- Corsen : réseau VHF/MHF actuel confirmé sans mapping primaire actuel Ch79 → site ; Fréhel/Bodic/Batz/Stiff/Raz restent des pistes non promotables.
- Guide Marine 2026 identifié comme référence primaire mais non extractible dans le workflow ; aucune preuve négative ni attribution n'en est déduite.
- Ajout de `cross-local-mapping-revalidation.json` et du garde-fou Sprint 78 ; aucune mutation publique Bretagne v0.2.

"""
changelog = replace_once(changelog, "# Changelog\n\n", "# Changelog\n\n" + entry, "changelog insertion")
changelog_path.write_text(changelog, encoding="utf-8")

# Restore exact reference archive expression in main CI if the prior full-file edit changed it.
ci_path = ROOT / ".github/workflows/ci.yml"
ci = ci_path.read_text(encoding="utf-8")
ci = ci.replace("path: RadioPack-France-${GITHUB_SHA}.zip", "path: RadioPack-France-${{ github.sha }}.zip")
ci_path.write_text(ci, encoding="utf-8")

# Remove one-shot finalization machinery from the final tree.
for relative in (
    "tools/finalize_sprint78.py",
    ".github/workflows/finalize-sprint78.yml",
    "research/.sprint78-finalize-trigger",
):
    path = ROOT / relative
    if path.exists():
        path.unlink()

print("Sprint 78 state/documentation finalization completed")
