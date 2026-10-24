"""Splash (RT-115) + Lagos map (GPP-060) repair resources. Out: /workspace/games/design/splash-map/"""
import os, json, subprocess, random, math
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/workspace/games/design/splash-map"; TMP = "/tmp/sm"; os.makedirs(TMP, exist_ok=True)
FONT = f"@font-face{{font-family:J;src:url(file://{R}/fonts/PlusJakartaSans-Bold.ttf)}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:J;background:transparent}}"
LV = ["Agege Bus Stop","Surulere Way","Ikorodu Road","Mushin Market","Oshodi Expressway","Ikeja Along","Ojota Intersect","Third Mainland Bridge","Lekki Toll Gate","Ojuelegba Chaos"]
STOPS = [1,2,2,2,3,2,2,3,2,2]

def shoot(html, png, w, h, dsf=1, alpha=True):
    p = f"{TMP}/{os.path.basename(png)}.html"; open(p, "w").write(f"<html><head><style>{FONT}</style></head><body>{html}</body></html>")
    os.makedirs(os.path.dirname(png), exist_ok=True)
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars",f"--force-device-scale-factor={dsf}","--virtual-time-budget=2000",
        f"--window-size={w},{h+300}"]+(["--default-background-color=00000000"] if alpha else [])+[f"--screenshot={png}", "file://"+p], capture_output=True)
    Image.open(png).crop((0,0,w*dsf,h*dsf)).save(png)

def sprite(name, html, w, h, sub):
    for d in (1,2): shoot(html, f"{OUT}/{sub}/sprites@{d}x/{name}.png", w, h, d)

# ---------- SPLASH ----------
def skyline(W, H):
    random.seed(7); s = H/1080; g = []
    # far + near skyline
    for layer, col, base, hmax in ((0,"#3A3566",0.66,0.30),(1,"#1E2140",0.70,0.22)):
        x = -20
        while x < W:
            bw = random.randint(40,130)*s; bh = random.uniform(.05,hmax)*H
            g.append(f'<rect x="{x:.0f}" y="{base*H-bh:.0f}" width="{bw:.0f}" height="{bh+4:.0f}" fill="{col}"/>')
            if layer == 1:
                for wy in range(int(base*H-bh+14*s), int(base*H-10*s), int(26*s)):
                    for wx in range(int(x+10*s), int(x+bw-12*s), int(22*s)):
                        if random.random() < .28: g.append(f'<rect x="{wx}" y="{wy}" width="{8*s:.0f}" height="{12*s:.0f}" fill="#FAE69E" opacity=".55"/>')
            x += bw + random.randint(0,12)*s
    # Third Mainland bridge
    by = .70*H
    g.append(f'<rect x="0" y="{by:.0f}" width="{W}" height="{14*s:.0f}" fill="#141729"/>')
    for px in range(0, W, int(150*s)): g.append(f'<rect x="{px}" y="{by:.0f}" width="{12*s:.0f}" height="{.08*H:.0f}" fill="#141729"/>')
    for px in range(0, W, int(36*s)): g.append(f'<circle cx="{px}" cy="{by-4*s:.0f}" r="{3*s:.1f}" fill="#E8B21E" opacity=".8"/>')
    # lagoon reflection + road + zebra crossing
    g.append(f'<rect x="0" y="{by+14*s:.0f}" width="{W}" height="{.08*H:.0f}" fill="url(#lag)"/>')
    ry = .86*H
    g.append(f'<rect x="0" y="{ry-.08*H:.0f}" width="{W}" height="{H}" fill="#1A1D27"/>')
    g.append(f'<rect x="0" y="{ry-.08*H:.0f}" width="{W}" height="{6*s:.0f}" fill="#E8B21E" opacity=".75"/>')
    zw = 54*s
    for i in range(int(W/(zw*1.9))+1):
        x = i*zw*1.9; g.append(f'<polygon points="{x:.0f},{ry-.05*H:.0f} {x+zw:.0f},{ry-.05*H:.0f} {x+zw*1.25:.0f},{H} {x-zw*.25:.0f},{H}" fill="#F5F5F0" opacity=".16"/>')
    # danfo silhouettes with headlights
    for dx in (.12,.71):
        x = dx*W; y = ry-.06*H; w = 230*s; h = 92*s
        g.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{14*s:.0f}" fill="#E8B21E"/><rect x="{x:.0f}" y="{y+h*.55:.0f}" width="{w:.0f}" height="{8*s:.0f}" fill="#0F1219"/>')
        for k in range(4): g.append(f'<rect x="{x+16*s+k*52*s:.0f}" y="{y+12*s:.0f}" width="{40*s:.0f}" height="{26*s:.0f}" rx="{4*s:.0f}" fill="#2B2F5C"/>')
        for k in (.2,.8): g.append(f'<circle cx="{x+w*k:.0f}" cy="{y+h:.0f}" r="{17*s:.0f}" fill="#0F1219"/>')
    return f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="display:block"><defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151A33"/><stop offset=".35" stop-color="#2B2F5C"/><stop offset=".55" stop-color="#6B4A6E"/><stop offset=".70" stop-color="#F28C4B"/></linearGradient>
<linearGradient id="lag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F28C4B" stop-opacity=".45"/><stop offset="1" stop-color="#2B2F5C" stop-opacity="0"/></linearGradient>
<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FAE69E"/><stop offset=".4" stop-color="#F28C4B" stop-opacity=".6"/><stop offset="1" stop-color="#F28C4B" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#0F1219" stop-opacity="0"/><stop offset="1" stop-color="#0F1219" stop-opacity=".75"/></radialGradient></defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/><circle cx="{W*.5:.0f}" cy="{H*.66:.0f}" r="{H*.32:.0f}" fill="url(#sun)"/>{"".join(g)}
<rect width="{W}" height="{H}" fill="url(#vig)"/></svg>'''

def logo_html(w):  # mark + Gidi++ lockup, horizontal; w = width px
    mark = open(f"{R}/logos/mark.svg").read(); lock = open(f"{R}/logos/lockup_tagline_light.svg").read()
    h = w*0.30
    return f'<div style="width:{w}px;height:{h:.0f}px;display:flex;align-items:center;gap:{w*.04:.0f}px"><div style="width:{h:.0f}px;height:{h:.0f}px;border-radius:{h*.18:.0f}px;overflow:hidden;flex:none">{mark.replace("<svg ",f"<svg width=\"{h:.0f}\" height=\"{h:.0f}\" ",1)}</div><div style="flex:1">{lock.replace("<svg ","<svg width=\"100%\" ",1)}</div></div>'

def splash():
    for W in (1920,2340):
        shoot(skyline(W,1080), f"{OUT}/splash/bg_splash_{W}x1080.png", W, 1080, 1, False)
    shoot(logo_html(2400), f"{OUT}/splash/logo_gidi_master.png", 2400, 720, 1)
    sprite("logo_gidi", logo_html(800), 800, 240, "splash")      # 1x 800x240, 2x 1600x480
    sprite("loader_track", '<div style="width:64px;height:20px;border-radius:10px;background:rgba(245,245,240,.16);box-shadow:inset 0 0 0 2px rgba(245,245,240,.10)"></div>', 64, 20, "splash")
    sprite("loader_fill", '<div style="width:64px;height:20px;border-radius:10px;background:linear-gradient(#FAE69E,#E8B21E 55%,#C99212)"></div>', 64, 20, "splash")
    sprite("loader_glint", '<div style="width:48px;height:20px;border-radius:10px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.7),rgba(255,255,255,0))"></div>', 48, 20, "splash")
    sprite("badge_rating", '<div style="width:72px;height:48px;border:3px solid #F5F5F0;border-radius:10px;color:#F5F5F0;font-size:24px;display:flex;align-items:center;justify-content:center">12+</div>', 72, 48, "splash")
    sprite("splash_scrim", '<div style="width:64px;height:256px;background:linear-gradient(rgba(15,18,25,0),rgba(15,18,25,.85))"></div>', 64, 256, "splash")

def splash_preview(W, H, prog=.62):
    s = H/1080; lw = 800*s
    bg = f"file://{OUT}/splash/bg_splash_{1920 if W/H<2 else 2340}x1080.png"
    return f'''<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:url({bg}) center/cover">
<div style="position:absolute;left:0;right:0;bottom:0;height:{H*.45:.0f}px;background:linear-gradient(rgba(15,18,25,0),rgba(15,18,25,.85))"></div>
<img src="file://{OUT}/splash/sprites@2x/logo_gidi.png" style="position:absolute;width:{lw:.0f}px;left:{(W-lw)/2:.0f}px;top:{H*.30-120*s:.0f}px">
<div style="position:absolute;left:{(W-720*s)/2:.0f}px;top:{H-200*s:.0f}px;width:{720*s:.0f}px;height:{20*s:.0f}px;border-radius:{10*s}px;background:rgba(245,245,240,.16)"><div style="width:{prog*100}%;height:100%;border-radius:{10*s}px;background:linear-gradient(#FAE69E,#E8B21E 55%,#C99212)"></div></div>
<div style="position:absolute;left:0;right:0;top:{H-160*s:.0f}px;text-align:center;font-size:{28*s:.1f}px;color:#9EA3AD">Loading Agege Bus Stop… <span style="color:#FAE69E">Tip: Owa! freeze the next lane.</span></div>
<img src="file://{OUT}/splash/sprites@2x/badge_rating.png" style="position:absolute;width:{72*s:.0f}px;left:{(132 if W>2000 else 40)*s:.0f}px;bottom:{40*s:.0f}px"></div>'''

# ---------- MAP ----------
def layout(W, H, notch=0):
    s = H/1080; m = 40*s; top = 160*s
    pw = 640*s; px = W-notch-m-pw; py = top; ph = H-top-m
    ax0 = notch+m; ax1 = px-m; ay0 = top; ay1 = H-m
    cw = (ax1-ax0)/5; rows = (ay0+(ay1-ay0)*.10, ay0+(ay1-ay0)*.58)
    nodes = []
    for i in range(10):
        r = i//5; c = i%5 if r == 0 else 4-i%5
        nodes.append(dict(level=i+1, cx=ax0+cw*(c+.5), cy=rows[r]+60*s))
    return dict(W=W,H=H,s=s,notch=notch,margin=m,topbar=top,panel=(px,py,pw,ph),area=(ax0,ay0,ax1,ay1),col=cw,nodes=nodes,
                node_d=120*s, dot_d=28*s, dot_gap=10*s, dot_top=60*s+12*s, label_top=60*s+12*s+28*s+10*s, label_w=cw-24*s, label_font=28*s, star_d=26*s)

def map_bg(L):
    W,H,s = L["W"],L["H"],L["s"]; random.seed(3); g=[]
    for _ in range(int(140*W/1920)):   # city blocks
        x=random.uniform(0,W); y=random.uniform(0,H); w=random.uniform(60,220)*s; h=random.uniform(40,140)*s
        g.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{6*s:.0f}" fill="#1B2030"/>')
    # lagoon (bottom right, Lagos Lagoon) + Atlantic strip
    g.append(f'<path d="M{W*.55:.0f},{H} C{W*.6:.0f},{H*.78:.0f} {W*.75:.0f},{H*.70:.0f} {W:.0f},{H*.62:.0f} L{W},{H} Z" fill="#163240"/>')
    g.append(f'<path d="M0,{H*.93:.0f} C{W*.3:.0f},{H*.90:.0f} {W*.5:.0f},{H*.97:.0f} {W*.6:.0f},{H} L0,{H} Z" fill="#163240"/>')
    # expressways
    for k,(a,b) in enumerate(((0,.35),(.2,1.0),(.5,.15))):
        g.append(f'<path d="M0,{H*a:.0f} Q{W*.5:.0f},{H*(a+b)/2+H*.1:.0f} {W},{H*b:.0f}" stroke="#262C3D" stroke-width="{26*s:.0f}" fill="none"/>')
    # gold road through nodes (baked)
    pts = L["nodes"]; d = f"M{pts[0]['cx']:.0f},{pts[0]['cy']:.0f}"
    for a,b in zip(pts, pts[1:]):
        if a["level"] == 5: d += f" C{a['cx']+L['col']*.6:.0f},{a['cy']:.0f} {b['cx']+L['col']*.6:.0f},{b['cy']:.0f} {b['cx']:.0f},{b['cy']:.0f}"
        else: d += f" L{b['cx']:.0f},{b['cy']:.0f}"
    g.append(f'<path d="{d}" stroke="#0F1219" stroke-width="{22*s:.0f}" fill="none" stroke-linecap="round"/><path d="{d}" stroke="#E8B21E" stroke-width="{6*s:.0f}" stroke-dasharray="{18*s:.0f} {12*s:.0f}" fill="none" stroke-linecap="round"/>')
    lbl = "".join(f'<text x="{x*W:.0f}" y="{y*H:.0f}" fill="#3A4256" font-size="{22*s:.0f}" letter-spacing="{4*s:.0f}">{t}</text>' for t,x,y in (("LAGOS LAGOON",.80,.80),("ATLANTIC",.05,.955)))
    return f'''<svg width="{W}" height="{H}" style="display:block;font-family:J"><rect width="{W}" height="{H}" fill="#121622"/>{"".join(g)}{lbl}
<rect width="{W}" height="{L['topbar']:.0f}" fill="url(#t)"/><defs><linearGradient id="t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0F1219" stop-opacity=".9"/><stop offset="1" stop-color="#0F1219" stop-opacity="0"/></linearGradient></defs></svg>'''

NODE = {"done":("#59D9B8","#173A3A","✓"),"open":("#F5F5F0","#2B2F5C",""),"locked":("#6B7180","#1E222E","lock"),"current":("#E8B21E","#3A3120","")}
LOCK = '<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#9EA3AD" stroke-width="2.4"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'
def node_html(kind, d=120):
    ring, fill, g = NODE[kind]; glow = "box-shadow:0 0 0 10px rgba(232,178,30,.22),0 0 28px 8px rgba(232,178,30,.35);" if kind=="current" else ""
    inner = LOCK if g=="lock" else (f'<span style="color:{ring};font-size:56px">✓</span>' if g else "")
    pad = 24 if kind=="current" else 4
    return f'<div style="width:{d+pad*2}px;height:{d+pad*2}px;display:flex;align-items:center;justify-content:center"><div style="width:{d}px;height:{d}px;border-radius:50%;border:6px solid {ring};background:{fill};{glow}display:flex;align-items:center;justify-content:center">{inner}</div></div>'
STAR = '<svg width="{d}" height="{d}" viewBox="0 0 24 24"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3 6.1 20.6l1.3-6.6L2.5 9.4l6.6-.8z" fill="{f}" stroke="{s}" stroke-width="1.6" stroke-linejoin="round"/></svg>'
DOT = {"done":("#59D9B8","#59D9B8"),"open":("#2B2F5C","#F5F5F0"),"locked":("#1E222E","#6B7180"),"selected":("#E8B21E","#FAE69E")}
def dot_html(k, d=28): f,b = DOT[k]; return f'<div style="width:{d+4}px;height:{d+4}px;padding:2px"><div style="width:{d}px;height:{d}px;border-radius:50%;background:{f};border:3px solid {b}"></div></div>'
PANEL = '<div style="width:96px;height:96px;border-radius:28px;background:rgba(15,18,25,.90);border:2px solid rgba(232,178,30,.55);box-shadow:inset 0 2px 0 rgba(245,245,240,.08)"></div>'
TAB = lambda on: f'<div style="width:64px;height:64px;border-radius:16px;background:{"rgba(232,178,30,.18)" if on else "rgba(245,245,240,.04)"};border:2px solid {"#E8B21E" if on else "rgba(245,245,240,.22)"}"></div>'

def map_sprites():
    for k in NODE: sprite(f"map_node_{k}", node_html(k), 168 if k=="current" else 128, 168 if k=="current" else 128, "map")
    sprite("map_star_filled", STAR.format(d=48,f="#E8B21E",s="#FAE69E"), 48, 48, "map")
    sprite("map_star_empty", STAR.format(d=48,f="rgba(245,245,240,.08)",s="#6B7180"), 48, 48, "map")
    for k in DOT: sprite(f"map_stopdot_{k}", dot_html(k), 32, 32, "map")
    sprite("map_panel", PANEL, 96, 96, "map"); sprite("map_tab_on", TAB(True), 64, 64, "map"); sprite("map_tab_off", TAB(False), 64, 64, "map")
    sprite("map_label_plate", '<div style="width:48px;height:48px;border-radius:12px;background:rgba(15,18,25,.78)"></div>', 48, 48, "map")

STATE = {i: ("done" if i<5 else "current" if i==5 else "locked") for i in range(1,11)}
STARS = {1:3,2:5,3:4,4:6,5:3}
def map_preview(L, sel=5):
    W,H,s = L["W"],L["H"],L["s"]; sp = f"file://{OUT}/map/sprites@2x"; o=[]
    bgf = f"{TMP}/mapbg_{W}x{H}.png"; shoot(map_bg(L), bgf, W, H, 1, False)
    for n in L["nodes"]:
        i=n["level"]; k=STATE[i]; cx,cy=n["cx"],n["cy"]; d=L["node_d"]; dd=d*(168/120) if k=="current" else d*(128/120)
        o.append(f'<img src="{sp}/map_node_{k}.png" style="position:absolute;left:{cx-dd/2:.1f}px;top:{cy-dd/2:.1f}px;width:{dd:.1f}px">')
        txt = "∞" if i==10 else f"L{i}"
        if k in("current",) or (k=="locked" and i==10): o.append(f'<div style="position:absolute;left:{cx-d/2:.1f}px;top:{cy-d/2:.1f}px;width:{d:.1f}px;height:{d:.1f}px;display:flex;align-items:center;justify-content:center;color:{"#E8B21E" if k=="current" else "#9EA3AD"};font-size:{44*s:.1f}px;{"background:rgba(30,34,46,1);border-radius:50%;transform:scale(.8)" if i==10 else ""}">{txt}</div>')
        ns = STOPS[i-1]; dw = L["dot_d"]+4*s; tot = ns*dw+(ns-1)*8*s; x0 = cx-tot/2
        for j in range(ns):
            dk = "done" if k=="done" else ("selected" if (k=="current" and j==0) else "open" if k=="current" else "locked")
            o.append(f'<img src="{sp}/map_stopdot_{dk}.png" style="position:absolute;left:{x0+j*(dw+8*s):.1f}px;top:{cy+L["dot_top"]:.1f}px;width:{dw:.1f}px">')
        lw = L["label_w"]
        o.append(f'<div style="position:absolute;left:{cx-lw/2:.1f}px;top:{cy+L["label_top"]:.1f}px;width:{lw:.1f}px;text-align:center;font-size:{L["label_font"]:.1f}px;line-height:1.15;color:{"#F5F5F0" if k!="locked" else "#9EA3AD"};text-shadow:0 1px 3px #0F1219">L{i} {LV[i-1]}</div>')
    px,py,pw,ph = L["panel"]; P = lambda v: f"{v*s:.1f}px"
    tabs = "".join(f'<div style="flex:1;height:{P(64)};border:{P(2)} solid {"#E8B21E" if j==0 else "rgba(245,245,240,.22)"};background:{"rgba(232,178,30,.18)" if j==0 else "transparent"};border-radius:{P(16)};display:flex;align-items:center;justify-content:center;font-size:{P(26)};color:{"#FAE69E" if j==0 else "#9EA3AD"}">Stop {j+1}</div>' for j in range(3))
    stars = "".join(f'<img src="{sp}/map_star_{"filled" if j<1 else "empty"}.png" style="width:{P(36)}">' for j in range(3))
    kv = lambda k,v: f'<div style="display:flex;gap:{P(16)};font-size:{P(26)};margin-top:{P(14)}"><span style="width:{P(150)};color:#9EA3AD;flex:none">{k}</span><b style="color:#F5F5F0;font-weight:400">{v}</b></div>'
    o.append(f'''<div style="position:absolute;left:{px:.1f}px;top:{py:.1f}px;width:{pw:.1f}px;height:{ph:.1f}px;border-radius:{P(28)};background:rgba(15,18,25,.90);border:{P(2)} solid rgba(232,178,30,.55);padding:{P(32)};display:flex;flex-direction:column">
<div style="font-size:{P(44)};color:#F5F5F0;line-height:1.1">L5 · Oshodi Expressway</div><div style="display:flex;gap:{P(12)};margin-top:{P(20)}">{tabs}</div>
{kv("Lanes","5")}{kv("Crowd","6 · Agbada Bigman and Slay Queen join")}{kv("Best","01:12")}<div style="display:flex;gap:{P(16)};font-size:{P(26)};margin-top:{P(14)};align-items:center"><span style="width:{P(150)};color:#9EA3AD">Stars</span>{stars}</div>
<div style="flex:1"></div><div style="height:{P(120)};border-radius:{P(24)};background:linear-gradient(#2F8F70,#1F6B54);border:{P(3)} solid #E8B21E;display:flex;align-items:center;justify-content:center;font-size:{P(44)};color:#F5F5F0">▷&nbsp; OYA, CROSS!</div></div>''')
    tb = lambda x,w,t: f'<div style="position:absolute;left:{x:.1f}px;top:{P(28)};width:{w:.1f}px;height:{P(104)};border-radius:{P(20)};background:rgba(15,18,25,.85);border:{P(2)} solid rgba(245,245,240,.15);display:flex;align-items:center;justify-content:center;color:#F5F5F0;font-size:{P(30)}">{t}</div>'
    m=L["margin"]; n=L["notch"]
    o.append(tb(n+m,104*s,"‹")+f'<div style="position:absolute;left:{n+m+128*s:.1f}px;top:{P(52)};font-size:{P(48)};color:#F5F5F0">Lagos map</div>')
    o.append(tb(W-n-m-104*s,104*s,"⚙")+tb(W-n-m-232*s,104*s,"♥ 3")+tb(W-n-m-512*s,264*s,'<span style="color:#FAE69E">₦12,450</span>'))
    return f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:url(file://{bgf})">{"".join(o)}</div>'

if __name__ == "__main__":
    splash(); map_sprites()
    for W,H in ((1920,1080),(1024,450)): shoot(splash_preview(W,H), f"{OUT}/preview/splash_{W}x{H}.png", W, H, 1, False)
    spec = {}
    for W,H,n in ((1024,450,0),(1920,1080,0),(2340,1080,132)):
        L = layout(W,H,n); spec[f"{W}x{H}"] = L
        if W != 1024: shoot(map_bg(L), f"{OUT}/map/bg_map_{W}x{H}.png", W, H, 1, False)
        shoot(map_preview(L), f"{OUT}/preview/map_{W}x{H}.png", W, H, 1, False)
    json.dump(spec, open(f"{OUT}/map/layout.json","w"), indent=1, default=lambda v: round(v,1))
