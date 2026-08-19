#!/usr/bin/env python3
from __future__ import annotations
import base64
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = ROOT / "tools/metropolitan_release_chunks"
SKIP_ARCHIVE_PATHS = {".github/workflows/temporary-readme-metropolitan.yml"}
README_BLOCK = '\n\n## Couverture métropolitaine complète — 19 août 2026\n\nAprès le Sprint 97, RadioPack France publie les **onze régions administratives métropolitaines restantes en v0.1**. Avec Normandie et Bretagne, la couverture administrative de la France métropolitaine atteint désormais **13/13 régions**. Annecy–Alpes–Léman reste disponible comme pack territorial spécialisé supplémentaire.\n\nLes nouvelles v0.1 utilisent un périmètre volontairement borné et non exhaustif : PMR446 RX, appels radioamateur RX, APRS/ISS RX et sélection régionale de relais FM 2 m publics et recoupés. Les paires 2 m retenues sont représentées en paired RX (sortie + entrée vérifiée) et toutes les mémoires publiques restent `Duplex=off` / `Offset=0.000000`.\n\nLes inventaires, exclusions, sources, portes de publication et cartes de revue sont conservés sous `research/<region>-v0.1/`. La synthèse de cette publication est `research/metropolitan-regions-v0.1-release.md`. L’aviation, l’UHF, le numérique et les extensions maritimes régionales restent hors de ces premières v0.1 tant qu’une revue dédiée n’a pas été menée.\n'
README_MARKER = "## Couverture métropolitaine complète — 19 août 2026"

def main() -> None:
    encoded = "".join(path.read_text(encoding="ascii").strip() for path in sorted(CHUNK_DIR.glob("*.txt")))
    payload = base64.b64decode(encoded)
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        for member in archive.getmembers():
            target = (ROOT / member.name).resolve()
            if ROOT.resolve() not in target.parents and target != ROOT.resolve():
                raise RuntimeError(f"Archive path escapes repository: {member.name}")
        for member in archive.getmembers():
            if member.name in SKIP_ARCHIVE_PATHS:
                continue
            archive.extract(member, ROOT, filter="data")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    if README_MARKER not in readme:
        readme_path.write_text(readme.rstrip() + README_BLOCK + "\n", encoding="utf-8")

    print("Applied complete metropolitan v0.1 release snapshot.")

if __name__ == "__main__":
    main()
