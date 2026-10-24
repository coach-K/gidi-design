"""GPP-066 Continue modal states (PR #109, ContinueModalRules / ContinueOfferPanel). 1 continue per run.
States: offer, ad loading (SetBusy), ad unavailable/failed, no continues left, countdown/timeout (design proposal: not in code yet)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT
from gen_more import shell, lab
from gen_screens import continue_cost
from brand import icon, P

LV = 5; COST = continue_cost(LV); T = 10   # proposed timeout seconds

def spinner(sz=44):
    return f'<svg width="{sz}" height="{sz}" viewBox="0 0 48 48"><circle cx="24" cy="24" r="19" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="5"/><path d="M24 5a19 19 0 0 1 19 19" fill="none" stroke="#F5F5F0" stroke-width="5" stroke-linecap="round"/></svg>'

def panel(state, extra_style=""):
    kicker, title, sub = "ALMOST THERE", "Continue this run?", f"Keep the curb run alive · {lab(LV)}"
    ad = f'<button class="cta sm" style="width:100%">{icon("ad",44,P["text"])} Watch ad, continue</button>'
    chips = f'<button class="gbtn" style="width:100%;color:#FAE69E">{icon("chip",44)} Continue: ₦{COST} Naira Chips</button>'
    end = '<button class="gbtn" style="width:100%;color:#9EA3AD">End run</button>'
    foot = "Naira Chips 12,450 · Fair play: max 1 continue per run"
    bar = ""
    dis = 'style="width:100%;opacity:.45;filter:grayscale(1)"'
    if state == "loading":
        ad = f'<button class="cta sm" {dis.replace("opacity:.45;filter:grayscale(1)","opacity:.85")}>{spinner()} Loading ad…</button>'
        chips = f'<button class="gbtn" {dis}>{icon("chip",44)} Continue: ₦{COST} Naira Chips</button>'
        end = f'<button class="gbtn" {dis}>End run</button>'; foot = "Loading ad… · countdown paused"
    if state == "failed":
        ad = (f'<button class="gbtn" style="width:100%;color:#9EA3AD;border-style:dashed">{icon("wifi_off",44,P["muted"])} Ad not available</button>')
        chips = chips.replace('class="gbtn"', 'class="gbtn" data-focus').replace('color:#FAE69E', 'color:#FAE69E;border-color:#E8B21E;box-shadow:0 0 0 4px rgba(232,178,30,.25)')
        foot = '<span style="color:#FF9E57">▲ Couldn\'t load an ad. Try again later or use chips.</span>'
    if state == "none":
        kicker, title, sub = "RUN OVER", "Run over", "No continues left this run"
        ad = f'<button class="cta sm" {dis}>{icon("ad",44,P["text"])} Watch ad, continue</button>'
        chips = f'<button class="gbtn" {dis}>{icon("chip",44)} Continue: ₦{COST} Naira Chips</button>'
        end = f'<button class="cta sm" style="width:100%">See results {icon("play",44,P["text"])}</button>'; foot = "1 of 1 continue used · Fair play: max 1 continue per run"
    if state == "countdown":
        kicker = f'ALMOST THERE · <b style="color:#F5F5F0">7</b>s'
        bar = '<div style="height:12px;border-radius:6px;background:rgba(255,255,255,.12);margin:22px 40px 0;overflow:hidden"><div style="width:70%;height:100%;background:#E8B21E;border-radius:6px"></div></div>'
    if state == "timeout":
        kicker = f'<span style="color:#FF9E57">◆ TIME UP · <b>2</b>s</span>'
        bar = '<div style="height:12px;border-radius:6px;background:rgba(255,255,255,.12);margin:22px 40px 0;overflow:hidden"><div style="width:20%;height:100%;background:#FF9E57;border-radius:6px"></div></div>'
        foot = "At 0 s the run ends (same as End run)"
    return (f'<div class="panel" style="width:1000px;{extra_style}"><div style="color:#E8B21E;font-size:26px;letter-spacing:.12em">{kicker}</div>'
            f'<div class="ph" style="color:#F5F5F0">{title}</div><div class="psub">{sub}</div>{bar}'
            f'<div style="display:flex;flex-direction:column;gap:20px;margin-top:30px">{ad}{chips}{end}</div>'
            f'<div class="psub" style="font-size:26px;margin-top:24px">{foot}</div></div>')

STATES = [("offer","1 · Offer","both enabled; chips disabled if wallet < cost"),("countdown","2 · Countdown","10 s bar drains, digits in kicker"),
          ("loading","3 · Ad loading","SetBusy(true): all buttons off, spinner"),("failed","4 · Ad unavailable / failed","ad slot off, chips focused, reason line"),
          ("timeout","5 · Last 3 s","orange + ◆ shape, then End run"),("none","6 · No continues left","TitleNoneLeft; only See results")]

def states(n):
    w = FRAMES[n][0]; sc = 0.46
    cells = "".join(f'<div style="display:flex;flex-direction:column;gap:10px;align-items:center"><div style="font-size:26px;color:#E8B21E">{t}<span style="color:#9EA3AD;font-size:20px"> · {d}</span></div>'
                    f'<div style="width:{1000*sc+45:.0f}px;height:{860*sc:.0f}px;position:relative"><div style="position:absolute;left:0;top:0;transform:scale({sc});transform-origin:0 0">{panel(k,"position:relative;left:0;top:0;transform:none")}</div></div></div>'
                    for k, t, d in STATES)
    body = (f'<div class="ov heavy"></div><div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;z-index:3">'
            f'<div style="font-size:44px;color:#F5F5F0">Continue modal · states <span style="color:#9EA3AD;font-size:28px">(GPP-066 · 1 per run)</span></div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,auto);gap:26px 36px">{cells}</div></div>')
    return shell(n, LV, body, "Continue states", blur=True)

def single(k): return lambda n: shell(n, LV, '<div class="ov heavy"></div>' + panel(k), "Continue " + k, blur=True)

SCREENS = [("continue-states", states), ("continue-loading", single("loading")), ("continue-failed", single("failed")),
           ("continue-none", single("none")), ("continue-countdown", single("countdown"))]
if __name__ == "__main__":
    for k, fn in SCREENS:
        for n in ("desktop", "phone"):
            open(os.path.join(OUT, f"{k}-{n}.html"), "w").write(fn(n))
