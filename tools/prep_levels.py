"""Mockup backgrounds built from the real level screenshots in reference/levels/Lxx.png (1600x720, current build camera):
inpaint the old in-game HUD, crop/scale to 1920x1080 and 2340x1080, then grade toward the art doc (Lagos dusk)."""
import cv2, numpy as np, os
from PIL import Image, ImageFilter, ImageEnhance
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{R}/assets/bg"; os.makedirs(OUT, exist_ok=True)
EXTRA = {"L02": [(288,602,1314,652)]}  # level-specific toast captured in the screenshot
HUD_BOXES = [(0,0,300,158),(495,10,918,126),(1100,10,1376,162),(503,600,1068,676),(1466,684,1600,720),(762,682,836,714)]

def clean(level):
    """Old HUD removal. Top boxes sit over horizontal lane stripes, so each masked pixel takes the median
    colour of its own row (outside the mask, same road segment) plus a little noise; small bottom
    boxes use cv2 Telea inpainting."""
    src = cv2.imread(f"{R}/reference/levels/{level}.png")
    out = src.copy()
    m = np.zeros(src.shape[:2], np.uint8)
    for x0,y0,x1,y1 in HUD_BOXES: m[y0:y1, x0:x1] = 255
    rng = np.random.default_rng(1)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape
    # road edges are straight lines in the perspective view: fit them on unmasked rows
    ys, xl, xr = [], [], []
    for y in range(180, 600, 6):
        road = np.where(gray[y] > 70)[0]
        if len(road) > 200: ys.append(y); xl.append(road[0]); xr.append(road[-1])
    fl, fr = np.polyfit(ys, xl, 1), np.polyfit(ys, xr, 1)
    top_m = np.zeros_like(m)
    for x0,y0,x1,y1 in HUD_BOXES[:3]: top_m[y0:y1, x0:x1] = 255
    for y in range(0, 720):
        if not top_m[y].any(): continue
        L, Rr = int(np.polyval(fl, y)), int(np.polyval(fr, y))
        xs = np.arange(W); ok = top_m[y] == 0
        inroad = (xs >= L) & (xs <= Rr)
        road_px = src[y][ok & inroad]; sh_px = src[y][ok & ~inroad]
        rmed = np.median(road_px, axis=0) if len(road_px) else np.array([90, 90, 90])
        smed = np.median(sh_px, axis=0) if len(sh_px) else np.array([30, 30, 30])
        sel = ~ok
        fill = np.where(inroad[sel][:, None], rmed, smed) + rng.normal(0, 3, (sel.sum(), 3))
        out[y][sel] = np.clip(fill, 0, 255).astype(np.uint8)
    # hint bar (near road, uniform asphalt with a soft gradient): interpolate each row between its left/right neighbours
    boxes = [HUD_BOXES[3]] + EXTRA.get(level, [])
    for (x0, y0, x1, y1) in boxes:
      for y in range(y0, y1):
          a = src[y, x0-24:x0-4].astype(np.float32).mean(0); b = src[y, x1+4:x1+24].astype(np.float32).mean(0)
          t = np.linspace(0, 1, x1-x0)[:, None]
          base = a*(1-t) + b*t
          donor = src[y-(y1-y0)-4, x0:x1].astype(np.float32)  # texture from the clean rows just above
          tex = donor - cv2.blur(donor[None], (61,1))[0]
          big = cv2.dilate((np.abs(tex).max(1) > 14).astype(np.uint8)[None], np.ones((1,41),np.uint8))[0] > 0
          tex[big] = 0  # drop characters/props from the donor rows (texture only)
          out[y, x0:x1] = np.clip(base + tex*0.9 + rng.normal(0, 1.5, (x1-x0, 3)), 0, 255).astype(np.uint8)
    mb = np.zeros_like(m)
    for x0,y0,x1,y1 in HUD_BOXES[4:]: mb[y0:y1, x0:x1] = 255
    return cv2.inpaint(out, mb, 7, cv2.INPAINT_TELEA)

def grade(bgr):
    """Dusk grade: cool shadows (#2A2440), warm highlights (#FFC98A), mild S-curve, vignette, unsharp."""
    f = bgr.astype(np.float32) / 255.0
    lum = (0.114*f[...,0] + 0.587*f[...,1] + 0.299*f[...,2])[..., None]
    shadow = np.array([0x40, 0x24, 0x2A], np.float32) / 255.0  # BGR of #2A2440
    high   = np.array([0x8A, 0xC9, 0xFF], np.float32) / 255.0  # BGR of #FFC98A
    f = f * (1 - 0.32*(1-lum)) + shadow * 0.32*(1-lum)        # tint shadows
    f = f * (1 - 0.25*lum) + f * high * 0.25*lum * 1.2        # warm highlights
    f = 0.5 + (f - 0.5) * 1.10                                 # contrast
    f = f / (1 + 0.15*f) * 1.12                                # soft shoulder
    h, w = f.shape[:2]
    g = np.linspace(0, 1, h)[:, None, None]  # dusk sky bounce: violet top -> warm low
    f = f * (1 - 0.10) + (np.array([0x5C,0x2F,0x2B],np.float32)/255*(1-g) + np.array([0x4B,0x8C,0xF2],np.float32)/255*g) * 0.10
    yy, xx = np.mgrid[0:h, 0:w]
    v = 1 - 0.32*(((xx/w - 0.5)**2)*1.4 + ((yy/h - 0.55)**2)*1.6)
    f = f * v[..., None]
    out = np.clip(f*255, 0, 255).astype(np.uint8)
    blur = cv2.GaussianBlur(out, (0,0), 2.0)
    return cv2.addWeighted(out, 1.45, blur, -0.45, 0)            # unsharp after 1.5x upscale

def frame(img, W):
    up = cv2.resize(img, (2400, 1080), interpolation=cv2.INTER_CUBIC)
    x0 = (2400 - W) // 2
    return up[:, x0:x0+W]

USE = {"hud": "L05", "home": "L09", "shop": "L04", "gameover": "L05"}
if __name__ == "__main__":
    cache = {}
    for key, lv in USE.items():
        if lv not in cache: cache[lv] = clean(lv)
        for name, W in (("desktop",1920),("phone",2340)):
            im = grade(frame(cache[lv], W))
            if key == "home": im = cv2.GaussianBlur(im, (0,0), 2.2)
            if key in ("shop","gameover"): im = cv2.GaussianBlur(im, (0,0), 9)
            cv2.imwrite(f"{OUT}/lv_{key}_{name}.png", im)
    print(USE)

def all_levels():
    """Every level L01-L10: cleaned + dusk grade (desktop/phone) and a 960x540 card thumbnail; plus blurred variants for menu screens."""
    for i in range(1, 11):
        lv = f"L{i:02d}"
        try: c = clean(lv)
        except Exception as e:
            print("fallback inpaint", lv, e); src = cv2.imread(f"{R}/reference/levels/{lv}.png")
            m = np.zeros(src.shape[:2], np.uint8)
            for x0,y0,x1,y1 in HUD_BOXES: m[y0:y1, x0:x1] = 255
            c = cv2.inpaint(src, m, 9, cv2.INPAINT_TELEA)
        for name, W in (("desktop",1920),("phone",2340)):
            im = grade(frame(c, W)); cv2.imwrite(f"{OUT}/{lv}_{name}.png", im)
            cv2.imwrite(f"{OUT}/{lv}_{name}_blur.png", cv2.GaussianBlur(im, (0,0), 9))
        d = cv2.imread(f"{OUT}/{lv}_desktop.png"); cv2.imwrite(f"{OUT}/{lv}_card.jpg", cv2.resize(d, (960,540), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 86])

if __name__ == "__main__":
    all_levels()
