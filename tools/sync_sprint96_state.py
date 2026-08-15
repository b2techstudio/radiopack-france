from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "research/project-resume-state.json"

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
state["updated"] = "2026-08-15"
state["current_sprint"] = 96
state["state_version"] = "0.21.85"
state["latest_sprint96_site_design"] = {
    "sprint": 96,
    "state_version": "0.21.85",
    "completed_on": "2026-08-15",
    "status": "midnight_blue_soft_production_theme_and_registry_sync_complete",
    "design": "Midnight Blue Soft",
    "palette": {
        "background": "#182538",
        "surface": "#223249",
        "card": "#2B3D56",
        "text": "#F4F7FB",
        "blue": "#4EA8FF",
        "violet": "#9185FF",
        "rx_green": "#65D7B1",
        "signal_yellow": "#F4C95D",
    },
    "radioamateur_ui": True,
    "downloads_registry_backed": True,
    "versions_registry_backed": True,
    "stale_public_pack_metadata_guard": "tests/test_pack_registry.py",
    "production_origin": "https://radiopack-france.pages.dev/",
    "public_pack_mutation": False,
    "rf_data_mutation": False,
}

for item in [
    "research/sprint-96-summary.md",
    "website/src/pages/index.astro",
    "website/src/styles/global.css",
    "website/src/lib/packRegistry.ts",
    "website/src/pages/telechargements.astro",
    "website/src/pages/versions.astro",
    "tests/test_pack_registry.py",
]:
    if item not in state["sources_of_truth"]:
        state["sources_of_truth"].append(item)

recent = [item for item in state.get("recent_sprints", []) if item.get("sprint") != 96]
recent.insert(
    0,
    {
        "sprint": 96,
        "state_version": "0.21.85",
        "summary": "Midnight Blue Soft adopted across the public-site foundation; Downloads and Versions are registry-backed with deterministic stale-metadata guards; no RF or public CSV mutation.",
        "summary_file": "research/sprint-96-summary.md",
    },
)
state["recent_sprints"] = recent
STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

summary = """# Sprint 96 — Midnight Blue Soft production rollout

Date : **15 août 2026**  
État logique : **0.21.85**

## Résultat

- **Midnight Blue Soft** devient la direction visuelle de production de RadioPack France.
- Palette officielle : fond `#182538`, surface `#223249`, carte `#2B3D56`, texte `#F4F7FB`, bleu `#4EA8FF`, violet `#9185FF`, vert RX `#65D7B1`, jaune signal `#F4C95D`.
- La page d’accueil reprend une identité radioamateur épurée : double VFO, S-mètre, repères 6 m / 2 m / 70 cm et banques mémoire régionales.
- Header, footer et socle CSS public sont harmonisés avec la même direction.
- `telechargements.astro` et `versions.astro` utilisent désormais `publicPacks` comme source de vérité pour les versions, variantes, compteurs et URLs des packs régionaux.
- `tests/test_pack_registry.py` bloque le retour des anciennes références Bretagne v0.1 / Annecy v0.2 sur ces pages.

## Invariants préservés

- Normandie publique : **v0.4 / 142 RX**, immuable.
- Annecy–Alpes–Léman publique : **v0.4 / 77 RX**, variante **60 RX sans aviation**, immuable.
- Bretagne publique : **v0.2 / 151 RX**, immuable.
- Aucun CSV public, aucune fréquence, aucune mémoire RF et aucune règle d’émission n’ont été modifiés par ce sprint.
- Bretagne v0.3 reste à **151 RX, delta 0**, en attente de la revalidation AIRAC 09/26 à partir du 3 septembre 2026.
- Le domaine personnalisé `radiopack.b2tech.studio` reste séparé de l’origine Cloudflare Pages tant que sa configuration DNS n’est pas finalisée.

## Validation

Le sprint est conçu pour être clôturé uniquement après passage du build Astro, des tests dépôt/radio, de l’audit sécurité et des gardes permanentes sur le SHA final de documentation.
"""
(ROOT / "research/sprint-96-summary.md").write_text(summary, encoding="utf-8")

readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = readme.replace(
    "**État courant : Sprint 95 / 0.21.84 — Annecy–Alpes–Léman v0.4 publiée et immuable à 77 RX / 60 sans aviation ; audit sécurité live Cloudflare Pages validé ; Bretagne v0.3 reste en attente AIRAC 09/26.**",
    "**État courant : Sprint 96 / 0.21.85 — design public Midnight Blue Soft déployé ; Téléchargements et État des packs synchronisés sur le registre public ; packs RF inchangés ; Bretagne v0.3 reste en attente AIRAC 09/26.**",
)
readme = readme.replace("## État actuel — Sprint 95 / 0.21.84", "## État actuel — Sprint 96 / 0.21.85", 1)
marker = "## Sprint 95 — publication Annecy–Alpes–Léman v0.4"
section = """## Sprint 96 — Midnight Blue Soft et cohérence du site public

Le design **Midnight Blue Soft** est adopté en production avec une interface radioamateur épurée. Le socle public utilise désormais la palette bleu nuit intermédiaire retenue. Les pages **Téléchargements** et **État des packs** sont branchées sur `publicPacks`, et le test du registre interdit le retour des anciennes références Bretagne v0.1 / Annecy v0.2. **Aucun CSV public ni contenu RF n’a été modifié.** Résumé : `research/sprint-96-summary.md`.

"""
if section not in readme:
    readme = readme.replace(marker, section + marker, 1)
if "`research/sprint-96-summary.md`" not in readme.split(marker, 1)[0]:
    readme = readme.replace(
        "`research/sprint-92-summary.md` et `research/security-audit-sprint92.md`.",
        "`research/sprint-92-summary.md`, `research/security-audit-sprint92.md`, `research/sprint-93-summary.md`, `research/sprint-94-summary.md`, `research/sprint-95-summary.md` et `research/sprint-96-summary.md`.",
    )
readme_path.write_text(readme, encoding="utf-8")

status_path = ROOT / "PROJECT_STATUS.md"
status = status_path.read_text(encoding="utf-8")
status = status.replace("Sprint courant : **95**", "Sprint courant : **96**", 1)
status = status.replace("État logique : **0.21.84**", "État logique : **0.21.85**", 1)
status = status.replace("Résumé courant : `research/sprint-95-summary.md`.", "Résumé courant : `research/sprint-96-summary.md`.", 1)
marker = "## Sprint 95 — Annecy v0.4 publiée"
section = """## Sprint 96 — Midnight Blue Soft et synchronisation du site

La direction **Midnight Blue Soft** est désormais appliquée au socle public, avec une identité radioamateur épurée. `telechargements.astro` et `versions.astro` utilisent le registre `publicPacks` pour les versions, variantes, compteurs et liens ; `tests/test_pack_registry.py` garde cette synchronisation. Les packs publics restent **Normandie v0.4 142 RX, Annecy v0.4 77/60, Bretagne v0.2 151**, sans aucune mutation RF ou CSV.

"""
if section not in status:
    status = status.replace(marker, section + marker, 1)
status_path.write_text(status, encoding="utf-8")

changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
entry = """## 0.21.85 - 2026-08-15

- **Sprint 96** : adoption de **Midnight Blue Soft** comme design de production, avec interface radioamateur épurée et socle public harmonisé.
- `telechargements.astro` et `versions.astro` sont désormais alimentés par `publicPacks` pour éviter les versions et compteurs régionaux obsolètes.
- Extension de `tests/test_pack_registry.py` pour bloquer explicitement le retour des anciennes références Bretagne v0.1 / Annecy v0.2.
- Aucun CSV public, aucune fréquence ni mémoire RF modifiés.

"""
if "## 0.21.85 - 2026-08-15" not in changelog:
    changelog = changelog.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
changelog_path.write_text(changelog, encoding="utf-8")
