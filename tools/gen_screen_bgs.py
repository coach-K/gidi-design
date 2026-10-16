"""Abstract brand backgrounds for Splash / District intro (no screenshots, no text/logos/people).
Rendered at 2340x1080; desktop = centre 1920 crop, so the composition is safe for both."""
import numpy as np, random, os
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = f"{ROOT}/exports/unity/screens"
W, H = 2340, 1080
def hexc(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def grad(stops):
    y = np.linspace(0, 1, H)[:, None]; img = np.zeros((H, 1, 3))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (y >= a) & (y <= b); t = np.clip((y - a) / (b - a), 0, 1)
        img = np.where(m[..., None], np.array(hexc(ca)) * (1 - t[..., None]) + np.array(hexc(cb)) * t[..., None], img)
    return Image.fromarray(np.repeat(img, W, 1).astype(np.uint8)).convert("RGBA")
def make(seed, stops, horizon, bokeh_n, lanes=True, glow=.55):
    random.seed(seed); im = grad(stops)
    # horizon glow
    g = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(g)
    d.ellipse([W*.15, horizon-260, W*.85, horizon+200], fill=hexc("#F28C4B") + (int(255*glow*.5),))
    im = Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(160)))
    # skyline blocks (abstract)
    s = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(s); x = -40
    while x < W:
        w = random.randint(90, 240); h = random.randint(80, 330)
        d.rectangle([x, horizon - h, x + w, horizon + 40], fill=(16, 18, 34, 230))
        for _ in range(random.randint(2, 7)):   # lit windows
            wx = x + random.randint(10, max(11, w - 20)); wy = horizon - random.randint(20, max(21, h - 10))
            d.rectangle([wx, wy, wx + 10, wy + 14], fill=hexc(random.choice(["#FAE69E", "#F2C230", "#F28C4B"])) + (200,))
        x += w + random.randint(-10, 30)
    im = Image.alpha_composite(im, s.filter(ImageFilter.GaussianBlur(14)))
    # road + zebra lanes in perspective
    if lanes:
        r = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(r)
        d.polygon([(W*.38, horizon+30), (W*.62, horizon+30), (W*1.1, H), (-W*.1, H)], fill=(20, 22, 30, 235))
        for i in range(6):
            t0 = i / 6; t1 = t0 + .055
            y0 = horizon + 30 + (H - horizon - 30) * t0**1.6; y1 = horizon + 30 + (H - horizon - 30) * t1**1.6
            k0 = .12 + .48 * t0**1.6; k1 = .12 + .48 * t1**1.6
            d.polygon([(W*(.5-k0), y0), (W*(.5+k0), y0), (W*(.5+k1), y1), (W*(.5-k1), y1)], fill=(232, 226, 208, 70))
        im = Image.alpha_composite(im, r.filter(ImageFilter.GaussianBlur(10)))
    # bokeh: headlights, danfo yellow, LASTMA pink, teal, warm street lights (kept inside the centre 1920 x 80%)
    im = im.filter(ImageFilter.GaussianBlur(26)).convert("RGB")
    b = Image.new("RGB", (W, H)); d = ImageDraw.Draw(b)
    cols = ["#FAE69E"] * 5 + ["#F2C230"] * 4 + ["#F28C4B"] * 4 + ["#E8B21E"] * 3 + ["#59D9B8"] + ["#E07CC0"]
    for _ in range(bokeh_n):   # street lights / headlights along the horizon band, inside the centre 1920 x 70%
        cx = random.uniform(W*.15, W*.85); cy = random.gauss(horizon - 90, 120); rr = random.choice([18, 26, 34, 46, 62])
        k = random.uniform(.25, .6); c = hexc(random.choice(cols))
        d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=tuple(int(v*k) for v in c))
    b = b.filter(ImageFilter.GaussianBlur(16))
    A = np.array(im).astype(float); B = np.array(b).astype(float)
    im = Image.fromarray((255 - (255 - A) * (255 - B) / 255).astype(np.uint8))   # screen blend = glow
    # calm edges: vignette to ink
    yy, xx = np.mgrid[0:H, 0:W]; dx = (xx - W/2) / (W/2); dy = (yy - H/2) / (H/2)
    v = np.clip(1 - 0.55 * (np.maximum(np.abs(dx) - .55, 0) / .45)**1.5 - 0.45 * (np.maximum(np.abs(dy) - .5, 0) / .5)**1.5, 0, 1)[..., None]
    a = np.array(im).astype(float); ink = np.array(hexc("#0F1219"))
    a = a * v + ink * (1 - v)
    a += np.random.default_rng(seed).normal(0, 2.2, a.shape)   # fine grain against banding
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
splash = make(7, [(0, "#14162E"), (.45, "#2B2F5C"), (.62, "#5A3A52"), (.75, "#2A2238"), (1, "#0F1219")], 640, 70, glow=.9)
intro = make(21, [(0, "#0F1219"), (.35, "#1E2142"), (.56, "#4A3350"), (.70, "#241E33"), (1, "#0A0C12")], 600, 55, glow=.7)
x0 = (W - 1920) // 2
for name, img in (("bg_splash", splash), ("bg_intro", intro)):
    ph = f"{name}_phone_blur.png"; dk = f"{name}_desktop_blur.png" if name == "bg_splash" else f"{name}_blur.png"
    img.save(f"{OUT}/{ph}"); img.crop((x0, 0, x0 + 1920, H)).save(f"{OUT}/{dk}")
print(sorted(os.listdir(OUT)))
