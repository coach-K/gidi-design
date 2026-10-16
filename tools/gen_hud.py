"""Generates landscape in-run HUD mockups (desktop 1920x1080, phone 2340x1080 19.5:9)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "mockups")

FRAMES = {
  # name: (w, h, safe left, right, top, bottom, label)
  "desktop": (1920, 1080, 32, 32, 32, 32, "Desktop / WebGL 1920×1080 (32 px margin)"),
  "phone":   (2340, 1080, 132, 132, 0, 63, "Phone 19.5:9 landscape 2340×1080 @3x (780×360 dp) · notch inset 132 px, home indicator 63 px"),
}

def scene(w, h, sl, sb, lanes=6):
    # Camera framing: HUD band top 0..216, road lanes in 230..h-250, near sidewalk under controls.
    # top: HUD row ends at 32+144=176 -> far curb from 200. bottom: controls block 24+300+24 above safe bottom.
    top_curb, bot_curb = 200, h - sb - 348
    s = [f'<svg class="scene" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
         '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B2F5C"/><stop offset="1" stop-color="#F28C4B"/></linearGradient>'
         '<linearGradient id="asph" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1E1F26"/><stop offset="1" stop-color="#2A2B33"/></linearGradient>'
         '<radialGradient id="hl"><stop offset="0" stop-color="#FFE7B0" stop-opacity=".9"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{w}" height="{top_curb}" fill="url(#sky)" opacity=".35"/>',
         f'<rect y="0" width="{w}" height="{top_curb}" fill="#7A4630" opacity=".55"/>',  # far shore / laterite sidewalk (goal)
         f'<rect y="{top_curb-18}" width="{w}" height="18" fill="#9A9488"/>',
         f'<rect y="{top_curb}" width="{w}" height="{bot_curb-top_curb}" fill="url(#asph)"/>',
         f'<rect y="{bot_curb}" width="{w}" height="18" fill="#9A9488"/>',
         f'<rect y="{bot_curb+18}" width="{w}" height="{h-bot_curb-18}" fill="#5E3A2A"/>']
    lh = (bot_curb - top_curb) / lanes
    import random; random.seed(7)
    ch = min(68, lh * 0.72)
    for i in range(1, lanes):
        y = top_curb + i * lh
        s.append(f'<line x1="0" y1="{y:.0f}" x2="{w}" y2="{y:.0f}" stroke="#E8E2D0" stroke-opacity=".55" stroke-width="4" stroke-dasharray="60 50"/>')
    for i in range(lanes):
        y = top_curb + i * lh + lh / 2
        right = i % 2 == 0
        for k in range(2):
            x = random.randint(100, w - 300) if k == 0 else (random.randint(0, 200) if right else w - 220)
            col = random.choice(["#E8B21E", "#E8B21E", "#C9CCD2", "#7C2E2E", "#3A5A80"])
            L = 210 if col == "#E8B21E" else 170
            s.append(f'<g transform="translate({x},{y-ch/2:.0f})"><rect width="{L}" height="{ch:.0f}" rx="14" fill="{col}"/>'
                     f'<rect x="{L*0.25:.0f}" y="10" width="{L*0.5:.0f}" height="{ch-20:.0f}" rx="8" fill="#111" opacity=".55"/>'
                     + (f'<rect y="{ch/2-4:.0f}" width="{L}" height="8" fill="#111" opacity=".7"/>' if col == "#E8B21E" else "")
                     + f'<circle cx="{L+30 if right else -30}" cy="{ch/2:.0f}" r="40" fill="url(#hl)"/></g>')
        # edge telegraph (Danger chevrons) on one lane, caution triangle on another
        if i == 2:
            s.append(f'<g transform="translate({sl+16},{y-30})" fill="#FF7A1A"><path d="M0 0 L26 30 L0 60 L14 60 L40 30 L14 0Z"/><path d="M30 0 L56 30 L30 60 L44 60 L70 30 L44 0Z"/></g>')
        if i == 4:
            s.append(f'<g transform="translate({w-sl-90},{y-30})"><path d="M30 0 L60 56 L0 56Z" fill="#F0E442"/><text x="30" y="50" font-size="34" text-anchor="middle" fill="#111">!</text></g>')
    # player crowd at near curb
    cx = w // 2
    for dx in (-40, 0, 40):
        s.append(f'<g transform="translate({cx+dx},{bot_curb+40})"><circle r="16" fill="#F5F5F0"/><rect x="-14" y="16" width="28" height="40" rx="10" fill="#56B4E9"/></g>')
    s.append('</svg>')
    return "\n".join(s), top_curb, bot_curb, lh

def page(name, annot):
    w, h, sl, sr, st, sb, label = FRAMES[name]
    svg, tc, bc, lh = scene(w, h, sl, sb)
    dpad = 3 * 144
    a = f"""<!doctype html><html><head><meta charset="utf-8"><title>HUD {name}</title>
<link rel="stylesheet" href="../css/hud.css"></head>
<body style="width:{w}px;height:{h}px"><div class="frame {name}" style="width:{w}px;height:{h}px;--sl:{sl}px;--sr:{sr}px;--st:{st}px;--sb:{sb}px">
{svg}
{'<div class="notch"></div><div class="homebar"></div>' if name=='phone' else ''}
<div class="safe">
  <div class="toprow">
  <div class="hud-tl glass" id="level">
    <div class="lvl">L3 · OSHODI <span class="t">00:31</span></div>
    <div class="meta">Saved <b>4/6</b> · Best <b>00:42</b></div>
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
  {'<div class="keys glass">WASD / ← ↑ → ↓ move · Space pick up · Tab stats</div>' if name=='desktop' else ''}
</div>
"""
    if annot:
        a += f"""<div class="ann">
  <div class="safeline"></div>
  <div class="band hudband" style="top:0;height:{tc}px"><span>HUD band 0–{tc}px · far curb + goal shore visible under HUD</span></div>
  <div class="band roadband" style="top:{tc}px;height:{bc-tc}px"><span>ROAD: 6 lanes, full width · {bc-tc}px tall ({lh:.0f}px/lane) · no HUD over lanes</span></div>
  <div class="band ctlband" style="top:{bc}px;height:{h-bc}px"><span>Near curb + controls band · controls sit over sidewalk only</span></div>
  <div class="note cam">
   <h4>CAMERA FRAMING (RT-106)</h4>
   <ul><li>Pitch 65° (TailCameraFollow.fixedEulerAngles), yaw 0, X locked</li>
   <li>Vertical FOV 50–55°; keep vertical FOV fixed, so wider aspect = more lane length</li>
   <li>Fit lanes×4 m + 2×1.5 m curb into the road band ({(bc-tc)/h*100:.0f}% of height)</li>
   <li>Lane margin: ≥1.5 car lengths visible both sides of the crowd; at 19.5:9 ≈ 38 m of lane visible vs 32 m at 16:9 → cars seen ≈1.3–1.7 s before reaching the crowd</li>
   <li>8-lane levels: raise height (15 → ~20 m), don't shrink HUD</li></ul></div>
  <div class="note z"><h4>Z-ORDER</h4><ol><li>3D scene</li><li>World telegraphs (unlit, not graded)</li><li>HUD glass panels</li><li>Touch controls</li><li>Toasts</li><li>Modals (continue / pause)</li></ol></div>
</div>"""
    a += "</div></body></html>"
    fn = os.path.join(OUT, f"hud-{name}{'-annotated' if annot else ''}.html")
    open(fn, "w").write(a)
    return fn

if __name__ == "__main__":
    for n in FRAMES:
        for an in (False, True):
            print(page(n, an))
