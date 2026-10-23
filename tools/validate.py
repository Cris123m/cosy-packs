#!/usr/bin/env python3
"""Validate a scene pack against PACK-SPEC v1. Usage: validate.py packs/<id>"""
import json, re, sys
from pathlib import Path
COLOR = re.compile(r'^#[0-9A-Fa-f]{6}$')
PHASES = ("dawn", "day", "dusk", "night")
KEYS = ("s1", "s2", "s3", "h1", "h2", "h3")
WEATHERS = {"clear", "cloudy", "rain", "snow", "fog", "thunderstorm"}
def fail(msg):
    print(f"ERROR: {msg}"); sys.exit(1)
d = Path(sys.argv[1]) if len(sys.argv) > 1 else fail("usage: validate.py packs/<id>")
m = json.loads((d / "pack.json").read_text())
m.get("spec") == 1 or fail("spec must be 1")
m.get("id") == d.name or fail("id must match folder name")
for ph in PHASES:
    pal = (m.get("palettes") or {}).get(ph) or fail(f"missing palette {ph}")
    for k in KEYS:
        COLOR.match(pal.get(k, "")) or fail(f"bad color {ph}.{k}")
set(m.get("weather", [])) <= WEATHERS or fail("unknown weather effect")
(d / (m.get("landmark") or {}).get("file", "")).exists() or fail("landmark.svg missing")
print(f"OK: {m['id']} v{m.get('version', '?')} ({m.get('name')})")
