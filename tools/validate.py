#!/usr/bin/env python3
"""Validate a scene pack against PACK-SPEC v2. Usage: validate.py packs/<id>

Mirrors what ScenePack.fromJson enforces on device: spec == 2, required
structure, colors, op shapes, and the M/L/C/Z-only pathData subset (no
exponents, arcs, or other SVG commands — the in-app parser rejects them).
Unknown JSON keys are ignored (forward compatible); a missing phase only
warns (the engine falls back to the builtin valle palette for that phase).
"""

import json
import re
import sys
from pathlib import Path

COLOR = re.compile(r"^#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
PHASES = ("dawn", "day", "dusk", "night")
PALETTE_KEYS = ("s1", "s2", "s3", "h1", "h2", "h3", "win")
OP_COLORS = ("h1", "h2", "h3", "win")
NUM = r"[+-]?(?:\d+\.?\d*|\.\d+)"
PATHDATA = re.compile(
    r"^\s*(?:[MmLl]\s*NUM(?:[\s,]+NUM\s*)?|"
    r"[Cc]\s*NUM(?:[\s,]+NUM\s*){5}|[Zz]\s*)+$".replace("NUM", NUM)
)


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def warn(msg):
    print(f"WARN: {msg}")


def check_pathdata(d, where):
    if not isinstance(d, str) or not d.strip():
        fail(f"empty pathData at {where}")
    if "e" in d.lower().replace(" ", "") and re.search(
        r"\de[+-]?\d", d.lower().replace(" ", "")
    ):
        fail(f"exponent in pathData at {where} (parser accepts plain decimals only)")
    PATHDATA.match(d) or fail(
        f"bad pathData at {where} (only M/L/C/Z commands, no exponents/arcs)"
    )


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


d = Path(sys.argv[1]) if len(sys.argv) > 1 else fail("usage: validate.py packs/<id>")
try:
    m = json.loads((d / "pack.json").read_text())
except (OSError, ValueError) as e:
    fail(f"pack.json unreadable: {e}")

m.get("spec") == 2 or fail("spec must be 2")
m.get("id") == d.name or fail("id must match folder name")

pals = m.get("palettes") or fail("missing palettes object")
for ph in PHASES:
    pal = pals.get(ph)
    if pal is None:
        warn(f"missing palette {ph} (engine falls back to builtin valle)")
        continue
    for k in PALETTE_KEYS:
        COLOR.match(pal.get(k, "") or "") or fail(f"bad color {ph}.{k}")
    if "glow" in pal and not is_num(pal["glow"]):
        fail(f"bad glow {ph}.glow (must be a number)")
    if "darkText" in pal and not isinstance(pal["darkText"], bool):
        fail(f"bad darkText {ph}.darkText (must be true/false)")

hills = m.get("hills")
(isinstance(hills, list) and len(hills) == 3) or fail(
    "hills must be exactly 3 pathData strings"
)
for i, h in enumerate(hills):
    check_pathdata(h, f"hills[{i}]")

for i, e in enumerate(m.get("ops") or []):
    where = f"ops[{i}]"
    op = e.get("op")
    op in ("rect", "oval", "circle", "path") or fail(f"unknown op at {where}: {op!r}")
    c = e.get("color", "h3")
    (c in OP_COLORS or (isinstance(c, str) and COLOR.match(c))) or fail(
        f"bad color at {where}: {c!r}"
    )
    if op in ("rect", "oval"):
        p = e.get("params")
        (isinstance(p, list) and len(p) == 4 and all(is_num(v) for v in p)) or fail(
            f"{op} needs 4 numeric params at {where}"
        )
    elif op == "circle":
        p = e.get("params")
        (isinstance(p, list) and len(p) == 3 and all(is_num(v) for v in p)) or fail(
            f"circle needs 3 numeric params at {where}"
        )
    else:
        check_pathdata(e.get("params"), f"{where}.params")

s = m.get("smoke")
if s is not None:
    (is_num(s.get("x")) and is_num(s.get("y"))) or fail("smoke needs numeric x/y")

for i, w in enumerate(m.get("windows") or []):
    (isinstance(w, list) and len(w) == 4 and all(is_num(v) for v in w)) or fail(
        f"windows[{i}] needs 4 numbers"
    )

print(f"OK: {m['id']} spec=2 ({m.get('name', '?')})")
