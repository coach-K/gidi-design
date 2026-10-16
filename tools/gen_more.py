"""All remaining landscape screens (desktop 1920x1080, phone 2340x1080). Backgrounds: cleaned + dusk-graded real level
screenshots (assets/bg/Lxx_*.png from prep_levels.py). Numbers: prices per vision doc v2 (Kehinde, Oct 16); other values GidiEconomyTables / LevelManager; others are samples or TBD."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT, controls
from gen_screens import ECON, MAX_CONTINUES, START_LIVES, continue_cost, cashout
from brand import icon, badge, logo_mark, wordmark, P

# LevelManager.CreateDefaultLevels / Resources/Campaign/LagosCampaign.asset
LV = {1:("Agege Bus Stop",5),2:("Surulere Way",5),3:("Ikorodu Road",5),4:("Mushin Market",5),5:("Oshodi Expressway",5),
      6:("Ikeja Along",6),7:("Ojota Intersect",7),8:("Third Mainland Bridge",8),9:("Lekki Toll Gate",8),10:("Ojuelegba Chaos",8)}
LIVE = {pid:first for pid,_,_,_,_,first in ECON}
DUR = {"owa":4,"maltina_gala":4,"siren":5,"bribe_change":6,"agbero_whistle":6}  # LevelManager / GameManager seconds

def lab(n): return f"L{n} · {LV[n][0]}"

def shell(name, lv, body, title, blur=False, ctl=False):
    w,h,sl,sr,st,sb,_ = FRAMES[name]
    bg = f"../assets/bg/L{lv:02d}_{name}{'_blur' if blur else ''}.png"
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title} {name}</title>
<link rel="stylesheet" href="../css/hud.css"><link rel="stylesheet" href="../css/mock.css"><link rel="stylesheet" href="../css/more.css"></head>
<body style="width:{w}px;height:{h}px"><div class="frame {name} realbg" style="width:{w}px;height:{h}px;--sl:{sl}px;--sr:{sr}px;--st:{st}px;--sb:{sb}px"><img class="scene" src="{bg}" alt="">
{'<div class="notch"></div><div class="homebar"></div>' if name=='phone' else ''}
<div class="safe">{body}</div>{controls(w,h) if ctl else ''}</div></body></html>"""

def stock(g=(2,3), c=(1,2), o=(1,3), hi=None):
    def cell(k, v, cls=""):
        return f'<div class="cell {cls}"{" style=\"background:rgba(232,178,30,.18)\"" if hi==k else ""}><span class="k">{k}</span><span class="pips">'+"".join(f'<i class="{"on" if i<v[0] else ""}"></i>' for i in range(v[1]))+'</span></div>'
    return f'<div class="hud-tc glass{" hilite" if hi=="all" else ""}">{cell("GROUP",g)}{cell("CHANGE",c)}{cell("OWA!",o,"owa")}</div>'

def top_hud(lv, meta, **kw):
    return f'''<div class="toprow"><div class="hud-tl glass"><div class="lvl{' long' if len(lab(lv))>18 else ''}">{lab(lv)}</div><div class="meta">{meta}</div></div>
{stock(**kw)}<div class="hud-tr"><div class="glass chips"><span class="amt">₦12,450</span><small>NAIRA CHIPS</small></div>
<div class="glass lives"><span class="heart">♥</span> {START_LIVES}</div>
<button class="glass btn">{icon("stats",44,P["text"])}<small>Stats</small></button><button class="glass btn">{icon("pause",44,P["text"])}<small>Pause</small></button></div></div>'''

META = 'Saved <b>4/6</b> · Best <b>00:42</b> · <span class="t">00:31</span>'

def wallet():
    return f'''<div class="hud-tr"><div class="glass chips"><span class="amt">₦12,450</span><small>NAIRA CHIPS</small></div>
<div class="glass lives"><span class="heart">♥</span> {START_LIVES}</div><button class="glass btn">{icon("settings",44,P["text"])}<small>Settings</small></button></div>'''

def title_row(t, ic="back"):
    return f'<div class="toprow"><div class="ptitle"><button class="glass btn">{icon(ic,44,P["text"])}<small>Back</small></button>{t}</div><div></div>{wallet()}</div>'

# ---------------- screens ----------------
def splash(n):
    return shell(n, 1, f'''<div class="ov heavy"></div><div class="splash">{logo_mark(220)}{wordmark(150,True,True)}
<div class="bar"><i></i></div><div style="font-size:28px;color:#9EA3AD">Loading Agege Bus Stop… <span style="color:#FAE69E">Tip: Owa! freeze the next lane.</span></div></div>
<div class="rating" style="top:auto;bottom:24px;z-index:3">12+</div>''', "Splash", blur=True)

def lagos_map(n):
    cur = 3
    xs = [3,13,23,33,43,53,63,73,83,93]; ys = [55,30,52,22,46,18,42,14,38,10]
    nodes = ""
    for i in range(1,11):
        cls = "done" if i<cur else "cur" if i==cur else "lock"
        inner = "✓" if i<cur else (icon("lock",40,P["muted"]) if i>cur else f"L{i}")
        if i==10 and i>cur: inner = "∞"
        nodes += f'<div class="node {cls}" style="left:calc({xs[i-1]}% - 75px);top:{ys[i-1]}%"><div class="d">{inner}</div>L{i} {LV[i][0]}</div>'
    path = " ".join(f"{x*10},{y*4.4+40}" for x,y in zip(xs,ys))
    return shell(n, cur, f'''<div class="ov"></div>{title_row("Lagos map","back")}
<div class="mapline" style="top:170px;height:470px"><svg viewBox="0 0 1000 440" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%"><polyline points="{path}" fill="none" stroke="#E8B21E" stroke-width="5" stroke-dasharray="14 12" stroke-opacity=".7" vector-effect="non-scaling-stroke"/></svg>{nodes}</div>
<div class="dcard glass" style="width:600px;bottom:24px"><h3>{lab(cur)}</h3><div class="kv"><span>Lanes</span><b>{LV[cur][1]}</b><span>Crowd</span><b>5 · Agbada Bigman joins</b><span>Best</span><b>00:42 <span class="sample">sample</span></b><span>Stars</span><b><span class="tbd">TBD</span></b></div>
<button class="cta sm" style="width:100%">{icon("play",44,P["text"])} OYA, CROSS!</button></div>
<div class="toast" style="bottom:40px;left:34%">{icon("lock",32)} Clear Ikorodu Road first to open Mushin</div>''', "Map", blur=True)

def intro(n):
    lv = 6
    live = [pid for pid,_,_,_,_,f in ECON if f<=lv]
    chips = "".join(f'<span class="mini">{badge(p,40)}{d}</span>' for p,d,_,_,_,f in ECON if f<=lv)
    return shell(n, lv, f'''<div class="ov"></div>
<div class="panel" style="width:1180px;text-align:left"><div style="color:#E8B21E;font-size:26px;letter-spacing:.12em">DISTRICT 6 OF 10</div>
<div class="ph" style="font-size:72px;color:#F5F5F0">{LV[lv][0]}</div><div class="psub">Two wahala dey road today: LASTMA flag <b style="color:#E07CC0">and</b> KAI officers. Hold your change.</div>
<div class="grid4"><div class="stat"><b>{LV[lv][1]}</b><span>Lanes (first 6-lane road)</span></div><div class="stat"><b>7</b><span>People for curb</span></div><div class="stat"><b style="color:#E07CC0">LASTMA + KAI</b><span>Enforcement</span></div><div class="stat"><b>{continue_cost(lv)}</b><span>Continue (chips)</span></div></div>
<div style="margin-top:22px;font-size:24px;color:#9EA3AD">Power-ups live here</div><div class="chipsrow">{chips}</div>
<div class="row" style="justify-content:flex-end"><button class="gbtn">{icon("basecamp",44)} Base Camp</button><button class="cta sm">{icon("play",44,P["text"])} OYA, CROSS!</button></div></div>''', "Level intro")

def onboard(n, step):
    texts = {1:"Move Baba Gidi with the d-pad. Waka go the curb.",
             2:"Read the road: ▲ caution, ≫ danger. Wait for your gap.",
             3:"Your stock: GROUP → CHANGE → OWA!",
             4:"Reach the far curb with your people. We don reach!"}
    w,h = FRAMES[n][:2]
    extra = ""
    if step==1:
        dx,dy,dr = 0.861*w,0.702*h,0.167*h
        extra = f'<div class="ring c" style="position:fixed;left:{dx-dr-14:.0f}px;top:{dy-dr-14:.0f}px;width:{2*dr+28:.0f}px;height:{2*dr+28:.0f}px"></div>'
        px,py,pr = 0.122*w,0.729*h,0.1*h
        extra += f'<div class="tele" style="position:fixed;left:{px-80:.0f}px;top:{py-pr-70:.0f}px;z-index:6">{icon("pickup_person",32)} PICK UP when a person lights up</div>'
    if step==2:
        extra = (f'<div class="tele" style="position:fixed;left:{w*0.12:.0f}px;top:{h*0.36:.0f}px;border:3px solid {P["caution"]}">{icon("warn_caution",40)} Caution · slow down</div>'
                 f'<div class="tele" style="position:fixed;left:{w*0.52:.0f}px;top:{h*0.43:.0f}px;border:3px solid {P["danger"]}">{icon("warn_danger",40)} Danger · Danfo dey come</div>')
    if step==3: pass
    if step==4:
        extra = f'<div class="goal" style="position:fixed;left:{w*0.1:.0f}px;right:{w*0.1:.0f}px;top:{h*0.20:.0f}px;height:{h*0.08:.0f}px"><span style="top:auto;bottom:-54px">GOAL · far curb</span></div>'
    coach = f'<div class="coach"{chr(32)+'style="top:560px"' if step==4 else ''}><span class="n">{step}</span>{texts[step]}</div>'
    dots = '<div class="dots">'+"".join(f'<i class="{"on" if i==step else ""}"></i>' for i in range(1,5))+'</div>'
    skip = '' if step==1 else '<button class="gbtn skip" style="min-width:200px">Skip</button>'
    return shell(n, 1, top_hud(1, 'Tutorial · <b>step '+str(step)+'/4</b>', g=(0,3) if step<3 else (2,3), c=(0,2), o=(0,3), hi="all" if step==3 else None)+coach+skip+dots+extra, f"Onboarding {step}", ctl=True)

def hud_power(n):
    lv = 7; w,h = FRAMES[n][:2]
    def ring(p, frac, label):
        import math
        a = 2*math.pi*frac; x = 85+75*math.sin(a); y = 85-75*math.cos(a); large = 1 if frac>.5 else 0
        return f'<div class="puc">{badge(p,140)}<svg class="r" viewBox="0 0 170 170"><circle cx="85" cy="85" r="75" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="10"/><path d="M85 10 A75 75 0 {large} 1 {x:.1f} {y:.1f}" fill="none" stroke="#E8B21E" stroke-width="10" stroke-linecap="round"/></svg><div class="t">{label}</div></div>'
    return shell(n, lv, top_hud(lv, META, o=(2,3))+
      f'<div class="pu" style="left:50%;transform:translateX(-50%);top:190px">{ring("maltina_gala",.62,"Malta · 2.5s")}</div>'
      f'<div class="toast" style="top:420px;border-color:#C8743A">{icon("maltina_gala",36,"#C8743A")} Malta break! Traffic slow down 60% for {DUR["maltina_gala"]}s</div>', "HUD power-up", ctl=True)

def hud_warn(n):
    lv = 8; w,h = FRAMES[n][:2]
    t = lambda x,y,ic,txt,c: f'<div class="tele" style="position:fixed;left:{x*w:.0f}px;top:{y*h:.0f}px;border:3px solid {c}">{icon(ic,44)} {txt}</div>'
    return shell(n, lv, top_hud(lv, META)+
      t(0.06,0.20,"warn_caution","CAUTION",P["caution"])+t(0.66,0.30,"warn_danger","DANGER",P["danger"])+t(0.30,0.42,"warn_lastma","LASTMA",P["lastma"])+
      t(0.70,0.50,"warn_safe","GAP · GO",P["safe"]), "HUD warnings", ctl=True)

def hud_toast(n):
    lv = 2
    return shell(n, lv, top_hud(lv, 'Saved <b>2/4</b> · Best <b>00:51</b> · <span class="t">00:18</span>', o=(1,3), hi="OWA!")+
      f'<div class="toast" style="top:200px">{icon("owa",40)} Owa! unlocked in Surulere Way. Shout to freeze the next Danfo lane.</div>'
      f'<div class="toast" style="top:300px;color:#F5F5F0;border-color:rgba(89,217,184,.6)">{icon("group",36,"#59D9B8")} They\'re with you. Take one more, or cross now.</div>'
      f'<div class="toast" style="top:400px;color:#F5F5F0">{icon("chip",36)} Found Owa</div>', "HUD toasts", ctl=True)

def hud_endless(n):
    lv = 10
    return shell(n, lv, top_hud(lv, 'Endless · <b>no goal zone</b>', o=(2,3))+
      f'<div class="endl glass">Score <b>1,482</b> · <b>912 m</b> · <b>14</b> delivered · combo <b>x6</b> · Best <b>2,050</b></div>'
      f'<div class="toast" style="top:300px">Combo x6! +10 per step · +25 per delivery</div>', "HUD endless", ctl=True)

def pause(n):
    lv = 5
    return shell(n, lv, f'''<div class="ov"></div><div class="panel" style="width:900px"><div class="ph">Pause. Breathe small.</div><div class="psub">{lab(lv)} · Saved 4/6 · 00:31</div>
<div style="display:flex;flex-direction:column;gap:18px;margin-top:34px"><button class="cta sm" style="width:100%">{icon("play",44,P["text"])} CONTINUE CROSSING</button>
<div class="row" style="margin:0"><button class="gbtn" style="flex:1">↻ Restart</button><button class="gbtn" style="flex:1">{icon("settings",40)} Settings</button></div>
<div class="row" style="margin:0"><button class="gbtn" style="flex:1">{icon("map",40)} Lagos map</button><button class="gbtn" style="flex:1">{icon("stats",40)} Stats</button></div></div></div>''', "Pause", blur=True)

def stats(n):
    lv = 5
    return shell(n, lv, f'''<div class="ov"></div><div class="panel" style="width:1300px"><div class="ph">Your run so far</div><div class="psub">{lab(lv)} · values are samples</div>
<div class="grid4"><div class="stat"><b>4/6</b><span>Saved</span></div><div class="stat"><b>00:31</b><span>Time · Best 00:42</span></div><div class="stat"><b>₦640</b><span>Run tips</span></div><div class="stat"><b>0/{MAX_CONTINUES}</b><span>Continue used</span></div>
<div class="stat"><b>2</b><span>Owa! shouts</span></div><div class="stat"><b>1</b><span>Near misses</span></div><div class="stat"><b>{START_LIVES}</b><span>Lives</span></div><div class="stat"><b>{continue_cost(lv)}</b><span>Continue cost (chips)</span></div></div>
<div class="row"><button class="cta sm">{icon("back",40,P["text"])} BACK TO RUN</button></div></div>''', "Stats", blur=True)

def cont(n):
    lv = 5; c = continue_cost(lv)
    return shell(n, lv, f'''<div class="ov heavy"></div><div class="panel" style="width:1000px"><div style="color:#E8B21E;font-size:26px;letter-spacing:.12em">ALMOST THERE</div>
<div class="ph" style="color:#F5F5F0">Continue this run?</div><div class="psub">Keep the curb run alive · {lab(lv)}</div>
<div style="display:flex;flex-direction:column;gap:18px;margin-top:30px"><button class="cta sm" style="width:100%">{icon("ad",44,P["text"])} Watch ad, continue</button>
<button class="gbtn" style="width:100%;color:#FAE69E">{icon("chip",44)} Continue: ₦{c} Naira Chips</button><button class="gbtn" style="width:100%;color:#9EA3AD">End run</button></div>
<div class="psub" style="font-size:26px;margin-top:22px">Naira Chips 12,450 · Fair play: max {MAX_CONTINUES} continue per run</div></div>''', "Continue", blur=True)

def clear(n):
    lv = 6; nxt = 7
    return shell(n, lv, f'''<div class="ov"></div><div class="panel" style="width:1600px"><div class="ph" style="font-size:72px">{LV[lv][0]} Cleared!</div><div class="psub">We don reach! Everybody cross safe.</div>
<div class="grid4"><div class="stat"><b>7/7</b><span>Saved</span></div><div class="stat"><b>00:48</b><span>Time</span></div><div class="stat"><b>+{cashout(lv)}</b><span>Cash-out grant (chips)</span></div><div class="stat"><b><span class="tbd" style="font-size:30px">TBD</span></b><span>Stars rule</span></div></div>
<div class="row"><button class="gbtn">{icon("map",40)} Map</button><button class="gbtn">{icon("basecamp",40)} Base Camp</button><button class="cta sm">NEXT: {lab(nxt)} {icon("play",40,P["text"])}</button></div></div>''', "Level clear", blur=True)

def settings(n):
    lv = 9
    sl = lambda t,s,v: f'<div class="srow"><div>{t}<small>{s}</small></div><div class="slider"><i style="width:{v}%"></i><b style="left:{v}%"></b></div></div>'
    tg = lambda t,s,on: f'<div class="srow"><div>{t}<small>{s}</small></div><div class="tog {"on" if on else ""}"><b></b></div></div>'
    tabs = "".join(f'<div class="tab {"on" if i==0 else ""}">{t}</div>' for i,t in enumerate(["Audio","Controls","Display","Accessibility","Account"]))
    return shell(n, lv, f'''<div class="ov heavy"></div>{title_row("Settings")}
<div class="setgrid"><div class="glass tabs">{tabs}</div><div class="glass setbody">{sl("Music","Afrobeats / amapiano loop",70)}{sl("SFX","Horns, danfo, crowd",85)}{sl("Voice","Owa!, conductor calls",60)}
{tg("Colour-blind mode","Danger #D55E00 + thicker chevrons",False)}<div class="srow"><div>Text size<small>S / M / L</small></div><div class="seg"><span>S</span><span class="on">M</span><span>L</span></div></div></div></div>''', "Settings", blur=True)

def credits(n):
    lv = 10
    return shell(n, lv, f'''<div class="ov heavy"></div>{title_row("Credits")}
<div class="credits glass">{wordmark(110)}<h4>MADE IN LAGOS BY</h4><p>Gidi++ team <span class="tbd">names TBD</span></p>
<h4>TYPE</h4><p>Plus Jakarta Sans · Tokotype · SIL Open Font License 1.1</p><h4>ENGINE</h4><p>Unity 6 · Universal Render Pipeline</p>
<h4>MUSIC &amp; SFX</h4><p><span class="tbd">TBD</span></p><h4>THANKS</h4><p>Every Lagos commuter wey dey cross daily. Una try!</p></div>''', "Credits", blur=True)

SCREENS = [("splash",splash),("map",lagos_map),("intro",intro)]+[(f"onboard{i}",(lambda i: lambda n: onboard(n,i))(i)) for i in range(1,5)]+\
  [("hud-power",hud_power),("hud-warn",hud_warn),("hud-toast",hud_toast),("hud-endless",hud_endless),("pause",pause),("stats",stats),
   ("continue",cont),("clear",clear),("settings",settings),("credits",credits)]
if __name__ == "__main__":
    for key, fn in SCREENS:
        for n in FRAMES:
            open(os.path.join(OUT, f"{key}-{n}.html"), "w").write(fn(n))
    print(" ".join(k for k,_ in SCREENS))
