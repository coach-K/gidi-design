import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES=[("index","Brand"),("guidelines","Guidelines"),("palette","Palette"),("typography","Typography"),("icons","Icons"),("logos","Logos & app icons"),("screens","Screens"),("levels","Levels"),("costumes","Costumes"),("souvenirs","Souvenirs & perks"),("devices","Devices")]
def nav(cur):
    return '<nav><a class="brand" href="index.html">GIDI<span>++</span></a>'+"".join(f'<a href="{k}.html"{" class=on" if k==cur else ""}>{t}</a>' for k,t in PAGES)+'<small>Design system v0.1 · Oct 2026 · LANDSCAPE ONLY (RT-106)</small></nav>'
def page(k, body):
    t=dict(PAGES)[k]
    open(os.path.join(ROOT,f"{k}.html"),"w").write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gidi++ · {t}</title><link rel="stylesheet" href="css/site.css"></head><body>{nav(k)}<main>{body}</main></body></html>')
def stub(title, items):
    return f'<h1>{title} <span class="badge">STUB, phase 2</span></h1><div class="stub"><b>Planned contents</b><ul>'+"".join(f"<li>{i}</li>" for i in items)+'</ul></div>'

page("index", '''<h1>Gidi++ brand</h1><p class="lead">Cross Lagos. Don't get jammed. A 3D (Unity URP, semi-real, perspective camera) curb-crossing game for Millennials and Gen Z. You play Baba Gidi (12+, <b>not</b> a kids' game). You lead a crowd across Lagos traffic, from Agege to the endless chaos of Ojuelegba.</p>
<div class="card"><h3>Pillars</h3><ul><li><b>Semi-real Lagos dusk-glass.</b> Grounded proportions and believable materials, pushed about 20% toward readability. Ink glass UI, warm gold, hairline edges.</li><li><b>Readable threats first.</b> Every danger is shown by colour <i>and</i> shape <i>and</i> motion (colour-blind safe).</li><li><b>Fair free-to-play.</b> Soft-currency power-ups (₦ Naira Chips), <b>1 continue per run</b>, cosmetics only for real money.</li><li><b>Proudly Lagos.</b> Real places and Pidgin/Yoruba flavour ("Eiya!", "Owa!", "Enter with your change!"), with fictional brands only.</li></ul></div>
<div class="card"><h3>Voice</h3><table><tr><th>Do</th><th>Don't</th></tr><tr><td>Pidgin-first, warm, street-smart: "Chai! Traffic don catch you…", "Oya, cross!", "We don reach!"</td><td>Internal or marketing copy ("Elegant continue")</td></tr><tr><td>Pidgin flavour that a first-timer can still understand from context</td><td>Mocking accents, kid-speak, real trademarks</td></tr></table></div>
<div class="card"><h3>Platform rule</h3><p><b>Landscape only</b> on every device (Kehinde, Oct 16, 2026, RT-106). Cars cross sideways, so landscape shows whole lanes. There are no portrait layouts.</p></div>
<h2>Approval mockups (M1, Oct 30)</h2><div class="grid"><a href="screens.html"><img class="shot" src="exports/home-desktop.png" alt="Home"></a><a href="screens.html"><img class="shot" src="exports/shop-desktop.png" alt="Base Camp"></a><a href="screens.html"><img class="shot" src="exports/hud-desktop.png" alt="HUD"></a><a href="screens.html"><img class="shot" src="exports/gameover-desktop.png" alt="Game over"></a></div>''')

page("guidelines", '''<h1>Guidelines</h1><p class="lead">Rules every screen follows. The source is G-Prototype <code>docs/ui/ArtDirection_OnePager.md</code> and <code>UX_Flows_Sprint1.md</code>.</p>
<div class="card do"><h3>Layout</h3><ul><li><b>Landscape only.</b> Reference canvas 1920×1080, CanvasScaler matched on height.</li><li>Everything sits inside <code>Screen.safeArea</code>. Desktop margin 32 px. Phone (19.5:9, 2340×1080): notch inset 132 px, home indicator 63 px.</li><li>Minimum touch target <b>144 px = 48 dp</b>. Primary CTA 192 px tall.</li><li>Thumb zones: bottom-left (translucent PICK UP) and bottom-right (translucent 8-way d-pad, primary CTA). Pause and Settings top-right, where they need a deliberate reach.</li><li>In-run: camera and controls as in the current build (overlap of controls with lane ends accepted). See the <a href="screens.html#hud">HUD spec</a>.</li></ul></div>
<div class="card do"><h3>HUD</h3><ul><li>Stock order is always <b>GROUP → CHANGE → OWA!</b>, left to right.</li><li>Currency is always <b>₦</b> + amount (<code>₦12,450</code>), never "N".</li><li>Continue: <b>max 1 per run</b>. Cost: 100 chips at L1, 125 chips at L2+, or watch an ad (GidiEconomyTables).</li><li>Touch controls only on touch devices. No keyboard / "Space" hints on screen.</li></ul></div>
<div class="card do"><h3>Accessibility</h3><ul><li>Warning states pair colour with shape, icon and motion (see Palette).</li><li>Text contrast is WCAG AA or better on glass; graphics are at least 3:1.</li><li>Planned: colour-blind mode, text size S/M/L, reduce motion, haptics toggle.</li></ul></div>
<div class="card dont"><h3>Don't</h3><ul><li>No portrait layouts. No kid-style bubbly UI. No real brands.</li><li>No economy numbers that aren't in <code>GidiEconomyTables</code>.</li><li>Never rely on colour alone. Don't move controls away from the build positions without sign-off.</li></ul></div>''')

sw=lambda h,n,note,fg="#111":f'<div class="sw"><div class="c" style="background:{h};color:{fg}">Aa</div><p><b>{n}</b><br><code>{h}</code> {note}</p></div>'
page("palette", '<h1>Palette <span class="badge" style="background:#56B4E9">APPROVED · Kehinde, Oct 13 2026</span></h1><p class="lead">Dusk-glass UI, Okabe-Ito based warning colours, and Day/Dusk grade targets.</p>'
 +'<h2>UI</h2><div class="grid">'+sw("#0F1219","HUD glass (72%)","base","#F5F5F0")+sw("#F5F5F0","Text primary","17.1:1")+sw("#9EA3AD","Text muted","7.4:1")+sw("#FAE69E","Naira gold","15.1:1")+sw("#E8B21E","Danfo yellow","accent")+sw("#2E7A68","Primary CTA","#F5F5F0","#F5F5F0")+'</div>'
 +'''<h2>Warning palette (colour + shape + motion)</h2><table><tr><th>State</th><th>Hex</th><th>Shape</th><th>Icon / pattern</th><th>Motion / audio</th><th>vs glass</th></tr>
<tr><td>Safe / clear</td><td><code>#56B4E9</code></td><td>Rounded bar</td><td>✓ solid</td><td>static</td><td>8.1:1</td></tr>
<tr><td>Caution</td><td><code>#F0E442</code></td><td>Triangle</td><td>! + 45° stripes</td><td>1 Hz pulse</td><td>14.2:1</td></tr>
<tr><td>Danger</td><td><code>#FF7A1A</code></td><td>Chevrons ≫</td><td>scrolling double chevron</td><td>3 Hz flash, headlights, horn</td><td>7.2:1</td></tr>
<tr><td>LASTMA</td><td><code>#E07CC0</code></td><td>Diamond</td><td>whistle, dotted</td><td>whistle cue</td><td>7.0:1</td></tr>
<tr><td>Train</td><td><code>#FFFFFF</code></td><td>Lane band</td><td>rail ties ‖‖‖</td><td>bell + rumble</td><td>18.7:1</td></tr></table>
<div class="card dont">Under deuteranopia and protanopia, Safe, Danger and LASTMA collapse in hue (simulated contrast 1.0–1.6). <b>Shapes are mandatory.</b> Optional colour-blind mode: Danger <code>#D55E00</code> with thicker chevrons.</div>
<h2>Colour grade</h2><table><tr><th>Key</th><th>Day (L1–L4)</th><th>Dusk (L5–L10, menus)</th></tr>
<tr><td>Sky top / horizon</td><td><code>#7FB4E0</code> / <code>#F4E3C1</code></td><td><code>#2B2F5C</code> / <code>#F28C4B</code></td></tr>
<tr><td>Key light</td><td><code>#FFF1D6</code> ×1.2</td><td><code>#FFB070</code> ×0.8</td></tr>
<tr><td>Shadow tint</td><td><code>#3A4A66</code></td><td><code>#2A2440</code></td></tr>
<tr><td>Asphalt / laterite</td><td><code>#3C3F45</code> / <code>#B5643A</code></td><td><code>#26272E</code> / <code>#7A4630</code></td></tr>
<tr><td>Danfo yellow</td><td><code>#E8B21E</code></td><td>albedo <code>#E8B21E</code> → on-screen <code>#F0A830</code></td></tr>
<tr><td>Highlights tint</td><td><code>#FFF4E0</code></td><td><code>#FFC98A</code></td></tr>
<tr><td>Bloom</td><td>thr 1.1 · int 0.2 · <code>#FFFFFF</code></td><td>thr 0.9 · int 0.45 · <code>#FFB46B</code></td></tr></table>''')

page("typography", '''<h1>Typography</h1><p class="lead"><b style="font-family:Jakarta">Plus Jakarta Sans Bold</b> by Tokotype, under the SIL Open Font License 1.1 (<a href="fonts/OFL.txt" style="color:#FAE69E">licence</a>). Free for commercial use, includes the ₦ glyph, and looks modern and grown-up.</p>
<div class="card" style="font-family:Jakarta"><div style="font-size:56px">Cross Lagos. ₦12,450</div><div style="font-size:28px;color:#9EA3AD">GROUP → CHANGE → OWA! · Eiya! That traffic got you…</div></div>
<table><tr><th>Role</th><th>Constant</th><th>Ref px (1920×1080)</th><th>px @ 1280×720</th><th>Sample</th></tr>
<tr><td>Title</td><td><code>FontTitle</code></td><td>42</td><td>28</td><td style="font:700 28px Jakarta">L3 · Ikorodu Road</td></tr>
<tr><td>Naira wallet</td><td><code>FontNaira</code></td><td>48</td><td>32</td><td style="font:700 32px Jakarta;color:#FAE69E">₦12,450</td></tr>
<tr><td>Body</td><td><code>FontBody</code></td><td>33</td><td>22</td><td style="font:700 22px Jakarta">Continue this run?</td></tr>
<tr><td>Small (floor)</td><td><code>FontSmall</code> / <code>FontMin</code></td><td>27</td><td>18</td><td style="font:700 18px Jakarta;color:#9EA3AD">Saved 4/6 · Best 00:42</td></tr>
<tr><td>Button</td><td><code>FontButton</code></td><td>30</td><td>20</td><td style="font:700 20px Jakarta">CROSS!</td></tr></table>
<div class="card">No text goes below 27 ref px (18 px at 720p). Numbers use tabular figures where they tick (timer, wallet).</div>''')

import sections
page("screens", sections.screens())
page("icons", stub("Icons", ["Power-up icons for the 6 table items (Owa, Maltina &amp; Gala, Pure Water, Change Bundle, VIP Siren, Agbero Whistle), plus the vision v2 §8 next-gen set once it lands in code","Warning shapes: tick bar, triangle, chevrons, diamond, rail band (SVG, 24/48/96 px)","HUD glyphs: ₦, lives ♥, stats, pause, settings, map, Base Camp","Rules: 2 px stroke at 48 px, rounded joins, glass-safe colours"]))
page("logos", stub("Logos &amp; app icons", ["GIDI++ wordmark (light, dark, mono), clear-space and minimum size","App icons: iOS 1024 master + sizes, Android adaptive (foreground/background 432 px, 108 dp safe zone), WebGL favicon / PWA 192/512","Store feature graphic 1024×500 and landscape screenshots (from the approved mockups)","12+ rating badge usage"]))
page("levels", sections.levels())
page("costumes", sections.costumes())
page("souvenirs", stub("Souvenirs &amp; perks", ["Souvenir collectibles per district (non-power, collection meta)","Perk rules: soft-currency only, caps from <code>PowerUpInventoryCap</code>, unlock levels from <code>PowerUpFirstLiveLevel</code>","Owa meter / combo rewards (vision v2 §8), once the numbers are in GidiEconomyTables","No economy numbers until they are in code"]))
page("devices", stub("Devices (Android / iOS / Web)", ["All landscape: 16:9 desktop/WebGL 1920×1080, phones 19.5:9 (2340×1080) and 20:9 (2400×1080), tablets 4:3 (2048×1536)","Safe-area templates: iPhone notch/Dynamic Island (44 pt side insets, 21 pt home indicator), Android cutouts","Input: touch (PICK UP + d-pad) vs keyboard/mouse (hint card); gamepad later","Orientation lock: Landscape Left/Right in Player Settings; the WebGL template shows a rotate-device prompt when held in portrait"]))
print("ok")
