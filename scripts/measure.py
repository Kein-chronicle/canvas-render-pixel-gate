#!/usr/bin/env python3
"""render-pixel-gate: measure rendered richness of a screenshot.
exit 0 pass | 1 fail | 3 could not measure (never a pass)"""
import argparse, collections, os, sys

try:
    from PIL import Image
except ImportError:
    print("UNMEASURED: Pillow not installed (pip install pillow)"); sys.exit(3)


def measure(path, min_colors=1200, max_top24=92.0, min_side=200):
    if not os.path.isfile(path):
        return 3, f"UNMEASURED: {path} not found"
    try:
        im = Image.open(path).convert("RGB")
    except Exception as e:                       # unreadable file is not a pass
        return 3, f"UNMEASURED: cannot read image ({e})"
    w, h = im.size
    if min(w, h) < min_side:
        return 3, f"UNMEASURED: {w}x{h} is below {min_side}px - a decorative canvas, not the play screen"
    try: px = list(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata())     # getdata() is deprecated in newer Pillow
    except MemoryError: return 3, "UNMEASURED: image too large to analyse in memory - downscale the screenshot first"
    c = collections.Counter((r >> 2, g >> 2, b >> 2) for r, g, b in px)
    top24 = sum(v for _, v in c.most_common(24)) / len(px) * 100
    detail = f"{w}x{h} unique_colors={len(c)} top24_share={top24:.1f}%"
    if len(c) < min_colors or top24 > max_top24:
        return 1, f"FAIL {detail} (need colors>={min_colors} and top24<={max_top24}%): screen is dominated by flat fills"
    return 0, f"PASS {detail}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--min-colors", type=int, default=1200)
    ap.add_argument("--max-top24", type=float, default=92.0)
    a = ap.parse_args()
    code, msg = measure(a.image, a.min_colors, a.max_top24)
    print(msg); sys.exit(code)
