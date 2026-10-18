---
name: render-pixel-gate
description: Verify that art assets actually appear on screen by measuring rendered pixels instead of grepping source. Use when a game/app "has the sprites" but plays like grey boxes, when assets are generated but not wired into the play scene, when a gate counts load.image/add.image calls, or when you need an objective rendered-richness check (unique colours, top-N colour share) on a screenshot. Exit code 3 means "could not measure", never a pass.
---

# render-pixel-gate

A source-level check ("does the scene reference sprites?") passes when sprites are loaded but drawn
off-screen or at alpha 0. Measure the **rendered output** instead.

Idea: a grey-box screen is dominated by a few flat fills. Real sprite rendering spreads colour
through shading, outlines, dithering. Two axes, and **either one failing fails the gate**:

| Axis | Meaning | Default |
|---|---|---|
| unique colours (quantised to 6 bits/channel) | richness | >= 1200 |
| top-24 colours' share of all pixels | flat-fill dominance | <= 92 % |

The two axes catch different things: a screen can have plenty of distinct colours (a gradient) and still have almost all of its pixels in a couple of dozen flat fills.
The 6-bit quantisation means "unique colours" counts perceptually distinct colours, not exact RGB values.

## Use

```bash
python3 scripts/measure.py shot.png                       # defaults
python3 scripts/measure.py shot.png --min-colors 800 --max-top24 95
python3 scripts/measure.py missing.png                    # exit 3: could not measure
python3 tests/test_measure.py                             # synthetic grey-box vs rich image
```

Exit codes: `0` pass, `1` fail, `3` unmeasured (file missing, unreadable, or too small to be a play
canvas). Never treat 3 as a pass: if you could make the gate green by deleting Playwright, the gate
is decoration.

Capturing the screenshot (optional, see `scripts/capture.mjs`, status: draft - needs your app's
entry flow): launch the built app, click through lobby buttons until the **largest canvas** exceeds a
minimum size (ignore decorative canvases), screenshot that canvas. Don't click only `<button>`:
clickable cards are often plain `<div>`s.

## Calibrate honestly

- The defaults are starting points taken from a small number of builds, not universal constants. With few known-good controls, a legitimately tight-palette game may land in the gap. When that happens, do
  **not** delete the gate: add that game as a new control and re-calibrate.
- One still frame cannot prove a sprite is visible at every moment.
- Scope: only run on projects that invested in sprites (e.g. >= 20 image files). Otherwise report
  "not applicable", explicitly, instead of a silent skip.

Runtime dependency: install `requirements.txt` with `python3 -m pip install -r requirements.txt`. Pillow must be at least 12.3.0; optional model dependencies listed above are separate.
