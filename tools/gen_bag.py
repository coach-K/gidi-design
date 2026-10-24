"""Bag concept (GPP-021): in-run 4-slot bag, slot states, full bag, Base Camp with a bag, carry-over on the level intro.
Code names: GameManager.currentOwaCharges / maxOwaCapacity / bribeCount / GetPowerUpStock(id), GidiEconomyTables.PowerUpInventoryCap,
PowerUpChipRules (ActiveChipKind PureWater/Malta/Siren), PowerUpRingsView, BaseCampShopSession, RestartPoolKeepProgress(resetInventory)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT, DPAD
from gen_more import shell, top_hud, wallet, LV, META, lab
from gen_screens import continue_cost
from brand import icon, badge, P

SLOT, GAP, INSET_R, ABOVE_DPAD = 144, 12, 32, 24      # 1080-ref px (= 96 / 8 / 21.3 / 16 at 720)
SAFE_R = {1920: 0, 2340: 132, 1440: 0}
def bag_xy(w, h):
    """Row right edge = safe right - 32; row bottom = d-pad top - 24. Returns left, top of the 4-slot row."""
    dy, dr = DPAD[1]*h, DPAD[2]*h
    right = w - SAFE_R.get(w, 0) - INSET_R; bottom = dy - dr - ABOVE_DPAD
    return right - (4*SLOT + 3*GAP), bottom - SLOT

def ring(frac, size=124):
    r = size/2 - 6; c = 2*math.pi*r
    return (f'<svg class="ring" viewBox="0 0 {size} {size}"><circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="8"/>'
            f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="#E8B21E" stroke-width="8" stroke-linecap="round" stroke-dasharray="{c*frac:.1f} {c:.1f}" transform="rotate(-90 {size/2} {size/2})"/></svg>')

def slot(pid=None, n=0, state="filled", frac=0, cd=0, cdt="", lbl="", extra=""):
    if not pid: return f'<div class="bslot empty {extra}"></div>'
    inner = f'<div class="bd">{badge(pid, 96)}</div>'
    if state == "active": inner = ring(frac) + f'<div class="bd" style="width:84px;height:84px">{badge(pid, 84)}</div>'
    if cd: inner += f'<div class="cd" style="--p:{cd*100:.0f}%"></div><div class="cdt">{cdt}</div>'
    if n > 1 or pid == "owa": inner += f'<span class="cnt">×{n}</span>'
    if lbl: inner += f'<div class="lbl">{lbl}</div>'
    return f'<div class="bslot {state} {extra}">{inner}</div>'

def row(w, h, slots, cls=""):
    x, y = bag_xy(w, h)
    return f'<div class="baglbl" style="left:{x:.0f}px;top:{y-44:.0f}px">BAG · TAP TO USE</div><div class="bagrow {cls}" style="left:{x:.0f}px;top:{y:.0f}px">{"".join(slots)}</div>'

def chip(pid, frac, label, w):
    a = 2*math.pi*frac; x = 85+75*math.sin(a); y = 85-75*math.cos(a); large = 1 if frac > .5 else 0
    return (f'<div class="pu" style="left:50%;transform:translateX(-50%);top:198px"><div class="puc">{badge(pid,140)}<svg class="r" viewBox="0 0 170 170"><circle cx="85" cy="85" r="75" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="10"/>'
            f'<path d="M85 10 A75 75 0 {large} 1 {x:.1f} {y:.1f}" fill="none" stroke="#E8B21E" stroke-width="10" stroke-linecap="round"/></svg><div class="t">{label}</div></div></div>')

def page(fn, n, lv, body, title, **kw):
    return shell(n, lv, body, title, **kw).replace("</head>", '<link rel="stylesheet" href="../css/bag.css"></head>')

def hud_bag(n):
    w, h = FRAMES[n][:2]
    slots = [slot("owa", 3), slot("maltina_gala", 1, "active", .55), slot("siren", 1, "filled", cd=.6, cdt="6s"), slot()]
    out = page(None, n, 6, top_hud(6, META) + chip("maltina_gala", .55, "Malta · 2.2s", w), "HUD bag", ctl=True, owa=(3, 0, 3))
    return out.replace("</body>", row(w, h, slots) + "</body>")

def hud_bagfull(n):
    w, h = FRAMES[n][:2]
    x, y = bag_xy(w, h)
    slots = [slot("owa", 2, extra="full"), slot("maltina_gala", 2, extra="full"), slot("bribe_change", 2, extra="full"), slot("pure_water", 1, extra="full")]
    shake = f'<div class="shake" style="left:{x-44:.0f}px;top:{y+50:.0f}px">((</div><div class="shake" style="left:{x+4*SLOT+3*GAP+14:.0f}px;top:{y+50:.0f}px">))</div>'
    fail = f'<div class="pickfail" style="left:{w*0.30:.0f}px;top:{h*0.60:.0f}px">{badge("siren",72)}<span>stays on the curb</span></div>'
    body = top_hud(8, META) + '<div class="toast" style="top:230px;border-color:rgba(255,122,26,.7)">' + icon("bag", 36, "#FF7A1A") + ' Bag full · tap a slot to use one</div>'
    out = page(None, n, 8, body, "HUD bag full", ctl=True, owa=(2, 0, 3))
    return out.replace("</body>", row(w, h, slots) + shake + fail + "</body>")

def bag_states(n):
    cards = [(slot(), "Empty", "dashed, faint +"), (slot("maltina_gala", 2), "Filled · count", "badge 96 + ×N pill (N ≥ 2; OWA always)"),
             (slot("pure_water", 1, "active", .7), "Active / running", "timer ring, gold glow"), (slot("maltina_gala", 1, "filled", cd=.4, cdt="2s"), "Cooldown", "radial sweep + seconds"),
             (slot("siren", 1, "disabled", lbl="Used this level"), "Disabled", "grey 50%, reason label"), (slot("bribe_change", 2, extra="full"), "Bag full", "orange outline + shake"),
             (slot("owa", 3, extra="pressed"), "Pressed", "scale 0.92, light haptic")]
    grid = "".join(f'<div class="statecard">{s}<span>{t}<small>{d}</small></span></div>' for s, t, d in cards)
    body = f'''<div class="ov heavy"></div><div class="panel" style="width:{FRAMES[n][0]-2*FRAMES[n][2]-120}px;text-align:left"><div class="ph" style="font-size:48px">Bag slot states</div>
<div class="psub">4 shared slots · Pure Water, Malta, VIP Siren, Change and OWA charges · tap to activate, nothing auto-fires · carries over between levels</div>
<div style="display:flex;gap:14px;margin-top:34px">{grid}</div>
<div class="psub" style="margin-top:28px;font-size:24px">Tap: scale 0.92 (80 ms) → 1.0 (120 ms ease-out) · light haptic · <code>sfx_bag_slot_tap</code> then the item cue. Denied tap (cooldown, disabled): 6 px shake · <code>sfx_bag_denied</code>.</div></div>'''
    return page(None, n, 5, body, "Bag states", blur=True)

SIREN_PRICES = (120, 180, 270)   # 1st / 2nd / 3rd+ purchase in a run (anti-exploit); one per level, 8 s cooldown in-run
def siren_btn(state, price=120, nxt=180):
    if state == "buy":  return f'<button class="buy sm2" style="width:170px;min-width:170px">₦{price}</button>'
    if state == "used": return '<button class="buy full sm2" style="width:170px;min-width:170px;font-size:24px;line-height:1.15">Used this<br>level</button>'
    if state == "full": return '<button class="buy full">Bag full</button>'

def shop_bag(n):
    import re, gen_screens
    from gen_screens import shop
    old = gen_screens.LEVELS["shop"]; gen_screens.LEVELS["shop"] = (7, "Ojota Intersect")   # Siren + Change unlocked
    try: s = shop(n)
    finally: gen_screens.LEVELS["shop"] = old
    s = s.replace('lv_shop_', 'lv_shop_')
    strip = (f'<div class="bagstrip glass"><span class="h">YOUR BAG<br>4/4 · FULL</span>{slot("owa",2)}{slot("maltina_gala",1)}{slot("bribe_change",2)}{slot("siren",1)}</div>')
    # Pure Water: new item type, bag has no free slot -> Bag full. Malta: already in a slot, stack has room -> +1 allowed.
    s = s.replace('<button class="buy">₦110</button>', '<button class="buy full">Bag full</button>')
    s = re.sub(r'<button class="buy full sm2"[^>]*>used, cash out to refresh</button>', '<button class="buy full">Bag full</button>', s)
    s = s.replace('<button class="buy">₦90</button>', '<button class="buy full">Bag full</button>')   # Change ×2 already in the bag = cap 2
    s = s.replace('<span class="pips"><i class="on"></i><i class=""></i><em>1/2</em></span></div><button class="buy">₦80</button>',
                  '<span class="pips"><i class="on"></i><i class=""></i><em>1/2</em></span></div><button class="buy sm2" style="width:150px">+1 to stack<br>₦80</button>')
    # VIP Siren: bought for this level already -> 'Used this level', next price shown
    s = re.sub(r'(VIP Siren</b><span>)([^<]*)(</span>)', r'\1One per level · next price <b style="color:#FAE69E">₦180</b>\3', s)
    s = re.sub(r'(VIP Siren</b>.*?</div>)<button class="buy">₦120</button>', lambda m: m.group(1).replace('<i class=""></i><em>0/1</em>', '<i class="on"></i><em>1/1</em>') + siren_btn("used"), s, count=1, flags=re.S)
    s = s.replace('<div class="iaprow">', '<div class="iaprow" style="display:none">')
    s = s.replace('<link rel="stylesheet" href="../css/mock.css">', '<link rel="stylesheet" href="../css/mock.css"><link rel="stylesheet" href="../css/bag.css">')
    toast = ('<div style="position:absolute;left:744px;bottom:52px;z-index:5;padding:18px 34px;font-size:30px;white-space:nowrap;background:rgba(10,12,18,.86);'
             'border:2px solid #FF7A1A;border-radius:999px;color:#FAE69E;display:flex;gap:14px;align-items:center">' + icon("bag", 34, "#FF7A1A") + ' Bag full · use one in your next run</div>')
    return s.replace('<button class="cta shopgo">', strip + toast + '<button class="cta shopgo">')

def siren_states(n):
    """VIP Siren anti-exploit: tile states + in-run cooldown look."""
    def tile(btn, sub, extra=""):
        return (f'<div class="item glass {extra}" style="position:relative"><div class="ic">{badge("siren",96)}</div><div class="tx"><b>VIP Siren</b><span>{sub}</span>'
                f'<span class="pips"><i class="{"on" if "1/1" in sub or extra=="used" else ""}"></i><em>{"1/1" if extra=="used" else "0/1"}</em></span></div>{btn}</div>')
    tiles = [("Available · 1st buy", tile(siren_btn("buy", 120), 'Freezes all traffic · next <b style="color:#FAE69E">₦180</b>')),
             ("Used this level", tile(siren_btn("used"), 'One per level · next <b style="color:#FAE69E">₦180</b> at L8', "used")),
             ("2nd buy (next level)", tile(siren_btn("buy", 180), 'Price rises · next <b style="color:#FAE69E">₦270</b>')),
             ("Bag full", tile(siren_btn("full"), 'No free slot · use one first'))]
    grid = "".join(f'<div style="display:flex;flex-direction:column;gap:12px"><div style="font-size:24px;color:#E8B21E;letter-spacing:.08em">{t}</div><div class="shopgrid g3" style="position:static;display:block">{h}</div></div>' for t, h in tiles)
    ladder = "".join(f'<div class="statecard" style="gap:10px;padding:18px"><span style="font-size:44px;color:#FAE69E">₦{p}</span><span>{k}<small>{d}</small></span></div>'
                     for p, k, d in ((120, "1st buy", "base price"), (180, "2nd buy", "×1.5"), (270, "3rd+ buy", "×1.5, then stays")))
    cd = (f'<div class="statecard" style="gap:52px">{slot("siren",1,"active",.6)}<span>Running<small>5 s freeze, ring</small></span></div>'
          f'<div class="statecard" style="gap:52px">{slot("siren",1,"filled",cd=.7,cdt="6s")}<span>Cooldown<small>8 s radial + seconds</small></span></div>'
          f'<div class="statecard" style="gap:52px">{slot("siren",1,"disabled",lbl="Used this level")}<span>Used this level<small>grey 50%, can\'t fire again</small></span></div>')
    w = FRAMES[n][0] - 2*FRAMES[n][2] - 120
    body = f'''<div class="ov heavy"></div><div class="panel" style="width:{w}px;text-align:left;padding:36px 48px"><div class="ph" style="font-size:44px">VIP Siren · anti-exploit</div>
<div class="psub" style="font-size:24px">One per level · 8 s cooldown after it ends · price rises per run: ₦120 → ₦180 → ₦270 · resets at cash-out</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px 24px;margin-top:22px;--tile:1fr">{grid}</div>
<div style="display:flex;gap:14px;margin-top:26px">{ladder}{cd}</div></div>'''
    return page(None, n, 7, body, "VIP Siren states", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/mock.css"><link rel="stylesheet" href="../css/bag.css"></head>')

def intro_bag(n):
    lv = 7
    slots = "".join([slot("owa", 3), slot("maltina_gala", 2), slot("siren", 1), slot()])
    body = f'''<div class="ov"></div><div class="panel" style="width:1180px;text-align:left"><div style="color:#E8B21E;font-size:26px;letter-spacing:.12em">DISTRICT 7 OF 10</div>
<div class="ph" style="font-size:72px;color:#F5F5F0">{LV[lv][0]}</div><div class="psub">Two wahala dey road today: LASTMA flag <b style="color:#E07CC0">and</b> KAI officers. Hold your change.</div>
<div style="margin-top:30px;font-size:26px;color:#E8B21E;letter-spacing:.08em">IN YOUR BAG · carried over from Ikeja Along</div>
<div style="display:flex;gap:12px;margin-top:16px;align-items:center">{slots}<div style="margin-left:22px;font-size:24px;color:#9EA3AD;line-height:1.35">3 of 4 slots used.<br>Nothing fires by itself: tap a slot.<br>VIP Siren: one per level.</div></div>
<div class="row" style="justify-content:flex-end"><button class="gbtn">{icon("basecamp",44)} Base Camp</button><button class="cta sm">{icon("play",44,P["text"])} OYA, CROSS!</button></div></div>'''
    return page(None, n, lv, body, "Level intro with bag")

SCREENS = [("hud-bag", hud_bag), ("hud-bagfull", hud_bagfull), ("bag-states", bag_states), ("shop-bag", shop_bag), ("intro-bag", intro_bag), ("siren-states", siren_states)]
if __name__ == "__main__":
    for k, fn in SCREENS:
        for n in ("desktop", "phone"):
            open(os.path.join(OUT, f"{k}-{n}.html"), "w").write(fn(n))
    for w in (1920, 2340, 1440):
        x, y = bag_xy(w, 1080); print(w, "row x", round(x), "-", round(x+4*SLOT+3*GAP), "y", round(y), "-", round(y+SLOT))
