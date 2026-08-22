#!/usr/bin/env python3
"""Build Normandie v0.5 internal candidate using documented theoretical coverage."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_V04 = Path("website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv")
PUBLICATION_RECORD = Path("research/normandie-v0.4/publication-record.json")
PLAN = Path("research/normandie-v0.5/pack-plan.json")
THEORY = Path("research/normandie-v0.5/sprint112-theoretical-coverage.json")
POLICY = Path("research/normandie-v0.5/theoretical-coverage-policy.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r_km = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r_km * math.asin(math.sqrt(a))


def endpoint_envelope_km(h1_m: float, h2_m: float) -> float:
    return 4.12 * (math.sqrt(h1_m) + math.sqrt(h2_m))


def fspl_db(distance_km: float, frequency_mhz: float) -> float:
    return 32.44 + 20 * math.log10(distance_km) + 20 * math.log10(frequency_mhz)


def new_memory(location: int, name: str, frequency: float, comment: str) -> dict[str, str]:
    return {
        "Location": str(location),
        "Name": name,
        "Frequency": f"{frequency:.6f}",
        "Duplex": "off",
        "Offset": "0.000000",
        "Tone": "",
        "rToneFreq": "88.5",
        "cToneFreq": "88.5",
        "DtcsCode": "023",
        "DtcsPolarity": "NN",
        "RxDtcsCode": "023",
        "CrossMode": "Tone->Tone",
        "Mode": "NFM",
        "TStep": "12.50",
        "Skip": "",
        "Power": "",
        "Comment": comment,
        "URCALL": "",
        "RPT1CALL": "",
        "RPT2CALL": "",
        "DVCODE": "",
    }


def build_candidate(root: Path) -> dict[str, Any]:
    public_path = root / PUBLIC_V04
    record = load_json(root / PUBLICATION_RECORD)
    plan = load_json(root / PLAN)
    theory = load_json(root / THEORY)
    policy = load_json(root / POLICY)
    public_bytes = public_path.read_bytes()
    public_sha = hashlib.sha256(public_bytes).hexdigest()

    if record["status"] != "published_immutable":
        raise ValueError("Normandie v0.4 publication record is not immutable")
    if record["version"] != "0.4" or int(record["memory_count"]) != 142:
        raise ValueError("Unexpected Normandie v0.4 publication record")
    if record["public_csv_sha256"] != public_sha:
        raise ValueError("Normandie v0.4 public CSV SHA-256 does not match publication record")
    if plan["target_version"] != "0.5" or plan["based_on_published_version"] != "0.4":
        raise ValueError("Unexpected Normandie v0.5 plan")
    if plan["published_base_sha256"] != public_sha:
        raise ValueError("Normandie v0.5 plan base SHA-256 does not match public v0.4")
    if plan["current_candidate_memory_count"] != 146 or plan["current_new_memory_count"] != 4:
        raise ValueError("Normandie v0.5 plan is not the Sprint 112 theoretical candidate")
    if policy["decision_model"]["theoretical_coverage_may_close_coverage_gate"] is not True:
        raise ValueError("Theoretical coverage policy does not allow closing coverage gates")
    if policy["decision_model"]["field_reception_required_for_candidate_promotion"] is not False:
        raise ValueError("Field reception is unexpectedly required by current policy")
    if theory["candidate_memory_count_after"] != 146 or theory["candidate_memory_delta"] != 4:
        raise ValueError("Unexpected Sprint 112 theoretical coverage decision")

    with public_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if len(rows) != 142:
        raise ValueError(f"Expected 142 public base memories, got {len(rows)}")
    if not all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows):
        raise ValueError("Public Normandie v0.4 base violates RX-only CHIRP contract")

    mortain = theory["reference_point"]
    r3 = theory["promotions"][0]
    zha = theory["promotions"][1]
    r3_distance = haversine_km(
        mortain["latitude_deg"], mortain["longitude_deg"],
        r3["source_site"]["latitude_deg"], r3["source_site"]["longitude_deg"],
    )
    zha_distance = haversine_km(
        mortain["latitude_deg"], mortain["longitude_deg"],
        zha["source_site"]["locator_center_latitude_deg"], zha["source_site"]["locator_center_longitude_deg"],
    )
    if abs(r3_distance - r3["theory"]["great_circle_distance_km"]) > 0.05:
        raise ValueError("R3 theoretical distance drift")
    if abs(zha_distance - zha["theory"]["great_circle_distance_km"]) > 0.05:
        raise ValueError("F5ZHA theoretical distance drift")
    r3_envelope = endpoint_envelope_km(
        r3["source_site"]["antenna_elevation_m_asl"], mortain["representative_elevation_m_asl"]
    )
    zha_envelope = endpoint_envelope_km(
        zha["source_site"]["published_altitude_m_asl"], mortain["representative_elevation_m_asl"]
    )
    if r3_distance > r3_envelope or zha_distance > zha_envelope:
        raise ValueError("Theoretical endpoint-elevation envelope no longer supports promotion")
    if r3_distance > r3["source_site"]["published_usage_radius_km"]:
        raise ValueError("Mortain is outside published R3 usage radius")
    if abs(fspl_db(r3_distance, 145.675) - r3["theory"]["fspl_output_145_675_db"]) > 0.05:
        raise ValueError("R3 FSPL calculation drift")
    if abs(fspl_db(zha_distance, 145.4675) - zha["theory"]["fspl_vhf_145_4675_db"]) > 0.05:
        raise ValueError("F5ZHA VHF FSPL calculation drift")
    if abs(fspl_db(zha_distance, 432.575) - zha["theory"]["fspl_uhf_432_575_db"]) > 0.05:
        raise ValueError("F5ZHA UHF FSPL calculation drift")

    additions = [
        new_memory(178, "35-R3-IN", 145.075, "R3 Broceliande entree - couverture theorique Mortain - RX seule - ARA35 2026"),
        new_memory(179, "35-R3-OUT", 145.675, "R3 Broceliande sortie - couverture theorique Mortain - RX seule - ARA35 2026"),
        new_memory(180, "53-ZHA-V", 145.4675, "F5ZHA Laval VHF - couverture theorique Mortain - RX seule - REF 2026"),
        new_memory(181, "53-ZHA-U", 432.575, "F5ZHA Laval UHF - couverture theorique Mortain - RX seule - REF 2026"),
    ]
    rows_after = rows + additions
    locations = [int(row["Location"]) for row in rows_after]
    names = [row["Name"] for row in rows_after]
    frequencies = [round(float(row["Frequency"]), 6) for row in rows_after]
    new_frequencies = [round(float(row["Frequency"]), 6) for row in additions]
    if len(rows_after) != 146:
        raise ValueError("Expected 146 theoretical candidate memories")
    if len(locations) != len(set(locations)):
        raise ValueError("Duplicate CHIRP locations in Normandie v0.5 candidate")
    if len(names) != len(set(names)):
        raise ValueError("Duplicate CHIRP names in Normandie v0.5 candidate")
    if len(frequencies) != len(set(frequencies)):
        raise ValueError("Duplicate RF frequencies in Normandie v0.5 candidate")
    if any(len(name) > 10 for name in names):
        raise ValueError("CHIRP name exceeds 10 characters")
    if not all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows_after):
        raise ValueError("Normandie v0.5 candidate violates RX-only contract")
    if any(freq in new_frequencies for freq in [431.4125, 431.975, 430.375]):
        raise ValueError("Deferred or stale frequency was added by Sprint 112")

    return {
        "schema_version": "1.1",
        "pack": "Normandie",
        "target_version": "0.5",
        "status": "internal_candidate_theoretical_coverage_not_for_publication",
        "updated": "2026-08-22",
        "public_export_allowed": False,
        "published_base_version": "0.4",
        "published_base_memory_count": 142,
        "published_base_sha256": public_sha,
        "memory_count": 146,
        "new_memory_count": 4,
        "theoretical_coverage_memory_count": 4,
        "field_reception_verified_memory_count": 0,
        "remaining_known_potential_delta_excluding_f6zes": 1,
        "fieldnames": fieldnames,
        "rows": rows_after,
        "rules": {
            "rx_only": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "same_rf_frequency_deduplicated": True,
            "published_v0_4_immutable": True,
            "no_artificial_fill": True,
            "public_pack_mutation_allowed": False,
            "theoretical_coverage_may_close_coverage_gate": True,
            "theory_is_not_measured_reception": True,
            "field_reception_required_for_candidate_promotion": False,
            "unresolved_frequency_must_not_be_guessed": True,
        },
    }


def candidate_csv_bytes(candidate: dict[str, Any]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=candidate["fieldnames"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(candidate["rows"])
    return buffer.getvalue().encode("utf-8")


def write_candidate(candidate: dict[str, Any], output_dir: Path) -> tuple[Path, Path, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "normandie-v0.5-internal.csv"
    json_path = output_dir / "normandie-v0.5-internal.json"
    csv_bytes = candidate_csv_bytes(candidate)
    csv_path.write_bytes(csv_bytes)
    manifest = dict(candidate)
    manifest.pop("rows")
    manifest.pop("fieldnames")
    manifest["candidate_csv_sha256"] = hashlib.sha256(csv_bytes).hexdigest()
    manifest["candidate_csv"] = str(csv_path)
    json_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return csv_path, json_path, manifest["candidate_csv_sha256"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/normandie-v0.5/generated/internal-candidate"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    candidate = build_candidate(root)
    _, _, sha = write_candidate(candidate, output_dir)
    print(
        "NORMANDIE V0.5 THEORETICAL INTERNAL CANDIDATE: "
        f"{candidate['memory_count']} RX memories, delta=4, theoretical=4, sha256={sha}, public=false"
    )


if __name__ == "__main__":
    main()
