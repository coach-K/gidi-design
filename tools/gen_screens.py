"""Home, Base Camp shop, Game over mockups (landscape). Economy values come from
G-Prototype Economy/GidiEconomyTables.cs (copied into ECON below, do not edit by hand)."""
import os
from gen_hud import FRAMES, OUT

# --- from GidiEconomyTables.cs (team-branch, Oct 2026) ---
ECON = [  # id, display, blurb, cost, cap, first level
 ("owa","Owa","Shout freeze — short lane stop",80,3,2),
 ("maltina_gala","Maltina & Gala","Slows traffic briefly — not a speed boost",60,3,3),
 ("pure_water","Pure Water","Near-miss shield — one hit / ~2s, not run-through",60,2,3),
 ("bribe_change","Change Bundle","Settle LASTMA / KAI pressure",90,2,5),
 ("siren","VIP Siren","Short VIP clear (mid lane exempt)",100,2,5),
 ("agbero_whistle","Agbero Whistle","Brief reverse / crowd shove",120,2,7),
]
START_LIVES, MAX_CONTINUES = 3, 1
def continue_cost(l): return 100 if l <= 1 else 125
def cashout(l): return 50 if l <= 1 else 75
IAP = [("pack_skins_lagos","Lagos skins pack"),("pack_baba_fits","Baba fits pack"),("remove_ads","Remove ads")]
LEVEL = (3, "Ikorodu Road")   # sample context
ICON = {"owa":"📣","maltina_gala":"🥤","pure_water":"💧","bribe_change":"₦","siren":"🚨","agbero_whistle":"🎺"}

def shell(name, body, title):
    w,h,sl,sr,st,sb,label = FRAMES[name]
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title} {name}</title>
<link rel="stylesheet" href="../css/hud.css"><link rel="stylesheet" href="../css/mock.css"></head>
<body style="width:{w}px;height:{h}px"><div class="frame {name} bgscene" style="width:{w}px;height:{h}px;--sl:{sl}px;--sr:{sr}px;--st:{st}px;--sb:{sb}px">
{'<div class="notch"></div><div class="homebar"></div>' if name=='phone' else ''}
<div class="safe">{body}</div></div></body></html>"""

def wallet():
    return '''<div class="hud-tr"><div class="glass chips"><span class="amt">₦12,450</span><small>NAIRA CHIPS</small></div>
<div class="glass lives"><span class="heart">♥</span> 3</div>
<button class="glass btn"><span class="ico">⚙</span><small>Settings</small></button></div>'''

def home(name):
    lv, nm = LEVEL
    return shell(name, f'''
<div class="toprow"><div class="logo">GIDI<span>++</span><small>Cross Lagos. Don't get jammed.</small></div>{wallet()}</div>
<div class="rating">12+</div>
<div class="homecol">
  <button class="glass big2">🗺 Lagos map<small>10 districts</small></button>
  <button class="glass big2">🛍 Base Camp<small>Power-ups · fits</small></button>
  <button class="cta">▶ PLAY<small>L{lv} · {nm}</small></button>
</div>
<div class="tag glass">Dusk at Ikorodu Road · danfos running</div>''', "Home")

def shop(name):
    lv, nm = LEVEL
    rows = ""
    for pid, disp, blurb, cost, cap, first in ECON:
        locked = lv < first
        owned = {"owa":3,"maltina_gala":1,"pure_water":0}.get(pid,0)
        pips = "".join(f'<i class="{"on" if k<owned else ""}"></i>' for k in range(cap))
        btn = f'<button class="buy lock">🔒 L{first}</button>' if locked else (
              f'<button class="buy full">FULL</button>' if owned>=cap else f'<button class="buy">₦{cost}</button>')
        rows += f'''<div class="item glass {'locked' if locked else ''}"><div class="ic">{ICON[pid]}</div>
<div class="tx"><b>{disp}</b><span>{blurb}</span><span class="pips">{pips}<em>{owned}/{cap}</em></span></div>{btn}</div>'''
    iap = "".join(f'<div class="iap glass"><b>{d}</b><span>Store price</span></div>' for _,d in IAP)
    return shell(name, f'''
<div class="toprow"><div class="hud-tl glass"><div class="lvl">BASE CAMP</div><div class="meta">Before L{lv} · {nm}</div></div>{wallet()}</div>
<div class="shopgrid">{rows}</div>
<div class="iaprow"><span class="iaph">FITS &amp; EXTRAS · cosmetic only, no power for cash</span>{iap}</div>
<button class="cta shopgo">CROSS! ▶<small>L{lv} · {nm}</small></button>
<button class="glass btn back">◀<small>Back</small></button>''', "Base Camp")

def gameover(name):
    lv, nm = LEVEL
    return shell(name, f'''
<div class="dim"></div>
<div class="gopanel glass">
  <div class="goh">Eiya! That traffic got you…</div>
  <div class="gosub">Run over at L{lv} · {nm}</div>
  <div class="gostats">
    <div><b>4/6</b><span>Saved</span></div><div><b>00:31</b><span>Time · Best 00:42</span></div>
    <div><b>₦640</b><span>Run tips</span></div><div><b>{MAX_CONTINUES}/{MAX_CONTINUES}</b><span>Continue used</span></div>
  </div>
  <div class="gobtns">
    <button class="glass gob">🗺 Map</button><button class="glass gob">🛍 Base Camp</button>
    <button class="cta gocta">↻ RETRY L{lv}</button>
  </div>
  <div class="gonote">Fair play: max {MAX_CONTINUES} continue per run</div>
</div>''', "Game over")

if __name__ == "__main__":
    for n in FRAMES:
        for key, fn in (("home",home),("shop",shop),("gameover",gameover)):
            p = os.path.join(OUT, f"{key}-{n}.html"); open(p,"w").write(fn(n)); print(p)
