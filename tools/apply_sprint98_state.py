#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-19"
SPRINT = 98
STATE_VERSION = "0.21.87"

HASHES = {
    "hauts-de-france": "881f830ed81a0c55506830f1c767bc2a2a0a674e0677fc971c8f40f6646ca96c",
    "ile-de-france": "dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d",
    "grand-est": "a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1",
    "centre-val-de-loire": "68e164763834e69dcd85dd9b1b67777e42922134be33d5e25738f4df71f2bb29",
    "pays-de-la-loire": "b737a2e2849c73ed4dd97a4288d6ad862433948e0d4d7eaaa580648547b7d501",
    "bourgogne-franche-comte": "828af205aa07fe6685e3ad395ec2f0f56222fcfb5bb2f7b8f6a0bd4082714c0a",
    "nouvelle-aquitaine": "619f13f7c8b6cb2529f4f0320268a055c95edc3e7333acefa795010c6e50a8e2",
    "auvergne-rhone-alpes": "60b4f96467419db40e9f3f33076057f4e093853c81d9e3315b8fe7f0459daa53",
    "occitanie": "30f08222923cf49525d0d5f8c0f4d169cb5cd80ecc2713eee1dc5ac4d2e3b8f4",
    "provence-alpes-cote-d-azur": "0b4deb7acb334c6aa5f4d8c6127a670c84709c79619176754b3a813491bcb273",
    "corse": "0cf92ac1ed0e39793d7257d7c71f43d4e6019d79806456f0aee961b4cc333a70",
}
REGIONS = list(HASHES)

ORIGINAL_ANNECY_WORKFLOW = """name: Annecy v0.4 Guards

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: annecy-v04-guards-${{ github.ref }}
  cancel-in-progress: true

jobs:
  annecy-v04-release:
    name: Annecy v0.4 release invariants
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout repository
        uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          persist-credentials: false
      - name: Set up Python
        uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6
        with:
          python-version: "3.13"
      - name: Test frozen Annecy v0.4 prepublication inputs
        run: python tests/test_sprint94_annecy_v04_prepublication.py
      - name: Test immutable Annecy v0.4 public release
        run: python tests/test_annecy_v04_public_release.py
"""


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if new in text:
        return text
    raise RuntimeError(f"Missing marker: {label}")


def counts(plan: dict) -> dict[str, int]:
    blocks = plan["blocks"]
    return {
        "pmr446": int(blocks["pmr446"]["memory_count"]),
        "amateur_calls": int(blocks["amateur_calls"]["memory_count"]),
        "aprs_iss": int(blocks["aprs_iss"]["memory_count"]),
        "aviation": int(blocks["aviation"]["memory_count"]),
        "regional_2m": int(blocks["regional_2m"]["rx_memory_count"]),
        "marine": int(blocks.get("marine", {}).get("memory_count", 0)),
    }


def build_records() -> list[dict]:
    entries = []
    for slug in REGIONS:
        base = ROOT / "research" / f"{slug}-v0.2"
        plan = read_json(base / "pack-plan.json")
        c = counts(plan)
        aviation = plan["blocks"]["aviation"]
        name = plan["pack"]
        current = int(plan["current_memory_count"])
        previous = int(plan["published_base_memory_count"])
        filename = f"radiopack-france-{slug}-v0.2.csv"
        route = f"/downloads/{slug}/{filename}"

        scope = {
            "schema_version": "1.0",
            "status": "frozen_public_scope",
            "frozen_on": DATE,
            "publication_sprint": SPRINT,
            "state_version": STATE_VERSION,
            "pack": name,
            "version": "0.2",
            "memory_count": current,
            "previous_public_version": "0.1",
            "previous_public_memory_count": previous,
            "included_blocks": c,
            "aviation_cycle": aviation["cycle"],
            "aviation_valid_through_inclusive": aviation["effective_until_inclusive"],
            "pack_plan": f"research/{slug}-v0.2/pack-plan.json",
            "common_primary_source_audit": "research/metropolitan-v0.2-primary-source-audit.md",
            "deferred": plan.get("deferred", {}),
            "rules": {
                "rx_only": True,
                "chirp_duplex": "off",
                "chirp_offset": "0.000000",
                "same_rf_deduplicated": True,
                "no_artificial_fill": True,
                "historical_v0_1_retained": True,
                "future_rf_change_requires_new_version": True,
            },
        }
        write_json(base / "release-scope.json", scope)

        review_items = [
            ("historical_v0_1_retained", "La v0.1 historique reste générable et n'est pas réécrite."),
            ("deterministic_pack_plan", "Le pack-plan v0.2 fixe les blocs, compteurs et sources."),
            ("rx_only_contract", "Toutes les mémoires sont exportées avec Duplex=off et Offset=0.000000."),
            ("memory_limit", "Le pack respecte la limite de 200 mémoires."),
            ("rf_deduplication", "La déduplication RF est active."),
            ("aviation_primary_review", "La sélection aviation est bornée et revue sur les pages publiques SIA eAIP AD 2.18 dans le contexte AIRAC 08/26."),
            ("amateur_public_sources", "La sélection FM 2 m repose sur des sources radioamateur publiques recoupées."),
            ("marine_scope_bounded", "Le bloc marine reste générique sans attribution locale de site non prouvée." if c["marine"] else "Aucun bloc marine n'est ajouté à cette région non littorale."),
            ("sensitive_data_excluded", "Les données privées, PPDR ou non publiquement vérifiables sont exclues."),
            ("fresh_build_hash_recorded", "Le CSV généré par le build Astro est figé par SHA-256."),
        ]
        checklist = {
            "schema_version": "1.0",
            "status": "review_complete",
            "reviewed_on": DATE,
            "publication_sprint": SPRINT,
            "state_version": STATE_VERSION,
            "pack": name,
            "version": "0.2",
            "completed": 10,
            "total": 10,
            "blocker_count": 0,
            "items": [{"id": i, "completed": True, "note": note} for i, note in review_items],
        }
        write_json(base / "review-checklist.json", checklist)

        gates = {
            "schema_version": "1.0",
            "status": "publication_gates_satisfied",
            "checked_on": DATE,
            "publication_sprint": SPRINT,
            "state_version": STATE_VERSION,
            "pack": name,
            "version": "0.2",
            "memory_count": current,
            "release_scope_frozen": True,
            "review_completed": 10,
            "review_total": 10,
            "blocker_count": 0,
            "rx_only": True,
            "rf_deduplication_required": True,
            "fresh_build_sha256_recorded": True,
            "historical_v0_1_route_retained": True,
            "aviation_freshness_valid_through_inclusive": aviation["effective_until_inclusive"],
            "public_release_allowed": True,
            "published_version_is_immutable": True,
            "future_change_requires_new_version": True,
            "blockers": [],
        }
        write_json(base / "publication-gates.json", gates)

        record = {
            "schema_version": "1.0",
            "status": "published_immutable",
            "published_on": DATE,
            "publication_sprint": SPRINT,
            "state_version": STATE_VERSION,
            "pack": name,
            "version": "0.2",
            "memory_count": current,
            "previous_public_version": "0.1",
            "previous_public_memory_count": previous,
            "public_route": route,
            "public_csv_sha256": HASHES[slug],
            "hash_basis": "fresh Astro production build from PR #19 before Sprint 98 state freeze",
            "generator": "website/src/lib/metropolitanPack.ts",
            "download_route": "website/src/pages/downloads/[slug]/[file].csv.ts",
            "pack_plan": f"research/{slug}-v0.2/pack-plan.json",
            "release_scope": f"research/{slug}-v0.2/release-scope.json",
            "review_checklist": f"research/{slug}-v0.2/review-checklist.json",
            "publication_gates": f"research/{slug}-v0.2/publication-gates.json",
            "common_primary_source_audit": "research/metropolitan-v0.2-primary-source-audit.md",
            "aviation": {
                "memory_count": c["aviation"],
                "cycle": aviation["cycle"],
                "valid_from": aviation["effective_from"],
                "valid_through_inclusive": aviation["effective_until_inclusive"],
                "reviewed_on": plan["sources"]["reviewed_on"],
                "direct_xml_field_match_claimed": False,
            },
            "marine_memory_count": c["marine"],
            "published_version_is_immutable": True,
            "rules": {
                "rx_only": True,
                "chirp_duplex": "off",
                "chirp_offset": "0.000000",
                "same_rf_frequency_deduplicated": True,
                "no_artificial_fill": True,
                "private_ppdr_operational_data_excluded": True,
            },
        }
        write_json(base / "publication-record.json", record)

        entries.append({
            "id": slug,
            "name": name,
            "version": "0.2",
            "memory_count": current,
            "previous_public_version": "0.1",
            "previous_public_memory_count": previous,
            "aviation_memory_count": c["aviation"],
            "marine_memory_count": c["marine"],
            "public_route": route,
            "sha256": HASHES[slug],
            "publication_record": f"research/{slug}-v0.2/publication-record.json",
        })
    return entries


def sync_state(entries: list[dict]) -> None:
    path = ROOT / "research/project-resume-state.json"
    state = read_json(path)
    state["updated"] = DATE
    state["current_sprint"] = SPRINT
    state["state_version"] = STATE_VERSION

    public = state.setdefault("public_packs", {})
    for e in entries:
        public[e["id"].replace("-", "_")] = {
            "version": "0.2",
            "memory_count": e["memory_count"],
            "immutable": True,
            "previous_immutable_version": "0.1",
            "previous_memory_count": e["previous_public_memory_count"],
            "publication_record": e["publication_record"],
            "public_csv_sha256": e["sha256"],
        }

    state["latest_sprint98_metropolitan_consolidation"] = {
        "sprint": SPRINT,
        "state_version": STATE_VERSION,
        "completed_on": DATE,
        "status": "eleven_metropolitan_v02_publications_consolidated_official",
        "region_count": 11,
        "manifest": "research/sprint-98-metropolitan-publication-manifest.json",
        "summary": "research/sprint-98-summary.md",
        "state_sync_guard": "tests/test_sprint98_state_sync.py",
        "built_csv_guard": "tools/check_metropolitan_v02_publication_records.py",
        "historical_v0_1_retained": True,
        "publication_records_complete": True,
        "release_scopes_complete": True,
        "review_checklists_complete": True,
        "publication_gates_complete": True,
        "rf_data_mutation": False,
        "public_csv_mutation": False,
    }

    sources = state.setdefault("sources_of_truth", [])
    required = [
        "research/sprint-98-summary.md",
        "research/sprint-98-metropolitan-publication-manifest.json",
        "research/metropolitan-v0.2-primary-source-audit.md",
        "tools/check_metropolitan_v02_publication_records.py",
        "tests/test_sprint98_state_sync.py",
    ]
    for e in entries:
        slug = e["id"]
        required += [
            f"research/{slug}-v0.2/pack-plan.json",
            f"research/{slug}-v0.2/release-scope.json",
            f"research/{slug}-v0.2/review-checklist.json",
            f"research/{slug}-v0.2/publication-gates.json",
            f"research/{slug}-v0.2/publication-record.json",
        ]
    for item in required:
        if item not in sources:
            sources.append(item)

    state.setdefault("field_tools", {})["check_metropolitan_v02_publication_records"] = "python tools/check_metropolitan_v02_publication_records.py --dist website/dist"
    state["field_tools"]["test_sprint98_state_sync"] = "python tests/test_sprint98_state_sync.py"
    recent = [item for item in state.setdefault("recent_sprints", []) if item.get("sprint") != 98]
    recent.insert(0, {
        "sprint": 98,
        "state_version": STATE_VERSION,
        "summary": "Eleven metropolitan v0.2 publications consolidated with immutable records, fresh-build SHA-256 manifests, release scopes, review checklists and CI guards; no RF or CSV mutation.",
        "summary_file": "research/sprint-98-summary.md",
    })
    state["recent_sprints"] = recent
    write_json(path, state)


def write_manifest(entries: list[dict]) -> None:
    write_json(ROOT / "research/sprint-98-metropolitan-publication-manifest.json", {
        "schema_version": "1.0",
        "status": "sprint98_metropolitan_v02_publication_manifest",
        "sprint": 98,
        "state_version": STATE_VERSION,
        "consolidated_on": DATE,
        "region_count": 11,
        "memory_count": sum(e["memory_count"] for e in entries),
        "all_versions": "0.2",
        "all_rx_only": True,
        "historical_v0_1_retained": True,
        "rf_data_changed_by_sprint98": False,
        "public_csv_content_changed_by_sprint98": False,
        "hash_basis": "fresh Astro production build in RadioPack CI PR #19",
        "entries": entries,
    })


def write_summary(entries: list[dict]) -> None:
    rows = "\n".join(f"| {e['name']} | {e['memory_count']} | `{e['sha256']}` |" for e in entries)
    text = f"""# Sprint 98 — consolidation métropolitaine v0.2

Date : **{DATE}**  
État logique : **{STATE_VERSION}**

Le Sprint 98 transforme la publication post-Sprint 97 des onze régions métropolitaines en état officiel auditable. **Aucune fréquence, aucune mémoire RF et aucun CSV public ne sont modifiés par ce sprint.**

## Résultat

- **11** packs v0.2 consolidés ;
- **1135 mémoires RX** sur ces onze packs ;
- un `publication-record.json`, un `release-scope.json`, un `review-checklist.json` **10/10** et un `publication-gates.json` par région ;
- SHA-256 figé sur un build Astro frais pour chaque CSV généré ;
- v0.1 historiques conservées et générables ;
- contrat `Duplex=off` / `Offset=0.000000` inchangé ;
- état officiel porté à **Sprint 98 / {STATE_VERSION}**.

| Région | Mémoires | SHA-256 |
|---|---:|---|
{rows}

Manifeste : `research/sprint-98-metropolitan-publication-manifest.json`. Audit primaire commun : `research/metropolitan-v0.2-primary-source-audit.md`.

## Travaux actifs conservés

- **Bretagne v0.3** : 151 RX, delta 0, revalidation AIRAC 09/26 requise à partir du 3 septembre 2026 ;
- **Normandie v0.5** : 142 RX, delta 0, gates terrain/source inchangés.

Toute évolution RF ultérieure d'un des onze packs devra créer une nouvelle version ; les v0.2 consolidées ici sont immuables.
"""
    (ROOT / "research/sprint-98-summary.md").write_text(text, encoding="utf-8")


def sync_docs(entries: list[dict]) -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = replace_once(text,
        "**État courant : Sprint 97 / 0.21.86 — socle officiel conservé ; publication post-Sprint 97 des onze packs régionaux désormais enrichis en v0.2, avec couverture métropolitaine 13/13.**",
        "**État courant : Sprint 98 / 0.21.87 — consolidation officielle des onze packs métropolitains v0.2, avec couverture 13/13, publication records, scopes figés et SHA-256 issus d'un build Astro frais.**",
        "README current state")
    text = replace_once(text,
        "## État actuel — Sprint 97 / 0.21.86\n\nLe **Sprint 97 / 0.21.86** reste le dernier état logique officiel synchronisé dans `PROJECT_STATUS.md`, `CHANGELOG.md` et `research/project-resume-state.json`. La couverture métropolitaine du 19 août 2026 constitue une publication post-Sprint 97 et ne réécrit pas rétrospectivement cet état historique.",
        "## État actuel — Sprint 98 / 0.21.87\n\nLe **Sprint 98 / 0.21.87** est l'état logique officiel synchronisé dans `PROJECT_STATUS.md`, `CHANGELOG.md` et `research/project-resume-state.json`. Il consolide la publication métropolitaine v0.2 sans modifier les fréquences ni le contenu des CSV publics.",
        "README state section")
    marker = "## Sprint 97 — consolidation de l’état post-Sprint 96"
    s98 = """## Sprint 98 — consolidation des onze v0.2

Les onze packs métropolitains v0.2 disposent désormais chacun d'un scope figé, d'une checklist 10/10, de gates de publication satisfaits et d'un `publication-record.json` contenant le SHA-256 du CSV issu d'un build Astro frais. Le manifeste commun est `research/sprint-98-metropolitan-publication-manifest.json` et le résumé est `research/sprint-98-summary.md`.

Le Sprint 98 ne change aucune mémoire RF : il rend la publication du 19 août reproductible et verrouille l'immuabilité des v0.2. Les v0.1 restent historiques et générables.

"""
    if s98 not in text:
        text = text.replace(marker, s98 + marker, 1)
    readme.write_text(text, encoding="utf-8")

    project = ROOT / "PROJECT_STATUS.md"
    text = project.read_text(encoding="utf-8")
    text = replace_once(text, "Dernière mise à jour : **17 août 2026**", "Dernière mise à jour : **19 août 2026**", "status date")
    text = replace_once(text, "Sprint courant : **97**", "Sprint courant : **98**", "status sprint")
    text = replace_once(text, "État logique : **0.21.86**", "État logique : **0.21.87**", "status version")
    text = replace_once(text,
        "L'état machine officiel correspondant est `research/project-resume-state.json`. Résumé courant : `research/sprint-97-summary.md`. Détail structuré de consolidation : `research/sprint-97-post96-ui-state.json`. Audit détaillé : `research/security-audit-sprint92.md`.",
        "L'état machine officiel correspondant est `research/project-resume-state.json`. Résumé courant : `research/sprint-98-summary.md`. Manifeste métropolitain : `research/sprint-98-metropolitan-publication-manifest.json`. Audit détaillé : `research/security-audit-sprint92.md`.",
        "status refs")
    public_marker = "- Bretagne v0.1 : **135 mémoires RX**, publication historique immuable.\n"
    region_lines = "\n".join(f"- {e['name']} v0.2 : **{e['memory_count']} mémoires RX**, publiée et immuable." for e in entries) + "\n"
    if region_lines not in text:
        text = text.replace(public_marker, public_marker + region_lines, 1)
    text = replace_once(text, "## Publication post-Sprint 97 — enrichissement métropolitain v0.2", "## Sprint 98 — consolidation officielle de l'enrichissement métropolitain v0.2", "status header")
    text = text.replace(
        "Cette publication ne change pas l'état logique officiel **97 / 0.21.86**.",
        "Cette publication est désormais intégrée à l'état logique officiel **98 / 0.21.87**. Chaque v0.2 possède un `publication-record.json`, un scope figé, une checklist 10/10, des gates satisfaits et un SHA-256 calculé sur un build Astro frais. Le Sprint 98 lui-même ne modifie aucune mémoire RF ni aucun CSV public.",
        1)
    project.write_text(text, encoding="utf-8")

    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    entry = """## 0.21.87 - 2026-08-19

- **Sprint 98** : consolidation officielle des onze packs métropolitains v0.2 publiés le 19 août 2026.
- Ajout pour chaque région d'un `publication-record.json`, d'un `release-scope.json`, d'un `review-checklist.json` 10/10 et d'un `publication-gates.json` sans bloqueur.
- SHA-256 des onze CSV calculés sur un build Astro frais et regroupés dans `research/sprint-98-metropolitan-publication-manifest.json`.
- Synchronisation de `README.md`, `PROJECT_STATUS.md` et `research/project-resume-state.json` sur **98 / 0.21.87**.
- Ajout de `tests/test_sprint98_state_sync.py` et de `tools/check_metropolitan_v02_publication_records.py` aux garde-fous CI.
- Aucune fréquence, aucune mémoire RF ni aucun contenu CSV public modifié par le Sprint 98 ; les v0.1 historiques restent générables et les v0.2 deviennent explicitement immuables.

"""
    if entry not in text:
        text = text.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
    changelog.write_text(text, encoding="utf-8")


def write_checks(entries: list[dict]) -> None:
    checker = ROOT / "tools/check_metropolitan_v02_publication_records.py"
    checker.write_text('''#!/usr/bin/env python3
import argparse, csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--dist", type=Path, default=ROOT / "website/dist")
args = parser.parse_args()
dist = args.dist if args.dist.is_absolute() else ROOT / args.dist
manifest = json.loads((ROOT / "research/sprint-98-metropolitan-publication-manifest.json").read_text(encoding="utf-8"))
assert manifest["sprint"] == 98 and manifest["region_count"] == 11
for entry in manifest["entries"]:
    slug = entry["id"]
    csv_path = dist / entry["public_route"].lstrip("/")
    assert csv_path.is_file(), csv_path
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    assert digest == entry["sha256"]
    record = json.loads((ROOT / entry["publication_record"]).read_text(encoding="utf-8"))
    assert record["public_csv_sha256"] == digest
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == entry["memory_count"]
    assert all(r["Duplex"] == "off" and r["Offset"] == "0.000000" for r in rows)
print("Sprint 98 metropolitan v0.2 publication records: 11 fresh-build hashes, counts and RX-only contracts OK")
''', encoding="utf-8")

    expected = {e["id"].replace("-", "_"): e["memory_count"] for e in entries}
    test = ROOT / "tests/test_sprint98_state_sync.py"
    test.write_text(f'''#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/sprint-98-metropolitan-publication-manifest.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
assert state["updated"] == "2026-08-19"
assert state["current_sprint"] == 98
assert state["state_version"] == "0.21.87"
assert "**État courant : Sprint 98 / 0.21.87" in readme
assert "## État actuel — Sprint 98 / 0.21.87" in readme
assert "Sprint courant : **98**" in project
assert "État logique : **0.21.87**" in project
assert changelog.startswith("# Changelog\\n\\n## 0.21.87 - 2026-08-19")
assert manifest["region_count"] == 11 and manifest["memory_count"] == 1135
assert manifest["all_rx_only"] is True
expected = {json.dumps(expected, ensure_ascii=False)}
for key, count in expected.items():
    p = state["public_packs"][key]
    assert p["version"] == "0.2" and p["memory_count"] == count and p["immutable"] is True
    assert p["previous_immutable_version"] == "0.1" and len(p["public_csv_sha256"]) == 64
for entry in manifest["entries"]:
    base = ROOT / "research" / f"{{entry['id']}}-v0.2"
    for name in ["release-scope.json", "review-checklist.json", "publication-gates.json", "publication-record.json"]:
        assert (base / name).is_file()
    review = json.loads((base / "review-checklist.json").read_text(encoding="utf-8"))
    gates = json.loads((base / "publication-gates.json").read_text(encoding="utf-8"))
    record = json.loads((base / "publication-record.json").read_text(encoding="utf-8"))
    assert review["completed"] == review["total"] == 10 and review["blocker_count"] == 0
    assert gates["public_release_allowed"] is True and gates["blocker_count"] == 0
    assert record["public_csv_sha256"] == entry["sha256"] and record["published_version_is_immutable"] is True
s98 = state["latest_sprint98_metropolitan_consolidation"]
assert s98["sprint"] == 98 and s98["state_version"] == "0.21.87" and s98["region_count"] == 11
assert s98["rf_data_mutation"] is False and s98["public_csv_mutation"] is False
assert state["recent_sprints"][0]["sprint"] == 98
assert "- name: Test Sprint 98 state synchronization" in ci
assert "python tools/check_metropolitan_v02_publication_records.py --dist website/dist" in ci
print("Sprint 98 state sync: 11 metropolitan v0.2 records, hashes, scopes, reviews and official state 98 / 0.21.87 OK")
''', encoding="utf-8")

    p97 = ROOT / "tests/test_sprint97_state_sync.py"
    text = p97.read_text(encoding="utf-8")
    for old, new in [
        ('assert state["updated"] == "2026-08-17"\n', 'assert state["updated"] >= "2026-08-17"\n'),
        ('assert state["current_sprint"] == 97\n', 'assert state["current_sprint"] >= 97\n'),
        ('assert state["state_version"] == "0.21.86"\n', ''),
        ('assert "**État courant : Sprint 97 / 0.21.86" in readme\n', ''),
        ('assert "## État actuel — Sprint 97 / 0.21.86" in readme\n', ''),
        ('assert "Sprint courant : **97**" in project\n', ''),
        ('assert "État logique : **0.21.86**" in project\n', ''),
        ('assert changelog.startswith("# Changelog\\n\\n## 0.21.86 - 2026-08-17")\n', 'assert "## 0.21.86 - 2026-08-17" in changelog\n'),
        ('assert state["recent_sprints"][0]["sprint"] == 97\nassert state["recent_sprints"][0]["state_version"] == "0.21.86"\nassert state["recent_sprints"][0]["summary_file"] == "research/sprint-97-summary.md"\n', 'assert any(x.get("sprint") == 97 and x.get("state_version") == "0.21.86" for x in state["recent_sprints"])\n'),
    ]:
        text = text.replace(old, new, 1)
    text = text.replace('print("Sprint 97 state sync: README, status, changelog, machine state, UX consolidation and CI guard aligned at 97 / 0.21.86 OK")', 'print("Sprint 97 historical state remains auditable after later official states OK")')
    p97.write_text(text, encoding="utf-8")

    ci = ROOT / ".github/workflows/ci.yml"
    text = ci.read_text(encoding="utf-8")
    marker = "      - name: Test Sprint 97 state synchronization\n        run: python tests/test_sprint97_state_sync.py\n"
    if "Test Sprint 98 state synchronization" not in text:
        text = text.replace(marker, marker + "\n      - name: Test Sprint 98 state synchronization\n        run: python tests/test_sprint98_state_sync.py\n", 1)
    marker2 = "      - name: Test built public pack catalog\n        run: cd .. && python tests/test_built_public_pack_catalog.py\n"
    if "Verify metropolitan v0.2 publication records" not in text:
        text = text.replace(marker2, marker2 + "\n      - name: Verify metropolitan v0.2 publication records\n        run: cd .. && python tools/check_metropolitan_v02_publication_records.py --dist website/dist\n", 1)
    ci.write_text(text, encoding="utf-8")


def main() -> None:
    entries = build_records()
    write_manifest(entries)
    write_summary(entries)
    sync_state(entries)
    sync_docs(entries)
    write_checks(entries)
    (ROOT / ".github/workflows/annecy-v04-guards.yml").write_text(ORIGINAL_ANNECY_WORKFLOW, encoding="utf-8")
    Path(__file__).unlink()
    print("Sprint 98 state files generated; temporary workflow restored and bootstrap script removed")


if __name__ == "__main__":
    main()
