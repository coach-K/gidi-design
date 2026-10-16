"""Section bodies for the design site (screens, levels, icons, logos, costumes, souvenirs, devices, type, palette)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import P, icon, badge, ICONS, GROUPS, PU_ACCENT, logo_mark, wordmark

SCREENS = [  # key, title, group, note
 ("splash","Splash / boot","Boot","Logo, 12+ badge, loading bar with a tip toast. Background: L1 Agege Bus Stop (blurred)."),
 ("home","Title / home","Menus","Play (thumb zone, bottom-right), Lagos map, Base Camp, wallet, Settings. Background: L9 Lekki Toll Gate."),
 ("map","Lagos map level select","Menus","10 districts on a stylised road line; current district auto-centred; locked toast. Background: L3 Ikorodu Road."),
 ("intro","Level intro (district card)","Menus","Lanes, people, enforcement, live power-ups and continue cost from code. Background: L6 Ikeja Along."),
 ("onboard1","Onboarding 1 · Move","Onboarding","Coach pill + highlighted d-pad; PICK UP hint (code copy). Background: L1 Agege Bus Stop."),
 ("onboard2","Onboarding 2 · Read the road","Onboarding","Caution triangle vs Danger chevrons on the lanes."),
 ("onboard3","Onboarding 3 · Stock","Onboarding","GROUP → CHANGE → OWA! highlighted."),
 ("onboard4","Onboarding 4 · Reach the curb","Onboarding","Goal zone on the far curb. Skippable after step 1."),
 ("hud","In-run HUD (base)","In-run","Approved round-4 HUD. Background: L5 Oshodi Expressway."),
 ("hud-power","HUD · power-up active","In-run","Maltina ring timer (4 s, traffic −60%, LevelManager). Background: L7 Ojota Intersect."),
 ("hud-warn","HUD · warnings (colour + shape)","In-run","Caution ▲, Danger ≫, LASTMA ◆, Safe gap bar. Background: L8 Third Mainland Bridge (8 lanes, wide camera)."),
 ("hud-toast","HUD · toasts","In-run","Owa unlock (code copy), group coach line, \"Found Owa\" grant toast. Background: L2 Surulere Way."),
 ("hud-endless","HUD · endless (L10)","In-run","Score = metres + 25/delivery + 10/combo step (EndlessRunScore). Background: L10 Ojuelegba Chaos."),
 ("pause","Pause","Run modals","Resume, Restart, Settings, Map, Stats. Background: L5 (blurred)."),
 ("stats","Stats","Run modals","Run stats (values are samples)."),
 ("continue","Continue modal (1 per run)","Run modals","Watch ad / ₦125 chips at L2+ (₦100 at L1) / End run. MaxContinuesPerRun = 1."),
 ("clear","Level clear","Results","\"{location} Cleared!\" (code copy). Cash-out grant 75 chips (L2+). Stars rule TBD. Background: L6 Ikeja Along."),
 ("gameover","Game over","Results","After the single continue is used or declined. Background: L5."),
 ("shop","Base Camp shop","Menus","Six soft power-ups, caps, costs and unlock levels from GidiEconomyTables. Background: L4 Mushin Market."),
 ("settings","Settings","Menus","Audio, Controls (touch only), Display, Accessibility, Account. Background: L9 (blurred)."),
 ("credits","Credits","Menus","Names TBD. Background: L10 (blurred)."),
]

FLOW_NODES = {  # key: (col, row)
 "splash":(0,1),"onboard1":(1,0),"home":(1,1),"map":(2,1),"shop":(2,2),"settings":(2,0),"credits":(3,0),"intro":(3,1),
 "hud":(4,1),"pause":(5,0),"continue":(5,1),"clear":(5,2),"gameover":(6,1),"stats":(6,0)}
FLOW_EDGES = [("splash","home"),("splash","onboard1"),("onboard1","home"),("home","map"),("home","shop"),("home","settings"),("settings","credits"),
 ("map","intro"),("shop","intro"),("intro","hud"),("hud","pause"),("pause","stats"),("hud","continue"),("continue","hud"),("continue","gameover"),
 ("hud","clear"),("clear","map"),("gameover","map"),("gameover","hud")]

def flow_svg():
    W,H,bw,bh = 1400, 520, 170, 74
    pos = {k:(30+c*200, 40+r*160) for k,(c,r) in FLOW_NODES.items()}
    title = dict(splash="Splash / boot",onboard1="Onboarding 1–4",home="Home",map="Lagos map",shop="Base Camp",settings="Settings",credits="Credits",
                 intro="Level intro",hud="In-run HUD + states",pause="Pause",continue_="",clear="Level clear",gameover="Game over",stats="Stats"); title["continue"]="Continue (1/run)"
    s = f'<svg viewBox="0 0 {W} {H}" class="flow" role="img" aria-label="Screen flow"><defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#E8B21E"/></marker></defs>'
    for a,b in FLOW_EDGES:
        (x1,y1),(x2,y2) = pos[a],pos[b]
        cx1,cy1,cx2,cy2 = x1+bw/2,y1+bh/2,x2+bw/2,y2+bh/2
        # clip to box edges
        import math
        dx,dy = cx2-cx1, cy2-cy1; L = math.hypot(dx,dy) or 1
        def clip(dx,dy):
            tx = (bw/2)/abs(dx) if dx else 1e9; ty = (bh/2)/abs(dy) if dy else 1e9; t=min(tx,ty); return dx*t, dy*t
        ox,oy = clip(dx,dy)
        bend = 26 if (b,a) in FLOW_EDGES else 0
        mx,my = (cx1+cx2)/2 - dy/L*bend, (cy1+cy2)/2 + dx/L*bend
        s += f'<path d="M{cx1+ox:.0f} {cy1+oy:.0f} Q{mx:.0f} {my:.0f} {cx2-ox:.0f} {cy2-oy:.0f}" fill="none" stroke="#E8B21E" stroke-width="2.5" stroke-opacity=".8" marker-end="url(#ar)"/>'
    for k,(x,y) in pos.items():
        s += f'<a href="#s-{k}"><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="16" fill="#0F1219" fill-opacity=".9" stroke="#FAE69E" stroke-opacity=".5" stroke-width="2"/><text x="{x+bw/2}" y="{y+bh/2+6}" text-anchor="middle" fill="#F5F5F0" font-family="Jakarta,sans-serif" font-weight="700" font-size="16">{title[k]}</text></a>'
    return s + '</svg>'

def screens():
    groups = []
    for k,t,g,_ in SCREENS:
        if g not in groups: groups.append(g)
    toc = " · ".join(f'<a href="#s-{k}">{t}</a>' for k,t,_,_ in SCREENS)
    body = f'''<h1>Screens <span class="badge" style="background:#56B4E9">ROUND 4 APPROVED · full set</span></h1>
<p class="lead">Every screen from splash onward, <b>landscape only</b>, each as desktop / WebGL 1920×1080 and phone 19.5:9 2340×1080 (notch and home-indicator safe areas). Backgrounds are the real L1–L10 level screenshots from the current build (old HUD removed, dusk grade). Controls, camera, font, palette and copy follow the approved round-4 mockups. Economy numbers come from <code>GidiEconomyTables</code> and level facts from <code>LevelManager</code>; wallet, timer and score values are samples; anything undefined is marked <span class="badge">TBD</span>.</p>
<h2 id="flow">Flow</h2><div class="card scroll">{flow_svg()}</div><p class="small">Tap a box to jump to the screen. Onboarding runs on first launch (skippable after step 1); Continue appears once per run, then Game over.</p>
<div class="card toc">{toc}</div>'''
    for g in groups:
        body += f'<h2>{g}</h2>'
        for k,t,gg,note in SCREENS:
            if gg != g: continue
            d = f"exports/hud/hud-desktop.png" if k=="hud" else f"exports/{k}-desktop.png"
            p = f"exports/hud/hud-phone.png" if k=="hud" else f"exports/{k}-phone.png"
            body += f'''<section id="s-{k}" class="scr"><h3>{t}</h3><p>{note}</p><div class="pair"><a href="{d}"><img loading="lazy" class="shot" src="{d}" alt="{t}, desktop 1920×1080"></a><a href="{p}"><img loading="lazy" class="shot" src="{p}" alt="{t}, phone 2340×1080"></a></div><p class="small">Desktop 1920×1080 · Phone 2340×1080 · source <code>mockups/{k}-desktop.html</code></p></section>'''
    body += '''<h2 id="hud-spec">HUD spec (annotated)</h2><img loading="lazy" class="shot" src="exports/hud/hud-desktop-annotated.png" alt="Annotated HUD desktop"><p></p><img loading="lazy" class="shot" src="exports/hud/hud-phone-annotated.png" alt="Annotated HUD phone"><p>Spec: <a href="exports/hud/HUD_Landscape_Spec.md">HUD_Landscape_Spec.md</a>.</p>'''
    return body

# LevelManager.CreateDefaultLevels (== Resources/Campaign/LagosCampaign.asset), team-branch Oct 2026
LEVELS = [ # n, name, pool, speedMul, gapOffset, lanes, speedVar, luxury, lastma, kai, agbada, slay, regularOnly, powerups, endless
 (1,"Agege Bus Stop",3,0.46,1.2,5,0,0,0,0,0,0,1,[],0),
 (2,"Surulere Way",4,0.45,0.8,5,0,0,0,0,0,0,1,["owa"],0),
 (3,"Ikorodu Road",5,0.43,0.9,5,0,0,0,0,1,0,0,["owa","maltina_gala","pure_water"],0),
 (4,"Mushin Market",6,0.55,0.6,5,0,0,0,0,1,1,0,["owa","maltina_gala","pure_water"],0),
 (5,"Oshodi Expressway",6,0.56,0.5,5,0,0,1,0,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren"],0),
 (6,"Ikeja Along",7,0.55,0.9,6,0,0,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren"],0),
 (7,"Ojota Intersect",7,0.55,1.0,7,0.15,0,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren","agbero_whistle"],0),
 (8,"Third Mainland Bridge",8,1.2,0.35,8,0,0,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren","agbero_whistle"],0),
 (9,"Lekki Toll Gate",8,1.35,0.1,8,0,3,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren","agbero_whistle"],0),
 (10,"Ojuelegba Chaos",8,1.45,0.0,8,0.35,3.5,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren","agbero_whistle"],1),
]
LEVEL_NOTES = {1:"Tutorial. Commuters only, widest gaps (+1.2 s). No power-ups; Owa! not yet unlocked.",
 2:"Owa! unlocks here (toast). Base Camp opens (ShopAllowed L2+). Continue cost rises to 125 chips.",
 3:"First Agbada Bigman in the curb mix. Maltina &amp; Gala and Pure Water start spawning.",
 4:"Slay Queen joins the mix. Traffic jumps to ×0.55 with tighter gaps (+0.6 s).",
 5:"LASTMA flag enforcement starts (every 5–8 s, lane slows to ×0.8). Change Bundle and VIP Siren appear.",
 6:"First 6-lane road. KAI officers join LASTMA (KAI bribe ₦200).",
 7:"7 lanes, per-lane speed variation ±15%. Agbero Whistle unlocks (L7+).",
 8:"8 lanes: wide camera (20 m, FOV 58°). Traffic ×1.2, gaps +0.35 s. Big difficulty step.",
 9:"Luxury/aggressive cars +3 speed bonus, near-zero gap offset (+0.1 s).",
 10:"Truly endless: no goal zone. Difficulty climbs every 20 s (+4% speed, −0.05 s gaps per tick); ±35% lane variation. Score = metres + 25/delivery + 10/combo step."}
from gen_screens import ECON
NAMES = {p:d for p,d,*_ in ECON}

def levels():
    cards = ""
    for n,name,pool,mul,gap,lanes,var,lux,la,kai,ag,sq,reg,pus,endless in LEVELS:
        cruise = 12*(1+0.12*(n-1))*mul
        tags = [f"{lanes} lanes"] + (["wide camera"] if lanes>=8 else []) + (["LASTMA"] if la else []) + (["KAI"] if kai else []) + (["ENDLESS"] if endless else []) + (["Day grade"] if n<=4 else ["Dusk grade"])
        diff = min(5, 1 + (n>=4) + (n>=6) + (n>=8) + (n>=10))
        peds = "Commuters only" if reg else "Commuters" + (" + Agbada Bigman" if ag else "") + (" + Slay Queen" if sq else "")
        pu = "".join(f'<span class="pill">{badge(p,26)} {NAMES[p]}</span>' for p in pus) or '<span class="small">none</span>'
        cards += f'''<article class="lvcard" id="L{n}"><img loading="lazy" src="assets/bg/L{n:02d}_card.jpg" alt="L{n} {name} screenshot">
<div class="lvb"><div class="lvh"><b>L{n}</b> {name}<span class="diff" title="relative difficulty">{"●"*diff}{"○"*(5-diff)}</span></div>
<div class="tags">{"".join(f"<span>{t}</span>" for t in tags)}</div>
<table class="kv2"><tr><td>Curb pool</td><td>{pool} people · {peds}</td></tr><tr><td>Traffic</td><td>×{mul} profile · cruise ≈ {cruise:.1f} m/s<sup>*</sup></td></tr>
<tr><td>Spawn gap</td><td>{gap:+.2f} s offset{f" · lane speed ±{int(var*100)}%" if var else ""}{f" · luxury +{lux}" if lux else ""}</td></tr></table>
<p>{LEVEL_NOTES[n]}</p><div class="pills">{pu}</div></div></article>'''
    return f'''<h1>Levels</h1><p class="lead">The ten-district Lagos campaign as authored in <code>LevelManager.CreateDefaultLevels</code> (mirrors <code>Resources/Campaign/LagosCampaign.asset</code>). Screenshots: current build, original camera, old HUD removed, dusk grade. Landscape only.</p>
<div class="lvgrid">{cards}</div>
<p class="small">* Cruise = baseTrafficSpeed 12 × (1 + 0.12 × level index) × profile multiplier, before adaptive difficulty and luxury bonus (LevelManager.GetScaledTrafficSpeed). Difficulty dots are a design summary of lanes, speed and enforcement, not a code value. Stars / par times per level: <span class="badge">TBD</span> (not in code).</p>'''
