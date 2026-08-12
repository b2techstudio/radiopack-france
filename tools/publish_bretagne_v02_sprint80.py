#!/usr/bin/env python3
"""One-shot Sprint 80 publisher for immutable Bretagne v0.2 (151 RX memories)."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/bretagne-v0.2"
PUBLIC = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


def main() -> None:
    # Preconditions: Sprint 79 frozen scope and audit must be green before publication.
    state = load_json(ROOT / "research/project-resume-state.json")
    if state["current_sprint"] != 79 or state["state_version"] != "0.21.68":
        raise RuntimeError("Unexpected project state before Sprint 80 publication")

    scope = load_json(RESEARCH / "release-scope.json")
    checklist = load_json(RESEARCH / "review-checklist.json")
    gates = load_json(RESEARCH / "publication-gates.json")
    maturity = load_json(RESEARCH / "maturity-review.json")
    aviation = load_json(RESEARCH / "aviation-airac-08.json")

    if scope["final_candidate_memory_count"] != 151 or scope["prepublication_ready"] is not True:
        raise RuntimeError("Bretagne v0.2 scope is not frozen at 151")
    if checklist["completed"] != 10 or checklist["blocker_count"] != 0:
        raise RuntimeError("Bretagne v0.2 checklist is not 10/10 with zero blockers")
    if gates["status"] != "prepublication_ready_151_not_public":
        raise RuntimeError("Bretagne v0.2 publication gates are not in prepublication state")
    if maturity["release_blockers"] != [] or maturity["prepublication_ready"] is not True:
        raise RuntimeError("Bretagne v0.2 maturity review is not ready")
    if aviation["cycle"]["validation_cycle"] != "AIRAC 08/26":
        raise RuntimeError("Unexpected aviation cycle")
    if aviation["cycle"]["effective_until_inclusive"] != "2026-09-02":
        raise RuntimeError("Unexpected AIRAC 08/26 validity boundary")

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/run_bretagne_v02_prepublication_audit.py"),
            "--root",
            str(ROOT),
            "--require-prepublication-ready",
        ],
        check=True,
    )

    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/build_bretagne_v02_internal_candidate.py"),
                "--root",
                str(ROOT),
                "--output-dir",
                str(temp),
            ],
            check=True,
        )
        candidate_csv = temp / "bretagne-v0.2-internal.csv"
        candidate_json = load_json(temp / "bretagne-v0.2-internal.json")
        with candidate_csv.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if candidate_json["memory_count"] != 151 or len(rows) != 151:
            raise RuntimeError("Bretagne v0.2 candidate is not exactly 151 memories")
        if candidate_json["new_memory_count"] != 16:
            raise RuntimeError("Bretagne v0.2 aviation delta is not exactly 16")
        if any(row["Duplex"] != "off" or row["Offset"] != "0.000000" for row in rows):
            raise RuntimeError("RX-only contract broken")
        if len({round(float(row["Frequency"]), 6) for row in rows}) != 151:
            raise RuntimeError("Duplicate RF detected")
        PUBLIC.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(candidate_csv, PUBLIC)

    public_bytes = PUBLIC.read_bytes()
    public_sha256 = hashlib.sha256(public_bytes).hexdigest()

    # Immutable publication record.
    record = {
        "schema_version": "1.0",
        "status": "published_immutable",
        "published_on": "2026-08-12",
        "publication_sprint": 80,
        "state_version": "0.21.69",
        "pack": "Bretagne",
        "version": "0.2",
        "memory_count": 151,
        "new_memory_count_vs_v0_1": 16,
        "public_csv": "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
        "public_csv_sha256": public_sha256,
        "candidate_builder": "tools/build_bretagne_v02_internal_candidate.py",
        "release_scope": "research/bretagne-v0.2/release-scope.json",
        "review_checklist": "research/bretagne-v0.2/review-checklist.json",
        "publication_gates": "research/bretagne-v0.2/publication-gates.json",
        "maturity_review": "research/bretagne-v0.2/maturity-review.json",
        "previous_public_version": "0.1",
        "previous_public_memory_count": 135,
        "previous_public_csv": "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv",
        "aviation": {
            "memory_count": 16,
            "cycle": "AIRAC 08/26",
            "valid_from": "2026-08-06",
            "valid_through_inclusive": "2026-09-02",
            "freshness_rechecked_on": "2026-08-12",
            "current_sia_product_verified": True,
            "current_xml_export_bytes_extracted": False,
            "direct_xml_field_match_claimed": False,
        },
        "deferred_after_v0_2": [
            "F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY",
            "CROSS_LOCAL_TRANSMITTER_SITE_MAPPING",
            "STOPPED_OR_UNRESOLVED_AMATEUR_INFRASTRUCTURE",
        ],
        "published_version_is_immutable": True,
        "rules": {
            "rx_only": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "same_rf_frequency_deduplicated": True,
            "no_artificial_fill": True,
            "unpublished_data_not_inferred": True,
            "generic_ch64_ch79_do_not_claim_local_transmitter_site": True,
        },
    }
    write_json(RESEARCH / "publication-record.json", record)

    # Publication gates: historical prepublication artifacts remain otherwise unchanged.
    gates["status"] = "published_immutable_151"
    gates["updated"] = "2026-08-12"
    gates["published_on"] = "2026-08-12"
    gates["public_release_allowed"] = False
    gates["public_csv_sha256"] = public_sha256
    explicit = next(item for item in gates["gates"] if item["id"] == "explicit_publication")
    explicit["status"] = "passed_publication_completed_immutable"
    explicit["description"] = "Bretagne v0.2 published explicitly at 151 RX memories; CSV and registry are now immutable for this version."
    write_json(RESEARCH / "publication-gates.json", gates)

    # Generator metadata.
    options_path = ROOT / "generator/options.json"
    options = load_json(options_path)
    bzh_option = next(item for item in options["pack_selection"]["packs"] if item["id"] == "bretagne")
    bzh_option["version"] = "v0.2"
    bzh_option["default_memory_count"] = 151
    bzh_option["aviation_included"] = True
    bzh_option["aviation_memory_count"] = 16
    write_json(options_path, options)

    # Public registry.
    registry_path = ROOT / "website/src/lib/packRegistry.ts"
    registry = registry_path.read_text(encoding="utf-8")
    old_bzh = '''  {
    id: "bretagne",
    regionSlug: "bretagne",
    name: "Bretagne",
    version: "v0.1",
    status: "Disponible",
    description: "Pack régional Bretagne v0.1 de 135 mémoires RX, sans aviation dans ce périmètre initial.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 135,
        filename: "radiopack-france-bretagne-v0.1.csv",
        downloadUrl: "/downloads/bretagne/radiopack-france-bretagne-v0.1.csv",
      },
    ],
  },'''
    new_bzh = '''  {
    id: "bretagne",
    regionSlug: "bretagne",
    name: "Bretagne",
    version: "v0.2",
    status: "Disponible",
    description: "Pack régional Bretagne v0.2 de 151 mémoires RX, dont 16 mémoires aviation AIRAC 08/26.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 151,
        filename: "radiopack-france-bretagne-v0.2.csv",
        downloadUrl: "/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
        aviationIncluded: true,
      },
    ],
  },'''
    registry = replace_once(registry, old_bzh, new_bzh, "registry Bretagne object")
    registry_path.write_text(registry, encoding="utf-8")

    # Bretagne public page, complete replacement.
    bretagne_page = '''---
import BaseLayout from "../../layouts/BaseLayout.astro";
---
<BaseLayout title="Pack Bretagne v0.2 - RadioPack France" description="CSV CHIRP Bretagne v0.2 de 151 mémoires RX pour Quansheng UV-K5, dont 16 mémoires aviation AIRAC 08/26, en réception seule.">
  <section class="section"><div class="container page-grid">
    <div class="copy">
      <span class="eyebrow">Pack régional - v0.2</span>
      <h1>Bretagne</h1>
      <p class="lead">La version 0.2 contient 151 mémoires RX validées : le socle Bretagne v0.1 de 135 mémoires, complété par 16 mémoires aviation AIRAC 08/26.</p>
      <div class="button-row"><a class="button button-primary" href="/downloads/bretagne/radiopack-france-bretagne-v0.2.csv" download>Télécharger le CSV v0.2</a><a class="button button-secondary" href="/documentation">Procédure CHIRP</a></div>
      <div class="card legal"><strong>Réception seule sur les 151 mémoires</strong><p>Toutes les lignes utilisent <code>Duplex=off</code> et <code>Offset=0.000000</code>. Le pack n'accorde aucun droit d'émission.</p></div>
      <div class="memory-map card"><h2>Périmètre v0.2</h2><div class="ranges"><span><b>135</b> socle Bretagne v0.1</span><span><b>16</b> aviation</span><span><b>AIRAC</b> 08/26</span><span><b>Rennes</b> 7</span><span><b>Brest</b> 5</span><span><b>Dinard</b> 2</span><span><b>Quimper</b> 1</span><span><b>Urgence</b> 121.500</span></div></div>
      <div class="card legal"><strong>Fraîcheur aviation</strong><p>Le cycle AIRAC 08/26 a été recontrôlé le 12 août 2026 et est valable jusqu'au 2 septembre 2026 inclus. Le dépôt ne revendique pas de comparaison XML champ par champ non effectuée.</p></div>
    </div>
    <aside class="card status-card"><span class="badge badge-green">Disponible - v0.2</span><h3>151 mémoires sur 200</h3><div class="meter"><span></span></div><ul><li>RX-only</li><li>16 mémoires aviation AM, pas 8,33 kHz</li><li>Ch64 et Ch79 conservés en paires RX génériques</li><li>Aucune fréquence ADRASEC non publiée intégrée</li><li>Aucun site CROSS local non prouvé revendiqué</li></ul></aside>
  </div></section>
</BaseLayout>
<style>
.page-grid{display:grid;grid-template-columns:1.25fr .75fr;gap:30px;align-items:start}.copy{display:grid;gap:22px}.copy h1{font-size:clamp(3.8rem,8vw,6.4rem)}.status-card{padding:28px}.status-card h3{margin:18px 0 10px}.status-card ul{margin:0;padding-left:1.2rem;color:var(--muted)}.meter{height:10px;border-radius:999px;background:#dfe7f1;overflow:hidden;margin-bottom:18px}.meter span{display:block;width:75.5%;height:100%;border-radius:inherit;background:linear-gradient(90deg,#1687e9,#00a7bb,#6e3de8)}.legal,.memory-map{padding:22px}.legal p{margin-top:6px;color:var(--muted)}code{font-weight:800;color:#5f31cf}.ranges{display:flex;flex-wrap:wrap;gap:10px}.ranges span{padding:.55rem .7rem;border-radius:10px;border:1px solid var(--line);background:rgba(255,255,255,.8);color:var(--muted);font-size:.82rem}.ranges b{color:#1687e9;margin-right:4px}@media(max-width:800px){.page-grid{grid-template-columns:1fr}}
</style>
'''
    (ROOT / "website/src/pages/regions/bretagne.astro").write_text(bretagne_page, encoding="utf-8")

    # Generator copy: version/count plus fixed aviation summary behavior.
    generator_path = ROOT / "website/src/pages/generateur.astro"
    generator = generator_path.read_text(encoding="utf-8")
    generator = replace_once(generator, "Bretagne · 135", "Bretagne · 151", "generator Bretagne badge")
    generator = replace_once(
        generator,
        "Le générateur propose directement le CSV Bretagne v0.1 validé, sans aviation dans ce périmètre.",
        "Le générateur propose directement le CSV Bretagne v0.2 validé, avec 16 mémoires aviation AIRAC 08/26.",
        "generator Bretagne description",
    )
    generator = replace_once(
        generator,
        '      } else {\n        aviationSummary.textContent = "Configuration fixe";\n        if (variantNote) variantNote.textContent = "Ce pack est proposé dans sa variante publique fixe déjà validée.";\n      }',
        '      } else {\n        aviationSummary.textContent = variant.aviationIncluded ? "Incluse · variante fixe" : "Configuration fixe";\n        if (variantNote) variantNote.textContent = variant.aviationIncluded\n          ? "Ce pack public fixe inclut son bloc aviation validé."\n          : "Ce pack est proposé dans sa variante publique fixe déjà validée.";\n      }',
        "generator fixed aviation summary",
    )
    generator_path.write_text(generator, encoding="utf-8")

    # Sprint 73 historical test becomes forward-compatible while preserving v0.1 immutability.
    test73 = '''import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/bretagne-v0.1/publication-record.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/bretagne-v0.1/release-scope.json").read_text(encoding="utf-8"))
plan = json.loads((ROOT / "research/bretagne-v0.1/pack-plan.json").read_text(encoding="utf-8"))
gates = json.loads((ROOT / "research/bretagne-v0.1/publication-gates.json").read_text(encoding="utf-8"))
assert state["current_sprint"] >= 73 and state["state_version"] >= "0.21.62"
assert state["public_packs"]["bretagne"]["version"] in {"0.1", "0.2"}
assert state["public_packs"]["bretagne"]["memory_count"] in {135, 151}
assert state["public_packs"]["bretagne"]["immutable"] is True
assert state["public_packs"]["normandie"]["version"] == "0.4" and state["public_packs"]["normandie"]["memory_count"] == 142
assert state["public_packs"]["annecy_alpes_leman"]["version"] == "0.2" and state["public_packs"]["annecy_alpes_leman"]["memory_count"] == 65
assert record["status"] == "published_immutable" and record["memory_count"] == 135
assert record["version"] == "0.1" and record["published_version_is_immutable"] is True
assert scope["status"] == "scope_frozen_135_prepublication_not_public" and scope["sprint"] == 72
assert plan["status"] == "prepublication_ready_135_not_public" and plan["publication"]["explicit_publication_required"] is True
assert gates["status"] == "published_immutable_135"
assert next(g for g in gates["gates"] if g["id"] == "explicit_publication")["status"] == "passed_publication_completed_immutable"
assert scope["included"]["channel64_pair_mhz"] == [156.225,160.825]
assert scope["included"]["channel79_pair_mhz"] == [156.975,161.575]
assert {x["id"] for x in scope["deferred_to_v0_2"]} == {"AVIATION_CURRENT_SIA","ADRASEC_UNPUBLISHED_OPERATIONAL_FREQUENCIES","CROSS_LOCAL_TRANSMITTER_SITE_MAPPING","STOPPED_OR_UNRESOLVED_AMATEUR_INFRASTRUCTURE"}
assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()
if state["current_sprint"] >= 80:
    assert state["public_packs"]["bretagne"]["version"] == "0.2"
    assert state["public_packs"]["bretagne"]["memory_count"] == 151
print("Sprint 73: Bretagne v0.1 historical publication remains immutable and auditable after later Bretagne releases OK")
'''
    (ROOT / "tests/test_sprint73_bretagne_publication.py").write_text(test73, encoding="utf-8")

    # Sprint 79 remains a historical scope-freeze guard after publication.
    test79 = '''import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/bretagne-v0.2"

maturity = json.loads((RESEARCH / "maturity-review.json").read_text(encoding="utf-8"))
scope = json.loads((RESEARCH / "release-scope.json").read_text(encoding="utf-8"))
checklist = json.loads((RESEARCH / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((RESEARCH / "publication-gates.json").read_text(encoding="utf-8"))
record_path = RESEARCH / "publication-record.json"

assert maturity["status"] == "scope_freeze_recommended_prepublication_ready_not_public"
assert maturity["candidate_memory_count"] == 151
assert maturity["candidate_new_memory_count"] == 16
assert maturity["release_blockers"] == []
assert maturity["scope_freeze_allowed"] is True
assert maturity["prepublication_ready"] is True
assert maturity["public_release_allowed"] is False
assert maturity["included_scope"]["aviation_current_on_review_date"] is True
assert maturity["aviation_methodology_boundary"]["current_xml_export_bytes_extracted"] is False
assert maturity["aviation_methodology_boundary"]["direct_current_xml_field_match_claimed"] is False
assert maturity["decision"]["freeze_candidate_at"] == 151
assert maturity["decision"]["publication_must_be_separate_explicit_sprint"] is True

assert scope["status"] == "scope_frozen_151_prepublication_not_public"
assert scope["sprint"] == 79
assert scope["state_version"] == "0.21.68"
assert scope["final_candidate_memory_count"] == 151
assert scope["new_memory_count_vs_v0_1"] == 16
assert scope["prepublication_ready"] is True
assert scope["public_export_allowed"] is False
assert len(scope["deferred_after_v0_2"]) == 3

assert checklist["status"] == "review_complete_prepublication_ready_not_public"
assert checklist["candidate_memory_count"] == 151
assert checklist["completed"] == 10
assert checklist["total"] == 10
assert checklist["blocker_count"] == 0
assert checklist["prepublication_ready"] is True
assert all(item["passed"] is True for item in checklist["checks"])

assert gates["prepublication_ready"] is True
assert gates["public_release_allowed"] is False
assert gates["gates"][-1]["id"] == "explicit_publication"
if record_path.exists():
    assert gates["status"] == "published_immutable_151"
    assert gates["gates"][-1]["status"] == "passed_publication_completed_immutable"
else:
    assert gates["status"] == "prepublication_ready_151_not_public"
    assert gates["gates"][-1]["status"] == "pending_separate_publication_sprint"

subprocess.run([
    sys.executable,
    str(ROOT / "tools/run_bretagne_v02_prepublication_audit.py"),
    "--root",
    str(ROOT),
    "--require-prepublication-ready",
], check=True)

public = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
if record_path.exists():
    assert public.exists()
    assert "radiopack-france-bretagne-v0.2.csv" in registry
else:
    assert not public.exists()
    assert "radiopack-france-bretagne-v0.2.csv" not in registry

print("Sprint 79 Bretagne v0.2 maturity: frozen 151-memory scope remains auditable before or after explicit Sprint 80 publication OK")
'''
    (ROOT / "tests/test_sprint79_bretagne_v02_maturity.py").write_text(test79, encoding="utf-8")

    # Current registry test.
    registry_test = '''import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
GENERATOR = ROOT / "website/src/pages/generateur.astro"
REGIONS = ROOT / "website/src/data/regions.json"
NORMANDIE = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
BRETAGNE = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"

for path in [REGISTRY, GENERATOR, REGIONS, NORMANDIE, BRETAGNE]:
    assert path.is_file(), f"Fichier multi-régions manquant: {path.relative_to(ROOT)}"

registry = REGISTRY.read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"', 'regionSlug: "annecy-haute-savoie"', 'name: "Annecy–Alpes–Léman"',
    'version: "v0.2"', 'defaultVariant: "full"', 'includedVariant: "full"', 'excludedVariant: "no-aviation"',
    'memoryCount: 65', 'memoryCount: 48', 'id: "normandie"', 'regionSlug: "normandie"', 'version: "v0.4"',
    'defaultVariant: "standard"', 'memoryCount: 142', '/downloads/normandie/radiopack-france-normandie-v0.4.csv',
    'id: "bretagne"', 'regionSlug: "bretagne"', 'memoryCount: 151',
    '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv', 'aviationIncluded: true',
    'export const defaultPublicPackId = "annecy-alpes-leman"', "export const getPublicPack", "export const getPublicVariant",
]:
    assert expected in registry, f"Contrat registre absent: {expected}"

assert registry.count('downloadUrl: "') == 4
assert "annecy-haute-savoie-v0.1" not in registry

page = GENERATOR.read_text(encoding="utf-8")
for expected in [
    'import { defaultPublicPackId, publicPacks } from "../lib/packRegistry"', 'id="radiopack-generator"', 'id="pack-select"',
    'id="pack-summary"', 'id="aviation-fieldset"', 'id="notam-fieldset"', "publicPacks.find((pack) => pack.id === selectedId)",
    "pack.aviationToggle.includedVariant", "pack.aviationToggle.excludedVariant", "aviationFieldset.hidden = !aviationSupported",
    "notamFieldset.hidden = !pack.notamCheck", "downloadLink.href = variant.downloadUrl", 'downloadLink.setAttribute("download", variant.filename)',
    "Normandie · 142", "Bretagne · 151", "Annecy · 65 / 48", 'variant.aviationIncluded ? "Incluse · variante fixe"',
]:
    assert expected in page, f"Contrat générateur multi-régions absent: {expected}"

assert "new Blob" not in page
assert "URL.createObjectURL" not in page

for path, expected_count in [(NORMANDIE, 142), (BRETAGNE, 151)]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" for row in rows)
    assert all(row["Offset"] == "0.000000" for row in rows)
    assert all(len(row["Name"]) <= 10 for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count

print("Tests RadioPack public pack registry: Annecy 65/48 + Normandie 142 + Bretagne v0.2 151 OK")
'''
    (ROOT / "tests/test_pack_registry.py").write_text(registry_test, encoding="utf-8")

    # New immutable public release test.
    release_test = '''import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
RECORD = ROOT / "research/bretagne-v0.2/publication-record.json"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

with tempfile.TemporaryDirectory() as td:
    subprocess.run([sys.executable, str(ROOT / "tools/build_bretagne_v02_internal_candidate.py"), "--root", str(ROOT), "--output-dir", td], check=True)
    candidate = Path(td) / "bretagne-v0.2-internal.csv"
    assert PUBLIC.read_bytes() == candidate.read_bytes()

with PUBLIC.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 151
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert all(len(row["Name"]) <= 10 for row in rows)
assert len({row["Location"] for row in rows}) == 151
assert len({row["Name"] for row in rows}) == 151
assert len({round(float(row["Frequency"]), 6) for row in rows}) == 151
by_name = {row["Name"]: row for row in rows}
for name, freq in {"M64-S":156.225,"M64-C":160.825,"M79-S":156.975,"M79-C":161.575}.items():
    assert round(float(by_name[name]["Frequency"]), 6) == freq
    comment = by_name[name]["Comment"].lower()
    assert all(site not in comment for site in ["etel","corsen","fréhel","stiff","bodic"])
aviation = [row for row in rows if row["Name"].startswith(("AIR-", "RNS-", "BES-", "DIN-", "QUIM-"))]
assert len(aviation) == 16
assert all(row["Mode"] == "AM" and row["TStep"] == "8.33" for row in aviation)

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.2" and record["memory_count"] == 151
assert record["new_memory_count_vs_v0_1"] == 16
assert record["public_csv_sha256"] == hashlib.sha256(PUBLIC.read_bytes()).hexdigest()
assert record["published_version_is_immutable"] is True
assert record["aviation"]["cycle"] == "AIRAC 08/26"
assert record["aviation"]["valid_through_inclusive"] == "2026-09-02"
assert record["aviation"]["direct_xml_field_match_claimed"] is False
registry = REGISTRY.read_text(encoding="utf-8")
assert 'id: "bretagne"' in registry
assert 'memoryCount: 151' in registry
assert '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv' in registry
assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()
print("Bretagne v0.2 public release: immutable 151-memory RX-only CSV exactly matches frozen candidate OK")
'''
    (ROOT / "tests/test_bretagne_v02_public_release.py").write_text(release_test, encoding="utf-8")

    sprint80_test = '''import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/bretagne-v0.2/publication-record.json").read_text(encoding="utf-8"))
gates = json.loads((ROOT / "research/bretagne-v0.2/publication-gates.json").read_text(encoding="utf-8"))
assert state["current_sprint"] == 80
assert state["state_version"] == "0.21.69"
assert state["public_packs"]["bretagne"]["version"] == "0.2"
assert state["public_packs"]["bretagne"]["memory_count"] == 151
assert state["public_packs"]["bretagne"]["immutable"] is True
assert record["status"] == "published_immutable" and record["version"] == "0.2" and record["memory_count"] == 151
assert record["new_memory_count_vs_v0_1"] == 16
assert record["aviation"]["cycle"] == "AIRAC 08/26"
assert record["aviation"]["freshness_rechecked_on"] == "2026-08-12"
assert record["aviation"]["direct_xml_field_match_claimed"] is False
assert gates["status"] == "published_immutable_151"
assert next(g for g in gates["gates"] if g["id"] == "explicit_publication")["status"] == "passed_publication_completed_immutable"
assert (ROOT / record["public_csv"]).is_file()
assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()
print("Sprint 80: Bretagne v0.2 published immutable at 151 RX memories with AIRAC 08/26 boundary preserved OK")
'''
    (ROOT / "tests/test_sprint80_bretagne_v02_publication.py").write_text(sprint80_test, encoding="utf-8")

    # Site-files required list gains current v0.2 publication artifacts while retaining v0.1 history.
    site_test_path = ROOT / "tests/test_site_files.py"
    site_test = site_test_path.read_text(encoding="utf-8")
    site_test = replace_once(
        site_test,
        '    "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv",\n',
        '    "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv",\n    "research/bretagne-v0.2/publication-record.json",\n    "tests/test_bretagne_v02_public_release.py",\n    "tests/test_sprint80_bretagne_v02_publication.py",\n    "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",\n',
        "site files Bretagne v0.2 artifacts",
    )
    site_test_path.write_text(site_test, encoding="utf-8")

    # Project state.
    state["current_sprint"] = 80
    state["state_version"] = "0.21.69"
    state["public_packs"]["bretagne"] = {
        "version": "0.2",
        "memory_count": 151,
        "immutable": True,
        "research_only": False,
        "previous_immutable_version": "0.1",
        "previous_memory_count": 135,
    }
    active = state["active_work"]
    active["status"] = "published_immutable_151_airac08_scope"
    active["public_export_allowed"] = False
    active["public_registry_allowed"] = False
    active["public_release_ready"] = True
    active["published"] = True
    active["publication_sprint"] = 80
    active["published_on"] = "2026-08-12"
    active["publication_record"] = "research/bretagne-v0.2/publication-record.json"
    active["public_csv"] = record["public_csv"]
    active["public_csv_sha256"] = public_sha256
    for item in ("research/bretagne-v0.2/publication-record.json", "research/sprint-80-summary.md"):
        if item not in state["sources_of_truth"]:
            state["sources_of_truth"].append(item)
    state["field_tools"]["run_sprint80_test"] = "python tests/test_sprint80_bretagne_v02_publication.py"
    state["field_tools"]["run_bretagne_v02_public_release_test"] = "python tests/test_bretagne_v02_public_release.py"
    if not any(item.get("sprint") == 80 for item in state["recent_sprints"]):
        state["recent_sprints"].insert(0, {
            "sprint": 80,
            "state_version": "0.21.69",
            "summary": "Bretagne v0.2 published immutable at 151 RX memories; public CSV equals frozen candidate and AIRAC 08/26 freshness boundary is recorded.",
            "summary_file": "research/sprint-80-summary.md",
        })
    state["resume_rules"].update({
        "published_version_is_immutable": True,
        "publication_record_hash_must_match_public_csv": True,
        "historical_public_csv_must_be_retained": True,
        "airac_publication_freshness_boundary_must_be_recorded": True,
    })
    state["latest_sprint80_publication"] = {
        "file": "research/sprint-80-summary.md",
        "publication_record": "research/bretagne-v0.2/publication-record.json",
        "test": "tests/test_sprint80_bretagne_v02_publication.py",
        "public_release_test": "tests/test_bretagne_v02_public_release.py",
        "version": "0.2",
        "memory_count": 151,
        "new_memory_count_vs_v0_1": 16,
        "public_csv": record["public_csv"],
        "public_csv_sha256": public_sha256,
        "airac_cycle": "AIRAC 08/26",
        "airac_valid_through_inclusive": "2026-09-02",
        "published_on": "2026-08-12",
        "immutable": True,
    }
    write_json(ROOT / "research/project-resume-state.json", state)

    # Sprint summary.
    summary = f'''# Sprint 80 — publication Bretagne v0.2\n\nÉtat logique : **0.21.69**.\n\nBretagne v0.2 est publiée et immuable à **151 mémoires RX**. Le fichier public est la copie exacte du candidat gelé au Sprint 79 : base v0.1 de 135 mémoires + 16 mémoires aviation AIRAC 08/26.\n\n## Contrôles de publication\n\n- revue prépublication : **10/10**, **0 bloqueur** ;\n- contrôle SIA le 12 août 2026 : AIRAC 08/26 CORRIGENDUM toujours courant, valable du 6 août au 2 septembre 2026 inclus ;\n- aucune comparaison XML champ par champ n'est revendiquée sans extraction directe de l'XML ;\n- toutes les lignes restent RX-only (`Duplex=off`, `Offset=0.000000`) ;\n- aucune RF dupliquée ;\n- Ch64/Ch79 restent génériques sans site CROSS local non prouvé ;\n- aucune fréquence ADRASEC opérationnelle non publiée n'est intégrée.\n\n## Publication\n\n- CSV : `{record['public_csv']}` ;\n- mémoires : **151** ;\n- SHA-256 : `{public_sha256}` ;\n- record : `research/bretagne-v0.2/publication-record.json` ;\n- Bretagne v0.1 reste conservée comme publication historique immuable.\n\nLa bascule du registre et de la page Bretagne pointe maintenant vers v0.2.\n'''
    (ROOT / "research/sprint-80-summary.md").write_text(summary, encoding="utf-8")

    # README.
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = replace_once(
        readme,
        "**État courant : Sprint 79 / 0.21.68 — Bretagne v0.2 est figée à 151 mémoires RX, revue 10/10, 0 bloqueur, prépublication prête mais non publique.**",
        "**État courant : Sprint 80 / 0.21.69 — Bretagne v0.2 est publiée et immuable à 151 mémoires RX, avec 16 mémoires aviation AIRAC 08/26.**",
        "README current state",
    )
    readme = replace_once(readme, "## État actuel — Sprint 79 / 0.21.68", "## État actuel — Sprint 80 / 0.21.69", "README heading")
    readme = replace_once(readme, "- **Bretagne v0.1** — 135 mémoires RX, publiée et immuable.", "- **Bretagne v0.2** — 151 mémoires RX, publiée et immuable ;\n- Bretagne v0.1 — 135 mémoires RX, historique immuable.", "README public Bretagne")
    readme = replace_once(
        readme,
        "Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.2 est à **151 mémoires RX** : base publique v0.1=135 + 16 mémoires aviation AIRAC 08/26. Aucun CSV public Bretagne v0.2 n'existe et le registre public reste sur v0.1.",
        "Recherche : Normandie v0.5 reste à 142 mémoires, avec un plafond potentiel connu de **147 mémoires** hors F6ZES. Bretagne v0.2 est désormais **publique à 151 mémoires RX** : base historique v0.1=135 + 16 mémoires aviation AIRAC 08/26.",
        "README research paragraph",
    )
    readme = replace_once(readme, "`research/sprint-78-summary.md` et `research/sprint-79-summary.md`.", "`research/sprint-78-summary.md`, `research/sprint-79-summary.md` et `research/sprint-80-summary.md`.", "README resume files")
    section80 = f'''## Sprint 80 — publication Bretagne v0.2\n\nBretagne v0.2 est publiée et immuable à **151 mémoires RX**. Le CSV public correspond exactement au candidat gelé au Sprint 79 et son SHA-256 est enregistré dans `research/bretagne-v0.2/publication-record.json`.\n\n- 135 mémoires héritées de la v0.1 immuable + **16 aviation AIRAC 08/26** ;\n- cycle SIA recontrôlé le 12 août 2026, valable jusqu'au **2 septembre 2026 inclus** ;\n- RX-only, zéro doublon RF, aucun remplissage artificiel ;\n- aucune fréquence ADRASEC non publiée ni attribution locale CROSS non prouvée ;\n- la v0.1 reste disponible dans l'historique du dépôt mais le registre courant pointe vers v0.2.\n\nCSV : `website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv`  \nSHA-256 : `{public_sha256}`\n\nGarde-fous : `tests/test_bretagne_v02_public_release.py` et `tests/test_sprint80_bretagne_v02_publication.py`.\n\n'''
    readme = replace_once(readme, "## Sprint 79 — maturité et prépublication Bretagne v0.2\n", section80 + "## Sprint 79 — maturité et prépublication Bretagne v0.2\n", "README Sprint80 insertion")
    readme = replace_once(readme, "`research/sprint-61-summary.md` à `research/sprint-79-summary.md`", "`research/sprint-61-summary.md` à `research/sprint-80-summary.md`", "README history range")
    readme = replace_once(readme, "python tests\\test_sprint79_bretagne_v02_maturity.py\n", "python tests\\test_sprint79_bretagne_v02_maturity.py\npython tests\\test_bretagne_v02_public_release.py\npython tests\\test_sprint80_bretagne_v02_publication.py\n", "README test commands")
    readme = replace_once(readme, "python tools\\run_bretagne_v02_prepublication_audit.py --require-prepublication-ready\npython tests\\test_site_files.py", "python tools\\run_bretagne_v02_prepublication_audit.py --require-prepublication-ready\npython tests\\test_bretagne_v02_public_release.py\npython tests\\test_sprint80_bretagne_v02_publication.py\npython tests\\test_site_files.py", "README sync commands")
    readme_path.write_text(readme, encoding="utf-8")

    # PROJECT_STATUS.
    status_path = ROOT / "PROJECT_STATUS.md"
    status = status_path.read_text(encoding="utf-8")
    status = replace_once(status, "Sprint courant : **79**", "Sprint courant : **80**", "status sprint")
    status = replace_once(status, "État logique : **0.21.68**", "État logique : **0.21.69**", "status version")
    status = replace_once(status, "Résumé courant : `research/sprint-79-summary.md`.", "Résumé courant : `research/sprint-80-summary.md`.", "status summary")
    status = replace_once(status, "- Bretagne v0.1 : **135 mémoires RX**, publiée et immuable.\n- Bretagne v0.2 : aucune publication ; le registre public reste sur v0.1.", "- Bretagne v0.2 : **151 mémoires RX**, publiée et immuable.\n- Bretagne v0.1 : **135 mémoires RX**, publication historique immuable.", "status public Bretagne")
    status80 = f'''## Sprint 80 — Bretagne v0.2 publiée à 151\n\nLa publication explicite est terminée : le candidat gelé au Sprint 79 est devenu le CSV public Bretagne v0.2, **octet pour octet identique** au builder.\n\n- **151 mémoires RX**, dont 16 aviation AIRAC 08/26 ;\n- SHA-256 public : `{public_sha256}` ;\n- AIRAC 08/26 recontrôlé courant le 12 août 2026, valable jusqu'au 2 septembre 2026 inclus ;\n- registre et page Bretagne basculés sur v0.2 ;\n- v0.1 conservée comme historique immuable ;\n- dossiers F1ZUG, mappings CROSS et relais amateur arrêtés/non résolus restent reportés hors scope sans être inventés.\n\nTests : `tests/test_bretagne_v02_public_release.py` et `tests/test_sprint80_bretagne_v02_publication.py`.\n\n'''
    status = replace_once(status, "## Sprint 79 — scope v0.2 figé, prépublication prête\n", status80 + "## Sprint 79 — scope v0.2 figé, prépublication prête\n", "status Sprint80 insertion")
    status = replace_once(status, "python tests\\test_sprint79_bretagne_v02_maturity.py\n", "python tests\\test_sprint79_bretagne_v02_maturity.py\npython tests\\test_bretagne_v02_public_release.py\npython tests\\test_sprint80_bretagne_v02_publication.py\n", "status commands")
    status_path.write_text(status, encoding="utf-8")

    # Bretagne research README.
    bzh_path = RESEARCH / "README.md"
    bzh = bzh_path.read_text(encoding="utf-8")
    bzh = replace_once(bzh, "Bretagne v0.2 est la version de recherche active basée sur Bretagne v0.1 publiée et immuable (**135 mémoires RX**).", "Bretagne v0.2 est publiée et immuable à **151 mémoires RX**, construite depuis Bretagne v0.1 historique et immuable (**135 mémoires RX**) + 16 mémoires aviation AIRAC 08/26.", "Bretagne intro")
    bzh = replace_once(bzh, "## État Sprint 79 — prépublication prête", "## État Sprint 80 — publiée", "Bretagne heading")
    bzh = replace_once(bzh, "Aucun export public v0.2 n'existe et le registre public reste sur Bretagne v0.1.", "Le CSV public v0.2 et le registre sont désormais publiés ; Bretagne v0.1 reste conservée comme historique immuable.", "Bretagne state publication")
    publication_section = f'''### Publication Sprint 80\n\nLe CSV public `website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv` est la copie exacte du candidat figé à 151 mémoires. Son SHA-256 est `{public_sha256}`.\n\n`publication-record.json` enregistre l'empreinte, le cycle AIRAC 08/26, la fenêtre de validité jusqu'au 2 septembre 2026 inclus et les dossiers explicitement reportés après v0.2.\n\n'''
    bzh = replace_once(bzh, "### Aviation\n", publication_section + "### Aviation\n", "Bretagne publication section")
    bzh_path.write_text(bzh, encoding="utf-8")

    # CHANGELOG.
    changelog_path = ROOT / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    entry = f'''## 0.21.69 - 2026-08-12\n\n- **Sprint 80** : publication de Bretagne v0.2 à **151 mémoires RX**, désormais immuable.\n- CSV public généré directement depuis le candidat gelé au Sprint 79 ; SHA-256 `{public_sha256}` enregistré dans `publication-record.json`.\n- AIRAC 08/26 recontrôlé courant le 12 août 2026, valable jusqu'au 2 septembre 2026 inclus ; aucune comparaison XML champ par champ non effectuée n'est revendiquée.\n- Registre, générateur et page Bretagne basculés sur v0.2 ; Bretagne v0.1 reste conservée comme historique immuable.\n- Ajout des tests de publication v0.2 et adaptation forward-compatible des garde-fous Sprint 73/79.\n\n'''
    changelog = replace_once(changelog, "# Changelog\n\n", "# Changelog\n\n" + entry, "changelog Sprint80")
    changelog_path.write_text(changelog, encoding="utf-8")

    print(f"Sprint 80 Bretagne v0.2 publication prepared: 151 RX, sha256={public_sha256}")


if __name__ == "__main__":
    main()
