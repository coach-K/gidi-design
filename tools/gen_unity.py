"""Unity-ready sprite export (Home, Base Camp Shop, Game Over, in-run HUD).
Renders every sprite on one transparent HTML sheet with headless Chrome at 1x and 2x, then crops.
Output: exports/unity/{sprites@1x,sprites@2x,backgrounds,svg}/..., manifest.json. README is hand-written."""
import os, sys, json, re, shutil, subprocess
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import dpad_svg
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = f"{ROOT}/exports/unity"
GOLD, NAIRA, INK, TEAL = "#E8B21E", "#FAE69E", "#0F1219", "#59D9B8"
S = []   # sprites: dict(name, folder, w, h, html, pivot, border, screen, note)

def add(name, folder, w, h, html, screen, border=None, pivot=(0.5, 0.5), note=""):
    S.append(dict(name=name, folder=folder, w=w, h=h, html=html, screen=screen, border=border, pivot=pivot, note=note))

def box(w, h, css, pad=0):
    return f'<div style="position:absolute;left:{pad}px;top:{pad}px;width:{w-2*pad}px;height:{h-2*pad}px;box-sizing:border-box;{css}"></div>'

GLASS = "background:rgba(15,18,25,.72);border:2px solid rgba(255,216,115,.28)"
GLASS_P = "background:rgba(8,10,14,.86);border:2px solid rgba(255,216,115,.60)"
GLASS_D = "background:rgba(42,45,54,.55);border:2px solid rgba(158,163,173,.30)"
CTA = "background:linear-gradient(180deg,#2E7A68,#18493F);border:3px solid rgba(255,216,115,.6)"
CTA_P = "background:linear-gradient(180deg,#225C4F,#10342D);border:3px solid rgba(255,216,115,.9)"
CTA_D = "background:linear-gradient(180deg,#3A3D46,#2A2D36);border:3px solid rgba(158,163,173,.35)"
BUY = "background:#18493F;border:2px solid rgba(255,216,115,.5)"
BUY_P = "background:#10342D;border:2px solid rgba(255,216,115,.85)"
BUY_D = "background:#2a2d36;border:2px solid rgba(158,163,173,.35)"
BUY_L = "background:#1a1c22;border:2px solid rgba(158,163,173,.25)"
HI = "box-shadow:0 0 0 6px rgba(232,178,30,.40),0 0 22px 6px rgba(232,178,30,.50)"
G = 24  # glow padding

def nine(name, folder, screen, size, radius, states, note=""):
    w, h = size; b = radius + 8
    for st, css in states.items():
        if st == "highlight":
            add(f"{name}_highlight", folder, w+2*G, h+2*G, box(w+2*G, h+2*G, f"{css};border-radius:{radius}px;{HI}", G), screen, [b+G]*4, note=note+" Highlight: glow baked into a 24 px transparent margin (border values include it).")
        else:
            add(f"{name}_{st}", folder, w, h, box(w, h, f"{css};border-radius:{radius}px"), screen, [b]*4, note=note)

# ---------- shared glass panels (9-slice) ----------
nine("panel_glass", "common/panels", "all", (96, 96), 28, {"normal": GLASS}, "HUD dusk-glass panel: level card 400×144, stock panel, chips, lives, toasts, endless strip, shop item card, IAP card.")
nine("panel_levelcard", "hud", "hud", (96, 96), 28, {"normal": "background:rgba(15,18,25,.82);border:2px solid #E8B21E"}, "HUD level card (PR #59): 82% glass, 2 px gold outline baked.")
nine("panel_modal", "common/panels", "gameover,pause", (112, 112), 40, {"normal": "background:rgba(10,12,18,.88);border:2px solid rgba(255,216,115,.28)"}, "Modal panel (Game Over 1240 wide).")
nine("tile_stat", "common/panels", "gameover,shop", (80, 80), 24, {"normal": "background:rgba(255,255,255,.05)"}, "Stat tile / shop icon tile (Game Over stats, item icon well 110×110).")
nine("divider_cell", "hud", "hud", (4, 96), 0, {"normal": "background:rgba(255,216,115,.18)"}, "Stock-panel cell divider (stretch vertically).")
# ---------- buttons (9-slice, no text: use TextMeshPro) ----------
nine("btn_glass", "common/buttons", "all", (96, 96), 28, {"normal": GLASS, "pressed": GLASS_P, "disabled": GLASS_D, "highlight": GLASS}, "Glass button: Stats/Pause 144×144, Home big buttons 560×144, Game Over secondary 160 high, Back.")
nine("btn_cta", "common/buttons", "home,gameover,shop", (112, 112), 32, {"normal": CTA, "pressed": CTA_P, "disabled": CTA_D, "highlight": CTA}, "Primary CTA (Home PLAY 560×192, Game Over 160 high, pause CONTINUE 144 high).")
nine("btn_buy", "shop/buttons", "shop", (80, 80), 24, {"normal": BUY, "pressed": BUY_P, "disabled": BUY_D, "highlight": BUY}, "Shop Buy button 150×144 (sm2 144×144). Disabled = 'Bag full' / 'used, cash out to refresh'.")
nine("btn_buy_locked", "shop/buttons", "shop", (80, 80), 24, {"normal": BUY_L}, "Shop locked state (unlocks at Lx).")
nine("btn_buy_full", "shop/buttons", "shop", (80, 80), 24, {"normal": BUY_D}, "Shop 'Bag full' / 'used, cash out to refresh' (same look as btn_buy_disabled, own name for code).")
nine("btn_buy_locked", "shop/buttons", "shop", (80, 80), 24, {"pressed": "background:#121318;border:2px solid rgba(158,163,173,.45)"}, "Locked buy pressed (tap shows 'Opens Lx' / 'Coming soon' toast).")
# (a) locked / coming-soon tile
nine("tile_soon", "shop/tiles", "shop", (96, 96), 28, {"normal": "background:rgba(15,18,25,.58);border:2px solid rgba(158,163,173,.30)"}, "Coming-soon tile (Danfo Ride, Gist Bomb): icon + text at 55% alpha, ribbon top-left (22 px in), price box right.")
nine("btn_soon_price", "shop/tiles", "shop", (80, 80), 24, {"normal": "background:#1a1c22;border:2px solid rgba(158,163,173,.35)"}, "Coming-soon price box 150×144: icon_lock_white tinted #9EA3AD (28 px) above TMP price (32 px, #F5F5F0). Not interactive.")
add("ribbon_coming_soon", "shop/tiles", 64, 30, box(64, 30, "background:#E8B21E;border-radius:0 0 10px 10px"), "shop", [12, 12, 0, 12], (0, 1), "Ribbon base (9-slice, stretch to text width + 24). Text: TMP 'COMING SOON' 17 px, #0F1219, tracking 10%.")
add("ribbon_coming_soon_text", "shop/tiles", 176, 30, '<div style="width:176px;height:30px;background:#E8B21E;border-radius:0 0 10px 10px;color:#0F1219;font:700 17px Jakarta,sans-serif;letter-spacing:.1em;display:flex;align-items:center;justify-content:center">COMING SOON</div>', "shop", None, (0, 1), "Ribbon with baked text (if you don't want TMP).")
# (b) not-for-sale info tile
add("tile_info", "shop/tiles", 120, 120, '<svg width="120" height="120"><rect x="1" y="1" width="118" height="118" rx="28" fill="rgba(15,18,25,.50)" stroke="rgba(89,217,184,.65)" stroke-width="2" stroke-dasharray="8 6"/></svg>', "shop", [36, 36, 36, 36], note="Not-for-sale info tile (Agbada Armour, Okada Dash): dashed teal border, no buy button. Use Image Type Sliced; dashes on the stretched edges lengthen slightly (or use Tiled).")
add("tag_info", "shop/tiles", 64, 48, box(64, 48, "border-radius:24px;background:rgba(89,217,184,.10);border:2px solid rgba(89,217,184,.7)"), "shop", [24, 24, 22, 22], note="Info tag pill ('EARNED' / 'CURB PICKUP'): TMP 20 px, #59D9B8, tracking 8%, padding 16 px.")
add("tag_info_earned", "shop/tiles", 136, 48, '<div style="width:136px;height:48px;box-sizing:border-box;border-radius:24px;background:rgba(89,217,184,.10);border:2px solid rgba(89,217,184,.7);color:#59D9B8;font:700 20px Jakarta,sans-serif;letter-spacing:.08em;display:flex;align-items:center;justify-content:center">EARNED</div>', "shop", note="Baked-text variant.")
add("tag_info_curb_pickup", "shop/tiles", 200, 48, '<div style="width:200px;height:48px;box-sizing:border-box;border-radius:24px;background:rgba(89,217,184,.10);border:2px solid rgba(89,217,184,.7);color:#59D9B8;font:700 20px Jakarta,sans-serif;letter-spacing:.08em;display:flex;align-items:center;justify-content:center">CURB PICKUP</div>', "shop", note="Baked-text variant.")
nine("badge_rating", "home", "home", (48, 48), 12, {"normal": "border:3px solid #F5F5F0"}, "Age-rating outline box (Home).")

# ---------- toasts, telegraph pills, power-up timer ring ----------
add("panel_toast_normal", "hud", 96, 72, box(96, 72, "border-radius:36px;background:rgba(10,12,18,.86);border:2px solid rgba(255,216,115,.40)"), "hud", [36, 36, 36, 36], note="Toast pill (fixed height 72; no vertical stretch centre, stretch horizontally only).")
add("panel_tele_pill_normal", "hud", 56, 56, box(56, 56, "border-radius:28px;background:rgba(15,18,25,.78)"), "hud", [28, 28, 28, 28], note="World-telegraph pill, ink 78%, no border (fixed height 56; stretch horizontally only). Add the state outline/icon in code.")
add("ring_powerup_timer_track", "hud", 170, 170, '<svg viewBox="0 0 170 170" width="170" height="170"><circle cx="85" cy="85" r="75" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="10"/></svg>', "hud", note="Power-up timer track (PowerUpRings): r 75, 10 px stroke, white 15%. Badge 140 sits centred on top.")
add("ring_powerup_timer_fill", "hud", 170, 170, '<svg viewBox="0 0 170 170" width="170" height="170"><circle cx="85" cy="85" r="75" fill="none" stroke="#FFFFFF" stroke-width="10"/></svg>', "hud", note="Pure white ring, same geometry. Image Type Filled, Radial 360, origin Top, clockwise; tint #E8B21E (mockup) via Image.color; fillAmount = time left (Malta: 4 s).")

# ---------- PICK UP + OWA! ----------
add("pickup_disc", "hud/pickup", 216, 216, box(216, 216, "border-radius:50%;background:radial-gradient(circle,rgba(232,178,30,.30),rgba(232,178,30,.16) 70%)"), "hud", note="Fill only. Label '+ / PICK UP' is TMP text (44/26 px, #FFECBE at 95%).")
add("pickup_outline", "hud/pickup", 216, 216, box(216, 216, "border-radius:50%;border:6px solid rgba(232,178,30,.88)"), "hud")
add("pickup_pressed", "hud/pickup", 216, 216, box(216, 216, "border-radius:50%;background:rgba(232,178,30,.45)"), "hud", note="Overlay on top of the disc while held.")
add("pickup_disabled", "hud/pickup", 216, 216, box(216, 216, "border-radius:50%;background:rgba(40,40,48,.30);border:6px solid rgba(160,160,160,.55)"), "hud", note="Replaces disc+outline when nothing to pick up (optional).")
O = 144  # OWA canvas = touch target; disc 120 centred
add("owa_disc", "hud/owa", O, O, box(O, O, "border-radius:50%;background:radial-gradient(circle,rgba(40,32,14,.42),rgba(15,18,25,.30) 70%)", 12), "hud", note="144×144 canvas = touch target; visible disc 120 Ø centred.")
add("owa_outline", "hud/owa", O, O, box(O, O, "border-radius:50%;border:5px solid rgba(232,178,30,.88)", 12), "hud")
add("owa_disabled", "hud/owa", O, O, box(O, O, "border-radius:50%;background:rgba(40,40,48,.28);border:5px solid rgba(160,160,160,.55)", 12), "hud", note="Replaces disc+outline at 0 charges; label colour rgba(200,200,200,.6).")
add("owa_glow", "hud/owa", O+2*G, O+2*G, box(O+2*G, O+2*G, f"border-radius:50%;{HI}", G+12), "hud", note="Highlight layer behind the disc (unlock / tutorial / toast).")
add("owa_pressed", "hud/owa", O, O, box(O, O, "border-radius:50%;background:rgba(232,178,30,.35)", 12), "hud")
add("pip_empty", "hud/owa", 18, 18, box(18, 18, "border-radius:50%;background:rgba(20,22,30,.55);border:2px solid rgba(255,236,190,.55)"), "hud", note="OWA! pip base (18 Ø, 7 px gap).")
add("pip_filled", "hud/owa", 18, 18, box(18, 18, f"border-radius:50%;background:{TEAL};border:2px solid {TEAL}"), "hud")
add("pip_partial_fill", "hud/owa", 18, 18, box(18, 18, f"border-radius:50%;background:{TEAL}"), "hud", note="Image Type Filled, Radial 360, origin Top, clockwise; fillAmount = refill progress. Draw over pip_empty + pip_partial_ring.")
add("pip_partial_ring", "hud/owa", 18, 18, box(18, 18, f"border-radius:50%;border:2px solid {TEAL}"), "hud")
add("pip_partial_example", "hud/owa", 18, 18, box(18, 18, f"border-radius:50%;background:conic-gradient({TEAL} 50%,rgba(20,22,30,.55) 0);border:2px solid {TEAL}"), "hud", note="Reference only (50%).")
add("stock_pip_on", "hud", 24, 24, box(24, 24, f"border-radius:50%;background:{TEAL};border:2px solid {TEAL}"), "hud", note="GROUP/CHANGE pips 24 Ø, 10 px gap.")
add("stock_pip_off", "hud", 24, 24, box(24, 24, "border-radius:50%;background:#333846;border:2px solid #555"), "hud")

# ---------- D-pad (360 canvas; every arrow sprite shares the base rect, pivot centre) ----------
svg = dpad_svg(180)
base = re.sub(r'<g fill=.*?</g></g>', '', svg); base = re.sub(r'<g fill="rgba\(226.*', '', svg)
add("dpad_base", "hud/dpad", 360, 360, '<svg viewBox="-180 -180 360 360" width="360" height="360"><circle r="176" fill="rgba(255,255,255,.07)" stroke="rgba(255,255,255,.14)" stroke-width="3"/><circle r="24" fill="rgba(30,30,30,.35)"/></svg>', "hud", note="Base circle + centre dot. 360 Ø at 1x desktop/phone (radius 16.7% H); tablet 324.")
for i, d in enumerate(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]):
    for st, fill, stroke in (("normal", "rgba(226,196,128,.62)", "rgba(120,90,30,.35)"), ("pressed", "rgba(250,230,158,.95)", "rgba(232,178,30,.9)")):
        add(f"dpad_arrow_{d}_{st}", "hud/dpad", 360, 360, f'<svg viewBox="-180 -180 360 360" width="360" height="360"><g fill="{fill}" stroke="{stroke}" stroke-width="2" transform="rotate({i*45})"><rect x="-17" y="-128" width="34" height="58" rx="4"/><path d="M-44 -124 L0 -168 L44 -124 Z"/></g></svg>', "hud", note="Full 360 canvas so it stacks on dpad_base with the same RectTransform.")

# ---------- leaderboards (RT-109) ----------
nine("lb_row", "leaderboard", "leaderboard", (80, 80), 22, {"normal": "background:rgba(255,255,255,.045)",
     "top1": "background:rgba(232,178,30,.18);border:2px solid rgba(232,178,30,.55)", "top2": "background:rgba(201,207,217,.14);border:2px solid rgba(201,207,217,.45)",
     "top3": "background:rgba(200,116,58,.18);border:2px solid rgba(200,116,58,.55)", "you": "background:rgba(15,18,25,.92);border:3px solid #E8B21E"},
     "Leaderboard row, 84 px high (stretch horizontally). top1/2/3 = podium tint + outline; you = pinned player row (also used inline when the player is in view).")
nine("tab_level", "leaderboard", "leaderboard", (96, 96), 28, {"off": GLASS, "on": "background:#E8B21E;border:2px solid #E8B21E", "pressed": GLASS_P},
     "Level tab ≈163×144 desktop / ≈185×144 phone (flex, 8 px gaps). TMP 'L4' 44 px + short name 18 px; on = ink text #0F1219.")
nine("seg_filter", "leaderboard", "leaderboard", (80, 80), 28, {"off": "background:rgba(255,255,255,.04);border:2px solid rgba(255,216,115,.28)", "on": "background:rgba(232,178,30,.16);border:3px solid #E8B21E"},
     "Global / Friends segmented button, 192×144 each, 8 px gap. Icon 40 + TMP 28 px.")
_MS = {1: '<path d="M32 2l7.6 11.7 13.6-3-3 13.6L62 32l-11.7 7.6 3 13.6-13.6-3L32 62l-7.6-11.7-13.6 3 3-13.6L2 32l11.7-7.6-3-13.6 13.6 3z"/>',
       2: '<path d="M32 3l25 14.5v29L32 61 7 46.5v-29z"/>', 3: '<circle cx="32" cy="32" r="28"/>'}
_MC = {1: ("#E8B21E", "#7A5A00", "gold, 8-point star"), 2: ("#C9CFD9", "#5B6270", "silver, hexagon"), 3: ("#C8743A", "#5E3014", "bronze, circle")}
for _n in (1, 2, 3):
    f_, s_, d_ = _MC[_n]
    add(f"badge_rank_{_n}", "leaderboard", 64, 64, f'<svg viewBox="0 0 64 64" width="64" height="64"><g fill="{f_}" stroke="{s_}" stroke-width="3">{_MS[_n]}</g></svg>', "leaderboard", note=f"Rank {_n} badge ({d_}); add TMP '{_n}' 28 px #0F1219 centred. Shape differs per rank so it never relies on colour.")
    add(f"badge_rank_{_n}_text", "leaderboard", 64, 64, f'<svg viewBox="0 0 64 64" width="64" height="64"><g fill="{f_}" stroke="{s_}" stroke-width="3">{_MS[_n]}</g><text x="32" y="42" text-anchor="middle" font-family="Jakarta" font-weight="700" font-size="28" fill="#0F1219">{_n}</text></svg>', "leaderboard", note="Baked-number variant.")
add("avatar_mask", "leaderboard", 64, 64, box(64, 64, "border-radius:50%;background:#fff"), "leaderboard", note="Circle mask for player avatars (60 px in rows). Placeholder = this tinted with an Okabe-Ito colour + 2 initials TMP 24 px.")
add("avatar_ring", "leaderboard", 64, 64, box(64, 64, "border-radius:50%;border:3px solid rgba(245,245,240,.85)"), "leaderboard", note="Avatar outline, on top of the masked image.")
add("tag_you", "leaderboard", 40, 28, box(40, 28, "border-radius:10px;background:#E8B21E"), "leaderboard", [10, 10, 10, 10], note="'YOU' tag behind TMP 18 px #0F1219, padding 10 px.")
add("skeleton_bar", "leaderboard", 40, 18, box(40, 18, "border-radius:9px;background:rgba(255,255,255,.12)"), "leaderboard", [9, 9, 9, 9], note="Loading placeholder line (stretch). Pulse alpha .6→1, 900 ms.")
add("skeleton_row", "leaderboard", 64, 56, box(64, 56, "border-radius:18px;background:rgba(255,255,255,.07)"), "leaderboard", [20, 20, 20, 20], note="Loading row base; add the moving shimmer in code (or skip if Reduce motion).")
add("spinner_arc", "leaderboard", 72, 72, '<svg viewBox="0 0 72 72" width="72" height="72"><circle cx="36" cy="36" r="30" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="8"/><path d="M36 6a30 30 0 0 1 30 30" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/></svg>', "leaderboard", note="Spinner: rotate 360°/1 s; tint the arc #E8B21E.")

# ---------- bag (GPP-021) ----------
nine("bag_slot", "hud/bag", "hud,shop,intro", (96, 96), 28, {"normal": GLASS, "pressed": GLASS_P, "full": "background:rgba(15,18,25,.72);border:3px solid #FF7A1A",
     "active": "background:rgba(15,18,25,.72);border:3px solid #E8B21E"}, "Bag slot frame 144×144 HUD (120×120 Base Camp strip). Badge 96 centred (84 while active, inside the timer ring).")
add("bag_slot_empty", "hud/bag", 144, 144, '<svg width="144" height="144"><rect x="1" y="1" width="142" height="142" rx="28" fill="rgba(15,18,25,.45)" stroke="rgba(255,236,190,.35)" stroke-width="2" stroke-dasharray="10 8"/><path d="M72 56v32M56 72h32" stroke="rgba(255,236,190,.35)" stroke-width="4" stroke-linecap="round"/></svg>', "hud", note="Empty slot (not 9-slice, use at 144 or 120). Not tappable.")
add("bag_overlay_active_glow", "hud/bag", 144+2*G, 144+2*G, box(144+2*G, 144+2*G, f"border-radius:28px;{HI}", G), "hud", [28+G]*4, note="Active/running glow, 24 px margin. Ring: reuse ring_powerup_timer_track + ring_powerup_timer_fill scaled to 124 (r 59).")
add("bag_overlay_cooldown", "hud/bag", 144, 144, box(144, 144, "border-radius:28px;background:#FFFFFF"), "hud", note="White rounded square: Image Type Filled, Radial 360, origin Top, clockwise, fillAmount = cooldown left; tint #0A0C12 @66%. TMP seconds 22 px bottom.")
add("bag_overlay_disabled", "hud/bag", 144, 144, box(144, 144, "border-radius:28px;background:rgba(42,45,54,.6)"), "hud", note="Disabled (used this level / not usable now): over a greyscale badge at 50% alpha; reason label TMP 18 px #9EA3AD under the slot.")
add("bag_count_badge", "hud/bag", 44, 44, box(44, 44, "border-radius:22px;background:#E8B21E;border:2px solid #0F1219"), "hud,shop", [22, 22, 22, 22], note="Count pill ×N (N ≥ 2; OWA always), top-right at (−8, −8) outside the slot. TMP 24 px #0F1219, stretch horizontally.")

# ---------- icons from SVG ----------
ISV = f"{ROOT}/icons/svg"
def inline(path, color, size):
    t = open(path).read()
    t = re.sub(r'<svg', f'<svg width="{size}" height="{size}" style="color:{color}"', t, 1)
    t = re.sub(r'\swidth="\d+"\s+height="\d+"(?=[^>]*width=)', '', t, 1)
    return t
for f in sorted(os.listdir(ISV)):
    n = f[:-4]
    if n.startswith("badge_"): add(n, "icons/powerup_badges", 140, 140, inline(f"{ISV}/{f}", NAIRA, 140), "hud,shop", note=("Earned only (fill the Owa meter), NOT a shop item." if "agbada" in n else "Curb pickup only, NOT a shop item." if "okada" in n else "Coming soon in the shop (locked tile, price shown)." if n[6:] in ("danfo_ride","gist_bomb") else "Power-up badge (Base Camp tiles, HUD timer ring, curb pickups)."))
    elif n.startswith("warn_"): add(n, "icons/warnings", 64, 64, inline(f"{ISV}/{f}", NAIRA, 64), "hud", note="Warning shape; keeps its state colour. Telegraph pill = panel_glass + 3 px outline in the state colour.")
    elif n.startswith("iap_"):
        add(n, "icons/iap", 64, 64, inline(f"{ISV}/{f}", NAIRA, 64), "shop", note="IAP row icon (Fits & Extras).")
    else:
        grp = "powerups" if n in ("owa","maltina_gala","pure_water","bribe_change","siren","danfo_ride","gist_bomb","agbada_armour","okada_dash") else "pickups" if n.startswith("pickup") or n in ("group","change") else "ui"
        add(f"icon_{n}", f"icons/{grp}", 64, 64, inline(f"{ISV}/{f}", NAIRA, 64), "all", note=("Earned only, NOT a shop item. " if n=="agbada_armour" else "Curb pickup only, NOT a shop item. " if n=="okada_dash" else "Game Over 'TRY AM AGAIN'. " if n=="retry" else "")+"Line icon, Naira gold #FAE69E baked.")
        add(f"icon_{n}_white", f"icons/{grp}/white", 64, 64, inline(f"{ISV}/{f}", "#FFFFFF", 64), "all", note="White version for Image.color tinting (accents keep their colour).")
# ---------- logos ----------
for n, w in (("wordmark_dark", 720), ("wordmark_light", 720), ("lockup_tagline_dark", 720), ("mark", 256)):
    p = f"{ROOT}/logos/{n}.svg"
    if os.path.exists(p):
        im = re.search(r'viewBox="([\d.\s-]+)"', open(p).read()).group(1).split()
        h = round(w * float(im[3]) / float(im[2]))
        add(f"logo_{n}", "logos", w, h, f'<img src="file://{p}" width="{w}" height="{h}">', "home", note="From logos/*.svg (kept in exports/unity/svg/logos).")

def render():
    PAD = 6; X = Y = 0; rowh = 0; MAXW = 2400
    for s in S:
        if X + s["w"] + PAD > MAXW: X = 0; Y += rowh + PAD; rowh = 0
        s["x"], s["y"] = X, Y; X += s["w"] + PAD; rowh = max(rowh, s["h"])
    H = Y + rowh
    body = "".join(f'<div style="position:absolute;left:{s["x"]}px;top:{s["y"]}px;width:{s["w"]}px;height:{s["h"]}px;overflow:visible">{s["html"]}</div>' for s in S)
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>@font-face{{font-family:Jakarta;src:url(file://{ROOT}/fonts/PlusJakartaSans-Bold.ttf)}}html,body{{margin:0;background:transparent}}*{{box-sizing:border-box}}</style></head><body style="width:{MAXW}px;height:{H}px;position:relative">{body}</body></html>'
    p = "/tmp/unity_sheet.html"; open(p, "w").write(html)
    for sc in (1, 2):
        out = f"/tmp/unity_sheet@{sc}.png"
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={sc}",
                        "--default-background-color=00000000", f"--window-size={MAXW},{H+300}", f"--screenshot={out}", f"file://{p}"], stderr=subprocess.DEVNULL)
        sheet = Image.open(out).convert("RGBA")
        for s in S:
            d = f"{U}/sprites@{sc}x/{s['folder']}"; os.makedirs(d, exist_ok=True)
            sheet.crop((s["x"]*sc, s["y"]*sc, (s["x"]+s["w"])*sc, (s["y"]+s["h"])*sc)).save(f"{d}/{s['name']}.png")

def backgrounds():
    d = f"{U}/backgrounds"; os.makedirs(d, exist_ok=True); out = []
    top, mid, bot = (43,47,92,.55), (242,140,75,.18), (15,18,25,.55)
    for scr in ("home", "shop", "gameover", "hud"):
        for dev in ("desktop", "phone"):
            im = Image.open(f"{ROOT}/assets/bg/lv_{scr}_{dev}.png").convert("RGB"); w, h = im.size
            if scr != "hud":   # bake the .grade overlay used by the menu mockups
                ov = Image.new("RGBA", (w, h)); px = ov.load()
                for y in range(h):
                    t = y / h
                    a, b, k = (top, mid, t/.55) if t < .55 else (mid, bot, (t-.55)/.45)
                    c = tuple(round(a[i]+(b[i]-a[i])*k) for i in range(3)) + (round(255*(a[3]+(b[3]-a[3])*k)),)
                    for x in range(w): px[x, y] = c
                im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
            n = f"bg_{scr}_{dev}"; im.save(f"{d}/{n}.png"); im.filter(ImageFilter.GaussianBlur(18)).save(f"{d}/{n}_blur.png")
            out += [dict(name=n, file=f"backgrounds/{n}.png", size=[w, h], pivot=[.5, .5], border=None, screen=scr),
                    dict(name=n+"_blur", file=f"backgrounds/{n}_blur.png", size=[w, h], pivot=[.5, .5], border=None, screen=scr)]
    return out

if __name__ == "__main__":
    for sub in ("sprites@1x", "sprites@2x"): shutil.rmtree(f"{U}/{sub}", ignore_errors=True)
    render()
    sv = f"{U}/svg"; shutil.rmtree(sv, ignore_errors=True); shutil.copytree(ISV, f"{sv}/icons")
    os.makedirs(f"{sv}/logos", exist_ok=True)
    for f in os.listdir(f"{ROOT}/logos"):
        if f.endswith(".svg"): shutil.copy(f"{ROOT}/logos/{f}", f"{sv}/logos/{f}")
    man = [dict(name=s["name"], file=f"sprites@1x/{s['folder']}/{s['name']}.png", file2x=f"sprites@2x/{s['folder']}/{s['name']}.png",
                size=[s["w"], s["h"]], pivot=list(s["pivot"]), border=(dict(zip(("left","right","top","bottom"), s["border"])) if s["border"] else None),
                screen=s["screen"], note=s["note"]) for s in S]
    man += backgrounds()
    # keep entries written by other generators (splash/map, souvenirs, bag): replace only the ones produced here
    mine = {m["name"] for m in man}
    if os.path.exists(f"{U}/manifest.json"):
        prev = json.load(open(f"{U}/manifest.json"))["sprites"]
        order = [m["name"] for m in prev]; byname = {m["name"]: m for m in man}
        man = [byname.get(m["name"], m) if m.get("file", "").startswith(("sprites@", "backgrounds/")) else m for m in prev] + [m for m in man if m["name"] not in set(order)]
    json.dump(dict(reference="1920x1080, CanvasScaler match height 1.0", pixelsPerUnit=100, borderUnits="px at 1x (double for @2x)", sprites=man),
              open(f"{U}/manifest.json", "w"), indent=1, ensure_ascii=False)
    print(len(S), "sprites x2 +", len(man)-len(S), "backgrounds")
