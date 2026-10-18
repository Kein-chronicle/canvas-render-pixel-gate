import os, random, subprocess, sys, tempfile
from PIL import Image, ImageDraw
here = os.path.dirname(os.path.abspath(__file__)); script = os.path.join(here, "..", "scripts", "measure.py")
d = tempfile.mkdtemp(); ok = True

def run(p, *extra):
    return subprocess.run([sys.executable, script, p, *extra], capture_output=True, text=True).returncode

def expect(name, got, want):
    global ok; good = got == want; ok &= good; print(("ok   " if good else "FAIL ") + f"{name}: exit {got} (want {want})")

# grey-box: a few flat rectangles
g = Image.new("RGB", (400, 400), (30, 30, 30)); dr = ImageDraw.Draw(g)
for i, col in enumerate([(200, 40, 40), (40, 200, 40), (40, 40, 200)]): dr.rectangle([20+i*120, 100, 100+i*120, 300], fill=col)
gp = os.path.join(d, "greybox.png"); g.save(gp)
# rich: seeded noisy gradient with many colours
random.seed(7); r = Image.new("RGB", (400, 400))
r.putdata([((x*3 + random.randint(0, 60)) % 256, (y*3 + random.randint(0, 60)) % 256, (x+y+random.randint(0, 90)) % 256) for y in range(400) for x in range(400)])
rp = os.path.join(d, "rich.png"); r.save(rp)
tiny = os.path.join(d, "tiny.png"); Image.new("RGB", (73, 73)).save(tiny)

expect("grey-box fails", run(gp), 1)
expect("rich render passes", run(rp), 0)
expect("missing file is unmeasured, not pass", run(os.path.join(d, "nope.png")), 3)
expect("decorative tiny canvas is unmeasured", run(tiny), 3)
sys.exit(0 if ok else 1)
