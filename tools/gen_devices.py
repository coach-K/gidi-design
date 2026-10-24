"""Landscape device templates (safe areas) + device-framed mockups. Output: mockups/dev-*.html -> exports/devices/*.png"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import ROOT, icon, P
OUT = f"{ROOT}/mockups"; EXP = f"{ROOT}/exports/devices"
DEV = {  # key: label, W, H, insets (l,r,t,b) px, cutout, corner radius
 "iphone": ("iPhone 15/16 Pro · 2556×1179 @3x (852×393 pt)", 2556, 1179, (177,177,0,63), "island", 165),
 "android": ("Android 20:9 punch-hole · 2400×1080 (~2.75x)", 2400, 1080, (110,0,0,48), "punch", 110),
 "ipad": ("iPad 11\" · 2388×1668 @2x (1194×834 pt)", 2388, 1668, (0,0,48,40), "none", 72),
 "web": ("Desktop / WebGL · 1920×1080 browser viewport", 1920, 1080, (32,32,32,32), "web", 0),
}
CSS = """@font-face{font-family:Jakarta;src:url(../fonts/PlusJakartaSans-Bold.ttf)}*{box-sizing:border-box;margin:0}body{background:#14162a;font-family:Jakarta,sans-serif;color:#F5F5F0}
.dev{position:absolute;background:#05060a;box-shadow:0 0 0 6px #3a3d48,0 30px 80px rgba(0,0,0,.6)}
.scr{position:absolute;overflow:hidden;background:#26272E}
.unsafe{position:absolute;background:repeating-linear-gradient(45deg,rgba(255,122,26,.38) 0 14px,rgba(255,122,26,.12) 14px 28px)}
.safe{position:absolute;outline:6px dashed #56B4E9;outline-offset:-3px}
.lab{position:absolute;font-size:30px;background:#0F1219;padding:6px 16px;border-radius:12px;white-space:nowrap}
.island{position:absolute;background:#000;border-radius:60px}.punch{position:absolute;background:#000;border-radius:50%}
.home{position:absolute;height:15px;border-radius:8px;background:#F5F5F0;opacity:.8}
.chrome{position:absolute;left:0;right:0;top:-90px;height:90px;background:#2a2d36;border-radius:16px 16px 0 0;display:flex;align-items:center;gap:14px;padding:0 24px;font-size:26px;color:#9EA3AD}
.chrome i{width:22px;height:22px;border-radius:50%;background:#555;display:inline-block}
.url{flex:1;background:#14162a;border-radius:12px;padding:10px 20px;margin-left:20px}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:60px 60px}"""

def page(key, framed=None):
    lab, W, H, (l,r,t,b), cut, rad = DEV[key]
    pad = 140; top = pad + (90 if key=="web" else 0)
    bez = 0 if key=="web" else 60
    CW, CH = W + 2*bez + 2*pad, H + 2*bez + top + pad + 80
    x0, y0 = pad + bez, top + bez
    inner = ""
    if framed:
        inner += f'<img src="../{framed}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
    else:
        inner += '<div class="grid"></div>'
        if l: inner += f'<div class="unsafe" style="left:0;top:0;bottom:0;width:{l}px"></div>'
        if r: inner += f'<div class="unsafe" style="right:0;top:0;bottom:0;width:{r}px"></div>'
        if t: inner += f'<div class="unsafe" style="left:0;right:0;top:0;height:{t}px"></div>'
        if b: inner += f'<div class="unsafe" style="left:0;right:0;bottom:0;height:{b}px"></div>'
        inner += f'<div class="safe" style="left:{l}px;right:{r}px;top:{t}px;bottom:{b}px"></div>'
        inner += f'<div class="lab" style="left:{l+40}px;top:{t+40}px;font-size:40px">Safe area {W-l-r}×{H-t-b} px</div>'
        inner += f'<div class="lab" style="left:{l+40}px;top:{t+110}px;color:#9EA3AD">insets L {l} · R {r} · T {t} · B {b} px · read <b style="color:#FAE69E">Screen.safeArea</b> at runtime</div>'
        inner += f'<div class="lab" style="left:{l+40}px;bottom:{b+40}px;color:#FAE69E">LANDSCAPE ONLY · touch: PICK UP bottom-left, d-pad bottom-right, inside the safe area</div>'
    if cut == "island": inner += f'<div class="island" style="left:30px;top:{H/2-190:.0f}px;width:110px;height:380px"></div>'
    if cut == "punch": inner += f'<div class="punch" style="left:36px;top:{H/2-34:.0f}px;width:68px;height:68px"></div>'
    if cut in ("island",) or key=="ipad": inner += f'<div class="home" style="left:{W/2-210:.0f}px;bottom:18px;width:420px"></div>'
    if key=="android": inner += f'<div class="home" style="left:{W/2-150:.0f}px;bottom:16px;width:300px;opacity:.6"></div>'
    dev = f'<div class="dev" style="left:{pad}px;top:{top}px;width:{W+2*bez}px;height:{H+2*bez}px;border-radius:{rad+bez if rad else 16}px">'
    if key=="web": dev += '<div class="chrome"><i></i><i></i><i></i><span class="url">gidi.example / play</span></div>'
    dev += f'<div class="scr" style="left:{bez}px;top:{bez}px;width:{W}px;height:{H}px;border-radius:{rad}px">{inner}</div></div>'
    caption = f'<div class="lab" style="left:{pad}px;top:{CH-pad+10}px;font-size:36px">{lab}{" · framed: "+framed.split("/")[-1] if framed else ""}</div>'
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="width:{CW}px;height:{CH}px;position:relative">{dev}{caption}</body></html>'
    name = f"dev-{key}{'-'+os.path.basename(framed)[:-4] if framed else ''}"
    open(f"{OUT}/{name}.html","w").write(html)
    return name, CW, CH

def rotate_prompt():
    W,H = 1179, 2556
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="width:{W+400}px;height:{H+400}px;position:relative">
<div class="dev" style="left:140px;top:140px;width:{W+120}px;height:{H+120}px;border-radius:225px"><div class="scr" style="left:60px;top:60px;width:{W}px;height:{H}px;border-radius:165px;background:linear-gradient(180deg,#2B2F5C,#6B4A6E 60%,#F28C4B)">
<div class="island" style="left:{W/2-190}px;top:30px;width:380px;height:110px"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:60px;text-align:center;padding:80px">
<svg viewBox="0 0 200 200" width="520" height="520"><rect x="62" y="20" width="76" height="140" rx="14" fill="none" stroke="#F5F5F0" stroke-width="8" opacity=".45"/><g transform="rotate(-90 100 110)"><rect x="62" y="40" width="76" height="140" rx="14" fill="#0F1219" stroke="#E8B21E" stroke-width="8"/></g><path d="M150 40 A70 70 0 0 1 176 96" fill="none" stroke="#E8B21E" stroke-width="8" stroke-linecap="round"/><path d="M168 86l8 12 10-12" fill="none" stroke="#E8B21E" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div style="font-size:96px;line-height:1.1">Abeg, turn phone sideways</div><div style="font-size:56px;color:#FAE69E">Gidi++ na landscape game. Road wide, so screen must wide too.</div></div></div></div>
<div class="lab" style="left:140px;top:{H+290}px;font-size:36px">Web on a phone held upright: rotate prompt (no portrait layout)</div></body></html>'''
    open(f"{OUT}/dev-rotate-prompt.html","w").write(html); return "dev-rotate-prompt", W+400, H+400

def shoot(name, W, H):
    out = f"{EXP}/{name}.png"
    subprocess.run(["bash", f"{ROOT}/tools/shoot.sh", f"{OUT}/{name}.html", out, str(W), str(H)])
    from PIL import Image
    im = Image.open(out); im.thumbnail((1600, 1600)); im.save(out)

if __name__ == "__main__":
    jobs = [page(k) for k in DEV]
    jobs += [page("iphone","exports/hud-phone.png"), page("iphone","exports/home-phone.png"), page("android","exports/hud-warn-phone.png"), page("android","exports/shop-phone.png"),
             page("web","exports/hud-desktop.png"), page("web","exports/map-desktop.png"), page("iphone","exports/leaderboard-phone.png"), page("web","exports/leaderboard-desktop.png"), rotate_prompt()]
    for j in jobs: shoot(*j)
    print(" ".join(j[0] for j in jobs))
