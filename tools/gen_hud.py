"""Generates landscape in-run HUD mockups (desktop 1920x1080, phone 2340x1080 19.5:9)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "mockups")

FRAMES = {
  # name: (w, h, safe left, right, top, bottom, label)
  "desktop": (1920, 1080, 32, 32, 32, 32, "Desktop / WebGL 1920×1080 (32 px margin)"),
  "phone":   (2340, 1080, 132, 132, 0, 63, "Phone 19.5:9 landscape 2340×1080 @3x (780×360 dp) · notch inset 132 px, home indicator 63 px"),
}

CROWD = {"desktop": (956, 845), "phone": (1166, 845)}  # Baba Gidi + crowd position in the real capture

def scene(w, h, sl, sb, name="desktop"):
    """REAL 3D capture: reference/levels/L08_phone_landscape.jpg (dev build, L8 Third Mainland Bridge),
    old HUD inpainted out, cropped/scaled by tools/prep_bg.py. Top 200 px = far shoulder fill (camera-aim proposal)."""
    return f'<img class="scene" src="../assets/bg/hud_{name}.png" width="{w}" height="{h}" alt="real in-game capture">', 176, 0, 0

def page(name, annot):
    w, h, sl, sr, st, sb, label = FRAMES[name]
    svg, tc, bc, lh = scene(w, h, sl, sb, name)
    cx, cy = CROWD[name]
    dpad = 3 * 144
    a = f"""<!doctype html><html><head><meta charset="utf-8"><title>HUD {name}</title>
<link rel="stylesheet" href="../css/hud.css"></head>
<body style="width:{w}px;height:{h}px"><div class="frame {name}" style="width:{w}px;height:{h}px;--sl:{sl}px;--sr:{sr}px;--st:{st}px;--sb:{sb}px">
{svg}
{'<div class="notch"></div><div class="homebar"></div>' if name=='phone' else ''}
<div class="safe">
  <div class="toprow">
  <div class="hud-tl glass" id="level">
    <div class="lvl">L8 · 3RD MAINLAND</div>
    <div class="meta">Saved <b>4/6</b> · Best <b>00:42</b> · <span class="t">00:31</span></div>
  </div>
  <div class="hud-tc glass" id="stock">
    <div class="cell"><span class="k">GROUP</span><span class="pips"><i class="on"></i><i class="on"></i><i></i></span></div>
    <div class="cell"><span class="k">CHANGE</span><span class="pips"><i class="on"></i><i></i></span></div>
    <div class="cell owa"><span class="k">OWA!</span><span class="pips"><i class="on"></i><i></i><i></i></span></div>
  </div>
  <div class="hud-tr" id="wallet">
    <div class="glass chips"><span class="amt">₦12,450</span><small>NAIRA CHIPS</small></div>
    <div class="glass lives"><span class="heart">♥</span> 3</div>
    <button class="glass btn" id="stats"><span class="ico">▤</span><small>Stats</small></button>
    <button class="glass btn" id="pause"><span class="ico">II</span><small>Pause</small></button>
  </div>
  </div>
  <button class="pickup {'touchonly' if name=='desktop' else ''}" id="pickup"><span>PICK<br>UP</span></button>
  <div class="dpad {'touchonly' if name=='desktop' else ''}" id="dpad" >
    <b class="u">▲</b><b class="l">◀</b><b class="d">▼</b><b class="r">▶</b>
  </div>
  {'<div class="keys glass">WASD / arrows: waka · Space: pick up · Tab: stats</div>' if name=='desktop' else ''}
</div>
"""
    if annot:
        a += f"""<div class="ann">
  <div class="safeline"></div>
  <div class="band hudband" style="top:0;height:{tc}px"><span>HUD row 0–176 px over far shoulder / beyond-goal (camera aim proposal: far curb at y ≥ 200)</span></div>
  <div class="crowdcol" style="left:{cx-240}px;width:480px;top:{cy-200}px;bottom:0"><span>Crowd column: keep clear (±240 px around Baba Gidi)</span></div>
  <div class="persp"><span>Perspective: far lanes narrower than near lanes</span></div>
  <div class="note cam">
   <h4>CAMERA FRAMING: real perspective camera (RT-106)</h4>
   <ul><li>3D URP perspective camera behind and above Baba Gidi, pitch 65° (TailCameraFollow), yaw 0, X locked, follows the crowd on Z</li>
   <li>Vertical FOV fixed at 50–55°. A wider screen shows more lane length (19.5:9 shows more than 16:9)</li>
   <li>Aim: crowd at ≈ 85% of screen height, so almost the whole screen is lanes still to cross</li>
   <li>Far curb / goal must sit below the HUD row (y ≥ 200). Tilt or offset the aim so the top 176 px shows shoulder or beyond-goal</li>
   <li>Far lane should span ≥ 70% of screen width so cars are seen early. On 8 lanes, raise the camera height before widening the FOV</li>
   <li>Controls sit in the bottom corners, over road already crossed, never in the crowd column</li></ul></div>
  <div class="note z"><h4>Z-ORDER</h4><ol><li>3D scene</li><li>World telegraphs (unlit)</li><li>HUD glass panels</li><li>Touch controls</li><li>Toasts</li><li>Modals</li></ol></div>
</div>"""
    a += "</div></body></html>"
    fn = os.path.join(OUT, f"hud-{name}{'-annotated' if annot else ''}.html")
    open(fn, "w").write(a)
    return fn

if __name__ == "__main__":
    for n in FRAMES:
        for an in (False, True):
            print(page(n, an))
