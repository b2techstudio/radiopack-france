#!/usr/bin/env python3
"""Security invariants for RadioPack France's static website and CI configuration."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"
WORKFLOWS = ROOT / ".github" / "workflows"


def fail(message: str) -> None:
    raise AssertionError(message)


# 1. Cloudflare Pages security headers must be present for all static responses.
headers_path = WEBSITE / "public" / "_headers"
headers = headers_path.read_text(encoding="utf-8")
required_headers = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Strict-Transport-Security": "max-age=31536000",
    "X-Permitted-Cross-Domain-Policies": "none",
}
for name, value in required_headers.items():
    if f"{name}: {value}" not in headers:
        fail(f"Missing security header: {name}: {value}")

if "Permissions-Policy:" not in headers:
    fail("Permissions-Policy is missing")
if "Content-Security-Policy:" not in headers:
    fail("Content-Security-Policy is missing")

csp_line = next(line.strip() for line in headers.splitlines() if "Content-Security-Policy:" in line)
for directive in [
    "default-src 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "frame-ancestors 'none'",
    "form-action 'self'",
    "script-src 'self' 'unsafe-inline'",
    "style-src 'self' 'unsafe-inline'",
    "connect-src 'self'",
    "upgrade-insecure-requests",
]:
    if directive not in csp_line:
        fail(f"CSP directive missing: {directive}")


# 2. Prevent common DOM-XSS/code execution sinks in first-party frontend source.
source_files = [
    path
    for path in (WEBSITE / "src").rglob("*")
    if path.is_file() and path.suffix in {".astro", ".ts", ".js", ".mjs"}
]
dangerous_patterns = {
    "innerHTML": re.compile(r"\.innerHTML\s*="),
    "outerHTML": re.compile(r"\.outerHTML\s*="),
    "insertAdjacentHTML": re.compile(r"\.insertAdjacentHTML\s*\("),
    "document.write": re.compile(r"document\.write\s*\("),
    "eval": re.compile(r"(?:^|[^\w])eval\s*\("),
    "Function constructor": re.compile(r"new\s+Function\s*\("),
    "javascript URL": re.compile(r"(?:href\s*=\s*[\"']|location\s*=\s*[\"'])javascript:", re.I),
}
for path in source_files:
    text = path.read_text(encoding="utf-8")
    for label, pattern in dangerous_patterns.items():
        if pattern.search(text):
            fail(f"Dangerous frontend sink {label} in {path.relative_to(ROOT)}")

# set:html is permitted only for escaped, repository-controlled JSON-LD in BaseLayout.
set_html_hits: list[tuple[str, str]] = []
for path in source_files:
    for line in path.read_text(encoding="utf-8").splitlines():
        if "set:html" in line:
            set_html_hits.append((str(path.relative_to(ROOT)), line.strip()))
expected_set_html = [
    ("website/src/layouts/BaseLayout.astro", '<script type="application/ld+json" set:html={structuredDataJSON} />')
]
if set_html_hits != expected_set_html:
    fail(f"Unexpected set:html usage: {set_html_hits!r}")

layout = (WEBSITE / "src" / "layouts" / "BaseLayout.astro").read_text(encoding="utf-8")
if '.replace(/</g, "\\u003c")' not in layout:
    fail("JSON-LD set:html value is not escaping '<'")

# target=_blank must explicitly prevent opener access.
blank_link = re.compile(r"<a\b(?=[^>]*target=[\"']_blank[\"'])[^>]*>", re.I | re.S)
for path in source_files:
    text = path.read_text(encoding="utf-8")
    for match in blank_link.finditer(text):
        tag = match.group(0)
        rel_match = re.search(r"rel=[\"']([^\"']+)[\"']", tag, re.I)
        if not rel_match or not ({"noopener", "noreferrer"} & set(rel_match.group(1).lower().split())):
            fail(f"target=_blank without noopener/noreferrer in {path.relative_to(ROOT)}: {tag}")


# 3. Public download registry may only point to same-origin download paths.
registry = (WEBSITE / "src" / "lib" / "packRegistry.ts").read_text(encoding="utf-8")
for url in re.findall(r'downloadUrl:\s*"([^"]+)"', registry):
    if not url.startswith("/downloads/") or "://" in url or "\\" in url or ".." in url:
        fail(f"Unsafe public download URL: {url}")

# Redirect destinations must remain same-origin paths; no open redirect target.
redirects = (WEBSITE / "public" / "_redirects").read_text(encoding="utf-8")
for raw in redirects.splitlines():
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split()
    if len(parts) < 2:
        fail(f"Malformed redirect: {line}")
    destination = parts[1]
    if not destination.startswith("/") or "://" in destination or destination.startswith("//"):
        fail(f"Potential open redirect target: {destination}")


# 4. High-signal secret/private-key checks on tracked text sources.
forbidden_names = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
    "credentials.json", "service-account.json",
}
for path in ROOT.rglob("*"):
    if path.is_file() and path.name in forbidden_names:
        fail(f"Sensitive filename tracked: {path.relative_to(ROOT)}")
    if path.is_file() and path.suffix.lower() in {".pem", ".p12", ".pfx", ".key"}:
        fail(f"Sensitive key/certificate file tracked: {path.relative_to(ROOT)}")

secret_patterns = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub classic token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
text_suffixes = {".md", ".txt", ".json", ".csv", ".py", ".ts", ".js", ".mjs", ".astro", ".yml", ".yaml"}
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in text_suffixes:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for label, pattern in secret_patterns.items():
        if pattern.search(text):
            fail(f"Possible {label} in {path.relative_to(ROOT)}")


# 5. GitHub Actions: least privilege, immutable action pins, no dangerous trigger.
sha_pin = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}(?:\s+#.*)?$")
for path in sorted(WORKFLOWS.glob("*.yml")):
    text = path.read_text(encoding="utf-8")
    if "pull_request_target:" in text:
        fail(f"pull_request_target is forbidden in {path.relative_to(ROOT)}")
    if "write-all" in text or re.search(r"contents:\s*write", text):
        fail(f"Broad repository write permission in {path.relative_to(ROOT)}")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("uses:"):
            value = stripped.removeprefix("uses:").strip()
            if value.startswith("./"):
                continue
            if not sha_pin.match(value):
                fail(f"Action is not pinned to a full commit SHA in {path.relative_to(ROOT)}: {value}")
        if "uses: actions/checkout@" in stripped:
            # checkout steps must be followed by an explicit persist-credentials: false nearby.
            lines = text.splitlines()
            index = lines.index(line)
            nearby = "\n".join(lines[index:index + 8])
            if "persist-credentials: false" not in nearby:
                fail(f"checkout persists credentials in {path.relative_to(ROOT)}")

# The main CI may grant statuses:write only to the status-reporting job, never globally.
ci = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")
prefix_before_jobs = ci.split("jobs:", 1)[0]
if "statuses: write" in prefix_before_jobs:
    fail("statuses:write must not be a global CI permission")
if "report-status:" not in ci or "statuses: write" not in ci.split("report-status:", 1)[1]:
    fail("report-status job is missing its scoped statuses:write permission")


# 6. npm lockfile must exist and use modern integrity-aware format.
lock = json.loads((WEBSITE / "package-lock.json").read_text(encoding="utf-8"))
if lock.get("lockfileVersion") != 3:
    fail("website/package-lock.json must use lockfileVersion 3")
if "astro" not in lock.get("packages", {}).get("", {}).get("dependencies", {}):
    fail("Astro dependency missing from lockfile root")

print(
    "Security hardening tests: headers/CSP, DOM-XSS sinks, same-origin downloads/redirects, "
    "secret patterns, GitHub Actions least privilege/SHA pins, and npm lockfile OK"
)
