"""Round 6 pages: Characters, Vehicles, Power-ups, Costumes (3D renders of our own models + concepts). Renders: /render3d three.js stage (not in repo), see README."""
from gen_screens import ECON
REF_NOTE = '<span class="badge" style="background:#56B4E9">REFERENCE</span>'
CON = '<span class="badge" style="background:#E8B21E">CONCEPT</span>'
GAME = '<span class="badge" style="background:#59D9B8">IN-GAME MODEL</span>'
import re, html as _h
def fig(src, cap, href=None, alt=None):
    alt = _h.escape(re.sub(r"<[^>]+>", "", alt or cap).strip(), quote=True)
    return f'<figure class="cos"><a href="{href or src}"><img loading="lazy" src="{src}" alt="{alt}"></a><figcaption>{cap}</figcaption></figure>'
def ref(name, folder, cap):
    return fig(f"img/ref/{name}.jpg", f"{REF_NOTE} {cap}", f"reference/{folder}/{name}.png")
def r3(name, cap): return fig(f"img/r3d/{name}.jpg", cap)
def pair(refhtml, r3html, notes):
    return f'<div class="pair"><div class="pp">{refhtml}</div><div class="pp">{r3html}</div><div class="pn">{notes}</div></div>'
LEGEND = f'''<div class="card"><b>How to read this page.</b> {REF_NOTE} = an existing project image (pipeline concept input or a render of our own model), hosted because it's project-made. {GAME} = <i>our treatment</i>: the shipped model re-staged at Lagos dusk (warm key light, cool rim, asphalt, soft shadows) in a three.js stage. Same mesh and texture as the build. {CON} = a new design proposal, not in the game yet. No real people are depicted: every human is one of our own generated in-game models. Provenance is listed in each <code>reference/*/README.md</code>.</div>'''

CHAR = [ # ref file, folder, render, name, role
 ("BabaGidi_concept","babagidi","ch_baba","Baba Gidi","Hero. Green kaftan + fila, the default fit. Reads from the 65° camera: gold-trimmed fila and white placket lines on green."),
 ("SlayQueen","peds","ch_SlayQueen","Slay Queen (Corporate)","Ped type <code>SlayQueen</code>. Leather jacket + orange bob. Moves fast and dodges; the bob gives her a warm hair colour that reads on asphalt."),
 ("SlayQueen1","peds","ch_SlayQueen1","Slay Queen (Casual)","Variant 1: graphic tee, ripped jeans, natural hair."),
 ("AgbadaMan","peds","ch_AgbadaMan","Agbada Man (Bigman)","Ped type <code>AgbadaMan</code>. Navy agbada with gold chain. Slow and heavy, so he's worth more when you deliver him."),
 ("AgbadaMan1","peds","ch_AgbadaMan1","Agbada Man (Chief)","Variant 1: burgundy agbada over a navy kaftan."),
 ("AgbadaMan2","peds","ch_AgbadaMan2","Agbada Man (Ankara shirt)","Variant 2: Ankara shirt + trousers (casual bigman)."),
 ("LASTMA_officer","officers","ch_LASTMAN","LASTMA officer","Faction AI. Hi-vis lime vest, navy trousers, peaked cap. Flags and fines you; Change settles am. VO: “Oga, park well!”"),
 ("KAI_officer","officers","ch_KAI","KAI officer","Faction AI. Khaki uniform + tactical vest, beret. Clears hawkers and crowds in zones."),
]
COMM = [("Commuter_0","ch_Ped","Ped · purple tee + fila"),("Commuter_1","ch_Ped1","Ped1 · office check shirt + bag"),("Commuter_2","ch_Ped2","Ped2 · lace blouse + gele"),
 ("Commuter_3","ch_Ped3","Ped3 · schoolboy"),("Commuter_4","ch_Ped4","Ped4 · yellow tee + backpack"),("Commuter_5","ch_Ped5","Ped5 · striped wrapper + gele"),
 ("Commuter_6","ch_Ped6","Ped6 · schoolgirl"),("Commuter_7","ch_Ped7","Ped7 · suit"),("Commuter_8","ch_Ped8","Ped8 · Ankara iro and buba"),
 ("Commuter_9","ch_Ped9","Ped9 · market woman"),("Commuter_10","ch_Ped10","Ped10 · aso-oke + gele")]

def characters():
    rows = "".join(pair(ref(f, d, "pipeline concept input"), r3(r, f"{GAME} <b>{n}</b>"), f"<h3>{n}</h3><p>{role}</p>") for f, d, r, n, role in CHAR)
    crowd = "".join(f'<div class="mini2">{ref(f,"peds",c.split(" · ")[0])}{r3(r, GAME+" "+c)}</div>' for f, r, c in COMM)
    return f'''<h1>Characters</h1><p class="lead">The cast of Gidi++: Baba Gidi, the people he carries across, and the officers who make it harder. On the left, the reference image the 3D model was built from. On the right, our treatment: the <b>shipped model</b> rendered in the Lagos dusk grade. Semi-real, 12+, no real people.</p>{LEGEND}
<h2>Hero, archetypes and officers</h2>{rows}
<h2>Commuters (the crowd)</h2><p>Eleven generic commuters fill the crowd you lead. Each card shows reference (top) and in-game model at dusk (bottom).</p><div class="crowd">{crowd}</div>
<h2>Hawkers {CON}</h2><p>Needed for <b>Gist Bomb</b> (“Have you heard?!”, vision v2 §8): hawkers' gossip pulls LASTMA/KAI officers off their posts. These concepts reuse shipped commuter bodies with head trays, so no new rig is needed. Tray props are about 1.5k tris (props budget, v2 §4).</p>
<div class="cosgrid wide">{r3("hawker_water", CON+" <b>Pure-water hawker</b> · Ped9 body + steel tray of sachets")}{r3("hawker_orange", CON+" <b>Orange hawker</b> · Ped2 body + tray of oranges")}</div>
<div class="card"><b>Still missing (no image yet):</b> conductor/agbero (VO “Oshodi! Oshodi! Enter with your change!”) and the Detty December concert crowd. LASTMA flags/cones props and faction zones: <span class="badge">TBD</span>.</div>'''

VEH = [("Danfo","veh_danfo","Danfo (yellow bus)","Hero traffic. About 7.4k tris after decimation (budget 5–10k). Telegraph: flashing headlights before it pulls out.",["Danfo_concept","Danfo_render","Danfo_ingame_front34"]),
       ("Keke","veh_keke","Keke Napep","About 7.4k tris. Short and fast in narrow lanes. More of them during fuel scarcity.",["Keke_concept","Keke_render"]),
       ("Taxi","veh_taxi","Lagos taxi","About 7.7k tris. Yellow with a black check band.",["Taxi_concept","Taxi_render"])]
def vehicles():
    rows = ""
    for k, r, n, note, refs in VEH:
        rr = "".join(ref(x, "vehicles", ("in-engine URP capture" if "ingame" in x else "mesh render" if "render" in x else "pipeline concept input")) for x in refs)
        rows += pair(f'<div class="refstack">{rr}</div>', r3(r, f"{GAME} <b>{n}</b>"), f"<h3>{n}</h3><p>{note}</p>")
    other = "".join(ref(x, "vehicles", c) for x, c in [("MarketLorry_render","Market lorry"),("MarketLorry_alt_render","Market lorry (alt)"),("SandTipper_concept","Sand tipper concept"),("SandTipper_render","Sand tipper render")])
    paints = "".join(r3("danfo_"+k, f"{CON} <b>{t}</b><br>{d}") for k, t, d in [
        ("classic","No Food for Lazy Man","Classic yellow, two black stripes, black back slogan"),("godstime","God's Time Is the Best","Bottle green, black stripes, gold slogan"),
        ("detty","Detty December","Royal purple, gold stripes, seasonal skin"),("eko","Eko o ni baje o!","Lagos red, black stripes, gold slogan")])
    return f'''<h1>Vehicles</h1><p class="lead">Lagos traffic as it's built today, plus concepts for the vehicles the vision asks for but that don't exist yet. Budgets (vision v2 §4): hero vehicles about 5–10k tris at LOD0, background traffic about 2–4k.</p>{LEGEND}
<h2>In the game</h2>{rows}
<h3>Trucks (references)</h3><div class="cosgrid">{other}</div>
<h2>New vehicles {CON}</h2><p>From the vision gaps: okada (fuel scarcity: “more keke and okada”), petrol tanker and BRT bus. Proportions are set against the danfo (about 3.6 m long). Liveries and company names are fictional; no real operators or brands.</p>
<div class="cosgrid wide">{r3("veh_okada", CON+" <b>Okada</b> · red commuter bike, spoked wheels, rear delivery box. Background traffic, target about 3k tris")}
{r3("veh_tanker", CON+" <b>Petrol tanker</b> · red cab, steel tank, orange bands, “EKO FUEL LOGISTICS” (fictional). Heavy and slow, wide hitbox. Target about 8k tris")}
{r3("veh_brt", CON+" <b>BRT bus</b> · “EKO RAPID” (fictional livery), blue/red/gold, lit destination board. Runs in its own BRT lane chunk (v2 §3). Target about 8k tris")}</div>
<h2 id="paint">Danfo paint jobs {CON}</h2><p>“Danfo garage: paint jobs, slogans painted on the back” (vision v1). These are rendered on the <b>shipped danfo mesh</b> with a repaint shader and projected decals, so they work as material/decal swaps with no new mesh. Part of <code>pack_skins_lagos</code> (price <span class="badge">TBD</span>, store).</p>
<div class="cosgrid wide">{paints}</div>'''

V2 = { # vision v2 §8: effect, duration, cap, cost, unlock
 "owa":("Freezes vehicles in the next lane in your facing direction, within 14 m","3 s","3","free","L2"),
 "pure_water":("One-hit shield: forgives the next traffic hit on you or a follower","until hit / 8 s","2","60","L3"),
 "maltina":("All traffic eases to 50% speed. Spawns paused","4 s","2","80","L3"),
 "change":("Spent automatically on LASTMA/KAI contact. Faction zone safe","6 s","2","90","L5"),
 "danfo_ride":("A danfo carries you + your group across the next 2 lanes; invulnerable while riding","~2 s","1","150","L4"),
 "siren":("Freezes every lane except the one you face. LASTMA ignores you","4 s","1","120","L5"),
 "agbada":("Full traffic immunity. Followers are not covered","2.5 s","1","earned only","L6"),
 "okada_dash":("Next 3 dashes go 1.5× and pass through one vehicle each","3 dashes / 6 s","2","not sold","L7"),
 "gist":("Hawkers' gossip pulls LASTMA/KAI off their posts. Clears flags and cones","5 s","1","100","L8"),
}
def powerups():
    E = {p:(d,c,cap,f) for p,d,_,c,cap,f in ECON}
    def code(pid): d,c,cap,f = E[pid]; return f"<b>Code (GidiEconomyTables):</b> {c} chips · cap {cap} · from L{f}"
    def vis(k): e,du,cap,cost,u = V2[k]; return f"<b>Vision v2 §8:</b> {e}. {du} · cap {cap} · cost {cost} · {u}"
    items = [
     ("Pure Water","pure_water","pure_water", [ref("pure_water_current","powerups","in-game pickup (current)"), ref("pure_water_3d_render","powerups","regenerated mesh render")], r3("pu_purewater", GAME+" <b>Pure Water</b> pickup at dusk"),
      "v2 concept (not hosted, origin unclear): a pillow-shaped sachet with blue water, on white."),
     ("Maltina Break","maltina_gala","maltina", [ref("maltina_3d_render","powerups","regenerated mesh render")], r3("pu_maltina", GAME+" <b>Maltina &amp; Gala</b> pickup at dusk"),
      "Not hosted: <code>maltina_current.png</code> (the in-game pickup image) shows real-brand-style “Gala” and malt-drink packaging. ⚠️ Flag: the shipped model and the item name use real brands, but our rule is fictional brands only. The v2 concept (not hosted, origin unclear) is a plain brown malt bottle with a red/gold label."),
     ("Change (Bribe)","bribe_change","change", [ref("change_current","powerups","in-game pickup (current)")], r3("pu_change", GAME+" <b>Change Bundle</b> pickup at dusk"),
      "v2 concept (not hosted, origin unclear): a rubber-banded stack of worn naira-style notes and a coin."),
     ("VIP Siren","siren","siren", [ref("vip_siren_current","powerups","in-game pickup (current)"), ref("vip_siren_3d_render","powerups","regenerated mesh render")], r3("pu_siren", GAME+" <b>VIP Siren</b> pickup at dusk"),
      "v2 concept (not hosted, origin unclear): a red/blue LED light bar."),
    ]
    rows = "".join(pair(f'<div class="refstack">{"".join(rs)}</div>', rr, f"<h3>{n}</h3><p>{code(pid)}</p><p>{vis(v)}</p><p class='small'>{note}</p>") for n, pid, v, rs, rr, note in items)
    conc = "".join(pair(f'<div class="card" style="margin:0"><b>No reference image exists.</b><br>{why}</div>', r3(img, CON+f" <b>{n}</b>"), f"<h3>{n}</h3><p>{extra}</p><p>{vis(v)}</p>") for n, v, img, why, extra in [
     ("Owa! (shout)","owa","pu_owa","Vision: “You read the traffic, shout ‘Owa!’, and everybody gets across safe.”",f"Baba Gidi cups his mouth; gold sound rings travel along his facing direction and the next lane's vehicle freezes in a pale-blue ice block (colour-blind safe: shape plus colour). Free in v2, but in the code today it's {E['owa'][1]} chips · cap {E['owa'][2]} · from L{E['owa'][3]}."),
     ("Danfo Ride","danfo_ride","pu_danforide","Use the shipped danfo (see Vehicles).","A gold-lit danfo at the curb; a gold arc shows the 2-lane hop. Toast copy: “ENTER WITH YOUR CHANGE!” Not in the code yet: price <span class='badge'>TBD</span> until Kehinde decides (vision says 150)."),
     ("Agbada Armour","agbada","pu_agbada_armour","Detty December flex. Earned only.","Baba Gidi in a gold agbada inside a gold fresnel shell with sparkles. 2.5 s of full immunity; followers stay vulnerable. Not in the code yet; never sold."),
    ])
    left = "".join(f'<li>{t}</li>' for t in ["Okada Dash (v2, L7, not sold): concept image exists but isn't hosted (origin unclear). Description: yellow open-face helmet with a black stripe.",
        "Gist Bomb (v2, 100, L8): concept image exists but isn't hosted (origin unclear). Description: a red retro transistor radio.",
        f"Agbero Whistle: still in the code ({E['agbero_whistle'][1]} chips, cap {E['agbero_whistle'][2]}, L{E['agbero_whistle'][3]}) but removed in vision v2."])
    return f'''<h1>Power-ups</h1><p class="lead">Current pickups (shipped models re-staged at dusk) next to the reference images, plus concepts for the three new v2 items that have no image. <b>Prices follow <code>GidiEconomyTables</code></b> until Kehinde decides; vision v2 numbers are shown for comparison only.</p>{LEGEND}
<h2>Current pickups</h2>{rows}
<h2>New v2 items {CON}</h2>{conc}
<h2>Not shown as images</h2><ul>{left}</ul>
<div class="card" style="max-width:440px">{r3("pu_whistle", GAME+" <b>Agbero Whistle</b> pickup (in code, cut in v2)")}</div>
<p class="small">HUD icons for every power-up: <a href="icons.html">Icons</a>.</p>'''

OUTFITS = [("baba_default",GAME,"Default fit","Green kaftan + fila (shipped texture)."),
 ("baba_agbada",CON,"Agbada","Cream agbada with gold embroidery over the matching kaftan, and a cream/gold fila. The robe is cloth-sim geometry over the same rig."),
 ("baba_ankara",CON,"Ankara fit","Blue/gold/red wax-print pattern on the kaftan + trousers (texture swap only)."),
 ("baba_okada",CON,"Okada helmet","Yellow open-face helmet with a black stripe and an orange hi-vis kaftan with reflective bands, next to his okada."),
 ("baba_owambe",CON,"Owambe (Detty December)","Purple lace with a gold-embroidered aso-oke agbada, gold fila and confetti. Seasonal."),
 ("baba_jersey",CON,"Generic jersey","Red/white stripes. Generic style only, no licensed kits (vision v1).")]
def costumes():
    cards = "".join(r3(k, f"{b} <b>{n}</b><br>{d}") for k, b, n, d in OUTFITS)
    return f'''<h1>Costumes &amp; skins</h1><p class="lead">Baba Gidi outfits, rendered on the <b>shipped Baba Gidi model and rig</b> at Lagos dusk. Fits are texture swaps plus, for agbada, a robe layer. The Humanoid rig, silhouette and hitbox don't change. These replace the earlier flat drawings.</p>{LEGEND}
<div class="card"><b>Sources.</b> Vision v1: “Baba Gidi outfits (agbada, okada helmet, Ankara fits, football jerseys in generic styles, no licensed kits)” and “Detty December … owambe outfits”. IAP SKUs in <code>GidiEconomyTables.IapSkus</code>: <code>pack_baba_fits</code> and <code>pack_skins_lagos</code>. Cosmetics are vanity only. Prices and pack contents: <span class="badge">TBD</span> (store; follow <code>GidiEconomyTables</code> until Kehinde decides).</div>
<h2>Baba Gidi fits (<code>pack_baba_fits</code>)</h2><div class="pair" style="grid-template-columns:1fr 1fr 1fr"><div class="pp">{ref("BabaGidi_concept","babagidi","model concept input")}</div><div class="pp">{ref("BabaGidi_rigged_render","babagidi","rigged model render")}</div><div class="pn"><h3>Reference</h3><p>Only the default outfit exists in the game. Every other fit below is a CONCEPT.</p></div></div>
<div class="cosgrid">{cards}</div>
<h2>Lagos Skins (<code>pack_skins_lagos</code>)</h2><p>Danfo paint jobs and slogans: see <a href="vehicles.html#paint">Vehicles · paint jobs</a>.</p>
<h2>Still missing</h2><ul><li>Translucent “ghost” Baba Gidi (async ghosts, v2 §6): <span class="badge">TBD</span>.</li><li>Emotes and trail effects: <span class="badge">TBD</span>.</li></ul>
<h2>Readability rules</h2><ul><li>The hat or helmet must contrast with both asphalt <code>#26272E</code> and the walkway at the 65° camera.</li><li>Same rig and hitbox for every fit.</li><li>Not costumes: Agbada Man, Slay Queen, commuters, LASTMA and KAI are NPCs (see <a href="characters.html">Characters</a>).</li></ul>'''
