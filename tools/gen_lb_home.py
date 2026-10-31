"""GPP-LEADERBOARD-HOME (Oct 31): Home leaderboard tile + weekly L10 / Country leaderboard.
Renders ONLY the new sprites (does not touch the rest of exports/unity), merges their manifest entries keyed by `file`
(never drops an entry), and renders the 1920x1080 previews into exports/ (HTML in mockups/).
Do not run gen_unity.py for this: its main block wipes sprites@1x/@2x. The definitions for seg_filter_pressed and
pill_week_reset also live in gen_unity.py so a full re-export reproduces them."""
import os, sys, json, re, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from brand import icon, P
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = f"{ROOT}/exports/unity"; OUT = f"{ROOT}/exports"; MK = f"{ROOT}/mockups"
TAG = "GPP-LEADERBOARD-HOME"

def chrome(html_path, png, w, h, sc=1):
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={sc}",
                    "--default-background-color=00000000", f"--window-size={w},{h+300}", f"--screenshot={png}", f"file://{html_path}"],
                   stderr=subprocess.DEVNULL, check=True)
    Image.open(png).convert("RGBA").crop((0, 0, w*sc, h*sc)).save(png)

# ------------------------------------------------------------------ sprites
def wifi_badge(size=40):
    """Offline badge for the Home tile: ink disc, muted ring, white wifi_off glyph (its slash keeps danger orange)."""
    g = icon("wifi_off", 26, "#FFFFFF")
    return (f'<div style="position:relative;width:{size}px;height:{size}px;border-radius:50%;background:#0F1219;border:2px solid rgba(158,163,173,.75);box-sizing:border-box">'
            f'<div style="position:absolute;left:5px;top:5px;width:26px;height:26px;display:flex">{g}</div></div>')

def sprites():
    import gen_unity as GU          # module import only builds GU.S; its __main__ block (which wipes folders) does not run
    mine = {"icon_country", "icon_country_white", "seg_filter_pressed", "pill_week_reset"}
    S = [s for s in GU.S if s["name"] in mine]
    assert {s["name"] for s in S} == mine, {s["name"] for s in S}
    S.append(dict(name="icon_trophy", folder="@home", w=44, h=44, html=icon("trophy", 44, "#FFFFFF"), screen="home", border=None, pivot=(0.5, 0.5),
                  note=f"Home leaderboard tile icon ({TAG}). White on transparent, same 3 px/48 stroke as icon_settings / icon_souvenirs; HomeScreenView.AddIcon loads UI/Home/{{1x|2x}}/icon_trophy and shows it untinted. Pressed: Image.color #FAE69E. SVG: svg/icons/trophy.svg"))
    S.append(dict(name="badge_tile_offline", folder="@home", w=40, h=40, html=wifi_badge(40), screen="home", border=None, pivot=(1, 1),
                  note=f"Offline badge on the Home leaderboard tile ({TAG}). Child Image 40×40, anchor/pivot top-right, anchoredPosition (−6, −6) inside the 144 tile. Tile stays tappable (opens the offline card with the cached best)."))
    PAD = 8; X = 0
    for s in S: s["x"] = X; X += s["w"] + PAD
    W, H = X, max(s["h"] for s in S)
    body = "".join(f'<div style="position:absolute;left:{s["x"]}px;top:0;width:{s["w"]}px;height:{s["h"]}px;overflow:visible">{s["html"]}</div>' for s in S)
    p = "/tmp/lbhome_sheet.html"
    open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}*{{box-sizing:border-box}}</style></head><body style="position:relative;width:{W}px;height:{H}px">{body}</body></html>')
    man = []
    for sc in (1, 2):
        png = f"/tmp/lbhome_sheet@{sc}.png"; chrome(p, png, W, H, sc); sheet = Image.open(png)
        for s in S:
            d = f"{U}/home/{sc}x" if s["folder"] == "@home" else f"{U}/sprites@{sc}x/{s['folder']}"
            os.makedirs(d, exist_ok=True)
            sheet.crop((s["x"]*sc, 0, (s["x"]+s["w"])*sc, s["h"]*sc)).save(f"{d}/{s['name']}.png")
    for s in S:
        f1, f2 = ((f"home/1x/{s['name']}.png", f"home/2x/{s['name']}.png") if s["folder"] == "@home"
                  else (f"sprites@1x/{s['folder']}/{s['name']}.png", f"sprites@2x/{s['folder']}/{s['name']}.png"))
        man.append(dict(name=s["name"], file=f1, file2x=f2, size=[s["w"], s["h"]], pivot=list(s["pivot"]),
                        border=(dict(zip(("left", "right", "top", "bottom"), s["border"])) if s["border"] else None), screen=s["screen"], note=s["note"]))
    os.makedirs(f"{U}/svg/icons", exist_ok=True); shutil.copy(f"{ROOT}/icons/svg/country.svg", f"{U}/svg/icons/country.svg")
    return man

def merge(path, entries):
    """Merge keyed by `file` (names repeat across folders, e.g. icon_souvenirs). Replaces same-file entries in place, appends new ones."""
    m = json.load(open(path)); n0 = len(m["sprites"])
    by = {e["file"]: e for e in entries}
    m["sprites"] = [by.pop(s.get("file"), s) for s in m["sprites"]] + [e for e in entries if e["file"] in by]
    assert len(m["sprites"]) >= n0
    json.dump(m, open(path, "w"), indent=1, ensure_ascii=False)
    return n0, len(m["sprites"])

# ------------------------------------------------------------------ home mock
def tile(x_right, cap, ic, cls="", badge=False):
    return (f'<div class="tile {cls}" style="right:{x_right}px;top:0"><div class="ti">{ic}</div><div class="tc">{cap}</div>'
            f'{"<div class=bdg>"+wifi_badge(40)+"</div>" if badge else ""}</div>')

def home_frame(W, sl, sr, st, sb, two_row=False, annotate=False, phone=False, state=""):
    from brand import wordmark
    wt = "#FFFFFF"
    r2 = 160 if two_row else 0          # second row (y +160) when safe aspect < 1.5
    rk_right, sv_right = (160, 0) if two_row else (732, 572)
    trophy_c = P["naira"] if state == "pressed" else wt
    tiles = (tile(0, "Settings", icon("settings", 44, wt)) +
             f'<div class="hlives glass" style="right:160px">{icon("lives",44,"#FF6B7A")}&nbsp;3</div>' +
             f'<div class="hchips glass" style="right:296px"><span style="display:flex;align-items:center;gap:8px">₦12,450</span><small>NAIRA CHIPS</small></div>')
    srow = f'<div style="position:absolute;right:0;top:{r2}px;width:{sv_right+144}px;height:144px">' if two_row else '<div style="position:absolute;inset:0 0 auto 0;height:144px">'
    srow += tile(sv_right, "Souvenirs", icon("souvenirs", 44, wt))
    srow += tile(rk_right, "Ranks", icon("trophy", 44, trophy_c), state, badge=(state == "offline")) + "</div>"
    logo = wordmark(98)
    body = f'''<div class="hlogo">{logo}</div><div class="htag">Carry dem cross. Lagos no dey wait.</div><div class="hrate">12+</div>
{tiles}{srow}
<div class="hcol">
 <button class="glass big2">{icon("map",56,P["naira"])}<div>Lagos map<small>10 districts · Agege to Ojuelegba</small></div></button>
 <button class="glass big2">{icon("basecamp",56,P["naira"])}<div>Base Camp<small>Load your bag before you cross</small></div></button>
 <button class="cta">{icon("play",64,P["text"])}<div>OYA, PLAY<small>L9 · Lekki Toll Gate</small></div></button>
</div>
<div class="htip glass">Baba Gidi don ready. Owa!</div>'''
    ann = ""
    if annotate:
        sw = W - sl - sr
        x0 = sl + sw - rk_right - 144; y0 = st + r2
        ann += f'<div class="ann" style="left:{x0-4}px;top:{y0-4}px;width:152px;height:152px"><b style="left:{0 if not two_row else -300}px;top:160px">Ranks · anchoredPosition ({-rk_right}, {-r2}) · 144×144 · x {x0}–{x0+144}, y {y0}–{y0+144}</b></div>'
        sx = sl + sw - sv_right - 144
        ann += f'<div class="ann" style="left:{sx-4}px;top:{y0-4}px;width:152px;height:152px;border-style:dotted"><b style="left:0;top:-34px;{"" if not two_row else "top:160px;left:auto;right:0"}">Souvenirs · x {sx}–{sx+144}</b></div>' if not two_row or True else ""
        ann += f'<div class="ann warn" style="left:{sl}px;top:{st+106}px;width:530px;height:40px"><b style="left:0;top:44px">tagline ends x {sl+526}</b></div>'
    pcls = "phone" if phone else "desktop"
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Home leaderboard {W}</title>
<link rel="stylesheet" href="../css/hud.css"><link rel="stylesheet" href="../css/mock.css"><link rel="stylesheet" href="../css/leaderboard_home.css"></head>
<body style="width:{W}px;height:1080px"><div class="frame {pcls} realbg home" style="width:{W}px;height:1080px;--sl:{sl}px;--sr:{sr}px;--st:{st}px;--sb:{sb}px"><img class="scene" src="../assets/bg/lv_home_desktop.png" alt=""><div class="grade"></div>
{'<div class="notch"></div><div class="homebar"></div>' if phone else ''}
<div class="safe">{body}</div>{ann}</div></body></html>"""

def states_sheet():
    wt = "#FFFFFF"
    def st(cls, label, spec, ic_c=wt, badge=False):
        t = f'<div class="tile {cls}"><div class="ti">{icon("trophy",44,ic_c)}</div><div class="tc">Ranks</div>{"<div class=bdg>"+wifi_badge(40)+"</div>" if badge else ""}</div>'
        return f'<div class="scard"><div class="stage">{t}</div><b class="n">{label}</b>{spec}</div>'
    cards = (st("", "Normal", '<p>Frame <code>btn_glass_normal</code> 9-slice (border 36). Icon <code>home/2x/icon_trophy</code> 44, white. Caption “Ranks” 22 px #9EA3AD, Best Fit off. Tap → leaderboard.</p>') +
             st("pressed", "Pressed", '<p>SpriteSwap → <code>btn_glass_pressed</code>. Icon Image.color #FAE69E, caption #F5F5F0. Scale 0.96 for 80 ms (Home tiles already do this).</p>', P["naira"]) +
             st("", "Offline", '<p>Normal frame + <code>badge_tile_offline</code> 40 px, top-right (−6, −6). <b style="color:#F5F5F0">Still tappable</b>: opens the board with the RT-109 Offline card and your saved best.</p>', wt, True) +
             st("disabled", "Disabled", '<p><code>btn_glass_disabled</code>; icon + caption 45%. interactable = false. Only when leaderboards are not in the build / remote-config off. Not used for offline.</p>') +
             st("focus", "Focus (WebGL)", '<p>Keyboard / controller focus: <code>btn_glass_highlight</code> (glow in a 24 px margin). Enter = tap.</p>'))
    body = f'''<div class="sheet"><div class="kk">{TAG} · HOME TILE STATES</div><h1>Leaderboard tile · 144 × 144 · caption “Ranks” · a11y name “Leaderboard”</h1>
<p class="lead">Previews shown at 1.5×. Same frame sprites and layout as Settings / Souvenirs (44 px icon at (0, +16), 22 px caption in a 144 × 30 rect at (0, −34)). Text: legacy UI.Text, Best Fit OFF, no Outline, one Shadow (0, −2) #000 @ 60%.</p>
<div class="cards">{cards}</div>
<p class="lead" style="margin-top:36px">Caption: “Leaderboard” is 139.5 px at 22 px in a 144 px tile (2 px each side), so it only fits by Best Fit shrinking it, and Best Fit is not allowed. “Ranks” is 64 px. Fallback if the full word is wanted: “Leaderboard” at a fixed 20 px (127 px).</p></div>'''
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../css/hud.css"><link rel="stylesheet" href="../css/leaderboard_home.css"></head>
<body style="width:1920px;height:1080px"><div class="frame" style="width:1920px;height:1080px">{body}</div></body></html>'''

def aspects_sheet(pngs):
    """Compose 16:9 / 20:9 / 4:3 renders onto one 1920x1080 board with labels (PIL)."""
    F = f"{ROOT}/fonts/PlusJakartaSans-Bold.ttf"
    bd = Image.new("RGB", (1920, 1080), (15, 18, 25)); d = ImageDraw.Draw(bd)
    f1, f2, f3 = ImageFont.truetype(F, 34), ImageFont.truetype(F, 22), ImageFont.truetype(F, 20)
    d.text((56, 36), f"{TAG} · Home leaderboard tile across aspect ratios (canvas match height 1.0)", font=f1, fill=(245, 245, 240))
    sc = 0.385
    spots = [("16:9 · 1920×1080 desktop · safe 32 px", pngs["16x9"], (56, 120), "Ranks x 1012–1156, y 32–176 · left of Souvenirs (1172–1316) · 16 px gaps"),
             ("4:3 · 1024×768 → canvas 1440×1080 · safe 1376×1016 (aspect 1.35 < 1.5)", pngs["4x3"], (56 + int(1920*sc) + 48, 120), "Two rows: Souvenirs at anchoredPosition (0, −160), Ranks (−160, −160) → x 1104–1248, y 192–336"),
             ("20:9 · 2400×1080 phone · notch inset 132 (symmetric), bottom 63", pngs["20x9"], (56, 120 + int(1080*sc) + 96), "Ranks x 1392–1536, y 0–144 · same offsets as 16:9, 550+ px free to the tagline")]
    for lab, p, (x, y), note in spots:
        im = Image.open(p).convert("RGB"); im = im.resize((int(im.width*sc), int(im.height*sc)), Image.LANCZOS)
        bd.paste(im, (x, y + 34)); d.rectangle((x-1, y+33, x+im.width, y+34+im.height), outline=(232, 178, 30), width=2)
        d.text((x, y), lab, font=f2, fill=(250, 230, 158)); d.text((x, y + 34 + im.height + 10), note, font=f3, fill=(158, 163, 173))
    x = 56 + int(2400*sc) + 56; y = 120 + int(1080*sc) + 96
    rules = ["Rule (HomeScreenView, pivot/anchor top-right):", "safe = SafeAreaFitter rect", "if safe.width / safe.height < 1.5:", "  Souvenirs → anchoredPos (0, −160)", "  Ranks     → anchoredPos (−160, −160)",
             "else:", "  Souvenirs → anchoredPos (−572, 0)", "  Ranks     → anchoredPos (−732, 0)", "", "Same threshold the HUD uses for its", "two-row layout. Map column top sits", "at 504 (4:3) so row 2 (192–336) is clear."]
    for i, r in enumerate(rules): d.text((x, y + 34 + i*30), r, font=f2 if i else f2, fill=(245, 245, 240) if i else (232, 178, 30))
    bd.save(f"{OUT}/home-leaderboard-aspects-desktop.png")

# ------------------------------------------------------------------ leaderboard mocks
import gen_leaderboard as GL
from gen_more import shell

WEEK = dict(kicker="WEEKLY · L10 · W44", title="Ojuelegba Chaos", road="Same road for everybody this week. Fastest clear wins.", resets="Resets in 1d 19h")

def tabs_weekly(sel=10):
    GL.UNLOCKED = 10
    return GL.tabs(sel).replace('<span>Ojuelegba</span>', '<span>Weekly</span>')

def side_weekly(flt, cc="NG", best="02:31.44", rank="#412", players="18,730", cc_label=None, hot=False, pressed=None):
    def seg(k, ic, label, extra=""):
        on = k == flt; pr = k == pressed
        c = P["text"] if pr else P["naira"] if on else P["muted"]
        return f'<div class="hit"><div class="{"pr" if pr else "on" if on else ""}">{icon(ic, 40, c)}<span class="{extra}">{label}</span></div></div>'
    segs = seg("Global", "trophy", "Global") + seg("Country", "country", cc_label or cc, "cc")
    return f'''<div class="lbside glass"><div class="k">{icon("trophy",30,P["gold"])} {WEEK["kicker"]}</div><h2>{WEEK["title"]}</h2>
<div class="road">{WEEK["road"]}</div>
<div class="wpill{" hot" if hot else ""}">{icon("timer",28,P["danger"] if hot else P["naira"])} {WEEK["resets"] if not hot else "Resets in 42m"}</div>
<div class="seg2">{segs}</div>
<div class="kv2"><span>Your best this week</span><b>{best}</b><span>Your rank</span><b>{rank}</b><span>Players</span><b>{players}</b></div>
<button class="cta sm">{icon("play",40,P["text"])} BEAT AM</button></div>'''

def lst(rows_data, me, head_extra=""):
    C = GL.COLS_T
    rows = "".join(GL.rowhtml(k+1, n, i, f'<div class="tm">{GL.t(ms)}</div><div class="ch">{GL.chips(ch)}</div>') for k, (n, i, ms, ch) in enumerate(rows_data))
    mrow = GL.rowhtml(me[0], GL.ME, 7, f'<div class="tm">{GL.t(me[1])}</div><div class="ch">{GL.chips(me[2])}</div>', "you")
    return f'''<div class="lblist glass" style="--cols:{C}">{head_extra}<div class="lbhead" style="--cols:{C}"><span style="text-align:center">RANK</span><span></span><span>PLAYER</span><span class="r">CLEAR TIME</span><span class="r">CHIPS (RUN)</span></div>
{rows}<div class="more">· · · scroll · · ·</div><div class="pinlbl">YOUR BEST THIS WEEK · PINNED</div>{mrow}</div>'''

def page(body, title):
    return shell("desktop", 10, body, title, blur=True).replace("</head>", '<link rel="stylesheet" href="../css/leaderboard.css"><link rel="stylesheet" href="../css/leaderboard_home.css"></head>')

def weekly_global():
    base = [128904, 131277, 132015, 134560, 135092, 137418, 138803]; ch = [420, 390, 445, 360, 410, 380, 400]
    data = [(GL.NAMES[k], k, base[k], ch[k]) for k in range(7)]
    body = f'<div class="ov"></div><div class="lb">{tabs_weekly()}{side_weekly("Global")}{lst(data, (412, 151442, 310))}</div>'
    return page(body, "Leaderboard weekly L10 global")

def weekly_country():
    ng = ["Tunde_Waka", "Chidi.Zoom", "Bisi_Okada", "Emeka404", "Ngozi_Danfo", "Kunle.Kerb", "Ifeoma_99"]
    idx = [GL.NAMES.index(n) for n in ng]
    base = [128904, 132015, 134560, 135092, 138803, 139250, 140117]; ch = [420, 445, 360, 410, 400, 385, 370]
    data = [(ng[k], idx[k], base[k], ch[k]) for k in range(7)]
    cap = f'<div class="lbcap" style="padding:2px 20px 4px">{icon("country",28,P["muted"])} NG · NIGERIA · THIS WEEK</div>'
    body = f'<div class="ov"></div><div class="lb">{tabs_weekly()}{side_weekly("Country", rank="#57", players="3,412")}{lst(data, (57, 151442, 310), cap)}</div>'
    return page(body, "Leaderboard weekly L10 country")

def country_unavailable(cc="KE"):
    title = f"No {cc} board yet" if cc else "Country board no dey yet"
    seg_label = cc or "Country"
    cen = (f'<div class="lblist glass lbempty"><div class="cen">{icon("country",96,P["muted"])}<h4>{title}</h4>'
           f'<p>Country boards are open for a few countries for now. Your time still counts on Global.</p>'
           f'<button class="gbtn2">{icon("trophy",44,P["naira"])} See Global</button>'
           f'<p class="cap">Country comes from your device region{f" ({cc})" if cc else ""}.</p></div></div>')
    body = f'<div class="ov"></div><div class="lb">{tabs_weekly()}{side_weekly("Country", cc=seg_label, rank="—", players="—")}{cen}</div>'
    return page(body, "Leaderboard country unavailable")

def empty_states():
    cards = [
        ("COUNTRY NOT AVAILABLE · REGION KNOWN (KE) <span>· cards at 70%, real CTAs 392×144</span>", f'<div class="cen">{icon("country",96,P["muted"])}<h4>No KE board yet</h4><p>Country boards are open for a few countries for now. Your time still counts on Global.</p><button class="gbtn2">{icon("trophy",44,P["naira"])} See Global</button><p class="capx">Country comes from your device region (KE).</p></div>', ""),
        ("COUNTRY NOT AVAILABLE · REGION UNKNOWN", f'<div class="cen">{icon("country",96,P["muted"])}<h4>Country board no dey yet</h4><p>We no fit tell your country from this device. Your time still counts on Global.</p><button class="gbtn2">{icon("trophy",44,P["naira"])} See Global</button><p class="capx">Tab label reads “Country”.</p></div>', ""),
        ("COUNTRY BOARD OPEN · NO TIMES YET (NG)", f'<div class="cen">{icon("country",96,P["gold"])}<h4>No times yet in NG this week</h4><p>Clear Ojuelegba Chaos and your time goes up first.</p><button class="cta sm" style="min-width:392px;height:144px;font-size:34px">{icon("play",40,P["text"])} OYA, CROSS!</button></div>', ""),
        ("NO FRIENDS YET", f'<div class="cen">{icon("group",96,P["gold"])}<h4>No friends on this board yet</h4><p>Add friends with their Gidi name and race their times here.</p><div style="display:flex;gap:16px"><button class="cta sm" style="min-width:300px;height:144px;font-size:30px">{icon("user",40,P["text"])} Add friends</button><button class="gbtn2" style="min-width:300px;font-size:30px">Share my name</button></div><p class="capx">Your Gidi name: <b style="color:#FAE69E">BabaGidiFan#4821</b></p></div>', '<span class="parked">PARKED · NOT IN v1</span>'),
    ]
    grid = "".join(f'<div class="st glass">{extra}<div class="stk">{k}</div>{c}</div>' for k, c, extra in cards)
    css = '<style>.st .cen h4{font-size:32px}.st .cen p{font-size:22px}.st .cen .capx{font-size:20px}.st .cen{gap:8px}.st .gbtn2{height:100px;min-width:320px;font-size:28px}.st .cen svg[width="96"]{width:64px;height:64px}.st .cta.sm{height:100px!important}.st .stk span{color:#9EA3AD}</style>'
    body = f'{css}<div class="ov"></div><div class="lb">{tabs_weekly()}{side_weekly("Country", cc="KE", rank="—", players="—")}<div class="stgrid">{grid}</div></div>'
    return page(body, "Leaderboard country + friends empty states")

def seg_options():
    def opt(title, w, segs, note, bad=False, sm=False):
        cells = "".join(f'<div class="{"on" if i == 0 else ""}{" sm" if sm else ""}" style="width:{sw}px;flex:none">{icon(ic,40,P["naira"] if i==0 else P["muted"])}{"" if lab is None else lab}</div>' for i, (ic, lab, sw) in enumerate(segs))
        return (f'<div class="opt{" bad" if bad else ""}" style="width:{w+48}px"><div class="kk">{title}</div><div class="cardw" style="width:{w}px;margin-top:12px;padding:22px">'
                f'<div class="seg3" style="margin:0">{cells}</div></div><p>{note}</p></div>')
    a = opt("v1 · SHIPS · CARD 440 (INNER 392)", 440, [("trophy", "Global", 192), ("country", "NG", 192)],
            "Two hit rects of 196 × 144 (sprite inset 4 px on the inner edge so the art keeps the 8 px gap). L1–L9: row hidden; caption “GLOBAL · ALL-TIME”.")
    b = opt("LATER · OPTION A (RECOMMENDED) · CARD 520 (INNER 472)", 520, [("trophy", "Global", 152), ("group", "Friends", 152), ("country", "NG", 152)],
            "3 × 152 + 2 × 8 = 472. List panel shrinks 1392 → 1312 (x 544). Labels fit at 28 px (Friends 111 px).")
    c = opt("LATER · OPTION B · ICON TABS · CARD 496 (INNER 448)", 496, [("trophy", None, 144), ("group", None, 144), ("country", None, 144)],
            "3 × 144 + 2 × 8 = 448. Icon only, name in a 22 px caption under the row (“Global”). Saves 24 px vs A but loses the CC text.")
    d = opt("DON’T · 3 TABS IN 392", 440, [("trophy", "Global", 125), ("group", "Friends", 125), ("country", "NG", 125)],
            "125 px each is under the 144 px minimum tap target.", bad=True, sm=True)
    body = f'''<div class="sheet"><div class="kk">{TAG} · FILTER TABS</div><h1>Global / Country in v1 (Friends hidden: UGS Friends off)</h1>
<p class="lead">Country tab: generic globe + pin <b style="color:#F5F5F0">icon_country</b> (40 px) over the ISO code in 28 px (“NG”, “GB”). Region unknown → label “Country”. No flags: legacy UI.Text has no emoji glyphs, ~250 flag sprites to ship, and some regions are disputed.</p>
<div style="display:grid;grid-template-columns:auto auto;gap:20px 40px;margin-top:20px;align-items:start">{a}{b}{c}{d}</div></div>'''
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../css/hud.css"><link rel="stylesheet" href="../css/leaderboard_home.css"></head>
<body style="width:1920px;height:1080px"><div class="frame" style="width:1920px;height:1080px">{body}</div></body></html>'''

def previews():
    os.makedirs(MK, exist_ok=True); made = []
    def go(name, html, w=1920):
        hp = f"{MK}/{name}.html"; open(hp, "w").write(html)
        png = f"{OUT}/{name}.png"; chrome(hp, png, w, 1080); made.append(png); return png
    go("home-leaderboard-desktop", home_frame(1920, 32, 32, 32, 32))
    p169 = go("home-leaderboard-annotated-desktop", home_frame(1920, 32, 32, 32, 32, annotate=True))
    p43 = go("home-leaderboard-4x3", home_frame(1440, 32, 32, 32, 32, two_row=True, annotate=True), 1440)
    p209 = go("home-leaderboard-20x9", home_frame(2400, 132, 132, 0, 63, annotate=True, phone=True), 2400)
    aspects_sheet({"16x9": p169, "4x3": p43, "20x9": p209}); made.append(f"{OUT}/home-leaderboard-aspects-desktop.png")
    go("home-leaderboard-states-desktop", states_sheet())
    go("leaderboard-weekly-desktop", weekly_global())
    go("leaderboard-country-desktop", weekly_country())
    go("leaderboard-country-unavailable-desktop", country_unavailable("KE"))
    go("leaderboard-country-empty-states-desktop", empty_states())
    go("leaderboard-tabs-desktop", seg_options())
    return made

if __name__ == "__main__":
    man = sprites()
    print("manifest", merge(f"{U}/manifest.json", man))
    json.dump(man, open("/tmp/lbhome_manifest_entries.json", "w"), indent=1, ensure_ascii=False)
    for p in previews(): print(p, Image.open(p).size)
