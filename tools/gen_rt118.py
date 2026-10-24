"""RT-118 power-up active on the HUD (PR #107: ActivePowerUpHudRules, MobileControlsView.SetOwaActive).
Owa freeze ring: Image 'FreezeTimer', sprite ring_powerup_timer_fill (white, tinted), Filled Radial360, origin Top, counter-clockwise,
140 px, 8 px stroke, OwaTeal; last WarningSeconds -> Danger. Other power-ups keep the timer chip (PowerUpChipRules)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT, owa_btn, pick_pos
from gen_more import shell, top_hud, META
from brand import icon, badge, P

TEAL, DANGER = "#59D9B8", P["danger"]

from gen_bag import slot, row, ring as _ring

def ring_svg(frac, col, d=124, sw=8):
    """Owa freeze ring on the bag slot: counter-clockwise from top."""
    r = d/2 - 6; c = 2*math.pi*r
    return (f'<svg class="ring" viewBox="0 0 {d} {d}"><circle cx="{d/2}" cy="{d/2}" r="{r}" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="{sw}"/>'
            f'<circle cx="{d/2}" cy="{d/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{c*frac:.1f} {c:.1f}" transform="translate({d} 0) scale(-1 1) rotate(-90 {d/2} {d/2})"/></svg>')

def owa_slot(n, frac, warn=False, extra=""):
    st = "active" if frac > 0 else "filled"
    h = slot("owa", n, st, frac, extra=extra)
    if frac > 0:
        a = h.index('<svg class="ring"'); b = h.index('</svg>', a) + 6
        h = h[:a] + ring_svg(frac, DANGER if warn else TEAL) + h[b:]
        h = h.replace('class="bslot active', 'style="border-color:%s" class="bslot active' % (DANGER if warn else TEAL))
    return h

def chip(pid, frac, label, x="50%"):
    a = 2*math.pi*frac; X = 85+75*math.sin(a); Y = 85-75*math.cos(a); lg = 1 if frac > .5 else 0
    return (f'<div class="pu" style="left:{x};transform:translateX(-50%);top:198px"><div class="puc">{badge(pid,140)}<svg class="r" viewBox="0 0 170 170"><circle cx="85" cy="85" r="75" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="10"/>'
            f'<path d="M85 10 A75 75 0 {lg} 1 {X:.1f} {Y:.1f}" fill="none" stroke="#E8B21E" stroke-width="10" stroke-linecap="round"/></svg><div class="t">{label}</div></div></div>')

def page(n, lv, body, title, **kw):
    return shell(n, lv, body, title, **kw).replace("</head>", '<link rel="stylesheet" href="../css/bag.css"></head>')

def hud_owa(n):
    w, h = FRAMES[n][:2]
    slots = [owa_slot(1, .6), slot("maltina_gala", 1, "active", .5), slot("siren", 1), slot()]
    body = (top_hud(7, META, g=(2,3), c=(1,2)) + chip("maltina_gala", .5, "Malta · 2s") +
            f'<div class="toast" style="top:420px;border-color:{TEAL}">{icon("owa",36,TEAL)} Owa! Next Danfo lane frozen</div>' + row(w, h, slots))
    return page(n, 7, body, "HUD Owa active", ctl=True)

def states(n):
    cells = [("Ready · ×2", 2, 0, False, "no ring, count badge"), ("Freeze starts", 1, 1, False, "fill 1.0, teal"),
             ("Running · 2.4 s of 4", 1, .6, False, "fill = remaining01"), ("◆ Last second", 1, .2, True, "≤ WarningSeconds → Danger + pulse"),
             ("Ended", 1, 0, False, "remaining ≤ MinActive → hidden")]
    def cell(t, cnt, f, warn, d):
        return (f'<div class="statecard" style="flex-direction:column;gap:14px;padding:26px 22px;min-width:250px;align-items:center">{owa_slot(cnt, f, warn)}'
                f'<div style="text-align:center;font-size:24px;color:#F5F5F0">{t}<div style="font-size:19px;color:#9EA3AD;margin-top:6px">{d}</div></div></div>')
    rowh = "".join(cell(*c) for c in cells)
    maprow = "".join(f'<tr><td>{badge(p,56)}</td><td>{nm}</td><td><code>{ind}</code></td><td>{how}</td></tr>' for p, nm, ind, how in (
        ("owa","Owa","OwaButtonRing → bag slot","teal ring on the Owa bag slot (no OWA! button)"),("maltina_gala","Maltina","TimerChip · Malta","chip under top band + gold ring on its slot"),
        ("pure_water","Pure Water","TimerChip · PureWater","chip + slot ring"),("siren","VIP Siren","TimerChip · Siren","chip + slot ring, then 8 s cooldown"),("bribe_change","Bribe / Change","StockCountOnly","slot count drops by 1")))
    body = (f'<div class="ov heavy"></div><div class="panel" style="width:{FRAMES[n][0]-2*FRAMES[n][2]-160}px;text-align:left;padding:36px 48px">'
            f'<div class="ph" style="font-size:44px">Power-up active · Owa countdown ring (RT-118)</div>'
            f'<div class="psub" style="font-size:24px">OWA! button removed: the freeze ring draws on the Owa bag slot. ring_powerup_timer_fill at 124 px, 8 px, Radial 360 from top, counter-clockwise; slot outline tints to match.</div>'
            f'<div style="display:flex;gap:16px;margin-top:22px">{rowh}</div>'
            f'<table style="margin-top:22px;font-size:24px;border-spacing:18px 6px;color:#F5F5F0">{maprow}</table></div>')
    return page(n, 7, body, "Owa ring states", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/mock.css"><link rel="stylesheet" href="../css/bag.css"></head>')

SCREENS = [("hud-owa", hud_owa), ("owa-ring-states", states)]
if __name__ == "__main__":
    for k, fn in SCREENS:
        for n in ("desktop", "phone"):
            open(os.path.join(OUT, f"{k}-{n}.html"), "w").write(fn(n))
