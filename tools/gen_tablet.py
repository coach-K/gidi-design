"""Tablet 4:3 two-row HUD (reference canvas 1440x1080: CanvasScaler 1920x1080, match height). Spec lives in exports/hud/HUD_Landscape_Spec.md."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT, dpad_svg
import gen_more as G
from brand import icon, P
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, M, MB = 1440, 1080, 32, 40          # safe margin 32 (iPad status bar ~24 pt), bottom 40 (home indicator)
FRAMES["tablet"] = (W, H, M, M, M, MB, "Tablet 4:3 landscape, reference 1440x1080")
bg = f"{ROOT}/assets/bg/L03_tablet.png"
im = Image.open(f"{ROOT}/assets/bg/L03_desktop.png"); x0 = (im.width - W) // 2; im.crop((x0, 0, x0 + W, H)).save(bg)

def body(annot=False):
    tl = f'<div class="hud-tl glass" style="min-width:0;width:560px"><div class="lvl">{G.lab(3)}</div><div class="meta">{G.META}</div></div>'
    stock = G.stock(g=(3,5), c=(1,2), o=(2,3)).replace('class="hud-tc glass"', 'class="hud-tc glass" style="width:560px;box-sizing:border-box;justify-content:space-between"')
    tr = (f'<div class="hud-tr"><div class="glass chips"><span class="amt">₦12,450</span><small>NAIRA CHIPS</small></div>'
          f'<div class="glass lives"><span class="heart">♥</span> {G.START_LIVES}</div>'
          f'<button class="glass btn">{icon("stats",44,P["text"])}<small>Stats</small></button><button class="glass btn">{icon("pause",44,P["text"])}<small>Pause</small></button></div>')
    hud = f'<div class="toprow" style="height:auto;align-items:flex-start"><div style="display:flex;flex-direction:column;gap:16px">{tl}{stock}</div>{tr}</div>'
    pr, dr = 0.1 * H, 0.15 * H
    px, py = M + 24 + pr, H - MB - 24 - pr
    dx, dy = W - M - 12 - dr, H - MB - 12 - dr
    ctl = (f'<div class="pick2" style="left:{px-pr:.0f}px;top:{py-pr:.0f}px;width:{2*pr:.0f}px;height:{2*pr:.0f}px"><b>+</b><span>PICK UP</span></div>'
           f'<div class="dpad2" style="left:{dx-dr:.0f}px;top:{dy-dr:.0f}px">{dpad_svg(dr)}</div>')
    ann = ""
    if annot:
        def box(x, y, w, h, t, c="#56B4E9", ty=None):
            return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:3px dashed {c};border-radius:14px;z-index:9"></div>'
                    f'<div style="position:absolute;left:{x+w-22}px;top:{y-14}px;z-index:9;background:{c};color:#111;font:700 24px Jakarta,sans-serif;width:40px;height:40px;line-height:40px;text-align:center;border-radius:20px">{t}</div>')
        SW = W - 2*M
        ann = (box(0, 0, 560, 144, "1") +
               box(0, 160, 560, 144, "2") +
               box(SW-705, 0, 705, 144, "3", "#FAE69E") +
               f'<div style="position:absolute;left:584px;top:200px;width:{SW-584}px;height:104px;z-index:9;border:3px dashed #59D9B8;border-radius:14px;display:flex;align-items:center;justify-content:center;color:#59D9B8;font:700 24px Jakarta,sans-serif;background:rgba(0,0,0,.25)">4 · keep clear: far curb / goal stays visible</div>' +
               f'<div style="position:absolute;left:-{M}px;right:-{M}px;top:{304+12}px;border-top:3px solid #FF6B7A;z-index:9"></div><div style="position:absolute;right:0;top:{304+20}px;z-index:9;color:#FF6B7A;font:700 22px Jakarta,sans-serif">HUD band ends y = {M+304} ref px (31% of height)</div>')
    return hud + ann, ctl

def page(annot):
    b, ctl = body(annot)
    html = G.shell("tablet", 3, b, "Tablet 2-row HUD").replace(f'<div class="safe">{b}</div>', f'<div class="safe">{b}</div>{ctl}')
    name = f"tablet-hud{'-annot' if annot else ''}"
    p = f"{OUT}/{name}.html"; open(p, "w").write(html)
    out = f"{ROOT}/exports/devices/dev-{name}.png"
    subprocess.run(["bash", f"{ROOT}/tools/shoot.sh", p, out, str(W), str(H)])
    return out

if __name__ == "__main__":
    print(page(False), page(True))
