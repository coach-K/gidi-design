# Splash + District-intro screens (G-Prototype PRs #86 / #87)

| File | Size | Used by |
|---|---|---|
| `bg_splash_desktop_blur.png` | 1920×1080 | `SplashScreenView` (desktop / WebGL) |
| `bg_splash_phone_blur.png` | 2340×1080 | `SplashScreenView` (`Application.isMobilePlatform`) |
| `bg_intro_blur.png` | 1920×1080 | `DistrictIntroView` (`bg_intro_blur`) |
| `bg_intro_phone_blur.png` | 2340×1080 | phone variant: `DistrictIntroView` currently loads only `bg_intro_blur`; add a mobile switch like the splash to use it |
| `district_subtitles.md` | — | subtitle copy for LASTMA only / KAI only / no enforcement |

Drop into `Resources/UI/Screens/1x/` (ScreenKit looks there first). These are full-screen 1x art: there is no 2x.

**Art:** abstract brand backgrounds made from gradients, soft bokeh and blurred street/skyline shapes in the dusk palette (`#0F1219` ink, `#2B2F5C` dusk, `#F28C4B` horizon, gold `#E8B21E` / `#FAE69E`, small accents of teal `#59D9B8` and LASTMA pink `#E07CC0`). No screenshots, text, logos or people. Each pair is the same scene: the desktop file is the centre 1920 crop of the 2340 phone file, so content stays safe on both. Edges fade to ink for notches and the home indicator. Splash still gets the code's heavy dim (rgba 4,6,10,.72) on top. Regenerate with `tools/gen_screen_bgs.py`.

**Import settings:** Texture Type **Sprite (2D and UI)**, Single, Mesh Full Rect, Pixels Per Unit 100, **Generate Mip Maps off**, **Wrap Mode Clamp**, Filter Bilinear, sRGB on, Max Size 4096 (so 2340 isn't downscaled to 2048). Compression: soft gradients band with ASTC/ETC at high block sizes, so use **None** or high quality (ASTC 4×4 on mobile, BC7 on desktop). The PNGs carry a little grain to hide banding. Image: `preserveAspect` off, stretch to fill, or an Aspect Ratio Fitter set to Envelope Parent.
