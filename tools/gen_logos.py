"""Wordmark/logo variants (SVG+PNG) and app icon exports (iOS set, Android adaptive, web favicons/PWA)."""
import os, sys, subprocess, json
sys.path.insert(0, os.path.dirname(__file__))
from brand import ROOT, P, wordmark, logo_mark
from PIL import Image
L = f"{ROOT}/logos"

def render(svg, out, W, H, transparent=True):
    html = f"{L}/_r.html"
    open(html,"w").write(f'<html><body style="margin:0;background:transparent">{svg.replace("<svg ", f"<svg width={chr(34)}{W}{chr(34)} height={chr(34)}{H}{chr(34)} ",1)}</body></html>')
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=1",
                    "--default-background-color=00000000",f"--window-size={W},{H+300}",f"--screenshot={out}",f"file://{html}"],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    Image.open(out).crop((0,0,W,H)).save(out); os.remove(html)

def strip_hw(svg): 
    import re; return re.sub(r' (width|height)="\d+"', '', svg, count=2)

VARIANTS = {"wordmark_light": dict(light=True), "wordmark_dark": dict(light=False), "wordmark_mono_white": dict(mono="#FFFFFF"), "wordmark_mono_black": dict(mono="#000000"),
            "lockup_tagline_light": dict(light=True, tagline=True), "lockup_tagline_dark": dict(light=False, tagline=True)}

def fg_layer():  # Android adaptive foreground: art inside the 66/108 safe circle, transparent
    m = logo_mark(256, bg=False)
    return m.replace('viewBox="0 0 256 256"', 'viewBox="-64 -64 384 384"')
def bg_layer():
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["dusk"]}"/><stop offset=".62" stop-color="#6B4A6E"/><stop offset="1" stop-color="{P["horizon"]}"/></linearGradient></defs><rect width="108" height="108" fill="url(#g)"/></svg>'

if __name__ == "__main__":
    for k, kw in VARIANTS.items():
        svg = strip_hw(wordmark(120, **kw)); open(f"{L}/{k}.svg","w").write(svg)
        vb = [float(v) for v in svg.split('viewBox="')[1].split('"')[0].split()]; W = 1200; H = int(W*vb[3]/vb[2])
        render(svg, f"{L}/{k}.png", W, H)
    mark = strip_hw(logo_mark(256)); open(f"{L}/mark.svg","w").write(mark)
    render(mark, f"{L}/app/icon_master_1024.png", 1024, 1024)
    master = Image.open(f"{L}/app/icon_master_1024.png").convert("RGB")  # iOS: no alpha
    ios = {"AppIcon-1024.png":1024,"AppIcon-180.png":180,"AppIcon-167.png":167,"AppIcon-152.png":152,"AppIcon-120.png":120,"AppIcon-87.png":87,
           "AppIcon-80.png":80,"AppIcon-76.png":76,"AppIcon-60.png":60,"AppIcon-58.png":58,"AppIcon-40.png":40,"AppIcon-29.png":29,"AppIcon-20.png":20}
    for n,s in ios.items(): master.resize((s,s), Image.LANCZOS).save(f"{L}/app/ios/{n}")
    json.dump({"images":[{"filename":n,"size":f"{s}x{s}px"} for n,s in ios.items()],"note":"Single-size 1024 is enough for Xcode 14+; smaller sizes provided for older targets."},open(f"{L}/app/ios/Contents-sizes.json","w"),indent=1)
    open(f"{L}/app/android/ic_launcher_foreground.svg","w").write(fg_layer()); open(f"{L}/app/android/ic_launcher_background.svg","w").write(bg_layer())
    render(fg_layer(), f"{L}/app/android/ic_launcher_foreground_432.png", 432, 432)
    render(bg_layer(), f"{L}/app/android/ic_launcher_background_432.png", 432, 432)
    master.resize((512,512), Image.LANCZOS).save(f"{L}/app/android/play_store_icon_512.png")
    for dpi,s in {"mdpi":48,"hdpi":72,"xhdpi":96,"xxhdpi":144,"xxxhdpi":192}.items(): master.resize((s,s), Image.LANCZOS).save(f"{L}/app/android/ic_launcher_{dpi}_{s}.png")
    # web
    for s in (16,32,48): master.resize((s,s), Image.LANCZOS).save(f"{L}/app/web/favicon-{s}.png")
    master.save(f"{L}/app/web/favicon.ico", sizes=[(16,16),(32,32),(48,48)])
    master.resize((180,180), Image.LANCZOS).save(f"{L}/app/web/apple-touch-icon.png")
    for s in (192,512): master.resize((s,s), Image.LANCZOS).save(f"{L}/app/web/pwa-{s}.png")
    # maskable: art within 80% safe zone
    bg = Image.open(f"{L}/app/android/ic_launcher_background_432.png").convert("RGBA").resize((512,512)); fg = Image.open(f"{L}/app/android/ic_launcher_foreground_432.png").convert("RGBA").resize((512,512))
    Image.alpha_composite(bg, fg).convert("RGB").save(f"{L}/app/web/pwa-maskable-512.png")
    json.dump({"name":"Gidi++","short_name":"Gidi++","orientation":"landscape","display":"fullscreen","background_color":P["ink"],"theme_color":P["dusk"],"start_url":"./",
               "icons":[{"src":"pwa-192.png","sizes":"192x192","type":"image/png"},{"src":"pwa-512.png","sizes":"512x512","type":"image/png"},{"src":"pwa-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},
              open(f"{L}/app/web/manifest.webmanifest","w"), indent=1)
    print("ok")
