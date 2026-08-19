#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / "tools/apply_sprint98_state.py"
text = target.read_text(encoding="utf-8")

# The one-shot GitHub Actions token may write repository content, but GitHub
# deliberately rejects workflow-file updates without the workflows permission.
# Keep workflow edits for the authenticated connector and let this generated
# commit contain only docs/state/research/tests/tools content.
start = text.find('    ci = ROOT / ".github/workflows/ci.yml"')
end = text.find("\n\ndef main()", start)
if start == -1 or end == -1:
    raise RuntimeError("Unable to locate Sprint 98 CI mutation block")
text = text[:start] + text[end:]

restore_line = '    (ROOT / ".github/workflows/annecy-v04-guards.yml").write_text(ORIGINAL_ANNECY_WORKFLOW, encoding="utf-8")\n'
if restore_line not in text:
    raise RuntimeError("Unable to locate temporary workflow restore line")
text = text.replace(restore_line, "", 1)

target.write_text(text, encoding="utf-8")
Path(__file__).unlink()
print("Sprint 98 bootstrap sanitized: workflow files will be updated separately")
