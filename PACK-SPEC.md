# Cosy Scene Pack spec — v1 (draft)

A pack is a zip with this layout:

  pack.json        # required: manifest (below)
  landmark.svg     # required: skyline/hito in vector paths, 1920x1080 viewBox
  preview.png      # optional: 1920x1080 preview for the picker

## pack.json

```json
{
  "spec": 1,
  "id": "quito",
  "name": "Quito",
  "author": "tu-usuario",
  "version": 1,
  "palettes": {
    "dawn":  { "s1": "#2E3A6B", "s2": "#C98A9A", "s3": "#F6C99A",
               "h1": "#7C6A93", "h2": "#54497A", "h3": "#2E2A4E" },
    "day":   { "s1": "#4F9CCB", "s2": "#93C6E4", "s3": "#D8EEF6",
               "h1": "#8DB59A", "h2": "#64957A", "h3": "#3F6E55" },
    "dusk":  { "s1": "#2F2350", "s2": "#B4506A", "s3": "#F2A65A",
               "h1": "#7A4560", "h2": "#4E2C4A", "h3": "#24162E" },
    "night": { "s1": "#04060E", "s2": "#0B1230", "s3": "#1A2550",
               "h1": "#1B2A3A", "h2": "#121E2A", "h3": "#0A121C" }
  },
  "weather": ["clear", "cloudy", "rain", "fog"],
  "landmark": { "file": "landmark.svg", "glowAtNight": true }
}
```

Rules: `spec` 1, `id` unique, colors `#RRGGBB`, `weather` only from the
engine list. The engine ignores unknown keys (forward compatible).
Packs never execute code: the launcher only reads JSON + SVG paths.
