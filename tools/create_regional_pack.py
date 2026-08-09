#!/usr/bin/env python3
"""Create a non-public research scaffold for a future RadioPack regional pack.

The starter never publishes a pack, never edits packRegistry.ts and never creates
website download routes. It only prepares a research workspace.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_inputs(name: str, slug: str, version: str) -> None:
    if not name.strip():
        raise ValueError("Le nom du pack ne peut pas être vide")
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("Slug invalide: utiliser uniquement a-z, 0-9 et des tirets simples")
    if not VERSION_RE.fullmatch(version):
        raise ValueError("Version invalide: utiliser X.Y ou X.Y.Z")


def build_scaffold(name: str, slug: str, version: str, created: str) -> dict[str, dict]:
    common_pack = {
        "name": name,
        "slug": slug,
        "target_version": version,
    }

    pack_plan = {
        "schema_version": "1.0",
        "status": "research_scaffold_not_public",
        "created": created,
        "pack": common_pack,
        "memory_plan": {
            "status": "draft_no_channels",
            "expected_memory_count": None,
            "blocks": [],
        },
        "publication": {
            "public_export_allowed": False,
            "public_registry_allowed": False,
            "public_routes_allowed": False,
            "review_required": True,
            "review_completed": False,
        },
        "rules": {
            "rx_only": True,
            "duplex": "off",
            "offset": "0.000000",
            "max_memories": 200,
            "max_name_length": 10,
            "no_artificial_fill": True,
            "published_versions_are_immutable": True,
        },
    }

    source_registry = {
        "schema_version": "1.0",
        "status": "research_sources_empty",
        "created": created,
        "pack": common_pack,
        "sources": [],
        "rules": {
            "prefer_primary_sources": True,
            "record_access_date": True,
            "record_scope_and_limitations": True,
            "unverified_data_must_not_enter_public_pack": True,
        },
    }

    publication_gates = {
        "schema_version": "1.0",
        "status": "blocked_research_not_started",
        "created": created,
        "pack": common_pack,
        "public_release_allowed": False,
        "gates": [
            {
                "id": "sources",
                "status": "pending",
                "required_for_public_release": True,
                "description": "Sources principales identifiées et documentées",
            },
            {
                "id": "memory_plan",
                "status": "pending",
                "required_for_public_release": True,
                "description": "Plan mémoire défini sans remplissage artificiel",
            },
            {
                "id": "data_validation",
                "status": "pending",
                "required_for_public_release": True,
                "description": "Fréquences retenues recoupées selon leur domaine",
            },
            {
                "id": "dynamic_rechecks",
                "status": "pending_scope_definition",
                "required_for_public_release": True,
                "description": "Contrôles dynamiques applicables identifiés et revalidés",
            },
            {
                "id": "review_map",
                "status": "pending",
                "required_for_public_release": True,
                "description": "Carte de revue finale créée et validée",
            },
            {
                "id": "explicit_publication",
                "status": "blocked_until_all_previous_gates_pass",
                "required_for_public_release": True,
                "description": "Ajout explicite au site et au registre public",
            },
        ],
    }

    memory_plan = {
        "schema_version": "1.0",
        "status": "draft_no_channels",
        "created": created,
        "pack": common_pack,
        "expected_memory_count": None,
        "blocks": [],
        "reserved_positions": [],
        "rules": {
            "max_memories": 200,
            "max_name_length": 10,
            "duplex": "off",
            "offset": "0.000000",
            "no_artificial_fill": True,
        },
    }

    return {
        "pack-plan.json": pack_plan,
        "source-registry.json": source_registry,
        "publication-gates.json": publication_gates,
        "memory-plan.json": memory_plan,
    }


def create_workspace(repository_root: Path, output_root: Path, name: str, slug: str, version: str) -> Path:
    validate_inputs(name, slug, version)
    target = output_root / "research" / f"{slug}-v{version}"
    if target.exists():
        raise FileExistsError(f"Le dossier existe déjà: {target}")

    target.mkdir(parents=True)
    created = date.today().isoformat()
    for filename, payload in build_scaffold(name, slug, version, created).items():
        write_json(target / filename, payload)

    readme = f"""# {name} — espace de recherche v{version}\n\n"
    readme += "Cet espace a été créé par `tools/create_regional_pack.py`.\n\n"
    readme += "## État initial\n\n"
    readme += "- statut : `research_scaffold_not_public` ;\n"
    readme += "- aucune fréquence n'est encore retenue ;\n"
    readme += "- aucun nombre cible de mémoires n'est imposé ;\n"
    readme += "- aucun fichier public n'est créé ;\n"
    readme += "- aucune entrée n'est ajoutée à `website/src/lib/packRegistry.ts`.\n\n"
    readme += "## Suite\n\n"
    readme += "Documenter d'abord les sources et le périmètre, puis construire les inventaires, le plan mémoire, les portes de publication et la carte de revue conformément à `REGIONAL-PACK-WORKFLOW.md`.\n\n"
    readme += "Une publication doit rester une action explicite après revue et CI verte.\n"
    (target / "README.md").write_text(readme, encoding="utf-8")

    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="Créer un starter de recherche pour un pack régional RadioPack France")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Racine du dépôt")
    parser.add_argument("--output-root", type=Path, help="Racine de sortie alternative, utile pour les tests")
    parser.add_argument("--name", required=True, help="Nom public envisagé du pack")
    parser.add_argument("--slug", required=True, help="Slug stable, ex: bretagne")
    parser.add_argument("--version", default="0.1", help="Version de travail, ex: 0.1 ou 0.1.0")
    args = parser.parse_args()

    root = args.root.resolve()
    output_root = args.output_root.resolve() if args.output_root else root
    target = create_workspace(root, output_root, args.name.strip(), args.slug.strip(), args.version.strip())
    print(f"Starter régional créé: {target}")
    print("NOT PUBLIC: aucune route CSV ni entrée packRegistry.ts n'a été créée")


if __name__ == "__main__":
    main()
