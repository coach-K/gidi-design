"""Generates landscape in-run HUD mockups (desktop 1920x1080, phone 2340x1080 19.5:9)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "mockups")

FRAMES = {
  # name: (w, h, safe left, right, top, bottom, label)
  "desktop": (1920, 1080, 32, 32, 32, 32, "Desktop / WebGL 1920×1080 (32 px margin)"),
  "phone":   (2340, 1080, 132, 132, 0, 63, "Phone 19.5:9 landscape 2340×1080 @3x (780×360 dp) · notch inset 132 px, home indicator 63 px"),
}

  # Baba Gidi + crowd position in the real capture

def scene(w, h, sl, sb, name="desktop"):
    """Real L5 Oshodi Expressway screenshot (current build camera), old HUD removed + dusk grade (tools/prep_levels.py)."""
    return f'<img class="scene" src="../assets/bg/lv_hud_{name}.png" width="{w}" height="{h}" alt="">', 176, 0, 0

# Build control layout (measured from reference/levels/L08_phone_landscape.jpg, as fractions of the frame)
PICK = (0.122, 0.729, 0.100)   # centre x, centre y, radius (fraction of height)
DPAD = (0.861, 0.702, 0.167)

def dpad_svg(R):
    arrows = []
    for i in range(8):
        arrows.append(f'<g transform="rotate({i*45})"><rect x="-17" y="-128" width="34" height="58" rx="4"/><path d="M-44 -124 L0 -168 L44 -124 Z"/></g>')
    return (f'<svg viewBox="-180 -180 360 360" width="{2*R}" height="{2*R}"><circle r="176" fill="rgba(255,255,255,.07)" stroke="rgba(255,255,255,.14)" stroke-width="3"/>'
            f'<g fill="rgba(226,196,128,.62)" stroke="rgba(120,90,30,.35)" stroke-width="2">{"".join(arrows)}</g><circle r="24" fill="rgba(30,30,30,.35)"/></svg>')

# OWA! button (Kehinde, Oct 16): smaller round button stacked above PICK UP, same visual family.
OWA_D, OWA_HIT, OWA_GAP = 120, 144, 32   # visual diameter, square touch target (48 dp @3x), gap between touch targets

def owa_btn(px, py, pr, owa=(2, 0.5, 3), hi=False):
    """owa = (full charges, partial refill 0..1 of next charge, cap). 0 full + 0 partial = disabled."""
    full, part, cap = owa
    cy = py - pr - OWA_GAP - OWA_HIT/2
    pips = "".join(f'<i class="on"></i>' if i < full else (f'<i class="part" style="--p:{part*100:.0f}%"></i>' if i == full and part > 0 else '<i></i>') for i in range(cap))
    dis = full == 0 and part == 0
    return (f'<div class="owa2{" off" if dis else ""}{" hi" if hi else ""}" style="left:{px-OWA_HIT/2:.0f}px;top:{cy-OWA_HIT/2:.0f}px">'
            f'<div class="disc"><span class="k">OWA!</span><span class="opips">{pips}</span></div></div>')

def controls(w, h, owa=(2, 0.5, 3), owa_hi=False, pick=None, dpad=None):
    px, py, pr = pick or (PICK[0]*w, PICK[1]*h, PICK[2]*h)
    dx, dy, dr = dpad or (DPAD[0]*w, DPAD[1]*h, DPAD[2]*h)
    return (f'<div class="pick2" style="left:{px-pr:.0f}px;top:{py-pr:.0f}px;width:{2*pr:.0f}px;height:{2*pr:.0f}px"><b>+</b><span>PICK UP</span></div>'
            + owa_btn(px, py, pr, owa, owa_hi) +
            f'<div class="dpad2" style="left:{dx-dr:.0f}px;top:{dy-dr:.0f}px">{dpad_svg(dr)}</div>')

def page(name, annot):
    w, h, sl, sr, st, sb, label = FRAMES[name]
    svg, tc, bc, lh = scene(w, h, sl, sb, name)
    dpad = 3 * 144
    a = f"""<!doctype html><html><head><meta charset="utf-8"><title>HUD {name}</title>
<link rel="stylesheet" href="../css/hud.css"></head>
<body style="width:{w}px;height:{h}px"><div class="frame {name}" style="width:{w}px;height:{h}px;--sl:{sl}px;--sr:{sr}px;--st:{st}px;--sb:{sb}px">
{svg}
{'<div class="notch"></div><div class="homebar"></div>' if name=='phone' else ''}
<div class="safe">
  <div class="toprow">
  <div class="hud-tl glass" id="level">
    <div class="lvl long">L5 · Oshodi Expressway</div>
    <div class="meta">Saved <b>4/6</b> · Best <b>00:42</b></div>
  </div>
  <div class="hud-tc glass" id="stock">
    <div class="cell"><span class="k">GROUP</span><span class="pips"><i class="on"></i><i class="on"></i><i></i></span></div>
    <div class="cell"><span class="k">CHANGE</span><span class="pips"><i class="on"></i><i></i></span></div>
  </div>
  <div class="hud-tr" id="wallet">
    <div class="glass chips"><span class="amt">₦12,450</span><small>NAIRA CHIPS</small></div>
    <div class="glass lives"><span class="heart">♥</span> 3</div>
    <button class="glass btn" id="stats"><span class="ico">▤</span><small>Stats</small></button>
    <button class="glass btn" id="pause"><span class="ico">II</span><small>Pause</small></button>
  </div>
  </div>
</div>
{controls(w, h)}
"""
    if annot:
        a += f"""<div class="ann">
  <div class="safeline"></div>
  <div class="band hudband" style="top:0;height:{tc}px"><span>HUD row 0–176 px (build: HudLandscapeConfig)</span></div>
  <div class="note cam">
   <h4>CAMERA: as in the current build (no change)</h4>
   <ul><li>URP perspective camera, pitch 65°, yaw 0, X locked, follows the crowd on Z (TailCameraFollow)</li>
   <li>Standard stages: height 15 m, focus offset Z −5 m, vertical FOV 52°</li>
   <li>Wide stages (≥ 8 lanes): height 20 m, FOV 58°. Shown: L5 (standard)</li>
   <li>Road narrows with distance; lanes enter from the screen edges</li>
   <li>Controls stay where the build puts them; their overlap with lane ends is accepted, as in the build</li></ul></div>
  <div class="note z"><h4>Z-ORDER</h4><ol><li>3D scene</li><li>World telegraphs</li><li>HUD glass panels</li><li>Touch controls (translucent): PICK UP, OWA! (same layer, no overlap), d-pad</li><li>Toasts</li><li>Modals</li></ol></div>
</div>"""
    a += "</div></body></html>"
    fn = os.path.join(OUT, f"hud-{name}{'-annotated' if annot else ''}.html")
    open(fn, "w").write(a)
    return fn

if __name__ == "__main__":
    for n in FRAMES:
        for an in (False, True):
            print(page(n, an))
