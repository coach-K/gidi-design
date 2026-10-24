"""Per-level leaderboards (RT-109). Desktop 1920x1080 + phone 2340x1080. Background: the selected level's own screenshot (blurred).
Ranked by clear time (fastest first) for L1-L10 (L10 no longer endless: RT-108, PR #94). Backend: UGS Leaderboards gidi_L01..L10_time.
Names and numbers are fictional samples. No leaderboard backend exists on team-branch yet (Oct 24)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_hud import FRAMES, OUT
from gen_more import shell, LV
from brand import icon, P

SHORT = {1:"Agege",2:"Surulere",3:"Ikorodu",4:"Mushin",5:"Oshodi",6:"Ikeja",7:"Ojota",8:"3rd Mainland",9:"Lekki",10:"Ojuelegba"}
# Okabe-Ito avatar fills (avatar = initials on a colour until profile art exists)
AVC = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#59D9B8"]
NAMES = ["Tunde_Waka", "AdaKerbQueen", "Chidi.Zoom", "Bisi_Okada", "Emeka404", "FolaGoGo", "Ngozi_Danfo", "Yemi_Rush", "Kunle.Kerb", "Ifeoma_99", "Sade_Shuffle", "Obi_NoBrakes"]
ME = "BabaGidiFan"
MEDAL = {1: ("#E8B21E", "#7A5A00"), 2: ("#C9CFD9", "#5B6270"), 3: ("#C8743A", "#5E3014")}

def medal(n, size=64):
    """Rank badge: number on a shape (1 = 8-point star, 2 = hexagon, 3 = circle) so rank never relies on colour alone."""
    f, s = MEDAL[n]
    shape = {1: '<path d="M32 2l7.6 11.7 13.6-3-3 13.6L62 32l-11.7 7.6 3 13.6-13.6-3L32 62l-7.6-11.7-13.6 3 3-13.6L2 32l11.7-7.6-3-13.6 13.6 3z"/>',
             2: '<path d="M32 3l25 14.5v29L32 61 7 46.5v-29z"/>', 3: '<circle cx="32" cy="32" r="28"/>'}[n]
    return (f'<svg class="medal" viewBox="0 0 64 64" width="{size}" height="{size}"><g fill="{f}" stroke="{s}" stroke-width="3">{shape}</g>'
            f'<text x="32" y="42" text-anchor="middle" font-family="Jakarta" font-weight="700" font-size="28" fill="#0F1219">{n}</text></svg>')

def av(name, i):
    c = AVC[i % len(AVC)]; fg = "#F5F5F0" if c in ("#0072B2", "#D55E00", "#009E73") else "#0F1219"
    return f'<div class="av" style="background:{c};color:{fg}">{name[0].upper()}{[c for c in name[1:] if c.isupper()][:1][0] if any(c.isupper() for c in name[1:]) else ""}</div>'

def t(ms):
    """mm:ss.hh (hundredths, truncated) per the Unity dev (Oct 24)."""
    return f"{ms//60000:02d}:{ms//1000%60:02d}.{ms%1000//10:02d}"

def chips(n): return f'{icon("chip", 30)}₦{n:,}'

UNLOCKED = 7   # sample progress: L1-L7 open, L8-L10 locked

def tabs(sel):
    out = f'<button class="glass btn back">{icon("back",44,P["text"])}<small>Back</small></button>'
    for i in range(1, 11):
        lab = f'L{i}'
        lk = i > UNLOCKED
        b = f'{icon("lock",30,P["muted"] if i != sel else "#0F1219")}{lab}' if lk else lab
        out += f'<div class="tab{" on" if i == sel else ""}{" lock" if lk else ""}"><b>{b}</b><span>{SHORT[i]}</span></div>'
    return f'<div class="lbtabs">{out}</div>'

def side(lv, flt, best, rank, endless=False, locked=False, players=None):
    seg = "".join(f'<div class="{"on" if k == flt else ""}">{icon(ic, 40, P["naira"] if k == flt else P["muted"])}{k}</div>' for k, ic in (("Global", "trophy"), ("Friends", "group")))
    metric = "Highest score · endless" if endless else "Fastest clear time"
    return f'''<div class="lbside glass"><div class="k">{icon("trophy",30,P["gold"])} LEADERBOARD · L{lv}</div><h2>{LV[lv][0]}</h2>
<div class="sub">{metric}</div><div class="seg">{seg}</div>
<div class="kv2"><span>Your best</span><b>{best}</b><span>Your rank</span><b>{rank}</b><span>Players</span><b>{players or ("38" if flt=="Friends" else "12,904")}</b></div>
{f'<button class="gbtn" style="opacity:.45;width:100%">{icon("lock",40,P["muted"])} Locked</button>' if locked else f'<button class="cta sm">{icon("play",40,P["text"])} BEAT AM</button>'}</div>'''

COLS_T = "88px 60px 1fr 250px 210px"
COLS_E = "88px 60px 1fr 190px 170px 190px"

def rowhtml(r, name, i, cells, cls=""):
    rk = medal(r) if r <= 3 and "you" not in cls else f'<div class="rk">{r:,}</div>'
    top = f" t{r}" if r <= 3 else ""
    you = '<span class="youtag">YOU</span>' if "you" in cls else ""
    return f'<div class="lbrow{top} {cls}">{rk}{av(name, i)}<div class="nm">{name}{you}</div>{cells}</div>'

def timed(n):
    lv = 4; w = FRAMES[n][0]
    base = [41237, 42810, 43095, 44518, 45002, 46377, 47911]
    ch = [240, 210, 260, 190, 230, 180, 200]
    rows = "".join(rowhtml(k+1, NAMES[k], k, f'<div class="tm">{t(base[k])}</div><div class="ch">{chips(ch[k])}</div>') for k in range(7))
    me = rowhtml(128, ME, 7, f'<div class="tm">{t(58406)}</div><div class="ch">{chips(150)}</div>', "you")
    lst = f'''<div class="lblist glass" style="--cols:{COLS_T}"><div class="lbhead" style="--cols:{COLS_T}"><span style="text-align:center">RANK</span><span></span><span>PLAYER</span><span class="r">CLEAR TIME</span><span class="r">CHIPS (RUN)</span></div>
{rows}<div class="more">· · · scroll · · ·</div><div class="pinlbl">YOUR BEST · PINNED</div>{me}</div>'''
    body = f'<div class="ov"></div><div class="lb">{tabs(lv)}{side(lv, "Global", t(58406), "#128", False)}{lst}</div>'
    return shell(n, lv, body, "Leaderboard", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/leaderboard.css"></head>')

def locked(n):
    lv = 9; w = FRAMES[n][0]
    base = [52184, 53902, 54460, 55731, 56015, 57390]; ch = [310, 280, 300, 260, 290, 250]
    rows = "".join(rowhtml(k+1, NAMES[k+3], k+3, f'<div class="tm">{t(base[k])}</div><div class="ch">{chips(ch[k])}</div>') for k in range(6))
    banner = (f'<div class="lockban">{icon("lock",44,P["gold"])}<div><b>Clear L8 to unlock</b><span>Third Mainland Bridge · you can look around; your times post once it opens.</span></div></div>')
    lst = f'''<div class="lblist glass" style="--cols:{COLS_T}">{banner}<div class="lbhead" style="--cols:{COLS_T}"><span style="text-align:center">RANK</span><span></span><span>PLAYER</span><span class="r">CLEAR TIME</span><span class="r">CHIPS (RUN)</span></div>
{rows}<div class="more">· · · scroll · · ·</div></div>'''
    body = f'<div class="ov"></div><div class="lb">{tabs(lv)}{side(lv, "Global", "—", "—", locked=True, players="4,117")}{lst}</div>'
    return shell(n, lv, body, "Leaderboard locked", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/leaderboard.css"></head>')

def friends_empty(n):
    lv = 4
    body_ = (f'<div class="lblist glass" style="display:flex;align-items:center;justify-content:center"><div class="cen" style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:22px">{icon("group",80,P["gold"])}<h4 style="font-size:44px">No friends on this board yet</h4>'
             f'<p style="max-width:900px;font-size:30px;line-height:1.35">Add your people by their Gidi name. When they clear Mushin Market, their time shows here next to yours.</p>'
             f'<div style="display:flex;gap:20px"><button class="cta sm" style="min-width:380px">{icon("user",44,P["text"])} Add friends</button>'
             f'<button class="gbtn" style="min-width:320px">Share my name</button></div>'
             f'<p style="font-size:24px">Your Gidi name: <b style="color:#FAE69E">BabaGidiFan#4821</b></p></div></div>')
    body = f'<div class="ov"></div><div class="lb">{tabs(lv)}{side(lv, "Friends", t(58406), "—", players="0")}{body_}</div>'
    return shell(n, lv, body, "Leaderboard friends empty", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/leaderboard.css"></head>')

def states(n):
    lv = 6
    sk = "".join(f'<div class="sk"><i class="c"></i><i style="width:{a}px"></i><i style="width:90px;margin-left:auto"></i></div>' for a in (220, 180, 240, 160))
    cards = [
        ("LOADING", f'{sk}<div class="cen" style="flex:none;gap:6px"><div class="spin" style="width:48px;height:48px;border-width:6px"></div><p>Loading Ikeja Along…</p></div>'),
        ("EMPTY", f'<div class="cen">{icon("trophy",64,P["gold"])}<h4>No times yet on Ikeja Along</h4><p>Clear L6 and your time goes up first.</p><button class="cta sm" style="min-width:300px;font-size:32px">{icon("play",40,P["text"])} OYA, CROSS!</button></div>'),
        ("OFFLINE", f'<div class="cen">{icon("wifi_off",64,P["text"])}<h4>Network no dey</h4><p>Showing your saved best: <b style="color:#F5F5F0">01:02.41</b> · ₦160. Ranks update when you’re back online.</p><button class="gbtn">{icon("retry",40)} Try again</button></div>'),
        ("NOT SIGNED IN", f'<div class="cen">{icon("user",64,P["text"])}<h4>Sign in to join the ranks</h4><p>Your best time is saved on this device. Sign in to post it and see Friends.</p><button class="cta sm" style="min-width:300px;font-size:32px">{icon("user",40,P["text"])} Sign in</button></div>'),
    ]
    grid = "".join(f'<div class="st glass"><div class="stk">{k}</div>{c}</div>' for k, c in cards)
    body = f'<div class="ov"></div><div class="lb">{tabs(lv)}{side(lv, "Global", "—", "—")}<div class="stgrid">{grid}</div></div>'
    return shell(n, lv, body, "Leaderboard states", blur=True).replace("</head>", '<link rel="stylesheet" href="../css/leaderboard.css"></head>')

SCREENS = [("leaderboard", timed), ("leaderboard-states", states), ("leaderboard-locked", locked), ("leaderboard-friends", friends_empty)]
if __name__ == "__main__":
    for k, fn in SCREENS:
        for n in ("desktop", "phone"):
            open(os.path.join(OUT, f"{k}-{n}.html"), "w").write(fn(n))
