# Cosy Scene Pack spec — v2

A pack is a folder with this layout:

  pack.json        # required: manifest (below)
  preview.png      # optional: 1920x1080 preview for the picker

## pack.json (v2)

```json
{
  "spec": 2,
  "id": "quito",
  "name": "Quito",
  "author": "tu-usuario",
  "version": 2,
  "palettes": {
    "dawn":  { "s1": "#2E3A6B", "s2": "#C98A9A", "s3": "#F6C99A",
               "h1": "#7C6A93", "h2": "#54497A", "h3": "#2E2A4E",
               "win": "#FFC27A", "glow": 0.5, "darkText": false },
    "day":   { "s1": "#4F9CCB", "s2": "#93C6E4", "s3": "#D8EEF6",
               "h1": "#8DB59A", "h2": "#64957A", "h3": "#3F6E55",
               "win": "#2B3A40", "glow": 0.0, "darkText": true },
    "dusk":  { "s1": "#2F2350", "s2": "#B4506A", "s3": "#F2A65A",
               "h1": "#7A4560", "h2": "#4E2C4A", "h3": "#24162E",
               "win": "#FFB35C", "glow": 0.75, "darkText": false },
    "night": { "s1": "#04060E", "s2": "#0B1230", "s3": "#1A2550",
               "h1": "#161D36", "h2": "#0E1326", "h3": "#070A14",
               "win": "#FFB35C", "glow": 1.0, "darkText": false }
  },
  "weather": ["clear", "cloudy", "rain", "fog"],
  "hills": [
    "M0,720 C240,640 420,660 640,700 C860,740 1040,640 1280,650 C1500,660 1700,720 1920,690 L1920,1080 L0,1080 Z",
    "M0,820 C260,760 520,790 760,820 C1000,850 1240,760 1500,770 C1700,778 1820,800 1920,790 L1920,1080 L0,1080 Z",
    "M0,940 C300,880 640,900 900,930 C1160,960 1440,900 1700,905 C1800,907 1880,915 1920,920 L1920,1080 L0,1080 Z"
  ],
  "ops": [
    { "op": "rect", "params": [1520, 722, 1610, 778], "color": "h3" },
    { "op": "path", "params": "M1508,726 L1565,684 L1622,726 Z", "color": "h3" }
  ],
  "smoke": { "x": 1595, "y": 680 },
  "windows": [[1540, 738, 1558, 754]]
}
```

Rules:

- `spec` must be 2; `id` must match the folder name.
- Palette colors are `#RRGGBB` (or `#AARRGGBB`); every phase needs
  `s1 s2 s3 h1 h2 h3 win`, plus optional numeric `glow` (window-glow
  strength) and boolean `darkText` (dark clock text on bright skies).
  A missing phase only warns: the engine falls back to the builtin
  valle palette for that phase.
- `hills` is exactly 3 ridge pathData strings (far, mid, near), drawn
  in 1920x1080 design space.
- `ops` are landmark shapes drawn between the mid and near hills:
  `rect`/`oval` take `[l,t,r,b]`, `circle` takes `[cx,cy,r]`, `path`
  takes an SVG pathData string. Colors are palette names
  (`h1 h2 h3 win`) or a literal `#RRGGBB`.
- pathData uses only `M L C Z` commands (upper or lower case) with
  plain decimals — no exponents, arcs, or other SVG commands; the
  in-app parser rejects anything else.
- `smoke` (optional) is the chimney anchor `{x, y}` smoke rises from;
  omit it and the pack has no smoke. `windows` (optional) are lit
  window rects `[l,t,r,b]`; their bounding-box centre is the night-glow
  centre. `weather` is advisory, from the engine list only.
- The engine ignores unknown keys (forward compatible).
- Packs never execute code: the launcher only reads JSON + pathData.

## v1 (deprecated)

v1 packs (`spec: 1`, `landmark.svg` + palettes without `win`) are
rejected by the engine. See git history for the old layout.
