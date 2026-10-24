"""RT-116 district-intro backgrounds: one per level L1-L10, clean (not blurred), from the cleaned + dusk-graded level screenshots
(assets/bg/Lxx_{desktop,phone}.png, tools/prep_levels.py). Bakes a feathered calm zone (darken + 35% desaturate) behind the
1180x660 intro card (centred, 40 px above the safe-area centre) and a light edge vignette. Output: exports/unity/screens/intro/."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/exports/unity/screens/intro"; os.makedirs(OUT, exist_ok=True)
SAFE = {1920: (32, 32, 32, 32), 2340: (132, 132, 24, 63)}   # l, r, t, b
CARD = (1184, 664); ZONE_PAD = (110, 80); FEATHER = 90; ZONE_DARK = .58; EDGE = .35

def make(src, w, h):
    im = Image.open(src).convert("RGB").resize((w, h), Image.LANCZOS)
    l, r, t, b = SAFE[w]; cx = l + (w - l - r) / 2; cy = t + (h - t - b) / 2 - 40
    cw, ch = CARD[0] + 2 * ZONE_PAD[0], CARD[1] + 2 * ZONE_PAD[1]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((cx - cw/2, cy - ch/2, cx + cw/2, cy + ch/2), radius=120, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(FEATHER))
    calm = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(.65)).enhance(1 - ZONE_DARK)
    im = Image.composite(calm, im, m)
    v = Image.new("L", (w, h), 0); ImageDraw.Draw(v).rectangle((0, 0, w, h), fill=int(255 * EDGE))
    ImageDraw.Draw(v).ellipse((-w*.1, -h*.15, w*1.1, h*1.15), fill=0)
    v = v.filter(ImageFilter.GaussianBlur(120))
    return Image.composite(Image.new("RGB", (w, h), (15, 18, 25)), im, v)

if __name__ == "__main__":
    for n in range(1, 11):
        make(f"{ROOT}/assets/bg/L{n:02d}_desktop.png", 1920, 1080).save(f"{OUT}/bg_intro_L{n:02d}.png", optimize=True)
        make(f"{ROOT}/assets/bg/L{n:02d}_phone.png", 2340, 1080).save(f"{OUT}/bg_intro_L{n:02d}_phone.png", optimize=True)
    print("ok")
