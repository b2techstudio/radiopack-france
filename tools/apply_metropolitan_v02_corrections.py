#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TS_PATH = ROOT / "website/src/lib/metropolitanPack.ts"

HDF_AVIATION = [
    {"name": "AIR-EMERG", "frequency": 121.500, "area": "France / aviation", "service": "EMERGENCY"},
    {"name": "LIL-FIS1", "frequency": 126.480, "area": "Lille", "service": "FIS", "icao": "LFQQ"},
    {"name": "LIL-FIS2", "frequency": 129.360, "area": "Lille", "service": "FIS", "icao": "LFQQ"},
    {"name": "LIL-FIS3", "frequency": 132.540, "area": "Lille", "service": "FIS", "icao": "LFQQ"},
    {"name": "LIL-APP", "frequency": 120.275, "area": "Lille", "service": "APP", "icao": "LFQQ"},
    {"name": "LIL-GND", "frequency": 121.855, "area": "Lille", "service": "GND", "icao": "LFQQ"},
    {"name": "LIL-TWR", "frequency": 118.555, "area": "Lille", "service": "TWR", "icao": "LFQQ"},
    {"name": "LIL-ATIS", "frequency": 119.330, "area": "Lille", "service": "ATIS", "icao": "LFQQ"},
    {"name": "LTQ-GND", "frequency": 121.755, "area": "Le Touquet", "service": "GND", "icao": "LFAT"},
    {"name": "LTQ-TWR", "frequency": 118.450, "area": "Le Touquet", "service": "TWR", "icao": "LFAT"},
    {"name": "LTQ-ATIS", "frequency": 123.130, "area": "Le Touquet", "service": "ATIS", "icao": "LFAT"},
    {"name": "BVS-FIS", "frequency": 119.800, "area": "Beauvais", "service": "FIS", "icao": "LFOB"},
    {"name": "BVS-APP", "frequency": 121.400, "area": "Beauvais", "service": "APP/TWR", "icao": "LFOB"},
    {"name": "BVS-AUX", "frequency": 123.985, "area": "Beauvais", "service": "APP/TWR", "icao": "LFOB"},
    {"name": "BVS-ATIS", "frequency": 118.380, "area": "Beauvais", "service": "ATIS", "icao": "LFOB"},
]

GRAND_EST_AVIATION = [
    {"name": "AIR-EMERG", "frequency": 121.500, "area": "France / aviation", "service": "EMERGENCY"},
    {"name": "SXB-FIS1", "frequency": 119.580, "area": "Strasbourg", "service": "FIS", "icao": "LFST"},
    {"name": "SXB-FIS2", "frequency": 132.215, "area": "Strasbourg", "service": "FIS", "icao": "LFST"},
    {"name": "SXB-FIS3", "frequency": 136.135, "area": "Strasbourg", "service": "FIS", "icao": "LFST"},
    {"name": "SXB-APP", "frequency": 118.185, "area": "Strasbourg", "service": "APP", "icao": "LFST"},
    {"name": "MLH-FIS1", "frequency": 129.250, "area": "Bâle-Mulhouse", "service": "FIS", "icao": "LFSB"},
    {"name": "MLH-FIS2", "frequency": 130.900, "area": "Bâle-Mulhouse", "service": "FIS", "icao": "LFSB"},
    {"name": "MLH-FIS3", "frequency": 134.680, "area": "Bâle-Mulhouse", "service": "FIS", "icao": "LFSB"},
    {"name": "MLH-APP1", "frequency": 125.160, "area": "Bâle-Mulhouse", "service": "APP", "icao": "LFSB"},
    {"name": "MLH-APP2", "frequency": 127.285, "area": "Bâle-Mulhouse", "service": "APP", "icao": "LFSB"},
    {"name": "MLH-DEL", "frequency": 121.955, "area": "Bâle-Mulhouse", "service": "DEL", "icao": "LFSB"},
    {"name": "MLH-GND", "frequency": 121.605, "area": "Bâle-Mulhouse", "service": "GND", "icao": "LFSB"},
    {"name": "MLH-TWR", "frequency": 118.300, "area": "Bâle-Mulhouse", "service": "TWR", "icao": "LFSB"},
    {"name": "MLH-ATIS", "frequency": 127.880, "area": "Bâle-Mulhouse", "service": "ATIS", "icao": "LFSB"},
    {"name": "ETZ-APP", "frequency": 119.125, "area": "Metz-Nancy", "service": "APP", "icao": "LFJL"},
    {"name": "ETZ-GND", "frequency": 121.705, "area": "Metz-Nancy", "service": "GND", "icao": "LFJL"},
    {"name": "ETZ-TWR", "frequency": 122.075, "area": "Metz-Nancy", "service": "TWR", "icao": "LFJL"},
    {"name": "ETZ-ATIS", "frequency": 136.580, "area": "Metz-Nancy", "service": "ATIS", "icao": "LFJL"},
    {"name": "ENC-INFO", "frequency": 119.605, "area": "Nancy-Essey", "service": "AFIS", "icao": "LFSN"},
]


def ts_channel(item: dict) -> str:
    bits = [
        f'name: "{item["name"]}"',
        f'frequency: {item["frequency"]:g}',
        f'area: "{item["area"]}"',
        f'service: "{item["service"]}"',
    ]
    if item.get("icao"):
        bits.append(f'icao: "{item["icao"]}"')
    return "      { " + ", ".join(bits) + " },"


def replace_aviation_block(text: str, pack_id: str, channels: list[dict]) -> str:
    pack_at = text.index(f'    id: "{pack_id}"')
    aviation_at = text.index("    aviation: [", pack_at)
    repeaters_at = text.index("    repeaters: [", aviation_at)
    new_block = "    aviation: [\n" + "\n".join(ts_channel(item) for item in channels) + "\n    ],\n"
    return text[:aviation_at] + new_block + text[repeaters_at:]


def to_plan_channels(channels: list[dict]) -> list[dict]:
    result = []
    for item in channels:
        result.append({
            "name": item["name"],
            "frequency_mhz": item["frequency"],
            "area": item["area"],
            "service": item["service"],
            "icao": item.get("icao"),
        })
    return result


def update_plan(slug: str, channels: list[dict], aerodromes: list[str]) -> None:
    path = ROOT / f"research/{slug}-v0.2/pack-plan.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    aviation = data["blocks"]["aviation"]
    aviation["memory_count"] = len(channels)
    aviation["channels"] = to_plan_channels(channels)
    aviation["aerodromes"] = aerodromes
    aviation["source_review_note"] = "Primary SIA eAIP AD 2.18 values rechecked on 2026-08-19; duplicated or stale labels were corrected before publication."
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "**État courant : Sprint 97 / 0.21.86 — socle officiel conservé ; publication post-Sprint 97 de onze packs régionaux v0.1 et mise à jour du site public vers une couverture métropolitaine 13/13.**",
        "**État courant : Sprint 97 / 0.21.86 — socle officiel conservé ; publication post-Sprint 97 des onze packs régionaux désormais enrichis en v0.2, avec couverture métropolitaine 13/13.**",
    )
    text = text.replace(
        "La couverture administrative métropolitaine est maintenant **13/13**. Normandie et Bretagne conservent leurs versions publiques matures ; les onze autres régions démarrent avec une **v0.1 volontairement non exhaustive**. Annecy–Alpes–Léman reste un pack territorial spécialisé en complément.",
        "La couverture administrative métropolitaine est **13/13**. Normandie et Bretagne conservent leurs versions publiques matures ; les onze autres régions disposent maintenant d'une **v0.2 enrichie**, tandis que leur v0.1 reste historique et immuable. Annecy–Alpes–Léman reste un pack territorial spécialisé en complément.",
    )
    replacements = {
        "- **Hauts-de-France v0.1** — 36 mémoires RX ;": "- **Hauts-de-France v0.2** — 144 mémoires RX ;",
        "- **Île-de-France v0.1** — 34 mémoires RX ;": "- **Île-de-France v0.2** — 58 mémoires RX ;",
        "- **Grand Est v0.1** — 36 mémoires RX ;": "- **Grand Est v0.2** — 59 mémoires RX ;",
        "- **Centre-Val de Loire v0.1** — 32 mémoires RX ;": "- **Centre-Val de Loire v0.2** — 42 mémoires RX ;",
        "- **Pays de la Loire v0.1** — 30 mémoires RX ;": "- **Pays de la Loire v0.2** — 130 mémoires RX ;",
        "- **Bourgogne-Franche-Comté v0.1** — 30 mémoires RX ;": "- **Bourgogne-Franche-Comté v0.2** — 37 mémoires RX ;",
        "- **Nouvelle-Aquitaine v0.1** — 42 mémoires RX ;": "- **Nouvelle-Aquitaine v0.2** — 151 mémoires RX ;",
        "- **Auvergne-Rhône-Alpes v0.1** — 38 mémoires RX ;": "- **Auvergne-Rhône-Alpes v0.2** — 62 mémoires RX ;",
        "- **Occitanie v0.1** — 44 mémoires RX ;": "- **Occitanie v0.2** — 156 mémoires RX ;",
        "- **Provence-Alpes-Côte d’Azur v0.1** — 42 mémoires RX ;": "- **Provence-Alpes-Côte d’Azur v0.2** — 159 mémoires RX ;",
        "- **Corse v0.1** — 28 mémoires RX ;": "- **Corse v0.2** — 137 mémoires RX ;",
        "Les variantes par défaut représentent **762 mémoires RX cumulées**": "Les variantes par défaut représentent **1505 mémoires RX cumulées**",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    start = text.index("### Périmètre des onze nouvelles v0.1")
    end = text.index("## Contrat RX-only et paired RX", start)
    new_scope = """### Périmètre des onze v0.2 enrichies

Chaque pack v0.2 conserve le socle PMR446, appels radioamateur et APRS/ISS, puis ajoute une sélection aviation AM revue sur les pages publiques SIA eAIP AD 2.18 dans le contexte AIRAC 08/26 et une sélection régionale de relais FM 2 m en paired RX. Les six régions littorales concernées intègrent également le module national VHF marine de 90 mémoires.

Les v0.1 restent générables à leurs URL historiques et ne sont jamais réécrites. UHF, numérique et réseaux privés/PPDR restent hors publication tant qu'une revue dédiée ne justifie pas leur présence. Le but est d'enrichir utilement les packs, pas de remplir artificiellement les 200 mémoires.

La synthèse de l'enrichissement est `research/metropolitan-regions-v0.2-enrichment.md`. Chaque région dispose d'un dossier `research/<region>-v0.2/` avec un `README.md` et un `pack-plan.json` traçant blocs, sources, exclusions et compteurs.

"""
    text = text[:start] + new_scope + text[end:]

    text = text.replace(
        "La sélection FM 2 m des nouvelles v0.1 a été revue le 19 août 2026 à partir de sources publiques complémentaires :",
        "La sélection FM 2 m des v0.2 a été revue le 19 août 2026 à partir de sources publiques complémentaires :",
    )
    text = text.replace(
        "Le dépôt ne transforme pas une présence dans un annuaire en garantie absolue de disponibilité terrain. Les v0.1 restent des bases d'écoute publiques et traçables ; les évolutions nécessitent une nouvelle validation.",
        "L'aviation est en plus contrôlée sur les pages publiques SIA eAIP AD 2.18 dans le contexte AIRAC 08/26. Le dépôt ne transforme jamais une présence dans un annuaire en garantie absolue de disponibilité terrain ; toute évolution RF nécessite une nouvelle validation.",
    )
    text = text.replace(
        "- `/regions/<slug>` — pages détaillées des onze nouvelles v0.1 générées depuis la définition déterministe ;",
        "- `/regions/<slug>` — pages détaillées des onze v0.2 enrichies générées depuis la définition déterministe ;",
    )
    text = text.replace(
        "Les onze nouvelles URL CSV sont générées au build par `website/src/pages/downloads/[slug]/[file].csv.ts`. Les versions historiques Normandie, Bretagne et Annecy restent des artefacts publics immuables.",
        "Les onze URL CSV v0.2 et leurs URL historiques v0.1 sont générées au build par `website/src/pages/downloads/[slug]/[file].csv.ts`. Les versions historiques Normandie, Bretagne et Annecy restent des artefacts publics immuables.",
    )

    marker = "## État actuel — Sprint 97 / 0.21.86"
    if "## Publication post-Sprint 97 — enrichissement métropolitain v0.2" not in text:
        block = """## Publication post-Sprint 97 — enrichissement métropolitain v0.2

Les onze régions ajoutées lors de la couverture 13/13 ont été enrichies sans réécrire leurs v0.1. Les packs v0.2 combinent désormais aviation SIA, relais FM 2 m paired RX et, pour les régions littorales, VHF marine. Le contrôle SIA final a notamment corrigé les libellés/fichiers Hauts-de-France, Île-de-France et Grand Est avant publication ; la validation de déduplication reste active.

Cette publication reste postérieure au Sprint 97 et ne modifie pas l'état logique officiel **97 / 0.21.86**.

"""
        text = text.replace(marker, block + marker)

    history_marker = "## Repères historiques importants"
    if "## Sprint 91 — Bretagne v0.3 AIRAC09 handoff" not in text:
        historical = """## Sprint 91 — Bretagne v0.3 AIRAC09 handoff

Bretagne v0.3 reste à **151 RX**, delta 0, avec revalidation AIRAC 09/26 prévue à partir du 3 septembre 2026 ; aucune anticipation de publication.

## Sprint 90 — Normandie v0.5 source refresh

Normandie v0.5 reste à **142 RX**, delta 0. Les gates terrain/source R3, F5ZHA, F1ZOV et F6ZES restent inchangés.

## Sprint 89 — Annecy v0.4 candidat

Le candidat Annecy–Alpes–Léman v0.4 était figé à **77 RX / 60 sans aviation** avant sa publication ultérieure immuable.

"""
        text = text.replace(history_marker, historical + history_marker)

    path.write_text(text, encoding="utf-8")


def update_project_status() -> None:
    path = ROOT / "PROJECT_STATUS.md"
    text = path.read_text(encoding="utf-8")
    marker = "## Sprint 97 — consolidation de l'état post-Sprint 96"
    if "## Publication post-Sprint 97 — enrichissement métropolitain v0.2" not in text:
        block = """## Publication post-Sprint 97 — enrichissement métropolitain v0.2

Les onze régions métropolitaines ajoutées après le Sprint 97 sont désormais publiées en v0.2 enrichie, leurs v0.1 restant historiques et générables. Comptes courants : Hauts-de-France 144, Île-de-France 58, Grand Est 59, Centre-Val de Loire 42, Pays de la Loire 130, Bourgogne-Franche-Comté 37, Nouvelle-Aquitaine 151, Auvergne-Rhône-Alpes 62, Occitanie 156, Provence-Alpes-Côte d'Azur 159 et Corse 137 mémoires RX.

Les v0.2 ajoutent une aviation AM SIA revue, conservent les relais FM 2 m en paired RX et intègrent le module VHF marine aux six régions littorales concernées. UHF/numérique et réseaux privés ou PPDR restent hors scope sans revue dédiée. Le contrat `Duplex=off` / `Offset=0.000000` reste inchangé. Cette publication ne change pas l'état logique officiel **97 / 0.21.86**.

"""
        text = text.replace(marker, block + marker)
    path.write_text(text, encoding="utf-8")


def update_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    marker = "## 0.21.86 - 2026-08-17"
    if "## Publication post-Sprint 97 - 2026-08-19" not in text:
        block = """## Publication post-Sprint 97 - 2026-08-19

- Enrichissement des onze packs métropolitains v0.1 vers des **v0.2** sans mutation des versions historiques.
- Ajout d'une sélection aviation AM revue sur les pages publiques SIA eAIP AD 2.18 dans le contexte AIRAC 08/26.
- Intégration du module national VHF marine de 90 mémoires aux six régions littorales concernées.
- Extension/revalidation des sélections de relais FM 2 m en paired RX, toujours `Duplex=off` / `Offset=0.000000`.
- Audit correctif SIA final : correction des canaux Lille, du libellé Le Bourget et de la sélection Grand Est, avec élimination du doublon 121.805 MHz détecté par le validateur.
- Ajout des dossiers `research/<region>-v0.2/` et conservation des URL CSV v0.1 historiques.
- Publication post-Sprint : l'état logique officiel reste **97 / 0.21.86**.

"""
        text = text.replace(marker, block + marker)
    path.write_text(text, encoding="utf-8")


def update_release_note() -> None:
    path = ROOT / "research/metropolitan-regions-v0.2-enrichment.md"
    text = path.read_text(encoding="utf-8")
    marker = "## Contrôle correctif SIA avant publication"
    if marker not in text:
        text = text.rstrip() + """

## Contrôle correctif SIA avant publication

Un second passage sur les pages primaires SIA eAIP AD 2.18 a été effectué avant publication. Il a corrigé les canaux de Lille dans Hauts-de-France, le rôle de 123.835 MHz au Bourget, et la sélection Grand Est. Le validateur de déduplication a notamment bloqué un doublon 121.805 MHz : la sélection Bâle-Mulhouse a été réalignée sur les valeurs SIA actuelles, dont 121.605 MHz pour le sol. Aucune désactivation du garde-fou n'a été utilisée.
""" + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    text = TS_PATH.read_text(encoding="utf-8")
    text = replace_aviation_block(text, "hauts-de-france", HDF_AVIATION)
    text = text.replace(
        '{ name: "LBG-APP", frequency: 123.835, area: "Le Bourget", service: "APP", icao: "LFPB" },',
        '{ name: "LBG-FIS", frequency: 123.835, area: "Le Bourget", service: "FIS", icao: "LFPB" },',
    )
    text = replace_aviation_block(text, "grand-est", GRAND_EST_AVIATION)
    TS_PATH.write_text(text, encoding="utf-8")

    update_plan("hauts-de-france", HDF_AVIATION, ["LFOB", "LFAT", "LFQQ"])
    update_plan("grand-est", GRAND_EST_AVIATION, ["LFST", "LFSB", "LFJL", "LFSN"])

    idf_path = ROOT / "research/ile-de-france-v0.2/pack-plan.json"
    idf = json.loads(idf_path.read_text(encoding="utf-8"))
    for item in idf["blocks"]["aviation"]["channels"]:
        if item["name"] == "LBG-APP" and item["frequency_mhz"] == 123.835:
            item["name"] = "LBG-FIS"
            item["service"] = "FIS"
    idf["blocks"]["aviation"]["source_review_note"] = "Le Bourget 123.835 MHz relabelled FIS from current SIA eAIP AD 2.18 review on 2026-08-19."
    idf_path.write_text(json.dumps(idf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    update_readme()
    update_project_status()
    update_changelog()
    update_release_note()

    # Remove the temporary one-shot applier and its workflow in the same generated commit.
    (ROOT / "tools/apply_metropolitan_v02_corrections.py").unlink(missing_ok=True)
    (ROOT / ".github/workflows/temporary-metropolitan-v02-corrections.yml").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
