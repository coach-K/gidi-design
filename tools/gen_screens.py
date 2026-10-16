"""Home, Base Camp shop, Game over mockups (landscape). Economy values come from
G-Prototype Economy/GidiEconomyTables.cs (copied into ECON below, do not edit by hand)."""
import os
from gen_hud import FRAMES, OUT

# --- ids/caps/unlocks from GidiEconomyTables.cs; PRICES per vision doc v2 §8 (Kehinde, Oct 16): Malta 80, VIP Siren 120, Owa 80. Game code still to be updated ---
ECON = [  # id, display, blurb, cost, cap, first level
 ("owa","Owa","FREE · starts every run full · refill ₦80 per charge",80,3,2),  # vision: free; 80 = refill per charge
 ("maltina_gala","Malta & Agege Roll","Slows traffic briefly — not a speed boost",80,2,3),
 ("pure_water","Pure Water","Full immunity, once until cash-out",110,1,3),  # exception: follows the game, not vision (Kehinde, Oct 16); cap 1 resets at cash-out
 ("bribe_change","Change Bundle","Settle LASTMA / KAI pressure",90,2,5),
 ("siren","VIP Siren","Freezes all traffic · LASTMA ignores you",120,1,5),
]  # Agbero Whistle removed from the game (#39)
SOON = [("danfo_ride","Danfo Ride","Hop two lanes in a danfo",150,1,4),("gist_bomb","Gist Bomb","Radio gist pulls traffic off one lane",100,1,8)]
INFO = [("agbada_armour","Agbada Armour","2.5 s full immunity · fill the Owa meter","Earned"),("okada_dash","Okada Dash","Grab one at the curb and dash","Curb pickup")]
START_LIVES, MAX_CONTINUES = 3, 1
def continue_cost(l): return 100 if l <= 1 else 125
def cashout(l): return 50 if l <= 1 else 75
IAP = [("pack_skins_lagos","Lagos skins pack"),("pack_baba_fits","Baba fits pack"),("remove_ads","Remove ads")]
LEVELS = {"home": (9, "Lekki Toll Gate"), "shop": (4, "Mushin Market"), "gameover": (5, "Oshodi Expressway")}  # match each background (LevelManager names)
ICON = {"owa":"📣","maltina_gala":"🥤","pure_water":"💧","bribe_change":"₦","siren":"🚨"}

def shell(name, body, title, bg):
    w,h,sl,sr,st,sb,label = FRAMES[name]
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title} {name}</title>
<link rel="stylesheet" href="../css/hud.css"><link rel="stylesheet" href="../css/mock.css"></head>
<body style="width:{w}px;height:{h}px"><div class="frame {name} realbg {bg}" style="width:{w}px;height:{h}px;--sl:{sl}px;--sr:{sr}px;--st:{st}px;--sb:{sb}px"><img class="scene" src="../assets/bg/lv_{bg}_{name}.png" alt=""><div class="grade"></div>
{'<div class="notch"></div><div class="homebar"></div>' if name=='phone' else ''}
<div class="safe">{body}</div></div></body></html>"""

def wallet():
    return '''<div class="hud-tr"><div class="glass chips"><span class="amt">₦12,450</span><small>NAIRA CHIPS</small></div>
<div class="glass lives"><span class="heart">♥</span> 3</div>
<button class="glass btn"><span class="ico">⚙</span><small>Settings</small></button></div>'''

def home(name):
    lv, nm = LEVELS["home"]
    return shell(name, f'''
<div class="toprow"><div class="logo">GIDI<span>++</span><small>Carry dem cross. Lagos no dey wait.</small></div>{wallet()}</div>
<div class="rating">12+</div>
<div class="homecol">
  <button class="glass big2">🗺 Lagos map<small>10 districts · Agege to Ojuelegba</small></button>
  <button class="glass big2">🛍 Base Camp<small>Load your bag before you cross</small></button>
  <button class="cta">▶ OYA, PLAY<small>L{lv} · {nm}</small></button>
</div>
<div class="tag glass">Baba Gidi don ready. Owa! 📣</div>''', "Home", "home")

def shop(name):
    """3x3 Base Camp grid (Oct 16 final): 5 buyable, 2 coming soon (price shown), 2 not-for-sale info tiles. Agbero Whistle removed (#39)."""
    from brand import badge, icon
    lv, nm = LEVELS["shop"]
    E = {e[0]: e for e in ECON}; SO = {e[0]: e for e in SOON}; IN = {e[0]: e for e in INFO}
    order = ["owa","pure_water","maltina_gala","bribe_change","siren","danfo_ride","gist_bomb","agbada_armour","okada_dash"]
    rows = ""
    for pid in order:
        if pid in E:
            _, disp, blurb, cost, cap, first = E[pid]
            locked = lv < first
            owned = {"owa":2,"maltina_gala":1,"pure_water":0}.get(pid,0)
            pips = "".join(f'<i class="{"on" if k<owned else ""}"></i>' for k in range(cap))
            btn = f'<button class="buy lock">{icon("lock",30,"#9EA3AD")} L{first}</button>' if locked else (
                  f'<button class="buy full">Bag full</button>' if owned>=cap else (f'<button class="buy full sm2" style="width:200px;min-width:200px">used, cash out to refresh</button>' if (pid=="pure_water" and name=="phone") else f'<span class="owabtns"><button class="buy sm2">Buy 1<br>₦{cost}</button><button class="buy sm2">Fill all<br>₦{cost*(cap-owned)}</button></span>' if pid=="owa" else f'<button class="buy">₦{cost}</button>'))
            rows += f'''<div class="item glass {'locked' if locked else ''}"><div class="ic">{badge(pid,96)}</div>
<div class="tx"><b>{"Owa refill" if pid=="owa" else disp}</b><span>{blurb}</span><span class="pips">{pips}<em>{owned}/{cap}</em></span></div>{btn}</div>'''
        elif pid in SO:
            _, disp, blurb, cost, cap, first = SO[pid]
            rows += f'''<div class="item glass soon"><span class="ribbon">COMING SOON</span><div class="ic">{badge(pid,96)}</div>
<div class="tx"><b>{disp}</b><span>{blurb}</span></div><button class="buy soonbtn">{icon("lock",28,"#9EA3AD")}<span>₦{cost}</span></button></div>'''
        else:
            _, disp, blurb, tag = IN[pid]
            rows += f'''<div class="item info"><div class="ic">{badge(pid,96)}</div>
<div class="tx"><b>{disp}</b><span>{blurb}</span></div><span class="infotag">{tag.upper()}</span></div>'''
    iap = "".join(f'<div class="iap glass"><b>{d}</b><span>Store price</span></div>' for _,d in IAP)
    return shell(name, f'''
<div class="toprow"><div class="hud-tl glass"><div class="lvl">BASE CAMP</div><div class="meta">Load your bag before L{lv} · {nm}</div></div>{wallet()}</div>
<div class="shopgrid g3">{rows}</div>
<div class="iaprow"><span class="iaph">FITS &amp; EXTRAS · na drip only, no power for cash</span>{iap}</div>
<button class="cta shopgo">OYA, CROSS! ▶<small>L{lv} · {nm}</small></button>
<button class="glass btn back">◀<small>Back</small></button>''', "Base Camp", "shop")

def gameover(name):
    lv, nm = LEVELS["gameover"]
    return shell(name, f'''
<div class="dim"></div>
<div class="gopanel glass">
  <div class="goh">Chai! Traffic don catch you…</div>
  <div class="gosub">Run don end for L{lv} · {nm}. No wahala, try am again.</div>
  <div class="gostats">
    <div><b>4/6</b><span>Saved</span></div><div><b>00:31</b><span>Time · Best 00:42</span></div>
    <div><b>₦640</b><span>Run tips</span></div><div><b>{MAX_CONTINUES}/{MAX_CONTINUES}</b><span>Continue used</span></div>
  </div>
  <div class="gobtns">
    <button class="glass gob">🗺 Map</button><button class="glass gob">🛍 Base Camp</button>
    <button class="cta gocta">↻ TRY AM AGAIN</button>
  </div>
  <div class="gonote">Fair play: max {MAX_CONTINUES} continue per run</div>
</div>''', "Game over", "gameover")

if __name__ == "__main__":
    for n in FRAMES:
        for key, fn in (("home",home),("shop",shop),("gameover",gameover)):
            p = os.path.join(OUT, f"{key}-{n}.html"); open(p,"w").write(fn(n)); print(p)
