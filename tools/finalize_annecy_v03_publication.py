#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_annecy_v03_release_candidate as release  # noqa: E402

VERSION = "0.3"
SPRINT = 88
STATE_VERSION = "0.21.77"
TODAY = "2026-08-15"
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.3"
PUBLIC_DIR = ROOT / "website/public/downloads/annecy-alpes-leman"
FULL_NAME = "radiopack-france-annecy-alpes-leman-v0.3.csv"
NO_AIR_NAME = "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Anchor absent dans {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before(path: Path, anchor: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if block.strip() in text:
        return
    if anchor not in text:
        raise RuntimeError(f"Anchor absent dans {path}: {anchor!r}")
    path.write_text(text.replace(anchor, block + anchor, 1), encoding="utf-8")


# 1) Deterministic frozen release build.
with tempfile.TemporaryDirectory(prefix="radiopack-annecy-v03-publication-") as td:
    out = Path(td)
    manifest = release.build_release(ROOT, out)
    if manifest["full_memory_count"] != 76 or manifest["without_aviation_memory_count"] != 59:
        raise RuntimeError("Annecy v0.3 release builder count mismatch")
    if manifest["publication_blocker_count"] != 0:
        raise RuntimeError("Annecy v0.3 still has publication blockers")

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    full_public = PUBLIC_DIR / FULL_NAME
    no_air_public = PUBLIC_DIR / NO_AIR_NAME
    shutil.copyfile(out / FULL_NAME, full_public)
    shutil.copyfile(out / NO_AIR_NAME, no_air_public)
    shutil.copyfile(out / release.REVIEW_MAP_FILENAME, RESEARCH / "prepublication-reviewed-memory-map.json")

full_public = PUBLIC_DIR / FULL_NAME
no_air_public = PUBLIC_DIR / NO_AIR_NAME
full_sha = sha256(full_public)
no_air_sha = sha256(no_air_public)
review_map_path = RESEARCH / "prepublication-reviewed-memory-map.json"
review_map_sha = sha256(review_map_path)

# 2) Immutable publication record.
publication_record = {
    "schema_version": "1.0",
    "status": "published_immutable",
    "pack": "Annecy–Alpes–Léman",
    "version": VERSION,
    "published_on": TODAY,
    "based_on_public_version": "0.2",
    "full_memory_count": 76,
    "without_aviation_memory_count": 59,
    "aviation_memory_count": 17,
    "new_unique_rf_memory_count": 11,
    "public_files": {
        "full": {
            "path": f"website/public/downloads/annecy-alpes-leman/{FULL_NAME}",
            "sha256": full_sha,
        },
        "without_aviation": {
            "path": f"website/public/downloads/annecy-alpes-leman/{NO_AIR_NAME}",
            "sha256": no_air_sha,
        },
    },
    "review_map": {
        "path": "research/annecy-alpes-leman-v0.3/prepublication-reviewed-memory-map.json",
        "sha256": review_map_sha,
    },
    "evidence": {
        "paired_rx_expansion": "research/annecy-alpes-leman-v0.3/paired-rx-expansion.json",
        "current_source_revalidation": "research/annecy-alpes-leman-v0.3/current-source-revalidation.json",
        "release_scope": "research/annecy-alpes-leman-v0.3/release-scope.json",
        "review_checklist": "research/annecy-alpes-leman-v0.3/review-checklist.json",
        "release_builder": "tools/build_annecy_v03_release_candidate.py",
    },
    "documented_exclusions": [
        {
            "id": "F1ZTH_50M_DEVICE_COMPATIBILITY",
            "frequency_mhz": 50.5375,
            "reason": "Public RF, but not guaranteed by the project-wide UV-K5/firmware receive baseline; excluded from v0.3.",
        },
        {
            "id": "F1ZJV_F1ZYT_ADRASEC_UHF_TRANSPONDER",
            "frequency_mhz": None,
            "reason": "No usable public RF published; no private or inferred operational frequency included.",
        },
    ],
    "rules": {
        "immutable": True,
        "rx_only": True,
        "chirp_duplex": "off",
        "chirp_offset": "0.000000",
        "same_rf_frequency_deduplicated": True,
        "no_artificial_fill": True,
        "private_professional_or_ppdr_frequencies_excluded": True,
        "unpublished_adrasec_frequency_inferred": False,
        "published_v0_2_remains_immutable": True,
    },
}
(RESEARCH / "publication-record.json").write_text(
    json.dumps(publication_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

# 3) Pack plan becomes a publication record pointer while preserving research history.
plan_path = RESEARCH / "pack-plan.json"
plan = json.loads(plan_path.read_text(encoding="utf-8"))
plan["status"] = "published_immutable_v0_3"
plan["updated"] = TODAY
plan["memory_plan"]["status"] = "published_frozen_76_59"
plan["publication"].update({
    "public_export_allowed": True,
    "public_registry_allowed": True,
    "public_routes_allowed": True,
    "review_required": True,
    "review_completed": True,
    "scope_frozen": True,
    "prepublication_ready": True,
    "published": True,
    "publication_record": "research/annecy-alpes-leman-v0.3/publication-record.json",
})
plan["latest_publication"] = {
    "sprint": SPRINT,
    "published_on": TODAY,
    "version": VERSION,
    "full_memory_count": 76,
    "without_aviation_memory_count": 59,
    "new_unique_rf_memory_count": 11,
    "full_sha256": full_sha,
    "without_aviation_sha256": no_air_sha,
}
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 4) Public registry points to immutable static v0.3 CSVs. Historical v0.2 routes stay untouched.
registry = '''export type PublicPackVariant = {
  id: string;
  label: string;
  memoryCount: number;
  filename: string;
  downloadUrl: string;
  aviationIncluded?: boolean;
};

export type PublicPack = {
  id: string;
  regionSlug: string;
  name: string;
  version: string;
  status: string;
  description: string;
  defaultVariant: string;
  aviationToggle?: {
    includedVariant: string;
    excludedVariant: string;
    memoryCount: number;
  };
  notamCheck: boolean;
  variants: PublicPackVariant[];
};

export const publicPacks: PublicPack[] = [
  {
    id: "annecy-alpes-leman",
    regionSlug: "annecy-haute-savoie",
    name: "Annecy–Alpes–Léman",
    version: "v0.3",
    status: "Disponible",
    description: "Pack Alpes du Nord / bassin lémanique v0.3 avec paired RX et variante sans aviation.",
    defaultVariant: "full",
    aviationToggle: {
      includedVariant: "full",
      excludedVariant: "no-aviation",
      memoryCount: 17,
    },
    notamCheck: true,
    variants: [
      {
        id: "full",
        label: "Version complète",
        memoryCount: 76,
        filename: "radiopack-france-annecy-alpes-leman-v0.3.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv",
        aviationIncluded: true,
      },
      {
        id: "no-aviation",
        label: "Sans aviation",
        memoryCount: 59,
        filename: "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv",
        downloadUrl: "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv",
        aviationIncluded: false,
      },
    ],
  },
  {
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
  },
  {
    id: "normandie",
    regionSlug: "normandie",
    name: "Normandie",
    version: "v0.4",
    status: "Disponible",
    description: "Pack régional Normandie v0.4 de 142 mémoires RX, publié en réception seule.",
    defaultVariant: "standard",
    notamCheck: false,
    variants: [
      {
        id: "standard",
        label: "Pack complet",
        memoryCount: 142,
        filename: "radiopack-france-normandie-v0.4.csv",
        downloadUrl: "/downloads/normandie/radiopack-france-normandie-v0.4.csv",
      },
    ],
  },
];

export const defaultPublicPackId = "annecy-alpes-leman";

export const getPublicPack = (packId: string) =>
  publicPacks.find((pack) => pack.id === packId);

export const getPublicVariant = (pack: PublicPack, variantId: string) =>
  pack.variants.find((variant) => variant.id === variantId);
'''
(ROOT / "website/src/lib/packRegistry.ts").write_text(registry, encoding="utf-8")

# 5) Generator metadata and public copy.
options_path = ROOT / "generator/options.json"
options = json.loads(options_path.read_text(encoding="utf-8"))
options["updated"] = TODAY
annecy = next(item for item in options["pack_selection"]["packs"] if item["id"] == "annecy-alpes-leman")
annecy["version"] = "v0.3"
annecy["default_memory_count"] = 76
annecy["optional_memory_count"] = 59
options["options"]["include_aviation"]["annecy_memory_count_when_enabled"] = 76
options["options"]["include_aviation"]["annecy_memory_count_when_disabled"] = 59
options_path.write_text(json.dumps(options, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

generator = ROOT / "website/src/pages/generateur.astro"
text = generator.read_text(encoding="utf-8")
text = text.replace("variante complète 65 mémoires ou la variante 48 sans aviation", "variante complète 76 mémoires ou la variante 59 sans aviation")
text = text.replace("Annecy · 65 / 48", "Annecy · 76 / 59")
generator.write_text(text, encoding="utf-8")

# 6) Region page rewritten for the finished release.
region_page = '''---
import BaseLayout from "../../layouts/BaseLayout.astro";
---

<BaseLayout
  title="Annecy–Alpes–Léman v0.3 — RadioPack France"
  description="Pack RX-only Annecy–Alpes–Léman v0.3 : 76 mémoires France–Suisse, avec variante 59 mémoires sans aviation."
>
  <section class="section">
    <div class="container page-grid">
      <div class="copy">
        <span class="eyebrow">Disponible — v0.3</span>
        <h1>Annecy–Alpes–<br /><span class="gradient-text">Léman</span></h1>
        <p class="lead">
          La v0.3 publie 76 mémoires RX et applique la politique paired RX aux satellites split,
          relais analogiques et transpondeurs sélectionnés, sans dupliquer une même fréquence RF.
        </p>

        <div class="button-row">
          <a class="button button-primary" href="/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv" download>Télécharger le CSV v0.3</a>
          <a class="button button-orange" href="/generateur">Personnaliser le pack</a>
          <a class="button button-secondary" href="/documentation">Méthode et sécurité</a>
        </div>

        <div class="card release-note">
          <strong>76 mémoires avec aviation · 59 sans aviation</strong>
          <p>La variante sans aviation retire uniquement les 17 mémoires aviation. Toutes les mémoires restent RX-only avec <code>Duplex=off</code> et <code>Offset=0.000000</code>.</p>
        </div>

        <div class="card scope">
          <h2>Contenu publié</h2>
          <div class="scope-grid">
            <div><span class="badge">National</span><p>16 PMR446 et le socle APRS / ISS / appels.</p></div>
            <div><span class="badge badge-green">Espace</span><p>13 mémoires APRS, ISS, satellites FM et montées split RX dédupliquées.</p></div>
            <div><span class="badge badge-orange">Radioamateur</span><p>30 mémoires France/Suisse, dont les deux côtés RX des relais et transpondeurs retenus.</p></div>
            <div><span class="badge">Aviation</span><p>17 mémoires AIRAC courantes au 15 août 2026.</p></div>
          </div>
        </div>

        <div class="work-grid grid-2">
          <article class="card"><span class="badge badge-green">16</span><h3>PMR446</h3><p>Les 16 canaux analogiques en écoute RX.</p></article>
          <article class="card"><span class="badge">13</span><h3>APRS / espace / appels</h3><p>APRS/ISS, satellites FM et montées split RX.</p></article>
          <article class="card"><span class="badge badge-orange">30</span><h3>Radioamateur</h3><p>France et Suisse avec paired RX et déduplication.</p></article>
          <article class="card"><span class="badge badge-green">17</span><h3>Aviation</h3><p>France/bassin genevois et Suisse, cycle courant lors de la publication.</p></article>
        </div>

        <div class="card conflict">
          <h2>Exclusions documentées</h2>
          <p>
            F1ZTH 50.5375 MHz reste hors v0.3 car RadioPack ne garantit pas encore une baseline UV-K5/firmware commune pour le 50 MHz.
            La liaison UHF ADRASEC évoquée pour F1ZJV/F1ZYT n'est pas ajoutée : aucune fréquence publique exploitable n'est publiée et aucune donnée opérationnelle privée n'est inférée.
            Les omissions aviation déjà documentées de la v0.2 ne sont pas comblées par des sources secondaires non validées.
          </p>
        </div>
      </div>

      <aside class="card status-card">
        <span class="badge badge-green">Publié</span>
        <h3>Version v0.3</h3>
        <div class="memory-count"><strong>76</strong><span>mémoires RX</span></div>
        <p class="status-copy">Revue 12/12, zéro bloqueur, +11 RF uniques par rapport à la v0.2. Variante 59 mémoires sans aviation.</p>
        <hr />
        <h4>Contrôles</h4>
        <ul>
          <li>Sources radioamateur courantes : validées</li>
          <li>Satellites AMSAT : recontrôlés</li>
          <li>AIRAC France/Suisse : courant à la publication</li>
          <li>Déduplication RF : validée</li>
        </ul>
        <hr />
        <h4>Règles permanentes</h4>
        <ul>
          <li>Réception seule avec <code>Duplex=off</code></li>
          <li>Noms ≤ 10 caractères</li>
          <li>Aucun doublon RF pour gonfler le total</li>
          <li>Aucune fréquence privée ou devinée</li>
        </ul>
      </aside>
    </div>
  </section>
</BaseLayout>

<style>
  .page-grid { display: grid; grid-template-columns: 1.25fr .75fr; gap: 30px; align-items: start; }
  .copy { display: grid; gap: 22px; }
  .copy h1 { font-size: clamp(3.2rem, 7vw, 5.6rem); }
  .release-note, .scope, .conflict { padding: 24px; }
  .release-note { background: linear-gradient(120deg, rgba(16,164,122,.13), rgba(255,255,255,.84)); }
  .release-note p, .scope p, .conflict p, .work-grid p, .status-copy { margin-top: 7px; color: var(--muted); }
  .scope { background: linear-gradient(145deg, rgba(255,255,255,.92), rgba(230,247,252,.82)); }
  .scope h2, .conflict h2 { margin-bottom: 16px; }
  .scope-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .scope-grid > div { padding: 18px; border: 1px solid var(--line); border-radius: 16px; background: rgba(255,255,255,.68); }
  .work-grid article { padding: 22px; }
  .work-grid h3 { margin: 14px 0 7px; }
  .conflict { background: linear-gradient(120deg, rgba(110,61,232,.10), rgba(255,255,255,.84)); }
  .status-card { position: sticky; top: 110px; padding: 28px; }
  .status-card h3 { margin: 18px 0 10px; }
  .status-card h4 { margin: 20px 0 8px; }
  .status-card ul { margin: 0; padding-left: 1.2rem; color: var(--muted); }
  .status-card hr { border: 0; border-top: 1px solid var(--line); margin: 22px 0 0; }
  .memory-count { display: flex; align-items: baseline; gap: 10px; margin-bottom: 14px; }
  .memory-count strong { font-family: "Space Grotesk", sans-serif; font-size: 4rem; line-height: .9; }
  .memory-count span { color: var(--muted); font-weight: 800; }
  code { font-weight: 800; color: #007c8a; }
  @media (max-width: 800px) { .page-grid, .scope-grid { grid-template-columns: 1fr; } .status-card { position: static; } }
</style>
'''
(ROOT / "website/src/pages/regions/annecy-haute-savoie.astro").write_text(region_page, encoding="utf-8")

# 7) Final Annecy README.
annecy_readme = f'''# Annecy–Alpes–Léman v0.3 — publiée

État : **Sprint {SPRINT} / {STATE_VERSION} — v0.3 publiée et immuable à 76 mémoires RX, 59 sans aviation**.

La v0.3 part de la v0.2 publique immuable (65 / 48) et ajoute **11 fréquences RF uniques** selon la politique paired RX. Les deux CSV publics sont générés par `tools/build_annecy_v03_release_candidate.py`, contrôlés par la CI puis figés par SHA-256 dans `publication-record.json`.

## Résultat

- version complète : **76 RX** ;
- sans aviation : **59 RX** ;
- aviation : **17 RX** ;
- delta v0.2 → v0.3 : **+11 RF uniques** ;
- émission désactivée : `Duplex=off`, `Offset=0.000000` ;
- aucune fréquence privée, PPDR ou ADRASEC opérationnelle non publiée ;
- aucune duplication d'une RF uniquement pour multiplier les sites ou rôles.

## Ajouts v0.3

- satellites split : 145.850 MHz (SO-50/AO-123, une seule mémoire) et 435.250 MHz (AO-91) ;
- relais France : 439.625, 145.0375, 145.050, 430.325, 431.425 MHz ;
- Haute-Savoie : 145.1875 / 145.7875 MHz pour la paire analogique publique F1ZJV/F1ZYT ;
- HB9G : 145.125 et 431.500 MHz en complément des sorties déjà présentes.

## Exclusions fermées pour cette version

- F1ZTH **50.5375 MHz** : fréquence publique mais hors v0.3 tant qu'une baseline UV-K5/firmware commune ne garantit pas le 50 MHz ;
- liaison UHF ADRASEC F1ZJV/F1ZYT : fréquence non publique, donc non recherchée dans des données privées et non inférée ;
- omissions aviation antérieures : pas de remplissage par source secondaire non vérifiée.

Sources de vérité : `paired-rx-expansion.json`, `current-source-revalidation.json`, `release-scope.json`, `review-checklist.json`, `prepublication-reviewed-memory-map.json` et `publication-record.json`.
'''
(RESEARCH / "README.md").write_text(annecy_readme, encoding="utf-8")

# 8) Project machine state.
state_path = ROOT / "research/project-resume-state.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
state["updated"] = TODAY
state["current_sprint"] = SPRINT
state["state_version"] = STATE_VERSION
annecy_public = state["public_packs"]["annecy_alpes_leman"]
annecy_public.clear()
annecy_public.update({
    "version": "0.3",
    "memory_count": 76,
    "without_aviation_memory_count": 59,
    "immutable": True,
    "previous_immutable_version": "0.2",
    "previous_memory_count": 65,
    "previous_without_aviation_memory_count": 48,
    "publication_record": "research/annecy-alpes-leman-v0.3/publication-record.json",
})
state["active_work"] = {
    "pack": "Annecy–Alpes–Léman",
    "target_version": "0.3",
    "status": "published_immutable_v0_3_complete",
    "published_base_version": "0.2",
    "published_base_memory_count": 65,
    "published_base_without_aviation_memory_count": 48,
    "published_base_is_immutable": True,
    "public_version": "0.3",
    "public_memory_count": 76,
    "public_without_aviation_memory_count": 59,
    "new_unique_rf_memory_count": 11,
    "aviation_memory_count": 17,
    "review_completed": True,
    "review_completed_count": 12,
    "review_total_count": 12,
    "publication_blocker_count": 0,
    "scope_frozen": True,
    "prepublication_ready": True,
    "public_export_allowed": True,
    "public_registry_allowed": True,
    "public_routes_allowed": True,
    "public_release_ready": True,
    "published": True,
    "full_sha256": full_sha,
    "without_aviation_sha256": no_air_sha,
    "publication_record": "research/annecy-alpes-leman-v0.3/publication-record.json",
    "release_scope": "research/annecy-alpes-leman-v0.3/release-scope.json",
    "review_checklist": "research/annecy-alpes-leman-v0.3/review-checklist.json",
    "current_source_revalidation": "research/annecy-alpes-leman-v0.3/current-source-revalidation.json",
    "f1zth_50m_frequency_mhz": 50.5375,
    "f1zth_50m_promoted": False,
    "f1zth_50m_scope_excluded": True,
    "unpublished_adrasec_frequency_inferred": False,
}
state["latest_sprint87_annecy_v0_3_prepublication"] = {
    "sprint": 87,
    "state_version": "0.21.76",
    "review": "12/12",
    "blocker_count": 0,
    "full_memory_count": 76,
    "without_aviation_memory_count": 59,
    "scope_frozen": True,
}
state["latest_sprint88_annecy_v0_3_publication"] = {
    "sprint": 88,
    "state_version": STATE_VERSION,
    "published_on": TODAY,
    "version": "0.3",
    "full_memory_count": 76,
    "without_aviation_memory_count": 59,
    "new_unique_rf_memory_count": 11,
    "full_sha256": full_sha,
    "without_aviation_sha256": no_air_sha,
    "immutable": True,
}
for item in [
    "research/annecy-alpes-leman-v0.3/current-source-revalidation.json",
    "research/annecy-alpes-leman-v0.3/release-scope.json",
    "research/annecy-alpes-leman-v0.3/review-checklist.json",
    "research/annecy-alpes-leman-v0.3/prepublication-reviewed-memory-map.json",
    "research/annecy-alpes-leman-v0.3/publication-record.json",
    "research/sprint-87-summary.md",
    "research/sprint-88-summary.md",
]:
    if item not in state.setdefault("sources_of_truth", []):
        state["sources_of_truth"].append(item)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 9) Sprint summaries.
(RESEARCH.parent / "sprint-87-summary.md").write_text(f'''# Sprint 87 — prépublication Annecy–Alpes–Léman v0.3

État logique : **0.21.76**.

Le périmètre v0.3 est figé à **76 mémoires RX / 59 sans aviation**, soit **+11 RF uniques** par rapport à la v0.2. La revalidation des sources courantes, le cycle AIRAC, les satellites, la déduplication et les exclusions ont été revus avant publication.

Checklist : **12/12**, bloqueurs : **0**. F1ZTH 50.5375 MHz est une exclusion de scope documentée, pas une fréquence devinée ni un bloqueur. La liaison UHF ADRASEC non publiée n'est pas inférée.

Le builder `tools/build_annecy_v03_release_candidate.py` reproduit les deux variantes et le plan de revue ligne par ligne avant toute copie publique.
''', encoding="utf-8")

(RESEARCH.parent / "sprint-88-summary.md").write_text(f'''# Sprint 88 — publication Annecy–Alpes–Léman v0.3

État logique : **{STATE_VERSION}**.

Annecy–Alpes–Léman **v0.3 est publiée et immuable** :

- complète : **76 mémoires RX** ;
- sans aviation : **59 mémoires RX** ;
- aviation : **17 mémoires** ;
- delta v0.2 → v0.3 : **+11 RF uniques** ;
- SHA-256 complet : `{full_sha}` ;
- SHA-256 sans aviation : `{no_air_sha}`.

Le registre public, le générateur et la page régionale pointent vers v0.3. La v0.2 reste dans l'historique et n'est pas modifiée.

Exclusions explicites : F1ZTH 50.5375 MHz tant que la baseline UV-K5/firmware 50 MHz n'est pas garantie ; aucune fréquence UHF ADRASEC non publiée n'est inférée.

La publication est RX-only, dédupliquée et sans remplissage artificiel. `publication-record.json` est la preuve immuable des deux CSV publics.
''', encoding="utf-8")

# 10) Public release test.
release_test = r'''import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.3"
RECORD = RESEARCH / "publication-record.json"
SCOPE = RESEARCH / "release-scope.json"
REVIEW = RESEARCH / "review-checklist.json"
MAP = RESEARCH / "prepublication-reviewed-memory-map.json"
FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
PAGE = ROOT / "website/src/pages/regions/annecy-haute-savoie.astro"
OLD_FULL_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
OLD_NO_AIR_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts"

for path in [RECORD, SCOPE, REVIEW, MAP, FULL, NO_AIR, REGISTRY, PAGE, OLD_FULL_ROUTE, OLD_NO_AIR_ROUTE]:
    assert path.is_file(), f"Missing Annecy v0.3 publication file: {path.relative_to(ROOT)}"

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.3"
assert record["full_memory_count"] == 76
assert record["without_aviation_memory_count"] == 59
assert record["aviation_memory_count"] == 17
assert record["new_unique_rf_memory_count"] == 11
assert record["rules"]["immutable"] is True
assert record["rules"]["rx_only"] is True
assert record["rules"]["unpublished_adrasec_frequency_inferred"] is False

assert hashlib.sha256(FULL.read_bytes()).hexdigest() == record["public_files"]["full"]["sha256"]
assert hashlib.sha256(NO_AIR.read_bytes()).hexdigest() == record["public_files"]["without_aviation"]["sha256"]
assert hashlib.sha256(MAP.read_bytes()).hexdigest() == record["review_map"]["sha256"]


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

full_rows = rows(FULL)
no_air_rows = rows(NO_AIR)
assert len(full_rows) == 76
assert len(no_air_rows) == 59
for data, count in [(full_rows, 76), (no_air_rows, 59)]:
    assert all(row["Duplex"] == "off" for row in data)
    assert all(row["Offset"] == "0.000000" for row in data)
    assert all(row["Tone"] == "" and row["Power"] == "" for row in data)
    assert all(len(row["Name"]) <= 10 for row in data)
    assert len({row["Location"] for row in data}) == count
    assert len({row["Name"] for row in data}) == count
    assert len({row["Frequency"] for row in data}) == count
    assert "50.537500" not in {row["Frequency"] for row in data}

expected_new = {
    "145.850000", "435.250000", "439.625000", "145.037500", "145.050000",
    "430.325000", "431.425000", "145.187500", "145.787500", "145.125000", "431.500000",
}
assert expected_new.issubset({row["Frequency"] for row in full_rows})
assert expected_new.issubset({row["Frequency"] for row in no_air_rows})

review_map = json.loads(MAP.read_text(encoding="utf-8"))
assert review_map["expected_memory_count"] == 76
assert review_map["expected_memory_count_without_aviation"] == 59
assert len(review_map["rows"]) == 76

scope = json.loads(SCOPE.read_text(encoding="utf-8"))
review = json.loads(REVIEW.read_text(encoding="utf-8"))
assert scope["publication_blocker_count"] == 0
assert review["completed"] == review["total"] == 12
assert review["blocker_count"] == 0

registry = REGISTRY.read_text(encoding="utf-8")
assert 'version: "v0.3"' in registry
assert 'memoryCount: 76' in registry
assert 'memoryCount: 59' in registry
assert '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv' in registry
assert '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv' in registry

page = PAGE.read_text(encoding="utf-8")
for expected in ["Disponible — v0.3", "76 mémoires avec aviation", "59 sans aviation", "F1ZTH", "50.5375"]:
    assert expected in page

print("Annecy–Alpes–Léman v0.3 public release: 76/59 immutable RX, +11 RF, hashes and registry OK")
'''
(ROOT / "tests/test_annecy_v03_public_release.py").write_text(release_test, encoding="utf-8")

# 11) Built public CSV test now validates the static immutable v0.3 release.
built_test = r'''import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website/dist/downloads/annecy-alpes-leman"
REVIEW_MAP = ROOT / "research/annecy-alpes-leman-v0.3/prepublication-reviewed-memory-map.json"
RECORD = ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json"
STANDARD = DIST / "radiopack-france-annecy-alpes-leman-v0.3.csv"
NO_AVIATION = DIST / "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"

for path in [STANDARD, NO_AVIATION, REVIEW_MAP, RECORD]:
    assert path.is_file(), f"Artefact public manquant après build: {path.relative_to(ROOT)}"

review = json.loads(REVIEW_MAP.read_text(encoding="utf-8"))
schema = review["schema"]
reviewed_rows = [dict(zip(schema, row)) for row in review["rows"]]
assert len(reviewed_rows) == 76
AVIATION_BLOCKS = {"Aviation France et bassin genevois", "Aviation Suisse"}
reviewed_no_aviation = [row for row in reviewed_rows if row["block"] not in AVIATION_BLOCKS]
assert len(reviewed_no_aviation) == 59


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(rows, expected_rows):
    assert len(rows) == len(expected_rows)
    assert len({row["Location"] for row in rows}) == len(rows)
    assert len({row["Name"] for row in rows}) == len(rows)
    assert len({row["Frequency"] for row in rows}) == len(rows)
    for actual, expected in zip(rows, expected_rows):
        assert actual["Location"] == str(expected["location"])
        assert actual["Name"] == expected["name"]
        assert actual["Frequency"] == f"{float(expected['frequency_mhz']):.6f}"
        assert actual["Mode"] == expected["mode"]
        assert actual["TStep"] == f"{float(expected['step_khz']):.2f}"
        assert actual["Duplex"] == "off"
        assert actual["Offset"] == "0.000000"
        assert actual["Tone"] == ""
        assert actual["Power"] == ""
        assert len(actual["Name"]) <= 10
        assert hashlib.sha256(actual["Comment"].encode("utf-8")).hexdigest() == expected["comment_sha256"]

standard_rows = read_rows(STANDARD)
no_aviation_rows = read_rows(NO_AVIATION)
validate(standard_rows, reviewed_rows)
validate(no_aviation_rows, reviewed_no_aviation)

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert hashlib.sha256(STANDARD.read_bytes()).hexdigest() == record["public_files"]["full"]["sha256"]
assert hashlib.sha256(NO_AVIATION.read_bytes()).hexdigest() == record["public_files"]["without_aviation"]["sha256"]
print("Tests built Annecy–Alpes–Léman public CSV: v0.3 76/76 + 59/59 OK")
'''
(ROOT / "tests/test_built_annecy_public_csv.py").write_text(built_test, encoding="utf-8")

# 12) Registry/catalog tests updated for the new current version.
registry_test = r'''import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
GENERATOR = ROOT / "website/src/pages/generateur.astro"
REGIONS = ROOT / "website/src/data/regions.json"
ANNECY_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
ANNECY_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
NORMANDIE = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
BRETAGNE = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
for path in [REGISTRY, GENERATOR, REGIONS, ANNECY_FULL, ANNECY_NO_AIR, NORMANDIE, BRETAGNE]:
    assert path.is_file(), f"Fichier multi-régions manquant: {path.relative_to(ROOT)}"

registry = REGISTRY.read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"', 'regionSlug: "annecy-haute-savoie"', 'name: "Annecy–Alpes–Léman"',
    'version: "v0.3"', 'defaultVariant: "full"', 'includedVariant: "full"', 'excludedVariant: "no-aviation"',
    'memoryCount: 76', 'memoryCount: 59', 'id: "normandie"', 'regionSlug: "normandie"', 'version: "v0.4"',
    'memoryCount: 142', '/downloads/normandie/radiopack-france-normandie-v0.4.csv',
    'id: "bretagne"', 'regionSlug: "bretagne"', 'memoryCount: 151',
    '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv',
    'export const defaultPublicPackId = "annecy-alpes-leman"', "export const getPublicPack", "export const getPublicVariant",
]:
    assert expected in registry
assert registry.count('downloadUrl: "') == 4

page = GENERATOR.read_text(encoding="utf-8")
for expected in ["Normandie · 142", "Bretagne · 151", "Annecy · 76 / 59", "publicPacks.find((pack) => pack.id === selectedId)"]:
    assert expected in page

for path, expected_count in [(ANNECY_FULL, 76), (ANNECY_NO_AIR, 59), (NORMANDIE, 142), (BRETAGNE, 151)]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count

print("Tests RadioPack public pack registry: Annecy v0.3 76/59 + Normandie 142 + Bretagne 151 OK")
'''
(ROOT / "tests/test_pack_registry.py").write_text(registry_test, encoding="utf-8")

catalog_test = r'''import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website/dist/downloads"
EXPECTED = {
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv": 76,
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv": 59,
    DIST / "normandie/radiopack-france-normandie-v0.4.csv": 142,
    DIST / "bretagne/radiopack-france-bretagne-v0.2.csv": 151,
}
for path, expected_count in EXPECTED.items():
    assert path.is_file(), f"CSV public absent du build Astro: {path.relative_to(ROOT)}"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    assert all(len(row["Name"]) <= 10 for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count
print("Tests built public pack catalog: Annecy v0.3 76/59 + Normandie 142 + Bretagne v0.2 151 OK")
'''
(ROOT / "tests/test_built_public_pack_catalog.py").write_text(catalog_test, encoding="utf-8")

# 13) Forward-compatible Sprint 86/87 guards after explicit publication.
s86 = ROOT / "tests/test_sprint86_annecy_v03_paired_rx_expansion.py"
text = s86.read_text(encoding="utf-8")
old = '''registry = REGISTRY.read_text(encoding="utf-8")\nassert "radiopack-france-annecy-alpes-leman-v0.2.csv" in registry\nassert "radiopack-france-annecy-alpes-leman-v0.3.csv" not in registry\n'''
new = '''registry = REGISTRY.read_text(encoding="utf-8")\nassert "radiopack-france-annecy-alpes-leman-v0.2.csv" in (ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts").read_text(encoding="utf-8")\npublication_record = ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json"\nif publication_record.exists():\n    assert "radiopack-france-annecy-alpes-leman-v0.3.csv" in registry\nelse:\n    assert "radiopack-france-annecy-alpes-leman-v0.3.csv" not in registry\n'''
if old not in text:
    raise RuntimeError("Sprint 86 registry anchor missing")
s86.write_text(text.replace(old, new, 1), encoding="utf-8")

s87 = ROOT / "tests/test_sprint87_annecy_v03_prepublication.py"
text = s87.read_text(encoding="utf-8")
old = '''# Sprint 87 itself must not publish; explicit publication is a separate guarded step.\nassert not PUBLIC_FULL.exists()\nassert not PUBLIC_NO_AIR.exists()\n\nprint("Sprint 87 Annecy v0.3 prepublication: frozen 76/59, +11 RF, 12/12 review, blockers=0, no public mutation OK")\n'''
new = '''# Sprint 87 is prepublication-only; a later explicit publication may make these files exist.\nif PUBLIC_FULL.exists() or PUBLIC_NO_AIR.exists():\n    assert PUBLIC_FULL.is_file() and PUBLIC_NO_AIR.is_file()\n    record = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json").read_text(encoding="utf-8"))\n    assert record["status"] == "published_immutable"\n    assert record["full_memory_count"] == 76 and record["without_aviation_memory_count"] == 59\n\nprint("Sprint 87 Annecy v0.3 prepublication: frozen 76/59, +11 RF, 12/12 review, blockers=0 OK")\n'''
if old not in text:
    raise RuntimeError("Sprint 87 publication anchor missing")
s87.write_text(text.replace(old, new, 1), encoding="utf-8")

# 14) Existing generator regression guard now expects v0.3 public metadata but keeps v0.2 legacy library checks.
web_test = ROOT / "tests/test_web_generator.py"
text = web_test.read_text(encoding="utf-8")
text = text.replace('"Annecy · 65 / 48",', '"Annecy · 76 / 59",')
text = text.replace("    'memoryCount: 65',\n    'memoryCount: 48',", "    'memoryCount: 76',\n    'memoryCount: 59',")
text = text.replace("/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv", "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv")
text = text.replace("/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv", "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv")
text = text.replace("Annecy 65/48 OK", "Annecy v0.3 76/59 OK")
web_test.write_text(text, encoding="utf-8")

# 15) Repository-wide file guard: add new permanent publication files and update current README token.
site_test = ROOT / "tests/test_site_files.py"
insert_before(
    site_test,
    '    "tests/test_normandie_v04_public_release.py",\n',
    '    "research/annecy-alpes-leman-v0.3/current-source-revalidation.json",\n'
    '    "research/annecy-alpes-leman-v0.3/release-scope.json",\n'
    '    "research/annecy-alpes-leman-v0.3/review-checklist.json",\n'
    '    "research/annecy-alpes-leman-v0.3/prepublication-reviewed-memory-map.json",\n'
    '    "research/annecy-alpes-leman-v0.3/publication-record.json",\n'
    '    "tools/build_annecy_v03_release_candidate.py",\n'
    '    "tests/test_sprint87_annecy_v03_prepublication.py",\n'
    '    "tests/test_annecy_v03_public_release.py",\n'
    '    "research/sprint-87-summary.md",\n'
    '    "research/sprint-88-summary.md",\n'
    f'    "website/public/downloads/annecy-alpes-leman/{FULL_NAME}",\n'
    f'    "website/public/downloads/annecy-alpes-leman/{NO_AIR_NAME}",\n',
)
text = site_test.read_text(encoding="utf-8")
text = text.replace('"Annecy–Alpes–Léman v0.2** — 65 mémoires RX",', '"Annecy–Alpes–Léman v0.3** — 76 mémoires RX",')
site_test.write_text(text, encoding="utf-8")

# 16) Permanent CI guards.
ci = ROOT / ".github/workflows/ci.yml"
insert_before(
    ci,
    '      - name: Test published web generator\n',
    '      - name: Test Sprint 87 Annecy v0.3 prepublication\n'
    '        run: python tests/test_sprint87_annecy_v03_prepublication.py\n\n'
    '      - name: Test Annecy v0.3 public release\n'
    '        run: python tests/test_annecy_v03_public_release.py\n\n',
)

# 17) README / PROJECT_STATUS / CHANGELOG concise current-state update while preserving history.
readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
first_line_old = "**État courant : Sprint 86 / 0.21.75 — Annecy–Alpes–Léman v0.3 atteint un candidat interne de 76 mémoires RX (59 sans aviation), +11 RF uniques, sans publication.**"
first_line_new = f"**État courant : Sprint {SPRINT} / {STATE_VERSION} — Annecy–Alpes–Léman v0.3 est publiée et immuable à 76 mémoires RX (59 sans aviation), +11 RF uniques par rapport à v0.2.**"
if first_line_old in text:
    text = text.replace(first_line_old, first_line_new, 1)
else:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith("**État courant :"):
            lines[idx] = first_line_new
            break
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
text = text.replace("## État actuel — Sprint 86 / 0.21.75", f"## État actuel — Sprint {SPRINT} / {STATE_VERSION}")
text = text.replace("**Annecy–Alpes–Léman v0.2** — 65 mémoires RX, variante 48 sans aviation", "**Annecy–Alpes–Léman v0.3** — 76 mémoires RX, variante 59 sans aviation, publiée et immuable")
if "## Sprint 88 — publication Annecy–Alpes–Léman v0.3" not in text:
    anchor = "## Sprint 86 —"
    block = f'''## Sprint 88 — publication Annecy–Alpes–Léman v0.3\n\nLa **v0.3 est publiée et immuable à 76 RX / 59 sans aviation**. Elle ajoute 11 RF uniques paired RX, reste RX-only, déduplique les fréquences identiques et conserve F1ZTH 50.5375 MHz ainsi que l'UHF ADRASEC non publiée hors scope. SHA-256 et preuve : `research/annecy-alpes-leman-v0.3/publication-record.json`.\n\n## Sprint 87 — prépublication Annecy–Alpes–Léman v0.3\n\nScope figé **76/59**, checklist **12/12**, bloqueurs **0**, sources radioamateur/satellites/AIRAC revalidées avant publication.\n\n'''
    pos = text.find(anchor)
    if pos < 0:
        raise RuntimeError("README Sprint 86 anchor missing")
    text = text[:pos] + block + text[pos:]
readme.write_text(text, encoding="utf-8")

status = ROOT / "PROJECT_STATUS.md"
text = status.read_text(encoding="utf-8")
text = text.replace("Sprint courant : **86**", f"Sprint courant : **{SPRINT}**", 1)
text = text.replace("État logique : **0.21.75**", f"État logique : **{STATE_VERSION}**", 1)
text = text.replace("Résumé courant : `research/sprint-86-summary.md`.", "Résumé courant : `research/sprint-88-summary.md`.", 1)
if "## Sprint 88 — Annecy v0.3 publiée" not in text:
    anchor = "## Sprint 86 —"
    block = '''## Sprint 88 — Annecy v0.3 publiée\n\nAnnecy–Alpes–Léman v0.3 est **publiée et immuable à 76 RX / 59 sans aviation**, avec +11 RF uniques, revue 12/12 et zéro bloqueur. Le registre, la page régionale et le générateur utilisent désormais v0.3.\n\n## Sprint 87 — Annecy v0.3 prépublication\n\nSources courantes, satellites et AIRAC revalidés ; scope figé 76/59 ; F1ZTH 50 MHz et UHF ADRASEC non publiée explicitement hors scope.\n\n'''
    pos = text.find(anchor)
    if pos < 0:
        raise RuntimeError("PROJECT_STATUS Sprint 86 anchor missing")
    text = text[:pos] + block + text[pos:]
status.write_text(text, encoding="utf-8")

changelog = ROOT / "CHANGELOG.md"
text = changelog.read_text(encoding="utf-8")
if "## 0.21.77 - 2026-08-15" not in text:
    anchor = "## 0.21.75 - 2026-08-15"
    block = f'''## 0.21.77 - 2026-08-15\n\n- **Sprint 88** : publication immuable d'Annecy–Alpes–Léman v0.3 à **76 mémoires RX / 59 sans aviation**.\n- +11 RF uniques paired RX par rapport à v0.2 ; registre, générateur et page régionale basculés sur v0.3.\n- SHA-256 publics enregistrés dans `research/annecy-alpes-leman-v0.3/publication-record.json`.\n- F1ZTH 50.5375 MHz et l'UHF ADRASEC non publiée restent explicitement hors scope.\n\n## 0.21.76 - 2026-08-15\n\n- **Sprint 87** : prépublication Annecy v0.3 figée à 76/59, checklist 12/12, zéro bloqueur.\n- Revalidation des sources radioamateur, satellites AMSAT et cycles aviation courants ; builder de release déterministe ajouté.\n\n'''
    if anchor not in text:
        raise RuntimeError("CHANGELOG 0.21.75 anchor missing")
    text = text.replace(anchor, block + anchor, 1)
changelog.write_text(text, encoding="utf-8")

print("Annecy–Alpes–Léman v0.3 publication finalized")
print(f"full_sha256={full_sha}")
print(f"no_air_sha256={no_air_sha}")
