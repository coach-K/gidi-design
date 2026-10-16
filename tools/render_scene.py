"""Draws Gidi++ scenes in the build's 3D perspective (pinhole camera, pitch 65°) with PIL + numpy.
Matches the framing of reference/levels/L08_phone_landscape.jpg (reference only, not used as a background).
Usage: python3 render_scene.py  -> assets/bg/scene_{desktop,phone}[_variant].png"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS = 2                      # supersampling
PITCH = math.radians(65)    # TailCameraFollow.fixedEulerAngles.x
CAM_H = 15.0                # HudLandscapeConfig.cameraHeight (wide stage, 8 lanes: 20)
VFOV = math.radians(52)     # HudLandscapeConfig.cameraVerticalFov (wide stage: 58)

class Cam:
    def __init__(s, W, H):
        s.W, s.H = W, H
        s.f = (H / 2) / math.tan(VFOV / 2)
        s.fw = np.array([0, -math.sin(PITCH), math.cos(PITCH)])
        s.up = np.array([0, math.cos(PITCH), math.sin(PITCH)])
        s.pos = np.array([0, CAM_H, 0.0])
    def p(s, x, y, z):
        v = np.array([x, y, z]) - s.pos
        zc = v @ s.fw; yc = v @ s.up
        zc = max(zc, 0.1)
        return (s.W / 2 + s.f * v[0] / zc, s.H / 2 - s.f * yc / zc)
    def ground_z(s, sy):
        a = math.atan((sy - s.H / 2) / s.f)
        return CAM_H / math.tan(PITCH + a)
    def scale(s, z):  # px per metre at ground depth z
        x0 = s.p(0, 0, z)[0]; x1 = s.p(1, 0, z)[0]; return x1 - x0

def hexc(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
def mix(c1, c2, t):
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3)) + (255,)

PAL = dict(asph=hexc('#2B2C34'), asph_far=hexc('#3A3550'), lat=hexc('#7A4630'), kerb=hexc('#B9B2A3'),
           pave=hexc('#8A7F70'), median=hexc('#A8977E'), line=hexc('#E8E2D0'), sky1=hexc('#2B2F5C'), sky2=hexc('#F28C4B'),
           shadow=hexc('#0C0A16'), danfo=hexc('#F0A830'), key=hexc('#FFB070'), hl=hexc('#FFC98A'))

def poly(d, cam, pts, fill):
    d.polygon([cam.p(*q) for q in pts], fill=fill)

def render(W, H, seed=3, lanes=6, crowd=True, traffic=1.0, cam_h=15.0, vfov=52.0):
    global CAM_H, VFOV
    CAM_H, VFOV = cam_h, math.radians(vfov)
    rnd = random.Random(seed)
    w, h = W * SS, H * SS
    cam = Cam(w, h)
    img = Image.new('RGBA', (w, h), PAL['lat'])
    d = ImageDraw.Draw(img)
    ROADX = 0.47 * 2340 * SS / cam.scale(cam.ground_z(h)) * (H / 1080)  # road ends at ~3%/97% of a 19.5:9 frame, as in L08
    z_kerb = cam.ground_z(0.765 * h)                 # near kerb (crowd stands here, as in the build)
    z_top = cam.ground_z(0.0)
    lane_w, med_w = 3.4, 1.1
    zs = []; z = z_kerb
    for i in range(lanes):
        zs.append((z, z + lane_w)); z += lane_w
        if i % 2 == 1 and i < lanes - 1: z += med_w
    z_far = z                                        # far kerb / goal shore
    # sky + far shore skyline (only shows if the goal is near the top)
    sky = Image.new('RGBA', (w, h)); sd = ImageDraw.Draw(sky)
    for y in range(h):
        sd.line([(0, y), (w, y)], fill=mix(PAL['sky1'], PAL['sky2'], min(1, y / (0.5 * h))))
    img.alpha_composite(sky)
    # ground: laterite shoulders + pavements
    poly(d, cam, [(-80, 0, z_kerb - 30), (80, 0, z_kerb - 30), (80, 0, z_far + 60), (-80, 0, z_far + 60)], PAL['lat'])
    # dust/texture noise on laterite
    noise = (np.random.default_rng(seed).normal(0, 9, (h, w))).astype(np.int16)
    # pavements
    poly(d, cam, [(-80, 0, z_kerb - 6), (80, 0, z_kerb - 6), (80, 0, z_kerb), (-80, 0, z_kerb)], PAL['pave'])
    poly(d, cam, [(-80, 0, z_far), (80, 0, z_far), (80, 0, z_far + 7), (-80, 0, z_far + 7)], PAL['pave'])
    for xx in np.arange(-80, 80, 1.6):
        a0, a1 = cam.p(xx, 0, z_kerb - 6), cam.p(xx, 0, z_kerb)
        d.line([a0, a1], fill=(120, 110, 98, 255), width=SS)
    for zz in np.arange(z_kerb - 6, z_kerb, 1.6):
        d.line([cam.p(-80, 0, zz), cam.p(80, 0, zz)], fill=(120, 110, 98, 255), width=SS)
    # road slab (finite X like the build's play area)
    for (a, b) in zs:
        poly(d, cam, [(-ROADX, 0, a), (ROADX, 0, a), (ROADX, 0, b), (-ROADX, 0, b)], PAL['asph'])
    for i in range(1, len(zs)):
        a = zs[i - 1][1]; b = zs[i][0]
        if b - a > 0.05:
            poly(d, cam, [(-ROADX, 0, a), (ROADX, 0, a), (ROADX, 0, b), (-ROADX, 0, b)], PAL['median'])
            poly(d, cam, [(-ROADX, 0.18, a), (ROADX, 0.18, a), (ROADX, 0.18, a + 0.15), (-ROADX, 0.18, a + 0.15)], PAL['kerb'])
    # kerbs (raised strip with lit top + dark face)
    for zk, face in ((z_kerb, -1), (z_far, 1)):
        poly(d, cam, [(-80, 0.18, zk - 0.35 * (face < 0)), (80, 0.18, zk - 0.35 * (face < 0)), (80, 0.18, zk + 0.35 * (face > 0)), (-80, 0.18, zk + 0.35 * (face > 0))], PAL['kerb'])
    # lane dashes
    for (a, b) in zs:
        zm = (a + b) / 2
    for i, (a, b) in enumerate(zs):
        if i % 2 == 0 and i + 1 < len(zs) and abs(zs[i + 1][0] - b) < 0.05:
            for x in np.arange(-ROADX, ROADX, 6):
                poly(d, cam, [(x, 0, b - 0.08), (x + 3, 0, b - 0.08), (x + 3, 0, b + 0.08), (x, 0, b + 0.08)], (232, 226, 208, 170))
    # edge lines
    for (a, b) in zs:
        for zz in (a + 0.3, b - 0.3):
            poly(d, cam, [(-ROADX, 0, zz - 0.06), (ROADX, 0, zz - 0.06), (ROADX, 0, zz + 0.06), (-ROADX, 0, zz + 0.06)], (240, 228, 66, 90))
    # far-shore props: bus shelter, palms, kiosk boxes
    props = []
    for x in np.arange(-60, 60, 9 + rnd.random() * 4):
        props.append(('build', x, z_far + 9 + rnd.random() * 3, rnd))
    # traffic
    cars = []
    if traffic:
        for i, (a, b) in enumerate(zs):
            right = i % 2 == 0
            x = -ROADX + rnd.random() * 10
            while x < ROADX:
                kind = rnd.choices(['danfo', 'car', 'truck', 'keke'], [3, 3, 1.0, 1.5])[0]
                L = dict(danfo=5.2, car=4.4, truck=7.0, keke=2.8)[kind]
                if rnd.random() < 0.38 * traffic:
                    cars.append((kind, x + L / 2, (a + b) / 2, right, rnd.random()))
                x += L + 6 + rnd.random() * 14
    # shadows layer (soft, cast toward +x/-z from a low key light on the left)
    shad = Image.new('L', (w, h), 0); sdraw = ImageDraw.Draw(shad)
    def box_shadow(cx, cz, L, Wd, Ht):
        off = Ht * 0.9
        q = [(cx - L / 2, 0, cz - Wd / 2), (cx + L / 2 + off, 0, cz - Wd / 2 - off * 0.3), (cx + L / 2 + off, 0, cz + Wd / 2 - off * 0.3), (cx - L / 2, 0, cz + Wd / 2)]
        sdraw.polygon([cam.p(*p) for p in q], fill=150)
    people = []
    if crowd:
        people.append(('baba', 0.0, z_kerb + 0.7))
        for k in range(7):
            people.append(('npc', -3.2 + (k % 4) * 1.6 + rnd.uniform(-.3, .3), z_kerb - 1.2 - (k // 4) * 1.4 + rnd.uniform(-.2, .2)))
    for kind, cx, cz, right, r in cars:
        L, Wd, Ht = dict(danfo=(5.2, 2.1, 2.4), car=(4.4, 1.85, 1.45), truck=(7.0, 2.5, 3.2), keke=(2.8, 1.4, 1.7))[kind]
        box_shadow(cx, cz, L, Wd, Ht)
    for kind, x, z in people:
        c = cam.p(x + 0.5, 0, z); s = cam.scale(z)
        sdraw.ellipse([c[0] - 0.7 * s, c[1] - 0.25 * s, c[0] + 0.9 * s, c[1] + 0.25 * s], fill=140)
    shad = shad.filter(ImageFilter.GaussianBlur(6 * SS))
    tint = Image.new('RGBA', (w, h), PAL['shadow'])
    tint.putalpha(shad.point(lambda v: int(v * 1.2)))
    img.alpha_composite(tint)
    d = ImageDraw.Draw(img)
    # draw far → near
    items = [('car',) + c for c in cars] + [('person',) + p for p in people] + [('prop',) + p for p in props]
    def zkey(it):
        return -(it[3] if it[0] == 'car' else it[3] if it[0] == 'person' else it[3])
    items.sort(key=lambda it: -(it[3]))
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for it in items:
        if it[0] == 'car':
            draw_vehicle(d, gd, cam, *it[1:])
        elif it[0] == 'person':
            draw_person(d, cam, it[1], it[2], it[3], rnd)
        else:
            draw_building(d, cam, it[2], it[3], it[4])
    glow = glow.filter(ImageFilter.GaussianBlur(10 * SS))
    img = Image.alpha_composite(img, glow)
    # grade: warm key from left, cool shadow vignette, light grain
    arr = np.asarray(img).astype(np.float32)
    xs = np.linspace(0, 1, w)[None, :, None]; ys = np.linspace(0, 1, h)[:, None, None]
    warm = np.array([255, 176, 112], np.float32)
    arr[..., :3] = arr[..., :3] * (0.86 + 0.22 * (1 - xs)) + warm * 0.06 * (1 - xs)
    vig = 1 - 0.38 * (((xs - 0.5) ** 2) * 1.6 + ((ys - 0.55) ** 2) * 1.8)
    arr[..., :3] *= vig
    arr[..., :3] += np.random.default_rng(seed + 1).normal(0, 5, (h, w, 1))
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img.resize((W, H), Image.LANCZOS), cam, z_kerb

def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)

def cuboid(d, cam, x0, x1, y0, y1, z0, z1, col, top_k=1.18, front_k=0.78, side_k=0.62):
    # faces visible from a camera above and in front (-z) : top, front (z0), side facing camera centre
    P = lambda x, y, z: cam.p(x, y, z)
    side_x = x0 if (x0 + x1) / 2 > 0 else x1
    d.polygon([P(side_x, y0, z0), P(side_x, y0, z1), P(side_x, y1, z1), P(side_x, y1, z0)], fill=shade(col, side_k))
    d.polygon([P(x0, y0, z0), P(x1, y0, z0), P(x1, y1, z0), P(x0, y1, z0)], fill=shade(col, front_k))
    d.polygon([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], fill=shade(col, top_k))

def draw_vehicle(d, gd, cam, kind, cx, cz, right, r):
    L, Wd, Ht = dict(danfo=(5.2, 2.1, 2.4), car=(4.4, 1.85, 1.45), truck=(7.0, 2.5, 3.2), keke=(2.8, 1.4, 1.7))[kind]
    col = dict(danfo=PAL['danfo'], car=[hexc('#C9CCD2'), hexc('#7C2E2E'), hexc('#1F2A3A'), hexc('#3A5A80')][int(r * 4)],
               truck=hexc('#3E4A3A'), keke=hexc('#2E7A68'))[kind]
    x0, x1, z0, z1 = cx - L / 2, cx + L / 2, cz - Wd / 2, cz + Wd / 2
    s = 1 if right else -1
    # wheels
    for wx in (x0 + 0.8, x1 - 0.8):
        p = cam.p(wx, 0.35, z0); sc = cam.scale(cz)
        d.ellipse([p[0] - 0.42 * sc, p[1] - 0.3 * sc, p[0] + 0.42 * sc, p[1] + 0.3 * sc], fill=(18, 18, 20, 255))
    if kind == 'car':
        cuboid(d, cam, x0, x1, 0.3, 0.9, z0, z1, col)
        cx0, cx1 = (x0 + 1.1, x1 - 1.4) if right else (x0 + 1.4, x1 - 1.1)
        cuboid(d, cam, cx0, cx1, 0.9, Ht, z0 + 0.15, z1 - 0.15, hexc('#1A1D24'), 1.6, 1.2, 1.0)
        cuboid(d, cam, cx0 + 0.2, cx1 - 0.2, Ht - 0.02, Ht, z0 + 0.25, z1 - 0.25, col)
    elif kind == 'danfo':
        cuboid(d, cam, x0, x1, 0.35, Ht, z0, z1, col)
        # window band + black stripes
        cuboid(d, cam, x0 + 0.3, x1 - 0.3, 1.45, 2.05, z0 - 0.01, z0 + 0.01, hexc('#15171C'), 1, 1, 1)
        cuboid(d, cam, x0, x1, 1.1, 1.22, z0 - 0.02, z0, hexc('#111111'), 1, 1, 1)
        for rx in (x0 + 1.2, (x0 + x1) / 2, x1 - 1.3):  # roof rack bars
            cuboid(d, cam, rx, rx + 0.08, Ht, Ht + 0.08, z0 + 0.4, z1 - 0.4, hexc('#8A6A2A'))
    elif kind == 'truck':
        cab = (x1 - 2.0, x1) if right else (x0, x0 + 2.0)
        bed = (x0, x1 - 2.1) if right else (x0 + 2.1, x1)
        cuboid(d, cam, bed[0], bed[1], 0.6, Ht, z0, z1, hexc('#4C5446'))
        cuboid(d, cam, cab[0], cab[1], 0.5, Ht * 0.8, z0 + 0.05, z1 - 0.05, col)
    else:  # keke
        cuboid(d, cam, x0, x1, 0.3, Ht, z0, z1, col)
        cuboid(d, cam, x0, x1, Ht, Ht + 0.15, z0, z1, hexc('#F0E442'))
    # headlights + glow on the front end
    fx = x1 if right else x0
    for zz in (z0 + 0.35, z1 - 0.35):
        p = cam.p(fx, 0.7, zz); sc = cam.scale(cz)
        d.ellipse([p[0] - 0.16 * sc, p[1] - 0.12 * sc, p[0] + 0.16 * sc, p[1] + 0.12 * sc], fill=(255, 241, 214, 255))
    p = cam.p(fx + s * 1.2, 0, cz); sc = cam.scale(cz)
    gd.ellipse([p[0] - 1.3 * sc, p[1] - 0.8 * sc, p[0] + 1.3 * sc, p[1] + 0.8 * sc], fill=(255, 214, 160, 34))
    # tail lights
    bx = x0 if right else x1
    for zz in (z0 + 0.3, z1 - 0.3):
        p = cam.p(bx, 0.75, zz); sc = cam.scale(cz)
        d.ellipse([p[0] - 0.1 * sc, p[1] - 0.08 * sc, p[0] + 0.1 * sc, p[1] + 0.08 * sc], fill=(220, 40, 40, 255))

def draw_person(d, cam, kind, x, z, rnd):
    k = 1.8 if kind != 'baba' else 2.2            # readability scale (game characters read larger than life)
    if kind == 'baba':
        robe, trim, skin, cap = hexc('#F2EBDD'), hexc('#E8B21E'), hexc('#6B4128'), hexc('#7C2E2E')
    else:
        robe = rnd.choice([hexc('#56B4E9'), hexc('#E07CC0'), hexc('#2E7A68'), hexc('#D55E00'), hexc('#F0E442'), hexc('#3A5A80'), hexc('#C9CCD2')])
        trim, skin = shade(robe, .7), rnd.choice([hexc('#5A3420'), hexc('#7A4A2E'), hexc('#4A2A18')])
        cap = rnd.choice([None, None, hexc('#222222'), hexc('#E8B21E')])
    sc = cam.scale(z)
    f = cam.p(x, 0, z); sh = cam.p(x, 1.35 * k, z); hd = cam.p(x, 1.7 * k, z)
    sw = 0.32 * k * sc * (1.5 if kind == 'baba' else 1)
    # legs / lower robe
    d.polygon([(f[0] - sw * .55, f[1]), (f[0] + sw * .55, f[1]), (sh[0] + sw * .8, sh[1]), (sh[0] - sw * .8, sh[1])], fill=shade(robe, .7))
    # shoulders seen from above (ellipse) with light from the left
    d.ellipse([sh[0] - sw, sh[1] - sw * .55, sh[0] + sw, sh[1] + sw * .55], fill=shade(robe, .85))
    d.ellipse([sh[0] - sw, sh[1] - sw * .6, sh[0] + sw * .6, sh[1] + sw * .35], fill=robe)
    if kind == 'baba':
        d.line([(sh[0], sh[1] - sw * .4), (sh[0], sh[1] + sw * .5)], fill=trim, width=max(3, int(.07 * sc * k)))
        d.arc([sh[0] - sw * .8, sh[1] - sw * .45, sh[0] + sw * .8, sh[1] + sw * .45], 200, 340, fill=trim, width=max(2, int(.05 * sc * k)))
    r = 0.15 * k * sc
    d.ellipse([hd[0] - r, hd[1] - r, hd[0] + r, hd[1] + r], fill=shade(skin, .85))
    d.ellipse([hd[0] - r, hd[1] - r, hd[0] + r * .5, hd[1] + r * .5], fill=skin)
    if cap:
        d.ellipse([hd[0] - r * .85, hd[1] - r * 1.05, hd[0] + r * .85, hd[1] + r * .3], fill=cap)

def draw_building(d, cam, x, z, rnd):
    Wd, Dp, Ht = 6 + rnd.random() * 5, 5, 4 + rnd.random() * 7
    col = rnd.choice([hexc('#6E5A7E'), hexc('#7A4630'), hexc('#5C5A66'), hexc('#8A6A50'), hexc('#4E5A72')])
    cuboid(d, cam, x, x + Wd, 0, Ht, z, z + Dp, col, 1.1, 0.8, 0.6)
    for wy in np.arange(1.2, Ht - 0.8, 1.6):
        for wx in np.arange(x + 0.8, x + Wd - 0.8, 1.6):
            lit = rnd.random() < 0.45
            p0 = cam.p(wx, wy, z - 0.01); p1 = cam.p(wx + 0.7, wy + 0.8, z - 0.01)
            d.rectangle([min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])], fill=(255, 201, 138, 255) if lit else (40, 38, 52, 255))

if __name__ == '__main__':
    out = os.path.join(ROOT, 'assets', 'bg'); os.makedirs(out, exist_ok=True)
    for name, W in (('desktop', 1920), ('phone', 2340)):
        # in-run: L8 Third Mainland = wide stage (8 lanes) -> height 20 m, FOV 58°, as in L08_phone_landscape.jpg
        im, cam, zk = render(W, 1080, seed=5, lanes=8, cam_h=20.0, vfov=58.0); im.save(os.path.join(out, f'scene_{name}.png'))
        im2, _, _ = render(W, 1080, seed=11, lanes=6, traffic=0.7); im2.save(os.path.join(out, f'scene2_{name}.png'))
        print(name, 'kerb z', round(zk, 1), 'top z', round(cam.ground_z(0), 1))
