# canvas-render-pixel-gate

**Detect grey-box screenshots: measure unique colors and flat-fill share of a rendered game canvas, and refuse to pass what it could not measure.**

[![test](https://github.com/Kein-chronicle/canvas-render-pixel-gate/actions/workflows/test.yml/badge.svg)](https://github.com/Kein-chronicle/canvas-render-pixel-gate/actions/workflows/test.yml) ![license](https://img.shields.io/badge/license-MIT-blue.svg)

## Why

"It renders" is not "it looks like a game". A screen built from a few flat rectangles passes every structural test. This gate counts distinct colors and how much of the image the top 24 colors cover, with no baseline image needed.

## Install

**As a Claude Code skill** (Claude uses it when the task matches the skill description):

```sh
git clone https://github.com/Kein-chronicle/canvas-render-pixel-gate.git ~/.claude/skills/render-pixel-gate
```

For a single project, clone into `<project>/.claude/skills/render-pixel-gate` instead, then start a new Claude Code session.

**As plain scripts:**

```sh
git clone https://github.com/Kein-chronicle/canvas-render-pixel-gate.git
cd canvas-render-pixel-gate
```

**Requires:** Node.js 22+ and Python 3.10+, Pillow.

Use the security-patched Pillow runtime:

```sh
python3 -m pip install -r requirements.txt
```

## Quick start

Measure a grey-box and a rich image:

```console
$ bash examples/demo.sh
# Does the rendered play canvas look like flat rectangles?
$ python3 scripts/measure.py .demo-tmp/greybox.png
FAIL 400x400 unique_colors=4 top24_share=100.0% (need colors>=1200 and top24<=92.0%): screen is dominated by flat fills
[exit 1]

$ python3 scripts/measure.py .demo-tmp/rich.png
PASS 400x400 unique_colors=119135 top24_share=0.1%
[exit 0]

# A screenshot that does not exist is 'unmeasured' (3), never a pass
$ python3 scripts/measure.py .demo-tmp/nope.png
UNMEASURED: .demo-tmp/nope.png not found
[exit 3]
```

The output above is real: it is produced by the files in `examples/`.

## Use it on your own files

```sh
python3 scripts/measure.py screenshot.png --min-colors 800 --max-top24 95
```

Sample inputs for every file format are in `examples/` and `tests/`; the details are in [SKILL.md](SKILL.md).

## What it checks

- `measure.py shot.png [--min-colors N --max-top24 P]`: exit `0` pass, `1` flat fills dominate, `3` unmeasured. "Unique colors" are quantised to 6 bits per channel.
- A missing, unreadable or tiny (decorative) canvas is `3`, never a pass.
- `scripts/capture.mjs` is an untested draft Playwright capture helper that picks the largest canvas and clicks through the page: review it before running it on anything but your own build (`npm install playwright`).

## Limits

- Richness is not beauty: a noisy image passes.
- Thresholds are starting points; calibrate on your own screens.

## Related projects

These solve neighbouring problems; use them when they fit better.

- **Playwright screenshot comparison / pixelmatch**: compare against a baseline; this needs none

## More from the same collection

Small, tested tools that grew out of running AI agents and game/app pipelines for months:

- [**web-game-asset-reality-check**](https://github.com/Kein-chronicle/web-game-asset-reality-check): Catch web-game bugs the type checker can't: fonts that are declared but not shipped, runtime CDN dependencies, and page errors from headless Chromium.
- [**ffmpeg-video-qa-gates**](https://github.com/Kein-chronicle/ffmpeg-video-qa-gates): Machine QA for short videos with ffmpeg: frozen frames, dead air, loudness, true peak, size, a busy opening, and readable subtitle timing.
- [**cold-read-comprehension-review**](https://github.com/Kein-chronicle/cold-read-comprehension-review): Grade whether a video or page communicates, using independent cold readers checked against the author's truth file, and flag stale judgements.

## Development

```sh
python3 tests/test_measure.py
```

The tests include inputs that are supposed to be rejected, so a green run also shows the checks can fail. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

If this saved you a debugging session, a star helps other people find it. Bug reports and failing test cases are even better.

<sub>Keywords: game-development, testing, visual-testing, screenshot, canvas, qa, claude-skills, playwright</sub>
