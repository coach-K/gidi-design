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
 ("onboard3","Onboarding 3 · Stock","Onboarding","GROUP and CHANGE highlighted up top; OWA! sits on its own button above PICK UP."),
 ("onboard4","Onboarding 4 · Reach the curb","Onboarding","Goal zone on the far curb. Skippable after step 1."),
 ("hud","In-run HUD (base)","In-run","Approved round-4 HUD. Background: L5 Oshodi Expressway."),
 ("hud-power","HUD · power-up active","In-run","Malta ring timer (4 s, traffic −60%, LevelManager). Background: L7 Ojota Intersect."),
 ("hud-warn","HUD · warnings (colour + shape)","In-run","Caution ▲, Danger ≫, LASTMA ◆, Safe gap bar. Background: L8 Third Mainland Bridge (8 lanes, wide camera)."),
 ("hud-toast","HUD · toasts","In-run","Owa unlock (code copy), group coach line, \"Found Owa\" grant toast. Background: L2 Surulere Way."),
 ("hud-endless","HUD · endless (L10)","In-run","Score = metres + 25/delivery + 10/combo step (EndlessRunScore). The score strip shows only in L10 endless mode; L1–L9 don't show it. Background: L10 Ojuelegba Chaos."),
 ("pause","Pause","Run modals","Resume, Restart, Settings, Map, Stats. Background: L5 (blurred)."),
 ("stats","Stats","Run modals","Run stats (values are samples)."),
 ("continue","Continue modal (1 per run)","Run modals","Watch ad / ₦125 chips at L2+ (₦100 at L1) / End run. MaxContinuesPerRun = 1."),
 ("clear","Level clear","Results","\"{location} Cleared!\" (code copy). Cash-out grant 75 chips (L2+). Stars rule TBD. Background: L6 Ikeja Along."),
 ("gameover","Game over","Results","After the single continue is used or declined. Background: L5."),
 ("shop","Base Camp shop","Menus","3×3 grid, 180 px tiles: buyable Owa refill, Pure Water 110 (once until cash-out), Malta 80, Change 90, VIP Siren 120; Danfo Ride 150 and Gist Bomb 100 coming soon (locked, price shown); Agbada Armour (Earned) and Okada Dash (Curb pickup) are not for sale. Agbero Whistle removed (#39). Prices, caps and unlocks per vision doc (Kehinde, Oct 16); game-side changes in G-Prototype PR #51. Background: L4 Mushin Market."),
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
<p class="lead">Every screen from splash onward, <b>landscape only</b>, each as desktop / WebGL 1920×1080 and phone 19.5:9 2340×1080 (notch and home-indicator safe areas). Backgrounds are the real L1–L10 level screenshots from the current build (old HUD removed, dusk grade). Controls, camera, font, palette and copy follow the approved round-4 mockups. Prices, caps and unlocks per vision doc (Kehinde, Oct 16); game-side changes in G-Prototype PR #51. Other economy numbers come from <code>GidiEconomyTables</code> and level facts from <code>LevelManager</code>; wallet, timer and score values are samples; anything undefined is marked <span class="badge">TBD</span>.</p>
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
 (7,"Ojota Intersect",7,0.55,1.0,7,0.15,0,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren"],0),
 (8,"Third Mainland Bridge",8,1.2,0.35,8,0,0,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren"],0),
 (9,"Lekki Toll Gate",8,1.35,0.1,8,0,3,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren"],0),
 (10,"Ojuelegba Chaos",8,1.45,0.0,8,0.35,3.5,1,1,1,1,0,["owa","maltina_gala","pure_water","bribe_change","siren"],1),
]
LEVEL_NOTES = {1:"Tutorial. Commuters only, widest gaps (+1.2 s). No power-ups; Owa! not yet unlocked.",
 2:"Owa! unlocks here (toast). Base Camp opens (ShopAllowed L2+). Continue cost rises to 125 chips.",
 3:"First Agbada Bigman in the curb mix. Malta &amp; Agege Roll and Pure Water unlock (Pure Water: full immunity, once until cash-out, 110 chips; follows the game, not the vision doc).",
 4:"Slay Queen joins the mix. Traffic jumps to ×0.55 with tighter gaps (+0.6 s).",
 5:"LASTMA flag enforcement starts (every 5–8 s, lane slows to ×0.8). Change Bundle and VIP Siren appear.",
 6:"First 6-lane road. KAI officers join LASTMA (KAI bribe ₦200).",
 7:"7 lanes, per-lane speed variation ±15%. Okada Dash appears at the curb (L7+, curb pickup, not sold).",
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
<div class="card dont"><b>Note on the screenshots:</b> the L01–L09 shots came from a broken import that was missing the danfo, keke, taxi, market lorry and Pure Water models, so those vehicles are missing from the shots, not absent from the game. Fresh captures are pending. L10 is a fresh capture from the fixed build (Oct 16).</div>
<div class="lvgrid">{cards}</div>
<p class="small">* Cruise = baseTrafficSpeed 12 × (1 + 0.12 × level index) × profile multiplier, before adaptive difficulty and luxury bonus (LevelManager.GetScaledTrafficSpeed). Difficulty dots are a design summary of lanes, speed and enforcement, not a code value. Pure Water follows the game, not the vision doc (Kehinde, Oct 16). Power-up unlocks per vision doc v2 §8 (Owa L2, Malta &amp; Pure Water L3, Change &amp; VIP Siren L5; new v2 items: Danfo Ride L4, Agbada Armour L6, Okada Dash L7, Gist Bomb L8). Prices, caps and unlocks per vision doc (Kehinde, Oct 16); game-side changes in G-Prototype PR #51. Stars / par times per level: <span class="badge">TBD</span> (not in code).</p>'''

def costumes():
    from gen_costumes import CFG, VEH
    ch = "".join(f'<figure class="cos"><a href="exports/costumes/{k}.png"><img loading="lazy" src="exports/costumes/{k}.png" alt="{c["label"]}"></a><figcaption><b>{c["label"]}</b><br><span class="badge" style="background:{"#59D9B8" if c["status"]=="IN-GAME" else "#E07CC0"}">{c["status"]}</span> <code>{c["sku"]}</code></figcaption></figure>' for k,c in CFG.items())
    vh = "".join(f'<figure class="cos veh"><a href="exports/costumes/{k}.png"><img loading="lazy" src="exports/costumes/{k}.png" alt="{lab}"></a><figcaption><b>{lab}</b><br><span class="badge">CONCEPT</span> <code>pack_skins_lagos</code></figcaption></figure>' for k,(_,_,_,_,lab) in VEH.items())
    return f'''<h1>Costumes &amp; skins</h1><p class="lead">Drawn renders of every cosmetic named in the code and the vision brief. <b>IN-GAME</b> = the look that ships in the current build; <b>CONCEPT</b> = design proposal for a cosmetic SKU, not yet modelled. Cosmetics are vanity only: no power for cash (Storefront IA).</p>
<div class="card"><b>Sources.</b> IAP SKUs in <code>GidiEconomyTables.IapSkus</code>: <code>pack_baba_fits</code> (“Baba Fits”) and <code>pack_skins_lagos</code> (“Lagos Skins: danfo / keke / korope”, Storefront IA). Brief: Baba Gidi outfits agbada, okada helmet, Ankara fits, generic jerseys. Art guide: Baba Gidi needs a cap that reads from above and a bold shirt that stays visible on white walkways and dark asphalt. Prices come from the store: <span class="badge">TBD</span>. Which fits go in which pack: <span class="badge">TBD</span>.</div>
<h2>Baba Gidi fits (<code>pack_baba_fits</code>)</h2><div class="cosgrid">{ch}</div>
<h2>Lagos Skins (<code>pack_skins_lagos</code>)</h2><p>Vehicle paint jobs with fictional back slogans (no real brands).</p><div class="cosgrid wide">{vh}</div>
<h2>Readability rules</h2><ul><li>Hat or helmet colour must contrast with both asphalt <code>#26272E</code> and walkway at the 65° camera.</li><li>Every fit keeps the same silhouette and Humanoid rig, so animations and hitbox don't change.</li><li>Not costumes: Agbada Bigman, Corporate Slay Queen, commuters, LASTMA and KAI are in-game NPC archetypes (<code>PedestrianController</code>, <code>FactionAI</code>).</li></ul>'''

def _lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]; return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def contrast(a,b):
    la,lb=sorted([_lum(a),_lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
def rate(r, text=True):
    return "AAA" if r>=7 else "AA" if r>=4.5 else ("AA large / UI" if r>=3 else "fail")

PALETTE = [ # group, name, hex, role
 ("UI","Ink (HUD glass base, 72%)","#0F1219","Panels, modals"),("UI","Text primary","#F5F5F0","Body, labels"),("UI","Text muted","#9EA3AD","Secondary labels"),
 ("UI","Naira gold","#FAE69E","Wallet, numbers, icon lines"),("UI","Danfo yellow","#E8B21E","Accent, OWA!, focus rings"),("UI","Primary CTA","#2E7A68","CTA fill (text #F5F5F0)"),
 ("UI","CTA deep","#18493F","CTA gradient end, buy buttons"),("UI","Pip on","#59D9B8","Stock pips, success"),("UI","Lives","#FF6B7A","Heart"),
 ("Warning","Safe / gap","#56B4E9","Rounded bar + tick"),("Warning","Caution","#F0E442","Triangle + !"),("Warning","Danger","#FF7A1A","Double chevrons"),
 ("Warning","LASTMA","#E07CC0","Diamond + whistle"),("Warning","Train","#FFFFFF","Rail-tie band"),("Warning","Danger (CB mode)","#D55E00","Colour-blind mode, thicker chevrons"),
 ("Brand","Dusk sky","#2B2F5C","Logo tile top, sky"),("Brand","Dusk violet","#6B4A6E","Gradient mid"),("Brand","Horizon","#F28C4B","Gradient end"),
]
TYPE = [ # role, const, ref px, weight, line, tracking, usage, sample
 ("Display","(logo / splash)",96,700,1.0,"+0.02em","Logo lockup, splash","GIDI++"),
 ("Hero","(results)",72,700,1.1,"0","Level clear / district name","Ikeja Along Cleared!"),
 ("Heading","(modal title)",56,700,1.15,"0","Modal titles, CTA label","Continue this run?"),
 ("Naira wallet","FontNaira",48,700,1.05,"0, tabular","Wallet, big numbers","₦12,450"),
 ("Title","FontTitle",42,700,1.2,"+0.02em","HUD level name","L5 · Oshodi Expressway"),
 ("Body","FontBody",33,700,1.3,"0","Body copy, buttons in lists","Load your bag before you cross"),
 ("Button","FontButton",30,700,1.2,"+0.02em","Buttons, stock labels","OYA, CROSS!"),
 ("Small (floor)","FontSmall / FontMin",27,700,1.3,"0","Meta, captions; nothing smaller","Saved 4 · Best 6"),
]

def palette():
    ink, text = "#0F1219", "#F5F5F0"
    out = '<h1>Palette <span class="badge" style="background:#56B4E9">FINAL · v1.0</span></h1><p class="lead">Dusk-glass UI, Okabe-Ito based warning colours and the dusk brand gradient. Contrast ratios are computed (WCAG 2.x) against ink glass <code>#0F1219</code> and against white text. Approved by Kehinde on Oct 13 2026; v1.0 adds CTA deep, pip, lives, colour-blind danger and brand tokens already used in the mockups.</p>'
    for g in ("UI","Warning","Brand"):
        out += f'<h2>{g}</h2><div class="grid">'
        for gg,n,h,role in PALETTE:
            if gg!=g: continue
            ci, ct = contrast(h,ink), contrast(h,text)
            fg = text if ct>ci else ink
            out += f'<div class="sw"><div class="c" style="background:{h};color:{fg}">Aa</div><p><b>{n}</b><br><code>{h}</code><br>{role}<br><span class="small">on ink {ci:.1f}:1 · {rate(ci)}<br>white text {ct:.1f}:1 · {rate(ct)}</span></p></div>'
        out += '</div>'
    out += '''<h2>Warning system (colour + shape + motion)</h2><table><tr><th>State</th><th>Hex</th><th>Shape</th><th>Icon</th><th>Motion / audio</th></tr>
<tr><td>Safe / gap</td><td><code>#56B4E9</code></td><td>Rounded bar</td><td>tick</td><td>static</td></tr>
<tr><td>Caution</td><td><code>#F0E442</code></td><td>Triangle</td><td>! + 45° stripes</td><td>1 Hz pulse</td></tr>
<tr><td>Danger</td><td><code>#FF7A1A</code></td><td>Double chevron ≫</td><td>scrolling chevrons</td><td>3 Hz flash, headlights, horn</td></tr>
<tr><td>LASTMA</td><td><code>#E07CC0</code></td><td>Diamond</td><td>whistle</td><td>whistle cue</td></tr>
<tr><td>Train</td><td><code>#FFFFFF</code></td><td>Lane band</td><td>rail ties</td><td>bell + rumble</td></tr></table>
<div class="card dont">Under deuteranopia/protanopia, Safe, Danger and LASTMA collapse in hue. <b>Shapes are mandatory.</b> Colour-blind mode swaps Danger to <code>#D55E00</code> with thicker chevrons. See <a href="icons.html#warn">warning icons</a>.</div>
<h2>Colour grade (3D)</h2><table><tr><th>Key</th><th>Day (L1–L4)</th><th>Dusk (L5–L10, menus)</th></tr>
<tr><td>Sky top / horizon</td><td><code>#7FB4E0</code> / <code>#F4E3C1</code></td><td><code>#2B2F5C</code> / <code>#F28C4B</code></td></tr>
<tr><td>Key light</td><td><code>#FFF1D6</code> ×1.2</td><td><code>#FFB070</code> ×0.8</td></tr>
<tr><td>Shadow tint</td><td><code>#3A4A66</code></td><td><code>#2A2440</code></td></tr>
<tr><td>Asphalt / laterite</td><td><code>#3C3F45</code> / <code>#B5643A</code></td><td><code>#26272E</code> / <code>#7A4630</code></td></tr>
<tr><td>Highlights tint</td><td><code>#FFF4E0</code></td><td><code>#FFC98A</code></td></tr>
<tr><td>Bloom</td><td>thr 1.1 · int 0.2</td><td>thr 0.9 · int 0.45 · <code>#FFB46B</code></td></tr></table>
<h2>Tokens</h2><pre class="card">''' + "\n".join(f"--{n.lower().split(' (')[0].replace(' / ','-').replace(' ','-')}: {h};" for _,n,h,_ in PALETTE) + '</pre>'
    return out

def typography():
    rows = "".join(f'<tr><td>{r}</td><td><code>{c}</code></td><td>{px}</td><td>{px*2/3:.0f}</td><td>{px/3:.0f} dp</td><td>{lh}</td><td>{tr}</td><td>{u}</td><td style="font:700 {min(px*2/3,44):.0f}px/{lh} Jakarta;{"color:#FAE69E" if "Naira" in r else ""}">{s}</td></tr>' for r,c,px,w,lh,tr,u,s in TYPE)
    return f'''<h1>Typography <span class="badge" style="background:#56B4E9">FINAL · v1.0</span></h1><p class="lead"><b style="font-family:Jakarta">Plus Jakarta Sans Bold</b> (Tokotype, SIL Open Font License 1.1, <a href="fonts/OFL.txt">licence</a>). One weight everywhere, includes the ₦ glyph, grown-up rather than kiddy. Bundled as <code>fonts/PlusJakartaSans-Bold.ttf</code>.</p>
<div class="card" style="font-family:Jakarta"><div style="font-size:64px;line-height:1.05">Cross Lagos. ₦12,450</div><div style="font-size:28px;color:#9EA3AD">GROUP → CHANGE → OWA! · Chai! Traffic don catch you…</div><div style="font-size:22px;color:#FAE69E;margin-top:8px">ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 ₦ ! ? · → ×</div></div>
<h2>Type scale (landscape, CanvasScaler 1920×1080 match height)</h2>
<table><tr><th>Role</th><th>Constant</th><th>Ref px</th><th>px @720p</th><th>Phone</th><th>Line</th><th>Tracking</th><th>Use</th><th>Sample</th></tr>{rows}</table>
<div class="card"><ul><li>Constants in <code>GameUiTheme</code>: FontTitle 42, FontNaira 48, FontBody 33, FontSmall/FontMin 27, FontButton 30. Display/Hero/Heading sizes are design tokens used by the mockups (not yet constants).</li>
<li>Floor: nothing below 27 ref px (18 px at 720p, 9 dp on a 360 dp-tall phone).</li><li>Numbers that tick (timer, wallet, score) use tabular figures.</li><li>Sentence case for copy, UPPERCASE only for CTAs and stock labels.</li><li>Pidgin first; keep lines short (≤ 48 characters in toasts).</li></ul></div>
<h2>Web (this site / storefront)</h2><table><tr><th>Role</th><th>Size</th></tr><tr><td>H1</td><td>40 px (28 px mobile)</td></tr><tr><td>H2</td><td>24 px</td></tr><tr><td>Body</td><td>16 px / 1.55, system UI</td></tr><tr><td>Caption</td><td>13 px</td></tr></table>'''

LABEL = {"owa":"Owa","maltina_gala":"Malta &amp; Agege Roll","pure_water":"Pure Water","bribe_change":"Change Bundle","siren":"VIP Siren","danfo_ride":"Danfo Ride","gist_bomb":"Gist Bomb","agbada_armour":"Agbada Armour","okada_dash":"Okada Dash","retry":"Retry (TRY AM AGAIN)","iap_skins_pack":"Lagos skins pack","iap_fits_pack":"Baba fits pack","iap_remove_ads":"Remove ads",
 "pickup_ring":"Curb pickup marker","pickup_person":"Recruit (person lights up)","chip":"Naira Chip","lives":"Lives","group":"GROUP","change":"CHANGE","stats":"Stats","pause":"Pause",
 "settings":"Settings","map":"Lagos map","basecamp":"Base Camp","play":"Play / cross","back":"Back","close":"Close","ad":"Watch ad","timer":"Timer","lock":"Locked",
 "warn_safe":"Safe / gap","warn_caution":"Caution","warn_danger":"Danger","warn_lastma":"LASTMA","warn_train":"Train"}
def icons():
    from gen_screens import ECON, SOON, INFO
    E = {p:(c,cap,f,b) for p,_,b,c,cap,f in ECON}
    SO = {p:(c,f) for p,_,_,c,_,f in SOON}; IN = {p:t for p,_,_,t in INFO}
    out = '<h1>Icons</h1><p class="lead">One SVG set on a 48×48 grid, 3 px rounded stroke, <code>currentColor</code> lines (default Naira gold <code>#FAE69E</code> on ink glass). Warning shapes are filled and keep their state colour. Download any icon from <code>icons/svg/</code>.</p>'
    out += '<h2>Power-up badges</h2><p>Ink disc + accent ring + gold glyph. Used in Base Camp rows, HUD timer rings and curb pickups. Ids, caps and unlock levels from the code. Prices, caps and unlocks per vision doc (Kehinde, Oct 16); game-side changes in G-Prototype PR #51. Display name of <code>maltina_gala</code> is now “Malta &amp; Agege Roll”.</p><div class="icgrid">'
    for p in PU_ACCENT:
        if p in E:
            c,cap,f,b = E[p]
            txt = f'{("FREE · refill "+str(c)+" chips/charge") if p=="owa" else str(c)+" chips"} · cap {cap}{" (resets at cash-out) · full immunity, follows the game" if p=="pure_water" else ""} · L{f}+'
        elif p in SO: txt = f"{SO[p][0]} chips · coming soon · L{SO[p][1]}+"
        else: txt = f"{IN[p]} · not sold"
        out += f'<a class="ic" href="icons/svg/badge_{p}.svg">{badge(p,96)}<b>{LABEL[p]}</b><code>{p}</code><span>{txt}</span></a>'
    out += '</div>'
    for g, names in GROUPS:
        anchor = ' id="warn"' if g.startswith("Warning") else ''
        out += f'<h2{anchor}>{g}</h2><div class="icgrid">'
        for n in names:
            out += f'<a class="ic" href="icons/svg/{n}.svg">{icon(n,64)}<b>{LABEL[n]}</b><code>{n}.svg</code></a>'
        out += '</div>'
    out += '<h2>Sizes</h2><div class="card" style="display:flex;gap:24px;align-items:end">' + "".join(icon("owa",s) for s in (24,32,48,64,96)) + "".join(icon("warn_danger",s) for s in (24,48,96)) + '</div>'
    out += '<div class="card"><ul><li>Minimum in-game size 48 ref px inside a 144 px touch target.</li><li>Never show a warning by colour alone: always the shape.</li><li>Pure Water is a sachet (pillow pack), not a bottle. Change Bundle is a ₦ note stack. Next-gen items from vision v2 (Danfo Ride, Okada Dash, Gist Bomb, Agbada Armour) get icons once they land in code: <span class="badge">TBD</span>.</li></ul></div>'
    return out

def logos():
    from gen_logos import VARIANTS
    bgs = {"wordmark_light":"#0F1219","wordmark_dark":"#F5F5F0","wordmark_mono_white":"#2B2F5C","wordmark_mono_black":"#FAE69E","lockup_tagline_light":"#0F1219","lockup_tagline_dark":"#F5F5F0"}
    wm = "".join(f'<figure class="logo" style="background:{bgs[k]}"><img src="logos/{k}.png" alt="{k}"><figcaption>{k.replace("_"," ")} · <a href="logos/{k}.svg">SVG</a> · <a href="logos/{k}.png">PNG</a></figcaption></figure>' for k in VARIANTS)
    ios = [1024,180,167,152,120,87,80,76,60,58,40,29,20]
    iosrow = "".join(f'<a href="logos/app/ios/AppIcon-{s}.png" class="ai"><img src="logos/app/ios/AppIcon-{s}.png" width="{min(s,120)}" height="{min(s,120)}" style="border-radius:{min(s,120)*0.2237:.0f}px" alt="iOS {s}"><span>{s}</span></a>' for s in ios)
    andr = "".join(f'<a href="logos/app/android/{f}" class="ai"><img src="logos/app/android/{f}" width="140" height="140" style="{st}" alt="{f}"><span>{lab}</span></a>' for f,lab,st in [
        ("ic_launcher_foreground_432.png","Foreground 432 (108 dp)","background:repeating-conic-gradient(#333 0 25%,#222 0 50%) 0/20px 20px"),("ic_launcher_background_432.png","Background 432",""),
        ("play_store_icon_512.png","Play Store 512","border-radius:20px"),("../web/pwa-maskable-512.png","Adaptive: circle mask","border-radius:50%"),("../web/pwa-maskable-512.png","Adaptive: squircle mask","border-radius:38%")])
    web = "".join(f'<a href="logos/app/web/{f}" class="ai"><img src="logos/app/web/{f}" width="{w}" height="{w}" alt="{f}"><span>{f}</span></a>' for f,w in [("favicon-16.png",16),("favicon-32.png",32),("favicon-48.png",48),("apple-touch-icon.png",90),("pwa-192.png",96),("pwa-512.png",128),("pwa-maskable-512.png",128)])
    return f'''<h1>Logos &amp; app icons</h1><p class="lead">The <b>GIDI++</b> wordmark: Plus Jakarta Sans Bold letters (outlined to paths, so the SVGs work without the font), two Danfo-yellow plus signs and a zebra-crossing underline. The app mark is the ++ crossing on a dusk tile.</p>
<h2>Wordmark &amp; lockups</h2><div class="logogrid">{wm}</div>
<div class="card"><ul><li><b>Clear space:</b> the height of one plus sign on every side. <b>Minimum size:</b> 120 px wide on screen (24 mm in print); below that use the mark alone.</li><li>Pluses are always Danfo yellow <code>#E8B21E</code> except in mono versions. Never recolour the pluses red or green, add a drop shadow or stretch the letters.</li><li>Tagline lockup: “Carry dem cross. Lagos no dey wait.”</li></ul></div>
<h2>App mark</h2><div class="card" style="display:flex;gap:24px;align-items:center;flex-wrap:wrap"><img src="logos/app/icon_master_1024.png" width="200" style="border-radius:44px" alt="App icon master"><div><b>Master 1024×1024</b>, RGB, no alpha (App Store rule). Source <a href="logos/mark.svg">mark.svg</a>.<br>Dusk gradient <code>#2B2F5C → #6B4A6E → #F28C4B</code>, pluses <code>#E8B21E</code> with ink outline, five crossing stripes.</div></div>
<h2>iOS (<code>logos/app/ios/</code>)</h2><div class="airow">{iosrow}</div><p class="small">1024 is the only size Xcode 14+ needs; the full legacy set is included. Shown with the iOS corner mask for preview only: files are square.</p>
<h2>Android adaptive (<code>logos/app/android/</code>)</h2><div class="airow">{andr}</div><p class="small">Foreground art sits inside the 66 dp safe circle of the 108 dp layer. Vector layers: <a href="logos/app/android/ic_launcher_foreground.svg">foreground.svg</a>, <a href="logos/app/android/ic_launcher_background.svg">background.svg</a>. Legacy mipmaps 48–192 px included.</p>
<h2>Web favicons &amp; PWA (<code>logos/app/web/</code>)</h2><div class="airow">{web}</div><p class="small"><a href="logos/app/web/favicon.ico">favicon.ico</a> (16/32/48) · <a href="logos/app/web/manifest.webmanifest">manifest.webmanifest</a> with <code>"orientation": "landscape"</code> and <code>"display": "fullscreen"</code>. This site uses these favicons.</p>'''

SOUV = [ # level, name, glyph inner (viewBox 0 0 64 64, centred around 32,32)
 (1,"Agege Bread",'<path d="M14 38c0-10 8-16 18-16s18 6 18 16v4H14z" fill="#D9A15A" stroke="#7A4630" stroke-width="2"/><path d="M22 28l3 6M32 26v7M42 28l-3 6" stroke="#7A4630" stroke-width="2.5" stroke-linecap="round"/>'),
 (2,"Surulere Match Ticket",'<rect x="12" y="22" width="40" height="22" rx="3" fill="#56B4E9"/><circle cx="12" cy="33" r="4" fill="#0F1219"/><circle cx="52" cy="33" r="4" fill="#0F1219"/><path d="M38 22v22" stroke="#0F1219" stroke-dasharray="2 2" stroke-width="2"/><circle cx="25" cy="33" r="6" fill="none" stroke="#0F1219" stroke-width="2.5"/>'),
 (3,"Ikorodu Road Sign",'<rect x="14" y="18" width="36" height="20" rx="3" fill="#2E7A68" stroke="#F5F5F0" stroke-width="2"/><path d="M20 28h20M34 23l6 5-6 5" stroke="#F5F5F0" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M31 38v10" stroke="#9EA3AD" stroke-width="3"/>'),
 (4,"Mushin Market Basket",'<path d="M14 30h36l-4 16H18z" fill="#C8743A" stroke="#7A4630" stroke-width="2"/><path d="M20 30c0-8 24-8 24 0" fill="none" stroke="#7A4630" stroke-width="3"/><circle cx="26" cy="28" r="4" fill="#FF6B7A"/><circle cx="36" cy="27" r="4" fill="#59D9B8"/>'),
 (5,"Oshodi Danfo Keyring",'<rect x="14" y="24" width="34" height="18" rx="4" fill="#E8B21E"/><path d="M14 32h34" stroke="#0F1219" stroke-width="3"/><circle cx="21" cy="44" r="3.5" fill="#0F1219"/><circle cx="41" cy="44" r="3.5" fill="#0F1219"/><circle cx="50" cy="18" r="5" fill="none" stroke="#9EA3AD" stroke-width="2.5"/><path d="M47 22l-3 3" stroke="#9EA3AD" stroke-width="2.5"/>'),
 (6,"Ikeja Along Phone Case",'<rect x="22" y="14" width="20" height="36" rx="4" fill="#E07CC0" stroke="#0F1219" stroke-width="2"/><circle cx="32" cy="20" r="2" fill="#0F1219"/><path d="M26 30h12M26 36h12" stroke="#0F1219" stroke-width="2"/>'),
 (7,"Ojota Park Flag",'<path d="M20 14v38" stroke="#9EA3AD" stroke-width="3"/><path d="M21 16h24l-6 8 6 8H21z" fill="#FF7A1A"/>'),
 (8,"Third Mainland Lamp",'<path d="M12 46h40" stroke="#9EA3AD" stroke-width="3"/><path d="M14 46c6-10 30-10 36 0" fill="none" stroke="#9EA3AD" stroke-width="2"/><path d="M32 46V18h8" stroke="#F5F5F0" stroke-width="3" fill="none"/><circle cx="42" cy="21" r="5" fill="#FAE69E"/>'),
 (9,"Lekki Toll Card",'<rect x="12" y="20" width="40" height="26" rx="4" fill="#2B2F5C" stroke="#FAE69E" stroke-width="2"/><rect x="17" y="27" width="10" height="8" rx="1.5" fill="#E8B21E"/><path d="M17 40h20" stroke="#FAE69E" stroke-width="2"/>'),
 (10,"Ojuelegba Under-bridge Sticker",'<path d="M12 40c6-14 34-14 40 0" fill="none" stroke="#9EA3AD" stroke-width="4"/><path d="M18 40v8M46 40v8" stroke="#9EA3AD" stroke-width="3"/><path d="M32 18l3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z" fill="#E8B21E"/>'),
]
def souv_svg(n, name, g, locked=False):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="120" height="120"><defs><radialGradient id="m{n}" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="#3A3F55"/><stop offset="1" stop-color="#0F1219"/></radialGradient></defs>'
            f'<circle cx="32" cy="32" r="30" fill="url(#m{n})" stroke="#E8B21E" stroke-width="2.5"/><circle cx="32" cy="32" r="26" fill="none" stroke="#FAE69E" stroke-opacity=".25"/>'
            f'<g{" opacity=\".25\" filter=\"grayscale(1)\"" if locked else ""}>{g}</g><text x="32" y="60" text-anchor="middle" font-family="Jakarta,sans-serif" font-weight="700" font-size="7" fill="#FAE69E">L{n}</text></svg>')

def souvenirs():
    import os
    from brand import ROOT
    for n,name,g in SOUV: open(f"{ROOT}/souvenirs/souvenir_L{n:02d}.svg","w").write(souv_svg(n,name,g))
    cards = "".join(f'<a class="ic" href="souvenirs/souvenir_L{n:02d}.svg">{souv_svg(n,name,g)}<b>{name}</b><span>L{n} · drop rule <span class="badge">TBD</span></span></a>' for n,name,g in SOUV)
    return f'''<h1>Souvenirs &amp; perks</h1><p class="lead">Perks come from the code. Souvenirs are not in code yet: this is the visual design, with all numbers <span class="badge">TBD</span>. Cosmetic and collection items never change crossing difficulty (Storefront IA: no pay-to-win).</p>
<h2>Perks in code today</h2><table><tr><th>Perk</th><th>Value</th><th>Source</th><th>UI</th></tr>
<tr><td>Starting lives</td><td>3</td><td><code>GidiEconomyTables.StartLives</code></td><td>♥ 3 in the HUD</td></tr>
<tr><td>Continue</td><td>1 per run · 100 chips at L1, 125 at L2+ · or watch an ad</td><td><code>MaxContinuesPerRun</code>, <code>ContinueChipsCost</code></td><td><a href="screens.html#s-continue">Continue modal</a></td></tr>
<tr><td>Cash-out grant</td><td>50 chips at L1, 75 at L2+</td><td><code>CashoutGrantChips</code></td><td><a href="screens.html#s-clear">Level clear</a></td></tr>
<tr><td>Owa! charges</td><td>cap 3 per run · refill 80 chips per charge · no free refill on level clear</td><td><code>PowerUpInventoryCap</code>, <code>GameManager.owaReplenishCostPerCharge</code></td><td>OWA! pips</td></tr>
<tr><td>Owa capacity upgrade</td><td>₦500 per +1, but max = hard cap = 3, so no headroom today</td><td><code>GameManager.owaCapacityUpgradeCost</code>, <code>absoluteMaxOwaCapacity</code></td><td>Hidden until the cap rises (<span class="badge">TBD</span>)</td></tr>
<tr><td>Power-up stock</td><td>caps 3/3/2/2/2/2; curb finds and shop buys share the cap</td><td><code>PowerUpInventoryCap</code></td><td>Base Camp pips</td></tr>
<tr><td>KAI bribe</td><td>₦200 (in-run Naira)</td><td><code>LevelManager.kaiBribeCostNaira</code></td><td>CHANGE pip / toast</td></tr>
<tr><td>Endless score</td><td>metres + 25 per delivery + 10 per combo step</td><td><code>EndlessRunScore</code></td><td><a href="screens.html#s-hud-endless">Endless HUD</a></td></tr></table>
<div class="card dont"><b>Open with Kehinde:</b> the vision brief proposes a 2-slot “Gidi Bag”, a free Owa (3 per run), Agbada Armour (earned only) and new items. The site now shows Owa as FREE (refill 80 chips per charge); Agbero Whistle is removed from the game (#39). Prices, caps and unlocks per vision doc (Kehinde, Oct 16); game-side changes in G-Prototype PR #51. (Malta 80, VIP Siren 120, Owa 80, Danfo Ride 150; Agbada Armour earned only.)</div>
<h2>Souvenirs: one per district (concept)</h2><p>A collectible medallion found once per district, shown in a Lagos collection book on the map. Gold rim = collected; dim = not found yet.</p>
<div class="icgrid">{cards}</div>
<div class="card" style="display:flex;gap:18px;align-items:center">{souv_svg(5,"","".join(g for n,_,g in SOUV if n==5))}{souv_svg(6,"","".join(g for n,_,g in SOUV if n==6),locked=True)}<div><b>States:</b> collected (left) vs not found (right, 25% and greyscale).<br>Drop chance, where it spawns, rewards for a full set and whether souvenirs give chips: <span class="badge">TBD</span>, needs economy numbers in <code>GidiEconomyTables</code> first.</div></div>
<h2>Perk badges (visual)</h2><div class="icgrid"><div class="ic">{badge("owa",80)}<b>Owa! +1 capacity</b><span>₦500 · cap TBD</span></div><div class="ic">{icon("lives",64,"#FF6B7A")}<b>Lives</b><span>3 per run</span></div><div class="ic">{icon("ad",64)}<b>Watch-ad continue</b><span>1 per run</span></div><div class="ic">{icon("chip",64)}<b>Cash-out</b><span>50 / 75 chips</span></div></div>'''

def devices():
    from gen_devices import DEV
    t = "".join(f'<tr><td>{lab}</td><td>{W}×{H}</td><td>L {l} · R {r} · T {t_} · B {b}</td><td>{W-l-r}×{H-t_-b}</td></tr>' for k,(lab,W,H,(l,r,t_,b),cut,rad) in DEV.items())
    tpl = "".join(f'<figure class="cos"><a href="exports/devices/dev-{k}.png"><img loading="lazy" src="exports/devices/dev-{k}.png" alt="{DEV[k][0]} template"></a><figcaption><b>{DEV[k][0]}</b></figcaption></figure>' for k in DEV)
    fr = "".join(f'<figure class="cos"><a href="exports/devices/{f}.png"><img loading="lazy" src="exports/devices/{f}.png" alt="{f}"></a><figcaption>{c}</figcaption></figure>' for f,c in [
        ("dev-iphone-hud-phone","iPhone · in-run HUD"),("dev-iphone-home-phone","iPhone · Home"),("dev-android-hud-warn-phone","Android · HUD warnings"),("dev-android-shop-phone","Android · Base Camp"),
        ("dev-web-hud-desktop","Web · in-run HUD"),("dev-web-map-desktop","Web · Lagos map")])
    return f'''<h1>Devices (Android · iOS · Web)</h1><p class="lead"><b>Landscape only on every device</b> (RT-106). One layout: CanvasScaler 1920×1080, match height; everything placed inside <code>Screen.safeArea</code> (<code>SafeAreaFitter</code>). Orange hatching = unsafe (notch, punch-hole, home indicator); blue dashes = safe area.</p>
<h2>Orientation lock</h2><div class="card"><ul>
<li><b>iOS / Android:</b> Player Settings → Resolution and Presentation → Default Orientation <b>Auto Rotation</b> with only <b>Landscape Left</b> and <b>Landscape Right</b> allowed (Android manifest ends up as <code>sensorLandscape</code>). Portrait never shows.</li>
<li><b>WebGL desktop:</b> fixed 16:9 canvas in the <code>GidiFullscreen</code> template; <code>AdaptiveCanvasMatch</code> re-applies the match on resize.</li>
<li><b>WebGL on a phone:</b> browsers can't hard-lock. When held upright, show the rotate prompt below (no portrait layout); in fullscreen, also try <code>screen.orientation.lock("landscape")</code>. PWA manifest sets <code>"orientation": "landscape"</code>.</li>
<li><b>Done:</b> the landscape lock is in the build (parent repo PR #9, merged to main).</li></ul></div>
<h2>Safe-area templates</h2><table><tr><th>Device</th><th>Pixels</th><th>Insets (typical)</th><th>Safe area</th></tr>{t}</table>
<p class="small">Inset values are typical for each class; Android cutouts differ per model, so always read <code>Screen.safeArea</code>. Touch controls: PICK UP bottom-left and d-pad bottom-right, both inside the safe area; minimum touch target 144 px (48 dp).</p>
<div class="cosgrid wide">{tpl}</div>
<h2>Tablet 4:3: two-row HUD</h2><p>Matching height gives a 1440×1080 reference canvas on 4:3, and the one-row HUD needs about 1,750 px. So when the safe-area aspect is under 1.5 the HUD <b>splits into two rows</b>: level card over the stock panel on the left (560 px column), and the wallet, lives, Stats and Pause on the right as usual. The area right of row 2 stays clear so the far curb is still visible. Full spec: <a href="exports/hud/HUD_Landscape_Spec.md">HUD_Landscape_Spec.md § Tablet 4:3</a>.</p>
<div class="cosgrid wide"><figure class="cos"><a href="exports/devices/dev-tablet-hud.png"><img loading="lazy" src="exports/devices/dev-tablet-hud.png" alt="Tablet two-row HUD"></a><figcaption><b>Tablet 4:3 · two-row HUD</b> (L3, 1440×1080 ref)</figcaption></figure><figure class="cos"><a href="exports/devices/dev-tablet-hud-annot.png"><img loading="lazy" src="exports/devices/dev-tablet-hud-annot.png" alt="Tablet HUD zones"></a><figcaption><b>Zones</b> ① level card 560×144 · ② stock 560×144 (gap 16) · ③ wallet / lives / stats / pause, touch ≥144 · ④ keep clear. HUD band ends at y 336.</figcaption></figure></div>
<h2>Device-framed mockups</h2><div class="cosgrid wide">{fr}</div>
<h2>Web: phone held upright</h2><div style="max-width:320px"><a href="exports/devices/dev-rotate-prompt.png"><img class="shot" src="exports/devices/dev-rotate-prompt.png" alt="Rotate prompt"></a></div>'''
