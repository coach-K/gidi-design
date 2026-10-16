"""Souvenirs & Perks sprites (RT-107) -> exports/unity/souvenirs/{1x,2x}/ (same filenames in both). Adds entries to exports/unity/manifest.json."""
import os, sys, json, re, subprocess
from PIL import Image, ImageEnhance
sys.path.insert(0, os.path.dirname(__file__))
from brand import icon, badge, P
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = f"{ROOT}/exports/unity"; OUT = f"{U}/souvenirs"
def sized(svg, n): return re.sub(r'width="\d+" height="\d+"', f'width="{n}" height="{n}"', svg, count=1)
items = [(f"souvenir_L{i:02d}", 256, sized(open(f"{ROOT}/souvenirs/souvenir_L{i:02d}.svg").read(), 256)) for i in range(1, 11)]
plus = '<div style="position:absolute;right:0;bottom:0;width:26px;height:26px;border-radius:13px;background:#59D9B8;color:#0F1219;font:700 17px Jakarta,sans-serif;display:flex;align-items:center;justify-content:center">+1</div>'
items += [("perk_lives", 64, icon("lives", 64, "#FF6B7A")), ("perk_ad_continue", 64, icon("ad", 64)), ("perk_cashout", 64, icon("chip", 64)),
          ("perk_owa_capacity", 64, f'<div style="position:relative;width:64px;height:64px">{badge("owa", 64)}{plus}</div>')]
X = 0; cells = []
for n, s, h in items: cells.append((n, s, X, h)); X += s + 8
html = '<!doctype html><html><head><meta charset="utf-8"><style>@font-face{font-family:Jakarta;src:url(file://%s/fonts/PlusJakartaSans-Bold.ttf)}html,body{margin:0;background:transparent}</style></head><body style="position:relative;width:%dpx;height:256px">' % (ROOT, X)
html += "".join(f'<div style="position:absolute;left:{x}px;top:0;width:{s}px;height:{s}px">{h}</div>' for n, s, x, h in cells) + "</body></html>"
open("/tmp/souv.html", "w").write(html)
man = []
for sc in (1, 2):
    o = f"/tmp/souv@{sc}.png"
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={sc}", "--default-background-color=00000000",
                    f"--window-size={X},556", f"--screenshot={o}", "file:///tmp/souv.html"], stderr=subprocess.DEVNULL)
    sh = Image.open(o).convert("RGBA"); d = f"{OUT}/{sc}x"; os.makedirs(d, exist_ok=True)
    for n, s, x, h in cells:
        im = sh.crop((x*sc, 0, (x+s)*sc, s*sc)); im.save(f"{d}/{n}.png")
        if n.startswith("souvenir"):   # not-found: desaturated, ~45% brightness and alpha
            rgb = ImageEnhance.Brightness(ImageEnhance.Color(im.convert("RGB")).enhance(0)).enhance(0.45)
            a = im.getchannel("A").point(lambda v: int(v*0.45)); rgb.putalpha(a); rgb.save(f"{d}/{n}_dim.png")
for n, s, x, h in cells:
    for v in ([n, n+"_dim"] if n.startswith("souvenir") else [n]):
        man.append(dict(name=v, file=f"souvenirs/1x/{v}.png", file2x=f"souvenirs/2x/{v}.png", size=[s, s], pivot=[.5, .5], border=None, screen="souvenirs",
                        note=("Not-found state: desaturated, 45% brightness and alpha." if v.endswith("_dim") else "Souvenir (found)." if n.startswith("souvenir") else "Perk icon (Souvenirs & Perks page).")))
mf = json.load(open(f"{U}/manifest.json"))
mf["sprites"] = [x for x in mf["sprites"] if x.get("screen") != "souvenirs"] + man
json.dump(mf, open(f"{U}/manifest.json", "w"), indent=1, ensure_ascii=False)
print(len(man), "entries")
