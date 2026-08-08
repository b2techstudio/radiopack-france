#!/usr/bin/env python3
"""Build a non-public local verification candidate for Annecy–Alpes–Léman v0.2."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_annecy_internal_candidate as internal
import check_annecy_release_readiness as readiness

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = Path("research/annecy-alpes-leman-v0.2")
OPTIONS = Path("generator/options.json")
DEFAULT_OUTPUT_DIR = RESEARCH / "generated/prepublication"

AVIATION_BLOCKS = {"Aviation France et bassin genevois", "Aviation Suisse"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def notam_summary(state: str, confirmed_at: str | None = None) -> dict[str, Any]:
    if state == "disabled":
        return {"state": state, "requested": False, "confirmed": False, "confirmed_at": None,
                "warning": "Contrôle NOTAM non demandé; les fréquences restent celles des sources AIP/AIRAC validées."}
    if state == "requested_unconfirmed":
        return {"state": state, "requested": True, "confirmed": False, "confirmed_at": None,
                "warning": "Contrôle NOTAM demandé mais non confirmé; la génération reste autorisée et le CSV n'est pas modifié."}
    if state == "user_confirmed":
        timestamp = confirmed_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
        return {"state": state, "requested": True, "confirmed": True, "confirmed_at": timestamp, "warning": None}
    raise ValueError(f"État NOTAM inconnu: {state}")


def build_prepublication(root: Path, include_aviation: bool = True, notam_check: str = "disabled",
                         notam_confirmed_at: str | None = None) -> dict[str, Any]:
    readiness_result = readiness.evaluate(root)
    if not readiness_result["ready_for_public_prepublication"]:
        blockers = ", ".join(blocker["id"] for blocker in readiness_result["blockers"])
        raise RuntimeError("Génération locale interdite tant que les portes bloquantes ne sont pas validées" + (f": {blockers}" if blockers else ""))

    options = load_json(root / OPTIONS)
    allowed_notam_states = set(options["options"]["notam_check"]["states"])
    if notam_check not in allowed_notam_states:
        raise ValueError(f"État NOTAM non autorisé: {notam_check}; attendus: {', '.join(sorted(allowed_notam_states))}")

    internal_candidate = internal.build_candidate(root)
    memories = [
        item for item in internal_candidate["memories"]
        if include_aviation or item["channel"].get("candidate_block") not in AVIATION_BLOCKS
    ]

    expected_count = 65 if include_aviation else 48
    if len(memories) != expected_count:
        raise ValueError(f"Total local inattendu: {len(memories)} au lieu de {expected_count}")

    locations = [item["location"] for item in memories]
    names = [item["channel"]["name"] for item in memories]
    frequencies = [float(item["channel"]["frequency_mhz"]) for item in memories]
    if len(locations) != len(set(locations)):
        raise ValueError("Conflit de numéros de mémoire")
    if len(names) != len(set(names)):
        raise ValueError("Noms de mémoire dupliqués")
    if len(frequencies) != len(set(frequencies)):
        raise ValueError("Fréquences dupliquées")

    return {
        "pack": "Annecy–Alpes–Léman",
        "target_version": "0.2.0",
        "status": "prepublication_candidate_not_public",
        "public_export_allowed": False,
        "generated_from_ready_state": True,
        "memory_count": len(memories),
        "include_aviation": include_aviation,
        "notam": notam_summary(notam_check, notam_confirmed_at),
        "rules": [
            "Ce fichier local reste hors de website/public.",
            "La v0.2 publique est générée séparément par website/src/lib/annecyPack.ts.",
            "Toutes les mémoires utilisent Duplex=off.",
            "L'option aviation modifie uniquement la présence des blocs aviation validés.",
            "L'option NOTAM est informative et ne modifie jamais automatiquement le CSV.",
        ],
        "memories": memories,
    }


def write_prepublication(candidate: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = "" if candidate["include_aviation"] else "-no-aviation"
    base_name = f"annecy-alpes-leman-v0.2-prepublication{suffix}"
    json_path = output_dir / f"{base_name}.json"
    csv_path = output_dir / f"{base_name}.csv"
    json_path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=internal.CHIRP_COLUMNS)
        writer.writeheader()
        for item in sorted(candidate["memories"], key=lambda row: row["location"]):
            writer.writerow(internal.chirp_row(item["location"], item["channel"]))
    return json_path, csv_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--aviation", action=argparse.BooleanOptionalAction, default=True,
                        help="Inclure ou retirer les blocs aviation validés.")
    parser.add_argument("--notam-check", choices=["disabled", "requested_unconfirmed", "user_confirmed"],
                        default="disabled", help="État du contrôle NOTAM facultatif; n'altère jamais les fréquences du CSV.")
    parser.add_argument("--notam-confirmed-at", default=None,
                        help="Horodatage facultatif utilisé avec --notam-check user_confirmed.")
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    candidate = build_prepublication(root, args.aviation, args.notam_check, args.notam_confirmed_at)
    json_path, csv_path = write_prepublication(candidate, output_dir)

    print(f"PREPUBLICATION READY: {candidate['memory_count']} memories; aviation={'on' if candidate['include_aviation'] else 'off'}; notam={candidate['notam']['state']}")
    print(json_path)
    print(csv_path)
    print("LOCAL CHECK ONLY: public v0.2 is generated by website/src/lib/annecyPack.ts")


if __name__ == "__main__":
    main()
