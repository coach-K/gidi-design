"""Drawn character / vehicle renders for every cosmetic in code + brief. SVG sources in costumes/, PNG renders in exports/costumes/."""
import os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIN, SKIN_D = "#7A4A2E", "#4E2C19"

def defs(uid, top, top_d, pat):
    p = ""
    if pat == "ankara":
        p = f'<pattern id="pt{uid}" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="{top}"/><circle cx="20" cy="20" r="11" fill="#E8B21E"/><circle cx="20" cy="20" r="5" fill="#0F1219"/><path d="M0 0l10 10M40 0L30 10M0 40l10-10M40 40L30 30" stroke="#F5F5F0" stroke-width="4"/></pattern>'
    elif pat == "agbada":
        p = f'<pattern id="pt{uid}" width="34" height="34" patternUnits="userSpaceOnUse"><rect width="34" height="34" fill="{top}"/><path d="M17 4l6 13-6 13-6-13z" fill="none" stroke="#FAE69E" stroke-opacity=".5" stroke-width="1.5"/></pattern>'
    elif pat == "jersey":
        p = f'<pattern id="pt{uid}" width="60" height="60" patternUnits="userSpaceOnUse"><rect width="60" height="60" fill="{top}"/><rect x="0" width="14" height="60" fill="#F5F5F0" opacity=".9"/></pattern>'
    elif pat == "default":
        p = f'<pattern id="pt{uid}" width="50" height="50" patternUnits="userSpaceOnUse"><rect width="50" height="50" fill="{top}"/><path d="M10 40l15-28 15 28" fill="none" stroke="#F5F5F0" stroke-width="5"/></pattern>'
    else:
        p = f'<pattern id="pt{uid}" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="{top}"/></pattern>'
    return (f'<defs>{p}<radialGradient id="sk{uid}" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#9A6440"/><stop offset=".6" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_D}"/></radialGradient>'
            f'<linearGradient id="sh{uid}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".0"/><stop offset=".55" stop-color="#000" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></linearGradient>'
            f'<linearGradient id="rim{uid}" x1="0" x2="1"><stop offset="0" stop-color="#FFB070" stop-opacity=".55"/><stop offset=".25" stop-color="#FFB070" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="bg{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B2F5C"/><stop offset=".7" stop-color="#6B4A6E"/><stop offset="1" stop-color="#F28C4B"/></linearGradient></defs>')

def figure(uid, top="#1E7A4A", top_d="#0F4A2C", pat="default", trousers="#2A2D36", hat="cap", hat_c="#0F1219", robe=False, extra=""):
    f = f'url(#pt{uid})'
    torso = ('<path d="M150 250 C120 260 95 300 88 360 L70 640 L330 640 L312 360 C305 300 280 260 250 250 Z"/>' if robe else
             '<path d="M150 250 C125 258 110 280 106 320 L104 470 L296 470 L294 320 C290 280 275 258 250 250 Z"/>')
    arms = ('<path d="M108 300 C70 330 40 420 50 520 L100 520 C100 440 115 370 130 340Z"/><path d="M292 300 C330 330 360 420 350 520 L300 520 C300 440 285 370 270 340Z"/>' if robe else
            '<path d="M112 290 C90 310 82 360 84 430 L112 430 C114 380 120 345 130 330Z"/><path d="M288 290 C310 310 318 360 316 430 L288 430 C286 380 280 345 270 330Z"/>')
    hats = {
     "cap": f'<path d="M150 118 C150 80 250 80 250 118 L252 132 L148 132Z" fill="{hat_c}"/><path d="M148 128 L268 128 Q275 138 250 140 L148 136Z" fill="{hat_c}"/><rect x="150" y="124" width="100" height="6" fill="#E8B21E"/>',
     "fila": f'<path d="M148 128 C140 70 270 70 254 128 Z" fill="{hat_c}"/><path d="M160 96 C190 80 240 82 250 110" stroke="#FAE69E" stroke-width="3" fill="none" opacity=".6"/><path d="M148 128 C175 120 230 120 254 128" stroke="#000" stroke-opacity=".3" stroke-width="4" fill="none"/>',
     "helmet": f'<path d="M136 150 C126 70 274 70 264 150 L264 168 L136 168Z" fill="{hat_c}"/><path d="M146 130 L254 130 L250 162 L150 162Z" fill="#1B2638" opacity=".85"/><path d="M152 136 L246 136" stroke="#9EC9FF" stroke-width="4" opacity=".7"/><path d="M200 74 L200 128" stroke="#E8B21E" stroke-width="8"/>',
     "none": ""}
    return (f'<g>{arms.replace("<path", f"<path fill={chr(34)}{SKIN if not robe else f}{chr(34)}")}'
            f'<rect x="138" y="460" width="56" height="200" rx="18" fill="{trousers}"/><rect x="206" y="460" width="56" height="200" rx="18" fill="{trousers}"/>'
            f'<path d="M126 652 h72 v22 h-82 q0-22 10-22z M202 652 h72 q10 0 10 22 h-82z" fill="#1A1410"/>'
            f'<g fill="{f}">{torso}</g><g fill="url(#sh{uid})">{torso}</g><g fill="url(#rim{uid})">{torso}</g>'
            f'<rect x="182" y="215" width="36" height="42" rx="12" fill="{SKIN_D}"/>'
            f'<ellipse cx="200" cy="168" rx="52" ry="60" fill="url(#sk{uid})"/>'
            f'<ellipse cx="182" cy="166" rx="5" ry="4" fill="#1A0F08"/><ellipse cx="218" cy="166" rx="5" ry="4" fill="#1A0F08"/>'
            f'<path d="M186 196 Q200 204 214 196" stroke="#2A160C" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<path d="M178 186 Q200 196 222 186 Q218 206 200 210 Q182 206 178 186Z" fill="#2A2A2A" opacity=".85"/>'
            f'{hats[hat]}{extra}</g>')

def card(uid, fig, label, status):
    col = "#59D9B8" if status=="IN-GAME" else "#E07CC0"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 760" width="800" height="1520">{defs(uid,*CFG[uid]["d"])}'
            f'<rect width="400" height="760" fill="url(#bg{uid})"/><ellipse cx="200" cy="676" rx="140" ry="20" fill="#000" opacity=".35"/>{fig}'
            f'<rect x="16" y="16" width="{len(status)*11+28}" height="32" rx="16" fill="{col}"/><text x="30" y="38" font-family="Jakarta,sans-serif" font-weight="700" font-size="16" fill="#111">{status}</text>'
            f'<rect x="0" y="696" width="400" height="64" fill="#0F1219" opacity=".85"/><text x="20" y="736" font-family="Jakarta,sans-serif" font-weight="700" font-size="24" fill="#F5F5F0">{label}</text></svg>')

CFG = {
 "baba_default": dict(d=("#1E7A4A","#0F4A2C","default"), f=dict(top="#1E7A4A",pat="default",hat="cap",hat_c="#0F1219"), label="Baba Gidi · Default fit", status="IN-GAME", sku="base character"),
 "baba_agbada": dict(d=("#F2EAD8","#C9BC9F","agbada"), f=dict(top="#F2EAD8",pat="agbada",hat="fila",hat_c="#7A1F2B",robe=True,trousers="#E9E0CC"), label="Agbada Baba (Owambe fit)", status="CONCEPT", sku="pack_baba_fits"),
 "baba_ankara": dict(d=("#2B4FA8","#18306B","ankara"), f=dict(top="#2B4FA8",pat="ankara",hat="fila",hat_c="#2B4FA8",trousers="#2B4FA8"), label="Ankara Fit", status="CONCEPT", sku="pack_baba_fits"),
 "baba_okada": dict(d=("#E06A1A","#A84A10","plain"), f=dict(top="#E06A1A",pat="plain",hat="helmet",hat_c="#E8B21E",trousers="#2A2D36",
                    extra='<path d="M106 330 L294 330 L294 350 L106 350Z" fill="#F5F5F0" opacity=".85"/><path d="M106 400 L294 400 L294 418 L106 418Z" fill="#F5F5F0" opacity=".85"/>'),
                    label="Okada Rider (hi-vis + helmet)", status="CONCEPT", sku="pack_baba_fits"),
 "baba_jersey": dict(d=("#C8102E","#7A0A1C","jersey"), f=dict(top="#C8102E",pat="jersey",hat="none",trousers="#F5F5F0",
                    extra='<text x="200" y="400" text-anchor="middle" font-family="Jakarta,sans-serif" font-weight="700" font-size="64" fill="#F5F5F0">10</text>'),
                    label="Street Jersey (generic, no club)", status="CONCEPT", sku="pack_baba_fits"),
}

def vehicle(kind, body, accent, slogan, uid):
    w = '<g fill="#111"><circle cx="{0}" cy="300" r="34"/></g><circle cx="{0}" cy="300" r="14" fill="#9EA3AD"/>'
    if kind == "danfo":
        shape = (f'<path d="M60 290 L60 150 Q62 118 96 112 L560 112 Q620 116 640 180 L660 290Z" fill="{body}"/>'
                 f'<path d="M60 200 h600 v22 h-600z M60 246 h600 v12 h-600z" fill="#0F1219"/>'
                 + "".join(f'<rect x="{90+i*86}" y="130" width="70" height="56" rx="6" fill="#1B2638"/>' for i in range(6)) +
                 f'<text x="330" y="276" text-anchor="middle" font-family="Jakarta,sans-serif" font-weight="700" font-size="26" fill="{accent}">{slogan}</text>'
                 + w.format(150) + w.format(560))
    elif kind == "keke":
        shape = (f'<path d="M200 120 Q210 92 280 90 L470 90 Q520 94 524 130 L520 140 L200 140Z" fill="{accent}"/>'
                 f'<path d="M210 140 L214 300 M330 140 L330 210 M510 140 L540 210" stroke="#0F1219" stroke-width="10" stroke-linecap="round"/>'
                 f'<rect x="232" y="150" width="90" height="56" rx="8" fill="#F5F5F0" opacity=".25"/>'
                 f'<path d="M200 210 L560 210 Q610 214 620 250 L630 296 L200 296Z" fill="{body}"/>'
                 f'<path d="M540 210 L610 160 L620 170 L560 214Z" fill="#1B2638"/>'
                 f'<text x="380" y="262" text-anchor="middle" font-family="Jakarta,sans-serif" font-weight="700" font-size="22" fill="#F5F5F0">{slogan}</text>'
                 + w.format(260) + w.format(580))
    else:  # korope
        shape = (f'<path d="M80 290 L80 140 Q84 110 120 108 L520 108 Q590 112 620 200 L630 290Z" fill="{body}"/>'
                 f'<path d="M80 236 h550 v20 h-550z" fill="{accent}"/>'
                 + "".join(f'<rect x="{110+i*100}" y="126" width="84" height="64" rx="8" fill="#1B2638"/>' for i in range(4)) +
                 f'<path d="M520 126 L580 126 Q600 150 606 196 L520 196Z" fill="#1B2638"/>'
                 f'<text x="300" y="226" text-anchor="middle" font-family="Jakarta,sans-serif" font-weight="700" font-size="24" fill="#F5F5F0">{slogan}</text>'
                 + w.format(170) + w.format(540))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 420" width="1440" height="840"><defs><linearGradient id="v{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B2F5C"/><stop offset=".75" stop-color="#6B4A6E"/><stop offset="1" stop-color="#F28C4B"/></linearGradient>'
            f'<linearGradient id="vs{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".25"/><stop offset=".4" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient></defs>'
            f'<rect width="720" height="420" fill="url(#v{uid})"/><rect y="330" width="720" height="90" fill="#26272E"/><ellipse cx="360" cy="336" rx="320" ry="16" fill="#000" opacity=".4"/>'
            f'{shape}'
            f'<rect x="16" y="16" width="122" height="32" rx="16" fill="#E07CC0"/><text x="30" y="38" font-family="Jakarta,sans-serif" font-weight="700" font-size="16" fill="#111">CONCEPT</text></svg>')

VEH = {"skin_danfo_gidi":("danfo","#E8B21E","#0F1219","NO TELL ME STORY","Danfo · \"No tell me story\" paint"),
       "skin_danfo_dusk":("danfo","#5B2A86","#FAE69E","EKO O NI BAJE","Danfo · Dusk purple"),
       "skin_keke_ankara":("keke","#2E7A68","#E8B21E","SHINE YA EYE","Keke · Green &amp; gold"),
       "skin_korope_owambe":("korope","#C8102E","#FAE69E","OWAMBE EXPRESS","Korope · Owambe red")}

if __name__ == "__main__":
    for uid, c in CFG.items():
        open(f"{ROOT}/costumes/{uid}.svg","w").write(card(uid, figure(uid, **c["f"]), c["label"], c["status"]))
    for uid,(k,b,a,s,_) in VEH.items():
        open(f"{ROOT}/costumes/{uid}.svg","w").write(vehicle(k,b,a,s,uid))
    for f in sorted(os.listdir(f"{ROOT}/costumes")):
        n = f[:-4]; veh = n.startswith("skin_"); W,H = (1440,840) if veh else (800,1520)
        html = f"{ROOT}/costumes/_{n}.html"
        open(html,"w").write(f'<html><head><style>@font-face{{font-family:Jakarta;src:url(../fonts/PlusJakartaSans-Bold.ttf)}}body{{margin:0}}</style></head><body>{open(f"{ROOT}/costumes/{f}").read()}</body></html>')
        subprocess.run(["bash", f"{ROOT}/tools/shoot.sh", html, f"{ROOT}/exports/costumes/{n}.png", str(W), str(H)])
        os.remove(html)
    print("ok")
