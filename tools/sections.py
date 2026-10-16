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
 ("Small (floor)","FontSmall / FontMin",27,700,1.3,"0","Meta, captions; nothing smaller","Saved 4/6 · Best 00:42"),
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
