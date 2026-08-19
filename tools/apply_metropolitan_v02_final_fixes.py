#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1) Hauts-de-France: keep the published v0.2 bounded at 14 aviation memories.
ts_path = ROOT / "website/src/lib/metropolitanPack.ts"
ts = ts_path.read_text(encoding="utf-8")
line = '      { name: "LIL-FIS3", frequency: 132.54, area: "Lille", service: "FIS", icao: "LFQQ" },\n'
assert line in ts, "Expected LIL-FIS3 line not found"
ts = ts.replace(line, "", 1)
ts_path.write_text(ts, encoding="utf-8")

plan_path = ROOT / "research/hauts-de-france-v0.2/pack-plan.json"
plan = json.loads(plan_path.read_text(encoding="utf-8"))
channels = plan["blocks"]["aviation"]["channels"]
assert any(item["name"] == "LIL-FIS3" for item in channels), "Expected LIL-FIS3 plan entry not found"
channels = [item for item in channels if item["name"] != "LIL-FIS3"]
assert len(channels) == 14, len(channels)
plan["blocks"]["aviation"]["channels"] = channels
plan["blocks"]["aviation"]["memory_count"] = 14
plan["blocks"]["aviation"]["bounded_selection_note"] = "132.540 MHz is current SIA FIS evidence but intentionally left outside this bounded 14-memory aviation selection; no artificial fill."
plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 2) Keep Sprint 97 / 0.21.86 as the first changelog release heading.
changelog_path = ROOT / "CHANGELOG.md"
changelog = changelog_path.read_text(encoding="utf-8")
post_heading = "## Publication post-Sprint 97 - 2026-08-19\n"
sprint97_heading = "## 0.21.86 - 2026-08-17\n"
previous_heading = "## 0.21.85 - 2026-08-15\n"
assert changelog.startswith("# Changelog\n\n" + post_heading), "Unexpected changelog prefix"
post_start = changelog.index(post_heading)
sprint97_start = changelog.index(sprint97_heading, post_start)
post_block = changelog[post_start:sprint97_start].rstrip() + "\n\n"
without_post = changelog[:post_start] + changelog[sprint97_start:]
insert_at = without_post.index(previous_heading)
changelog = without_post[:insert_at] + post_block + without_post[insert_at:]
assert changelog.startswith("# Changelog\n\n## 0.21.86 - 2026-08-17")
assert changelog.count(post_heading) == 1
changelog_path.write_text(changelog, encoding="utf-8")

# Remove this one-shot machinery from the generated correction commit.
(ROOT / "tools/apply_metropolitan_v02_final_fixes.py").unlink(missing_ok=True)
(ROOT / ".github/workflows/temporary-metropolitan-v02-final-fixes.yml").unlink(missing_ok=True)
