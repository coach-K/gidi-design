"""Builds mockup backgrounds from REAL in-game captures in reference/levels/.
The old prototype HUD baked into L08_phone_landscape.jpg is removed by inpainting (cv2.INPAINT_TELEA)."""
import cv2, numpy as np, os
R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = cv2.imread(f"{R}/reference/levels/L08_phone_landscape.jpg")  # 1640x720
m = np.zeros(src.shape[:2], np.uint8)
for x0,y0,x1,y1 in [(0,0,400,64),(1385,0,1640,232),(1555,0,1640,325),(115,440,288,612),(1288,386,1542,634),(555,608,1080,654),(1510,688,1640,720),(785,690,855,714)]:
    m[y0:y1, x0:x1] = 255
clean = cv2.inpaint(src, m, 9, cv2.INPAINT_TELEA)
cv2.imwrite(f"{R}/assets/bg/l08_clean.png", clean)

TOP = 200  # HUD row (176) + gap: no active lane above this line
def frame(img, W, H, _x0=None, _shift=None):
    """Scale the capture so the whole road fits H-TOP, centre the road (x=820 in the capture),
    extend the dark shoulders sideways (reflect), and fill the top TOP px with the far shoulder
    stretched + darkened (camera-aim proposal: far curb below the HUD row)."""
    s = (H - TOP) / img.shape[0]
    sc = cv2.resize(img, (round(img.shape[1] * s), H - TOP), interpolation=cv2.INTER_CUBIC)
    off = W // 2 - round(820 * s)
    left, right = max(0, off), max(0, W - off - sc.shape[1])
    sc = cv2.copyMakeBorder(sc, 0, 0, left, right, cv2.BORDER_REFLECT)
    x = left - off
    body = sc[:, x:x + W]
    row = cv2.blur(body[:4], (241, 1))           # wide horizontal blur: no car/prop smear
    top = cv2.resize(row, (W, TOP), interpolation=cv2.INTER_LINEAR)
    grad = np.linspace(0.18, 0.55, TOP)[:, None, None]
    return np.vstack([(top * grad).astype(np.uint8), body])
hd = frame(clean, 1920, 1080, 180, 140); cv2.imwrite(f"{R}/assets/bg/hud_desktop.png", hd)
hp = frame(clean, 2340, 1080, 20, 140);  cv2.imwrite(f"{R}/assets/bg/hud_phone.png", hp)
for name, W in (("desktop",1920),("phone",2340)):
    base = hd if W == 1920 else hp
    cv2.imwrite(f"{R}/assets/bg/home_{name}.png", cv2.GaussianBlur(base, (0,0), 5))
    cv2.imwrite(f"{R}/assets/bg/gameover_{name}.png", cv2.GaussianBlur(base, (0,0), 16))
    goal = cv2.imread(f"{R}/reference/levels/L01c_goal.png")
    h, w = goal.shape[:2]; ch = int(w * 1080 / W)
    g = cv2.resize(goal[max(0,(h-ch)//2):(h+ch)//2] if ch < h else goal, (W, 1080))
    cv2.imwrite(f"{R}/assets/bg/shop_{name}.png", cv2.GaussianBlur(g, (0,0), 14))
print("ok")
