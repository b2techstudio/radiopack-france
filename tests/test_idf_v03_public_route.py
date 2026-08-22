#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv"
HISTORICAL_ROUTE = ROOT / "website/src/pages/downloads/[slug]/[file].csv.ts"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

assert PUBLIC.is_file()
assert HISTORICAL_ROUTE.is_file()
registry = REGISTRY.read_text(encoding="utf-8")
assert 'version: "v0.3"' in registry
assert 'memoryCount: 57' in registry
assert '/downloads/${item.id}/${filename}' in registry

print("IDF v0.3 public route present; historical dynamic metropolitan routes retained OK")
