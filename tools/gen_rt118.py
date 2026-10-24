"""RT-118 power-up active on the HUD (PR #107: ActivePowerUpHudRules, MobileControlsView.SetOwaActive).
Owa freeze ring: Image 'FreezeTimer', sprite ring_powerup_timer_fill (white, tinted), Filled Radial360, origin Top, counter-clockwise,
140 px, 8 px stroke, OwaTeal; last WarningSeconds -> Danger. Other power-ups keep the timer chip (PowerUpChipRules)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT, owa_btn, pick_pos
from gen_more import shell, top_hud, META
from brand import icon, badge, P

TEAL, DANGER = "#59D9B8", P["danger"]

def ring_svg(frac, col, d=140, sw=8):
    r = (d - sw) / 2; c = 2 * math.pi * r
    # counter-clockwise from top: mirror the dash
    return (f'<svg style="position:absolute;left:{(144-d)/2}px;top:{(144-d)/2}px;z-index:2" width="{d}" height="{d}" viewBox="0 0 {d} {d}">'
            f'<circle cx="{d/2}" cy="{d/2}" r="{r}" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="{sw}"/>'
            f'<circle cx="{d/2}" cy="{d/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="butt" stroke-dasharray="{c*frac:.1f} {c:.1f}" transform="translate({d} 0) scale(-1 1) rotate(-90 {d/2} {d/2})"/></svg>')

def owa_with_ring(px, py, pr, owa, frac, warn=False):
    h = owa_btn(px, py, pr, owa)
    if frac <= 0: return h
    i = h.index('<div class="disc"')
    return h[:i] + ring_svg(frac, DANGER if warn else TEAL) + h[i:]

def chip(pid, frac, label, x="50%"):
    a = 2*math.pi*frac; X = 85+75*math.sin(a); Y = 85-75*math.cos(a); lg = 1 if frac > .5 else 0
    return (f'<div class="pu" style="left:{x};transform:translateX(-50%);top:198px"><div class="puc">{badge(pid,140)}<svg class="r" viewBox="0 0 170 170"><circle cx="85" cy="85" r="75" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="10"/>'
            f'<path d="M85 10 A75 75 0 {lg} 1 {X:.1f} {Y:.1f}" fill="none" stroke="#E8B21E" stroke-width="10" stroke-linecap="round"/></svg><div class="t">{label}</div></div></div>')

def hud_owa(n):
    w, h = FRAMES[n][:2]; px, py, pr = pick_pos(w, h)
    body = (top_hud(7, META, g=(2,3), c=(1,2)) + chip("maltina_gala", .5, "Malta · 2s") +
            f'<div class="toast" style="top:420px;border-color:{TEAL}">{icon("owa",36,TEAL)} Owa! Next Danfo lane frozen</div>')
    s = shell(n, 7, body, "HUD Owa active", ctl=True, owa=(1,0,3))
    i = s.index('<div class="owa2'); j = s.index('</div></div>', i) + 12
    return s[:i] + owa_with_ring(px, py, pr, (1,0,3), .6) + s[j:]

def states(n):
    cells = [("Ready · 2 charges", (2,0,3), 0, False, "no ring"), ("Freeze starts", (1,0,3), 1, False, "fill 1.0, teal"),
             ("Running · 2.4 s of 4", (1,0,3), .6, False, "fill = remaining01"), ("◆ Last second", (1,0,3), .2, True, "≤ WarningSeconds → Danger + pulse"),
             ("Ended", (1,0,3), 0, False, "remaining ≤ MinActive → hidden")]
    def cell(t, owa, f, warn, d):
        b = owa_with_ring(72, 72+72+16+72+200, 72, owa, f, warn)  # placeholder geometry replaced below
        b = b.replace(b[b.index('style="'):b.index('">')+1], 'style="position:relative;left:0;top:0"', 1)
        return (f'<div class="statecard" style="flex-direction:column;gap:14px;padding:26px 22px;min-width:250px;align-items:center">{b}'
                f'<div style="text-align:center;font-size:24px;color:#F5F5F0">{t}<div style="font-size:19px;color:#9EA3AD;margin-top:6px">{d}</div></div></div>')
    row = "".join(cell(*c) for c in cells)
    maprow = "".join(f'<tr><td>{badge(p,56)}</td><td>{nm}</td><td><code>{ind}</code></td><td>{how}</td></tr>' for p, nm, ind, how in (
        ("owa","Owa","OwaButtonRing","teal ring on OWA! (bag slot: same ring, 124 px)"),("maltina_gala","Maltina","TimerChip · Malta","chip under top band, gold ring"),
        ("pure_water","Pure Water","TimerChip · PureWater","chip"),("siren","VIP Siren","TimerChip · Siren","chip"),("bribe_change","Bribe / Change","StockCountOnly","CHANGE pips drop by 1")))
    body = (f'<div class="ov heavy"></div><div class="panel" style="width:{FRAMES[n][0]-2*FRAMES[n][2]-160}px;text-align:left;padding:36px 48px">'
            f'<div class="ph" style="font-size:44px">Power-up active · Owa countdown ring (RT-118)</div>'
            f'<div class="psub" style="font-size:24px">FreezeTimer: ring_powerup_timer_fill, 140 px (just outside the 120 px face), 8 px, Radial 360 from top, counter-clockwise. Pips keep showing charges left.</div>'
            f'<div style="display:flex;gap:16px;margin-top:22px">{row}</div>'
            f'<table style="margin-top:22px;font-size:24px;border-spacing:18px 6px;color:#F5F5F0">{maprow}</table></div>')
    return shell(n, 7, body, "Owa ring states", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/mock.css"></head>')

SCREENS = [("hud-owa", hud_owa), ("owa-ring-states", states)]
if __name__ == "__main__":
    for k, fn in SCREENS:
        for n in ("desktop", "phone"):
            open(os.path.join(OUT, f"{k}-{n}.html"), "w").write(fn(n))
