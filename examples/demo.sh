#!/usr/bin/env bash
cd "$(dirname "$0")/.."
run() { printf '$ %s\n' "$*"; "$@"; printf '[exit %s]\n\n' "$?"; }
tmp=.demo-tmp; rm -rf "$tmp"; mkdir "$tmp"; trap 'rm -rf "$tmp"' EXIT
python3 - "$tmp" <<'PY'
import random, sys
from PIL import Image, ImageDraw
d = sys.argv[1]
g = Image.new("RGB", (400, 400), (30, 30, 30)); dr = ImageDraw.Draw(g)       # three flat rectangles: a grey-box
for i, col in enumerate([(200, 40, 40), (40, 200, 40), (40, 40, 200)]): dr.rectangle([20 + i * 120, 100, 100 + i * 120, 300], fill=col)
g.save(d + "/greybox.png")
random.seed(7); r = Image.new("RGB", (400, 400))                              # a noisy gradient: lots of distinct colours
r.putdata([((x * 3 + random.randint(0, 60)) % 256, (y * 3 + random.randint(0, 60)) % 256, (x + y + random.randint(0, 90)) % 256) for y in range(400) for x in range(400)])
r.save(d + "/rich.png")
PY
echo "# Does the rendered play canvas look like flat rectangles?"
run python3 scripts/measure.py "$tmp/greybox.png"
run python3 scripts/measure.py "$tmp/rich.png"
echo "# A screenshot that does not exist is 'unmeasured' (3), never a pass"
run python3 scripts/measure.py "$tmp/nope.png"
