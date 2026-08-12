import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/bretagne-v0.2"

maturity = json.loads((RESEARCH / "maturity-review.json").read_text(encoding="utf-8"))
scope = json.loads((RESEARCH / "release-scope.json").read_text(encoding="utf-8"))
checklist = json.loads((RESEARCH / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((RESEARCH / "publication-gates.json").read_text(encoding="utf-8"))

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

assert gates["status"] == "prepublication_ready_151_not_public"
assert gates["prepublication_ready"] is True
assert gates["public_release_allowed"] is False
assert gates["gates"][-1]["id"] == "explicit_publication"
assert gates["gates"][-1]["status"] == "pending_separate_publication_sprint"

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

assert not (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv").exists()
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert "radiopack-france-bretagne-v0.2.csv" not in registry

print("Sprint 79 Bretagne v0.2 maturity: scope frozen at 151, review 10/10, blockers 0, prepublication ready and still not public OK")
