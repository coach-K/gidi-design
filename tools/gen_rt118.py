"""RT-118 power-up active on the HUD (PR #107: ActivePowerUpHudRules).
Owa = TimerChip like the others, OwaTeal ring + freeze badge; last WarningSeconds -> Danger + pulse. Bag slot active/disabled only."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT
from gen_more import shell, top_hud, META
from brand import icon, badge, P

TEAL, DANGER = "#59D9B8", P["danger"]

from gen_bag import slot, row

def owa_slot(n, running=False):
    """Bag slot only shows active/disabled while Owa runs: no ring, no glow (the chip carries the timer)."""
    if not running: return slot("owa", n) if n else slot("owa", 0, "disabled", lbl="none left")
    if n > 0: return slot("owa", n, extra="active noglow")
    return slot("owa", 0, "disabled", lbl="in use")

def chip(pid, frac, label, x="50%", col="#E8B21E", warn=False, frost=False):
    if frac <= 0: return ""
    col = DANGER if warn else col
    a = 2*math.pi*min(frac,.9999); X = 85+75*math.sin(a); Y = 85-75*math.cos(a); lg = 1 if frac > .5 else 0
    extra = (f'<div class="halo"></div>' if warn else "") + (f'<div class="frost">{icon("freeze",34,col)}</div>' if frost else "")
    return (f'<div class="pu{" warn" if warn else ""}" style="left:{x};transform:translateX(-50%);top:198px"><div class="puc">{extra}{badge(pid,140)}<svg class="r" viewBox="0 0 170 170"><circle cx="85" cy="85" r="75" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="10"/>'
            f'<path d="M85 10 A75 75 0 {lg} 1 {X:.1f} {Y:.1f}" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round"/></svg><div class="t"{f' style="color:{col}"' if warn else ""}>{label}</div></div></div>')

def owa_chip(frac, label, x="50%", warn=False):
    return chip("owa", frac, label, x, TEAL, warn, True)

def page(n, lv, body, title, **kw):
    return shell(n, lv, body, title, **kw).replace("</head>", '<link rel="stylesheet" href="../css/bag.css"></head>')

def hud_owa(n):
    w, h = FRAMES[n][:2]
    slots = [owa_slot(1, True), slot("maltina_gala", 1, "active", .5), slot("siren", 1), slot()]
    body = (top_hud(7, META, g=(2,3), c=(1,2)) + owa_chip(.6, "Owa · 2.4s", "calc(50% - 105px)") + chip("maltina_gala", .5, "Malta · 2s", "calc(50% + 105px)") +
            f'<div class="toast" style="top:430px;border-color:{TEAL}">{icon("freeze",36,TEAL)} Owa! Next Danfo lane frozen</div>' + row(w, h, slots))
    return page(n, 7, body, "HUD Owa active", ctl=True)

def states(n):
    cells = [("Ready · ×2", 0, False, 2, False, "no chip · bag slot normal"), ("Freeze starts", 1, False, 1, True, "chip appears, ring 1.0, teal"),
             ("Running · 2.4 s of 4", .6, False, 1, True, "fill = remaining01 · slot active, no ring"), ("Last second", .2, True, 0, True, "≤ WarningSeconds (1 s) → Danger red + pulse"),
             ("Ended · none left", 0, False, 0, False, "remaining ≤ MinActive → chip hidden")]
    def cell(t, f, warn, cnt, run, d):
        c = owa_chip(f, f"{f*4:.1f}s" if f else "", warn=warn).replace('style="left:50%;transform:translateX(-50%);top:198px"', 'style="position:relative;left:0;top:0"') if f else '<div style="height:200px;display:flex;align-items:center;color:#5D6370;font-size:20px">no chip</div>'
        return (f'<div class="statecard" style="flex-direction:column;gap:14px;padding:26px 18px;min-width:250px;align-items:center"><div style="height:210px;display:flex;align-items:center">{c}</div>{owa_slot(cnt, run)}'
                f'<div style="text-align:center;font-size:24px;color:#F5F5F0;margin-top:26px">{t}<div style="font-size:19px;color:#9EA3AD;margin-top:6px">{d}</div></div></div>')
    rowh = "".join(cell(*c) for c in cells)
    maprow = "".join(f'<tr><td>{badge(p,56)}</td><td>{nm}</td><td><code>{ind}</code></td><td>{how}</td></tr>' for p, nm, ind, how in (
        ("owa","Owa","TimerChip · Owa","teal #59D9B8 ring + freeze badge; slot active/disabled only"),("maltina_gala","Maltina","TimerChip · Malta","gold chip + ring on its slot"),
        ("pure_water","Pure Water","TimerChip · PureWater","chip + slot ring"),("siren","VIP Siren","TimerChip · Siren","chip + slot ring, then 20 s cooldown"),("bribe_change","Bribe / Change","StockCountOnly","slot count drops by 1")))
    body = (f'<div class="ov heavy"></div><div class="panel" style="width:{FRAMES[n][0]-2*FRAMES[n][2]-120}px;text-align:left;padding:32px 44px">'
            f'<div class="ph" style="font-size:44px">Power-up active · Owa timer chip (RT-118, PR #107)</div>'
            f'<div class="psub" style="font-size:24px">Owa uses the same timer chip as the others, accented OwaTeal #59D9B8 with a freeze badge. Last 1 s turns Danger red and pulses. The bag slot shows only active / disabled: no ring, no glow.</div>'
            f'<div style="display:flex;gap:14px;margin-top:20px">{rowh}</div>'
            f'<table style="margin-top:18px;font-size:23px;border-spacing:18px 4px;color:#F5F5F0">{maprow}</table></div>')
    return page(n, 7, body, "Owa chip states", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/mock.css"><link rel="stylesheet" href="../css/bag.css"></head>')

SCREENS = [("hud-owa", hud_owa), ("owa-ring-states", states)]
if __name__ == "__main__":
    for k, fn in SCREENS:
        for n in ("desktop", "phone"):
            open(os.path.join(OUT, f"{k}-{n}.html"), "w").write(fn(n))
