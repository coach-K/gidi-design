"""GPP-SETTINGS: Unity sprites for the Settings screen (slider, toggle, segment, tab, danger button).
Renders one transparent HTML sheet with headless Chrome at 1x and 2x, crops each sprite, and MERGES the
entries into exports/unity/manifest.json (replaces only names made here, appends new ones, keeps the rest).
Output lives in exports/unity/settings/sprites@{1x,2x}/ so tools/gen_unity.py (which wipes
exports/unity/sprites@*) never deletes it. Spec: exports/unity/settings/README.md."""
import os, json, subprocess
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = f"{ROOT}/exports/unity"
OUT = "settings"
TEAL, GOLD, WARN, INK, TRACK, MUTED, CREAM = "#59D9B8", "#E8B21E", "#FF7A1A", "#0F1219", "#333846", "#9EA3AD", "#F5F5F0"
S = []

def add(name, w, h, html, border=None, pivot=(0.5, 0.5), note=""):
    S.append(dict(name=name, w=w, h=h, html=html, border=border, pivot=pivot, note=note))

def div(w, h, css, x=0, y=0):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;{css}"></div>'

# ---------- slider (track 16 high, knob 56 Ø) ----------
add("settings_slider_track", 48, 16, div(48, 16, f"border-radius:8px;background:{TRACK};border:1px solid rgba(255,255,255,.08)"),
    [8, 8, 0, 0], note="Slider background, 520×16 desktop (400×16 when safe aspect < 1.5). Sliced, horizontal stretch only.")
add("settings_slider_fill", 48, 16, div(48, 16, f"border-radius:8px;background:{TEAL}"),
    [8, 8, 0, 0], note="Slider fill (teal accent), Image Type Sliced in the Slider's Fill Area. Hide the fill Image at value 0 so the 16 px cap never shows.")
add("settings_slider_knob", 80, 80,
    div(56, 56, f"border-radius:50%;background:{CREAM};box-shadow:0 4px 12px rgba(0,0,0,.5)", 12, 12) +
    div(16, 16, f"border-radius:50%;background:{TEAL}", 32, 32),
    note="Slider handle: 56 Ø knob centred on an 80×80 canvas (12 px shadow margin baked). Handle RectTransform 80×80, Simple, not sliced. Scale 1.1 while dragging.")
# ---------- toggle (132×72, knob 56, inset 8). Full-state sprites, not sliced (the knob is baked). ----------
add("settings_toggle_off", 132, 72,
    div(132, 72, f"border-radius:36px;background:{TRACK};border:2px solid rgba(255,255,255,.10)") +
    div(56, 56, f"border-radius:50%;background:{MUTED}", 8, 8),
    note="Toggle OFF: grey track, grey knob left. Swap sprite on state (Image Simple, 132×72, preserve aspect). Not 9-slice.")
add("settings_toggle_on", 132, 72,
    div(132, 72, f"border-radius:36px;background:rgba(89,217,184,.32);border:2px solid {TEAL}") +
    div(56, 56, f"border-radius:50%;background:{CREAM};box-shadow:0 2px 6px rgba(0,0,0,.35)", 68, 8) +
    '<svg style="position:absolute;left:68px;top:8px" width="56" height="56" viewBox="0 0 56 56"><path d="M17 29l7 7 15-16" fill="none" stroke="#1E6E5C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    note="Toggle ON: teal track + teal edge, cream knob right with a check (position + check = state, never colour alone). Not 9-slice.")
# ---------- segment (96 high; S/M/L 120 each, language stepper 120/360/120) ----------
EDGE, DIV = "rgba(255,216,115,.30)", "rgba(255,216,115,.18)"
for st, fill, edge, dv in (("normal", "rgba(255,255,255,.04)", EDGE, DIV), ("selected", TEAL, TEAL, TEAL)):
    add(f"settings_seg_left_{st}", 64, 96, div(64, 96, f"border-radius:22px 0 0 22px;background:{fill};border:2px solid {edge};border-right:none"),
        [24, 4, 24, 24], note=f"Segment left piece ({st}). Text 28 px, {'#0F1219 on teal' if st=='selected' else '#9EA3AD'}.")
    add(f"settings_seg_mid_{st}", 64, 96, div(64, 96, f"background:{fill};border-top:2px solid {edge};border-bottom:2px solid {edge};border-left:2px solid {dv}"),
        [4, 4, 4, 4], note=f"Segment middle piece ({st}); 2 px divider baked on its left edge.")
    add(f"settings_seg_right_{st}", 64, 96, div(64, 96, f"border-radius:0 22px 22px 0;background:{fill};border:2px solid {edge};border-left:2px solid {dv}"),
        [4, 24, 24, 24], note=f"Segment right piece ({st}); 2 px divider baked on its left edge.")
# ---------- tab rail (308×120 tabs) ----------
add("settings_tab_normal", 96, 96, div(96, 96, "border-radius:22px;background:rgba(255,255,255,.03)"), [30, 30, 30, 30],
    note="Tab, not selected. Label Text 30 px #9EA3AD. Pressed: Button ColorTint pressed #C8C8C8.")
add("settings_tab_selected", 96, 96, div(96, 96, "border-radius:22px;background:rgba(232,178,30,.15);border:2px solid rgba(232,178,30,.5)"), [30, 30, 30, 30],
    note="Tab, selected (gold = navigation). Label #FAE69E. Replaces the PR #136 Outline component.")
add("settings_tab_locked", 96, 96,
    '<svg width="96" height="96" viewBox="0 0 96 96"><rect x="1.5" y="1.5" width="93" height="93" rx="22" fill="none" stroke="rgba(158,163,173,.45)" stroke-width="3" stroke-dasharray="10 6"/></svg>',
    [30, 30, 30, 30], note="Tab, locked: dashed 3 px #9EA3AD 45% (same as RT-109 locked level tabs). icon_lock_white 30 px tinted #9EA3AD left of the label, label at 45% alpha. Still tappable (toast says why).")
# ---------- danger button (Reset) ----------
add("settings_btn_danger_normal", 96, 96, div(96, 96, f"border-radius:28px;background:rgba(255,122,26,.12);border:3px solid {WARN}"), [36, 36, 36, 36],
    note="Danger button (Reset game data row 240×96, confirm modal 392×144). Text #FF7A1A 28/36 px.")
add("settings_btn_danger_pressed", 96, 96, div(96, 96, f"border-radius:28px;background:rgba(255,122,26,.30);border:3px solid {WARN}"), [36, 36, 36, 36],
    note="Danger button pressed.")

def render():
    PAD = 8; X = 0
    for s in S:
        s["x"], s["y"] = X, 0; X += s["w"] + PAD
    W = X; H = max(s["h"] for s in S)
    body = "".join(f'<div style="position:absolute;left:{s["x"]}px;top:0;width:{s["w"]}px;height:{s["h"]}px;overflow:hidden">{s["html"]}</div>' for s in S)
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}*{{box-sizing:border-box}}</style></head><body style="width:{W}px;height:{H}px;position:relative">{body}</body></html>'
    p = "/tmp/settings_sheet.html"; open(p, "w").write(html)
    for sc in (1, 2):
        out = f"/tmp/settings_sheet@{sc}.png"
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={sc}",
                        "--default-background-color=00000000", f"--window-size={W},{H+200}", f"--screenshot={out}", f"file://{p}"], stderr=subprocess.DEVNULL, check=True)
        sheet = Image.open(out).convert("RGBA")
        d = f"{U}/{OUT}/sprites@{sc}x"; os.makedirs(d, exist_ok=True)
        for s in S:
            sheet.crop((s["x"]*sc, 0, (s["x"]+s["w"])*sc, s["h"]*sc)).save(f"{d}/{s['name']}.png")

if __name__ == "__main__":
    render()
    mine = [dict(name=s["name"], file=f"{OUT}/sprites@1x/{s['name']}.png", file2x=f"{OUT}/sprites@2x/{s['name']}.png",
                 size=[s["w"], s["h"]], pivot=list(s["pivot"]),
                 border=(dict(zip(("left", "right", "top", "bottom"), s["border"])) if s["border"] else None),
                 pixelsPerUnit=100, pixelsPerUnit2x=200, screen="settings", note="GPP-SETTINGS. " + s["note"]) for s in S]
    mp = f"{U}/manifest.json"
    m = json.load(open(mp))
    before = len(m["sprites"]); byname = {e["name"]: e for e in mine}
    names = {e["name"] for e in m["sprites"]}
    m["sprites"] = [byname.get(e["name"], e) for e in m["sprites"]] + [e for e in mine if e["name"] not in names]
    assert len(m["sprites"]) >= before
    json.dump(m, open(mp, "w"), indent=1, ensure_ascii=False)
    print(len(S), "settings sprites x2;", "manifest", before, "->", len(m["sprites"]))
