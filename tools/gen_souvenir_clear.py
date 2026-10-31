"""GPP-SOUVENIR-CLEAR: Level Clear souvenir row (G-Prototype PR #139).
Exports the NEW pill + NEW row frame (1x/2x, PPU 100/200, 9-slice) into exports/unity/sprites@{1x,2x}/clear/,
upserts them into exports/unity/manifest.json (keeps every other entry), writes the preview mockups
(mockups/clear-souvenir-*.html) and renders them to exports/clear-souvenir-*.png with headless Chrome.
Layout numbers mirror LevelClearView (panel 1180 wide, row 150 high at y 374)."""
import os, json, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = f"{ROOT}/exports/unity"
GOLD, NAIRA, INK, TEAL, ORANGE, MUTED, MAIN = "#E8B21E", "#FAE69E", "#0F1219", "#59D9B8", "#FF7A1A", "#9EA3AD", "#F5F5F0"

def rgba(h, a=1.0):
    h = h.lstrip("#"); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(round(a * 255)))

def rrect(w, h, r, fill, edge=None, edge_w=0, inner_hi=None, scale=1):
    """Anti-aliased rounded rect: drawn at 8x then downsampled."""
    S = 8 * scale
    W, H, R, E = w * S, h * S, r * S, edge_w * S
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if edge:
        d.rounded_rectangle([0, 0, W - 1, H - 1], R, fill=edge)
        # punch the inside, then fill (so a translucent fill doesn't sit on top of the edge colour)
        inner = Image.new("RGBA", (W, H), (0, 0, 0, 0)); di = ImageDraw.Draw(inner)
        di.rounded_rectangle([E, E, W - 1 - E, H - 1 - E], max(R - E, 0), fill=(255, 255, 255, 255))
        mask = inner.split()[3]
        im.paste((0, 0, 0, 0), (0, 0), mask)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
        dl.rounded_rectangle([E, E, W - 1 - E, H - 1 - E], max(R - E, 0), fill=fill)
        im = Image.alpha_composite(im, layer)
    else:
        d.rounded_rectangle([0, 0, W - 1, H - 1], R, fill=fill)
    if inner_hi:  # 2 px light line just inside the top edge (bevel), clipped to the shape
        hi = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dh = ImageDraw.Draw(hi)
        dh.rounded_rectangle([E, E, W - 1 - E, H - 1 - E], max(R - E, 0), outline=inner_hi, width=2 * S)
        cut = Image.new("L", (W, H), 0); ImageDraw.Draw(cut).rectangle([0, 0, W, H // 2], fill=255)
        hi.putalpha(Image.composite(hi.split()[3], Image.new("L", (W, H), 0), cut))
        im = Image.alpha_composite(im, hi)
    return im.resize((w * scale, h * scale), Image.LANCZOS)

SPRITES = [
    dict(name="clear_pill_new", w=56, h=56, border=[28, 28, 28, 28],
         draw=lambda s: rrect(56, 56, 28, rgba(GOLD), rgba(NAIRA), 2, inner_hi=rgba("#FFFFFF", .35), scale=s),
         note="GPP-SOUVENIR-CLEAR. Level Clear NEW pill: Image Sliced 140x56 (stretch horizontally only), gold #E8B21E fill, 2 px #FAE69E rim. "
              "Child legacy Text 'NEW' 28 px #0F1219 Middle Center, no Shadow (solid fill, not glass). Shown only when LevelClearSouvenir.IsNew."),
    dict(name="clear_souvenir_frame_new", w=80, h=80, border=[32, 32, 32, 32],
         draw=lambda s: rrect(80, 80, 24, rgba(GOLD, .10), rgba(GOLD, .80), 2, scale=s),
         note="GPP-SOUVENIR-CLEAR. Souvenir row frame, NEW state: Image Sliced 1068x150, gold 10% fill + 2 px #E8B21E 80% edge, radius 24 (matches tile_stat). "
              "Already-owned state uses tile_stat_normal instead (no gold edge)."),
]

def export_sprites():
    entries = []
    for sp in SPRITES:
        for sc, folder in ((1, "sprites@1x"), (2, "sprites@2x")):
            os.makedirs(f"{U}/{folder}/clear", exist_ok=True)
            sp["draw"](sc).save(f"{U}/{folder}/clear/{sp['name']}.png")
        l, r, t, b = sp["border"]
        entries.append({"name": sp["name"], "file": f"sprites@1x/clear/{sp['name']}.png", "file2x": f"sprites@2x/clear/{sp['name']}.png",
                        "size": [sp["w"], sp["h"]], "pivot": [0.5, 0.5], "border": {"left": l, "right": r, "top": t, "bottom": b},
                        "pixelsPerUnit": 100, "pixelsPerUnit2x": 200, "screen": "clear", "note": sp["note"]})
    return entries

def upsert(manifest, entries):
    names = {e["name"] for e in entries}
    before = len(manifest["sprites"])
    manifest["sprites"] = [s for s in manifest["sprites"] if s["name"] not in names] + entries
    return before

def write_manifest(entries):
    """Text-level upsert: other generators write this file with different JSON encoders, so never re-serialise
    the whole file (that would rewrite their entries). Remove any old copy of our entries, append ours before the
    closing ']', and check nothing else changed."""
    p = f"{U}/manifest.json"
    raw = open(p, encoding="utf-8").read()
    before = json.loads(raw)
    mine = {e["name"] for e in entries}
    if any(s["name"] in mine for s in before["sprites"]):
        # drop our previous block (always written last by this script, between the markers below)
        raw = re.sub(r',\n  \{\n   "name": "clear_pill_new".*?(?=\n \]\n\}\s*$)', "", raw, flags=re.S)
    body = ",\n".join("  " + json.dumps(e, indent=1, ensure_ascii=False).replace("\n", "\n  ") for e in entries)
    i = raw.rstrip().rindex("]")
    head = raw[:i].rstrip()
    nl = "\n" if raw.endswith("\n") else ""  # keep the file's trailing-newline style
    raw = head + ",\n" + body + "\n ]\n}" + nl
    after = json.loads(raw)
    others_before = [s for s in before["sprites"] if s["name"] not in mine]
    others_after = [s for s in after["sprites"] if s["name"] not in mine]
    assert others_before == others_after, "would change other entries"
    open(p, "w", encoding="utf-8").write(raw)
    print(f"manifest: {len(before['sprites'])} -> {len(after['sprites'])} sprites")

# ---------------------------------------------------------------- mockups
SOUV = {1: "Agege Bread", 2: "Surulere Match Ticket", 3: "Ikorodu Road Sign", 4: "Mushin Market Basket", 5: "Oshodi Danfo Keyring",
        6: "Ikeja Along Phone Case", 7: "Ojota Park Flag", 8: "Third Mainland Lamp", 9: "Lekki Toll Card", 10: "Ojuelegba Under-bridge Sticker"}
ICON_MAP = '<svg viewBox="0 0 48 48" width="40" height="40"><path fill="none" stroke="#FAE69E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M6 12l11-4 14 4 11-4v28l-11 4-14-4-11 4z"/><path fill="none" stroke="#FAE69E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M17 8v28M31 12v28"/></svg>'
ICON_BAG = '<svg viewBox="0 0 48 48" width="40" height="40"><path fill="none" stroke="#FAE69E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M10 18h28l-3 22H13z"/><path fill="none" stroke="#FAE69E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M17 18v-4a7 7 0 0 1 14 0v4"/><path fill="none" stroke="#FAE69E" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M19 28h10"/></svg>'
ICON_PLAY = '<svg viewBox="0 0 48 48" width="40" height="40"><path fill="none" stroke="#F5F5F0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M15 9l24 15-24 15z"/></svg>'
SH = "text-shadow:0 2px 0 rgba(0,0,0,.5)"

def A(x, y, w, h, css="", inner=""):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{css}">{inner}</div>'

def panel(level, location, state, collected, next_label, saved, time, grant, ann=False):
    """state: new | owned | hidden. Coordinates = LevelClearView (panel-local, y down)."""
    W, inner = 1180, 1068; tw = (inner - 48) / 4
    H = 44 + 90 + 60 + 150 + 30 + (180 if state != "hidden" else 0) + 144 + 44
    o = []
    o.append(A(56, 44, inner, 90, f"font-size:72px;line-height:90px;color:{NAIRA};text-align:center;white-space:nowrap", f"{location} Cleared!"))
    o.append(A(56, 134, inner, 44, f"font-size:30px;line-height:44px;color:{MUTED};text-align:center", "We don reach! Everybody cross safe."))
    for i, (v, l) in enumerate([(saved, "Saved"), (time, "Time"), (grant, "Cash-out grant (chips)"), ('<span class="tbd" style="font-size:30px">TBD</span>', "Stars rule")]):
        o.append(A(56 + i * (tw + 16), 194, tw, 150, "background:rgba(255,255,255,.05);border-radius:24px",
                   A(22, 18, tw - 44, 62, f"font-size:46px;color:{NAIRA}", v) + A(22, 96, tw - 44, 36, f"font-size:22px;color:{MUTED};display:flex;align-items:flex-end", l)))
    y = 374
    if state != "hidden":
        new = state == "new"
        frame = (f"background:url(../exports/unity/sprites@2x/clear/clear_souvenir_frame_new.png);border-image:url(../exports/unity/sprites@2x/clear/clear_souvenir_frame_new.png) 64 fill / 32px stretch;"
                 if new else "border-image:url(../exports/unity/sprites@2x/common/panels/tile_stat_normal.png) 64 fill / 32px stretch;")
        tx = 166
        name_w = inner - tx - (24 + 140 + 24 if new else 24)
        kick = ("SOUVENIR FOUND", GOLD) if new else ("SOUVENIR", MUTED)
        sub = f"Added to Lagos collection · {collected}/10" if new else f"Lagos collection · {collected}/10"
        row = A(12, 12, 126, 126, "", f'<img src="../exports/unity/souvenirs/2x/souvenir_L{level:02d}.png" style="width:126px;height:126px">')
        row += A(tx, 20, name_w, 28, f"font-size:22px;line-height:28px;color:{kick[1]};letter-spacing:.08em", kick[0])
        row += A(tx, 50, name_w, 52, f"font-size:40px;line-height:52px;color:{NAIRA};white-space:nowrap;{SH}", SOUV[level])
        row += A(tx, 104, name_w, 28, f"font-size:22px;line-height:28px;color:{MUTED};{SH}", sub)
        if new:
            row += A(inner - 24 - 140, 47, 140, 56, "border-image:url(../exports/unity/sprites@2x/clear/clear_pill_new.png) 54 fill / 27px stretch;"
                     f"font-size:28px;line-height:56px;color:{INK};text-align:center", "NEW")
        if ann:
            row += A(tx, 50, name_w, 52, "outline:2px dashed rgba(89,217,184,.9)")
        o.append(A(56, y, inner, 150, ("" if new else "") + frame.replace("background:url(../exports/unity/sprites@2x/clear/clear_souvenir_frame_new.png);", ""), row))
        y += 180
    nextW = 520; mapW = W - 56 - nextW - 16 - 300 - 16 - 56
    btn = "border-radius:28px;display:flex;align-items:center;justify-content:center;gap:16px;white-space:nowrap"
    o.append(A(56, y, mapW, 144, f"background:rgba(15,18,25,.72);border:2px solid rgba(255,216,115,.28);font-size:34px;{btn}", ICON_MAP + " Map"))
    o.append(A(W - 56 - nextW - 16 - 300, y, 300, 144, f"background:rgba(15,18,25,.72);border:2px solid rgba(255,216,115,.28);font-size:34px;{btn}", ICON_BAG + " Base Camp"))
    o.append(A(W - 56 - nextW, y, nextW, 144, f"background:linear-gradient(180deg,#2E7A68,#18493F);border:3px solid rgba(255,216,115,.6);box-shadow:0 12px 40px rgba(0,0,0,.5);font-size:36px;{btn}", next_label + " " + ICON_PLAY))
    return W, H, "".join(o)

def page(kind, w, h, bg, pnl, extra=""):
    W, H, body = pnl
    safe = {"desktop": "--sl:32px;--sr:32px;--st:32px;--sb:32px", "phone": "--sl:132px;--sr:132px;--st:0px;--sb:63px", "tablet": "--sl:24px;--sr:24px;--st:24px;--sb:24px"}[kind]
    cls = "phone" if kind == "phone" else "desktop"
    deco = '<div class="notch"></div><div class="homebar"></div>' if kind == "phone" else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>Level clear souvenir {kind}</title>'
            f'<link rel="stylesheet" href="../css/hud.css"><link rel="stylesheet" href="../css/mock.css"><link rel="stylesheet" href="../css/more.css"></head>'
            f'<body style="width:{w}px;height:{h}px"><div class="frame {cls} realbg" style="width:{w}px;height:{h}px;{safe}"><img class="scene" src="../assets/bg/{bg}" alt="">{deco}'
            f'<div class="safe"><div class="ov"></div><div class="panel" style="width:{W}px;height:{H}px;padding:0;text-align:left">{body}</div>{extra}</div></div></body></html>')

def shoot(html_rel, out, w, h):
    subprocess.run(["bash", f"{ROOT}/tools/shoot.sh", f"{ROOT}/{html_rel}", out, str(w), str(h)], check=True)

def mockups():
    jobs = [
        ("clear-souvenir-new-desktop", "desktop", 1920, 1080, "L06_desktop_blur.png", panel(6, "Ikeja Along", "new", 6, "NEXT: L7 · Ojota Intersect", "7/7", "00:48", "+75")),
        ("clear-souvenir-owned-phone", "phone", 2340, 1080, "L05_phone_blur.png", panel(5, "Oshodi Expressway", "owned", 5, "NEXT: Stop 3 of 3", "6/6", "00:57", "+75")),
        ("clear-souvenir-new-4x3", "tablet", 1440, 1080, "L10_desktop_blur.png", panel(10, "Ojuelegba Chaos", "new", 10, "PLAY AGAIN", "8/8", "01:42", "+100", ann=True)),
        ("clear-souvenir-hidden-desktop", "desktop", 1920, 1080, "L06_desktop_blur.png", panel(6, "Ikeja Along", "hidden", 5, "NEXT: L7 · Ojota Intersect", "7/7", "00:48", "+75")),
    ]
    outs = []
    for name, kind, w, h, bg, pnl in jobs:
        rel = f"mockups/{name}.html"
        open(f"{ROOT}/{rel}", "w").write(page(kind, w, h, bg, pnl))
        out = f"{ROOT}/exports/{name}.png"; shoot(rel, out, w, h); outs.append(out)
    return outs

def sheet():
    """exports/clear-souvenir-preview.png: the four renders on one sheet."""
    F = ImageFont.truetype(f"{ROOT}/fonts/PlusJakartaSans-Bold.ttf", 30)
    ims = [("NEW: first clear after the find · 1920x1080", "new-desktop"), ("Owned: no NEW, quiet frame · phone 2340x1080", "owned-phone"),
           ("NEW, longest name · 4:3 1440x1080", "new-4x3"), ("Not earned: row hidden · 1920x1080", "hidden-desktop")]
    th = []
    for t, n in ims:
        im = Image.open(f"{ROOT}/exports/clear-souvenir-{n}.png").convert("RGB")
        th.append((t, im.resize((int(im.width * 540 / im.height), 540), Image.LANCZOS)))
    W = max(th[0][1].width + th[1][1].width, th[2][1].width + th[3][1].width) + 60
    sh = Image.new("RGB", (W, 2 * (540 + 60) + 20), (15, 18, 25)); d = ImageDraw.Draw(sh)
    pos = [(20, 15), (40 + th[0][1].width, 15), (20, 630), (40 + th[2][1].width, 630)]
    for (t, im), (x, y) in zip(th, pos):
        d.text((x, y), t, font=F, fill=(250, 230, 158)); sh.paste(im, (x, y + 45))
    sh.save(f"{ROOT}/exports/clear-souvenir-preview.png")

if __name__ == "__main__":
    entries = export_sprites()
    if "--no-manifest" not in sys.argv:
        write_manifest(entries)
    json.dump(entries, open("/tmp/gpp_souvenir_entries.json", "w"), indent=1)
    for o in mockups(): print("rendered", o)
    sheet()
