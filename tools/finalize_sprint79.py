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
if state["current_sprint"] != 78 or state["state_version"] != "0.21.67":
    raise RuntimeError("Unexpected resume state before Sprint 79 finalization")
state["current_sprint"] = 79
state["state_version"] = "0.21.68"
aw = state["active_work"]
if aw["internal_candidate_memory_count"] != 151:
    raise RuntimeError("Bretagne v0.2 candidate must remain 151")
aw["status"] = "scope_frozen_151_review_10_of_10_zero_blockers_prepublication_ready_not_public"
aw["scope_frozen"] = True
aw["prepublication_ready"] = True
aw["public_release_ready"] = False
aw["public_export_allowed"] = False
aw["public_registry_allowed"] = False
aw["release_blocker_count"] = 0
aw["review_completed"] = 10
aw["review_total"] = 10
aw["maturity_review"] = "research/bretagne-v0.2/maturity-review.json"
aw["release_scope"] = "research/bretagne-v0.2/release-scope.json"
aw["review_checklist"] = "research/bretagne-v0.2/review-checklist.json"
aw["publication_gates"] = "research/bretagne-v0.2/publication-gates.json"
aw["prepublication_audit_tool"] = "tools/run_bretagne_v02_prepublication_audit.py"
aw["release_scope_frozen_on"] = "2026-08-12"
aw["aviation_freshness_rechecked_on"] = "2026-08-12"
aw["aviation_current_on_maturity_review_date"] = True
aw["deferred_non_blocking_ids"] = [
    "F1ZUG_ADRASEC35_ROLE_REVALIDATION",
    "CROSS_ETEL_CH64_LOCAL_MAPPING",
    "CROSS_CORSEN_CH79_LOCAL_MAPPING",
    "AMATEUR_INFRASTRUCTURE_REVALIDATION",
]

for item in (
    "research/bretagne-v0.2/maturity-review.json",
    "research/bretagne-v0.2/release-scope.json",
    "research/bretagne-v0.2/review-checklist.json",
    "research/bretagne-v0.2/publication-gates.json",
    "research/sprint-79-summary.md",
):
    if item not in state["sources_of_truth"]:
        state["sources_of_truth"].append(item)
state["field_tools"]["run_bretagne_v02_prepublication_audit"] = "python tools/run_bretagne_v02_prepublication_audit.py --require-prepublication-ready"
state["field_tools"]["run_sprint79_test"] = "python tests/test_sprint79_bretagne_v02_maturity.py"

if not any(item.get("sprint") == 79 for item in state["recent_sprints"]):
    state["recent_sprints"].insert(0, {
        "sprint": 79,
        "state_version": "0.21.68",
        "summary": "Bretagne v0.2 scope frozen at 151 RX memories; review 10/10, zero blockers, prepublication ready, still not public.",
        "summary_file": "research/sprint-79-summary.md",
    })

state["resume_rules"].update({
    "unresolved_optional_item_may_be_deferred_without_blocking_frozen_scope": True,
    "scope_freeze_requires_explicit_deferred_item_list": True,
    "prepublication_ready_does_not_equal_public_release_allowed": True,
    "explicit_publication_must_be_separate_step": True,
    "aviation_freshness_must_be_rechecked_if_publication_occurs_after_current_airac_window": True,
})
state["latest_sprint79_maturity"] = {
    "file": "research/sprint-79-summary.md",
    "maturity_review": "research/bretagne-v0.2/maturity-review.json",
    "release_scope": "research/bretagne-v0.2/release-scope.json",
    "review_checklist": "research/bretagne-v0.2/review-checklist.json",
    "publication_gates": "research/bretagne-v0.2/publication-gates.json",
    "audit_tool": "tools/run_bretagne_v02_prepublication_audit.py",
    "test": "tests/test_sprint79_bretagne_v02_maturity.py",
    "candidate_memory_count": 151,
    "candidate_memory_delta": 0,
    "review": "10/10",
    "release_blocker_count": 0,
    "scope_frozen": True,
    "prepublication_ready": True,
    "public_release_allowed": False,
    "aviation_cycle": "AIRAC 08/26",
    "aviation_current_on_review_date": True,
    "aviation_valid_through": "2026-09-02",
    "public_export_allowed": False,
    "public_registry_allowed": False,
}
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Global README.
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = replace_once(
    readme,
    "**État courant : Sprint 78 / 0.21.67 — Bretagne v0.2 reste à 151 mémoires RX après revalidation CROSS Ch64/Ch79, delta RF 0 et aucun site local promu.**",
    "**État courant : Sprint 79 / 0.21.68 — Bretagne v0.2 est figée à 151 mémoires RX, revue 10/10, 0 bloqueur, prépublication prête mais non publique.**",
    "README current state",
)
readme = replace_once(readme, "## État actuel — Sprint 78 / 0.21.67", "## État actuel — Sprint 79 / 0.21.68", "README heading")
readme = replace_once(
    readme,
    "`research/sprint-75-summary.md`, `research/sprint-76-summary.md`, `research/sprint-77-summary.md` et `research/sprint-78-summary.md`.",
    "`research/sprint-75-summary.md`, `research/sprint-76-summary.md`, `research/sprint-77-summary.md`, `research/sprint-78-summary.md` et `research/sprint-79-summary.md`.",
    "README resume files",
)
section79 = """## Sprint 79 — maturité et prépublication Bretagne v0.2

Le périmètre v0.2 est désormais **figé à 151 mémoires RX**. La revue `research/bretagne-v0.2/maturity-review.json` et la checklist de publication concluent à **10/10 contrôles passés, 0 bloqueur et prépublication prête**.

- les 16 mémoires aviation AIRAC 08/26 restent incluses ; le cycle est courant au 12 août 2026 et valable jusqu'au 2 septembre 2026 inclus ;
- l'absence d'extraction XML directe reste une limite méthodologique documentée, pas une comparaison fictive ;
- F1ZUG/ADRASEC35, les mappings locaux CROSS et F5ZPV/F5ZZH/F5ZZC-4 sont explicitement reportés hors du périmètre figé ;
- ces reports n'ajoutent aucune RF et ne bloquent pas la v0.2 ;
- `tools/run_bretagne_v02_prepublication_audit.py` reconstruit le candidat et vérifie RX-only, déduplication, aviation et absence de mutation publique.

**Important :** `prepublication_ready=true` ne signifie pas publication. Aucun CSV public v0.2 ni bascule du registre n'est effectué au Sprint 79.

Garde-fou : `tests/test_sprint79_bretagne_v02_maturity.py`.

"""
readme = replace_once(readme, "## Sprint 78 — revalidation CROSS Bretagne v0.2\n", section79 + "## Sprint 78 — revalidation CROSS Bretagne v0.2\n", "README Sprint 79 insertion")
readme = replace_once(readme, "`research/sprint-61-summary.md` à `research/sprint-78-summary.md`", "`research/sprint-61-summary.md` à `research/sprint-79-summary.md`", "README history range")
readme = replace_once(
    readme,
    "python tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tests\\test_bretagne_public_release.py",
    "python tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tests\\test_sprint79_bretagne_v02_maturity.py\npython tests\\test_bretagne_public_release.py",
    "README tests",
)
readme = replace_once(
    readme,
    "python tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tests\\test_site_files.py",
    "python tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tools\\run_bretagne_v02_prepublication_audit.py --require-prepublication-ready\npython tests\\test_sprint79_bretagne_v02_maturity.py\npython tests\\test_site_files.py",
    "README sync",
)
readme_path.write_text(readme, encoding="utf-8")

# PROJECT_STATUS.
status_path = ROOT / "PROJECT_STATUS.md"
status = status_path.read_text(encoding="utf-8")
status = replace_once(status, "Sprint courant : **78**", "Sprint courant : **79**", "status sprint")
status = replace_once(status, "État logique : **0.21.67**", "État logique : **0.21.68**", "status version")
status = replace_once(status, "Résumé courant : `research/sprint-78-summary.md`.", "Résumé courant : `research/sprint-79-summary.md`.", "status summary")
status79 = """## Sprint 79 — scope v0.2 figé, prépublication prête

Bretagne v0.2 est figée à **151 mémoires RX**. La revue de maturité est à **10/10**, avec **0 bloqueur** pour le périmètre explicitement retenu.

- AIRAC 08/26 reste courant au 12 août 2026 et les 16 mémoires aviation sont maintenues dans le scope ;
- F1ZUG/ADRASEC35, les mappings locaux Ch64/Ch79 et les infrastructures amateur arrêtées/non résolues sont reportés explicitement hors scope ;
- aucun de ces reports ne crée une RF manquante dans les 151 mémoires figées ;
- l'audit de prépublication reconstruit le candidat et interdit toute mutation publique prématurée.

État : `prepublication_ready=true`, **publication toujours false**. Un sprint séparé reste obligatoire pour créer/figer le CSV public, son empreinte et la bascule du registre.

Test : `tests/test_sprint79_bretagne_v02_maturity.py`. Audit : `tools/run_bretagne_v02_prepublication_audit.py --require-prepublication-ready`.

"""
status = replace_once(status, "## Sprint 78 — CROSS Ch64 / Ch79, candidat toujours 151\n", status79 + "## Sprint 78 — CROSS Ch64 / Ch79, candidat toujours 151\n", "status Sprint 79 insertion")
old_backlog = """## Backlog Bretagne v0.2 restant

- F1ZUG / ADRASEC 35 reste sans fréquence de transpondeur publiée ;
- ADRASEC 29 est résolu à delta RF 0 sur APRS 144.800 MHz déjà national ;
- F5ZPV, F5ZZH et F5ZZC-4 à revalider ultérieurement ;
- mapping local CROSS Étel Ch64 ;
- mapping local CROSS Corsen Ch79.

Ch64 et Ch79 existent déjà génériquement dans la base v0.1 : une attribution locale ne doit pas créer de doublon RF.
"""
new_backlog = """## Dossiers reportés après le scope Bretagne v0.2

Ces dossiers restent ouverts en recherche mais **ne bloquent plus le scope v0.2 figé** : F1ZUG / ADRASEC 35 sans fréquence de transpondeur publiée, F5ZPV/F5ZZH/F5ZZC-4 arrêtés ou non résolus, et mappings locaux CROSS Étel Ch64 / Corsen Ch79. ADRASEC 29 et F1ZBZ sont déjà résolus à delta RF 0.

Ch64 et Ch79 existent déjà génériquement dans la base v0.1 : une attribution locale future restera une métadonnée et ne devra pas créer de doublon RF.
"""
status = replace_once(status, old_backlog, new_backlog, "status deferred backlog")
status = replace_once(
    status,
    "python tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tests\\test_sprint74_bretagne_v02_initialization.py",
    "python tests\\test_sprint78_bretagne_cross_mapping_revalidation.py\npython tools\\run_bretagne_v02_prepublication_audit.py --require-prepublication-ready\npython tests\\test_sprint79_bretagne_v02_maturity.py\npython tests\\test_sprint74_bretagne_v02_initialization.py",
    "status commands",
)
status = replace_once(
    status,
    "- une promotion dans un candidat interne n'est jamais une publication ;",
    "- une promotion dans un candidat interne n'est jamais une publication ;\n- `prepublication_ready=true` n'autorise jamais à lui seul une publication ;",
    "status publication rule",
)
status_path.write_text(status, encoding="utf-8")

# Bretagne v0.2 research README.
bzh_path = ROOT / "research/bretagne-v0.2/README.md"
bzh = bzh_path.read_text(encoding="utf-8")
bzh = replace_once(bzh, "## État Sprint 78", "## État Sprint 79", "Bretagne heading")
bzh = replace_once(
    bzh,
    "Le candidat interne reste à **151 mémoires RX** : base v0.1=135 + **16 mémoires aviation AIRAC 08/26**. Les revalidations radioamateur du Sprint 76, ADRASEC publique du Sprint 77 et CROSS Ch64/Ch79 du Sprint 78 produisent chacune un **delta RF de 0**. Aucun export public v0.2 n'existe et le registre public reste sur Bretagne v0.1.",
    "Le candidat interne est désormais **figé à 151 mémoires RX** : base v0.1=135 + **16 mémoires aviation AIRAC 08/26**. Les revalidations radioamateur du Sprint 76, ADRASEC publique du Sprint 77 et CROSS Ch64/Ch79 du Sprint 78 produisent chacune un **delta RF de 0**. Le Sprint 79 clôt la revue de maturité à **10/10, 0 bloqueur, prépublication prête**. Aucun export public v0.2 n'existe et le registre public reste sur Bretagne v0.1.",
    "Bretagne current state",
)
prepub = """### Prépublication — Sprint 79

`maturity-review.json`, `release-scope.json`, `review-checklist.json` et `publication-gates.json` figent le périmètre à **151 mémoires RX**.

- revue : **10/10** ;
- bloqueurs : **0** ;
- audit reproductible : `tools/run_bretagne_v02_prepublication_audit.py --require-prepublication-ready` ;
- publication : **non effectuée**.

Le cycle AIRAC 08/26 est toujours courant au 12 août 2026. Les dossiers F1ZUG, mappings locaux CROSS et infrastructures amateur arrêtées/non résolues sont désormais explicitement reportés hors du scope figé et ne justifient aucun remplissage ou ajout RF.

"""
bzh = replace_once(bzh, "## Backlog restant\n", prepub + "## Dossiers reportés après le scope v0.2\n", "Bretagne prepublication insertion")
bzh = replace_once(
    bzh,
    "Restent ouverts : fréquence de la fonction transpondeur F1ZUG / ADRASEC 35 non publiée, attribution locale CROSS Étel Ch64, attribution locale CROSS Corsen Ch79, ainsi que les futures revalidations de F5ZPV, F5ZZH et F5ZZC-4. La revalidation publique générale ADRASEC 22/29/35/56 est close à delta RF 0.",
    "Restent ouverts pour une version ou une revue future : fréquence de la fonction transpondeur F1ZUG / ADRASEC 35 non publiée, attribution locale CROSS Étel Ch64, attribution locale CROSS Corsen Ch79, ainsi que les futures revalidations de F5ZPV, F5ZZH et F5ZZC-4. Ils sont explicitement hors du périmètre v0.2 figé. La revalidation publique générale ADRASEC 22/29/35/56 est close à delta RF 0.",
    "Bretagne deferred text",
)
bzh_path.write_text(bzh, encoding="utf-8")

# Changelog.
changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
entry = """## 0.21.68 - 2026-08-12

- **Sprint 79** : revue de maturité Bretagne v0.2 et gel du périmètre à **151 mémoires RX**.
- Checklist de prépublication portée à **10/10**, **0 bloqueur**, `prepublication_ready=true` ; aucune publication effectuée.
- AIRAC 08/26 recontrôlé comme cycle courant au 12 août 2026, valable jusqu'au 2 septembre 2026 inclus ; aucune comparaison XML champ par champ non effectuée n'est revendiquée.
- F1ZUG/ADRASEC35, mappings locaux CROSS Ch64/Ch79 et F5ZPV/F5ZZH/F5ZZC-4 sont explicitement reportés hors du scope figé et classés non bloquants.
- Ajout de `maturity-review.json`, `release-scope.json`, `review-checklist.json`, `publication-gates.json`, de l'audit v0.2 reproductible et du garde-fou Sprint 79.
- Le CSV public et le registre restent sur Bretagne v0.1 ; la publication v0.2 nécessite un sprint séparé explicite.

"""
changelog = replace_once(changelog, "# Changelog\n\n", "# Changelog\n\n" + entry, "changelog insertion")
changelog_path.write_text(changelog, encoding="utf-8")

# Remove one-shot script and trigger. The workflow itself is removed by the connector after this commit.
for relative in ("tools/finalize_sprint79.py", "research/.sprint79-finalize-trigger"):
    path = ROOT / relative
    if path.exists():
        path.unlink()

print("Sprint 79 state/documentation finalization completed")
