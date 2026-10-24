# RT-116 District intro: clean per-level backgrounds + card spec

Replaces the blurred abstract `bg_intro_blur` / `bg_intro_phone_blur` (dc19817) with **one clean background per district**, made from the real level screenshots (cleaned + dusk-graded, same source as the site's Levels page: `assets/bg/Lxx_*.png`, `tools/prep_levels.py`). Not blurred. Each has a **calm zone** baked in behind the card: a feathered rounded rect (card + 110/80 px, feather 90 px) darkened 58% and desaturated 35%, plus a light ink edge vignette. Generator: `tools/gen_intro_bgs.py`. Preview: `exports/intro-clean-{desktop,phone}.png` (L6).

## Files (`exports/unity/screens/intro/`, drop into `Resources/UI/Screens/1x/`)
20 PNGs: `bg_intro_L01.png` … `bg_intro_L10.png` (1920×1080) and `bg_intro_L01_phone.png` … `bg_intro_L10_phone.png` (2340×1080). Full-screen 1x art, no 2x, no 9-slice. Import: Sprite (2D and UI), Mesh Full Rect, PPU 100, mipmaps off, Clamp, Bilinear, Max Size 4096, compression None / ASTC 4×4 / BC7.

## Which background each level loads
Name = `bg_intro_L` + 2-digit `levelNumber`; add `_phone` when `Application.isMobilePlatform` (or screen aspect ≥ 1.9), same switch as the splash. Fallback: `bg_intro_blur`, then `ScreenKit.Night`.

| Level | Kicker | Title (`f.Location`) | Subtitle (`DistrictIntroRules.Subtitle`, from `district_subtitles.md`) | Desktop | Phone |
|---|---|---|---|---|---|
| L1 | DISTRICT 1 OF 10 | Agege Bus Stop | No wahala for road today: no LASTMA, no KAI. Just find your gap. | `bg_intro_L01` | `bg_intro_L01_phone` |
| L2 | DISTRICT 2 OF 10 | Surulere Way | No wahala for road today: no LASTMA, no KAI. Just find your gap. | `bg_intro_L02` | `bg_intro_L02_phone` |
| L3 | DISTRICT 3 OF 10 | Ikorodu Road | No wahala for road today: no LASTMA, no KAI. Just find your gap. | `bg_intro_L03` | `bg_intro_L03_phone` |
| L4 | DISTRICT 4 OF 10 | Mushin Market | No wahala for road today: no LASTMA, no KAI. Just find your gap. | `bg_intro_L04` | `bg_intro_L04_phone` |
| L5 | DISTRICT 5 OF 10 | Oshodi Expressway | One wahala dey road today: LASTMA flag. Hold your change. | `bg_intro_L05` | `bg_intro_L05_phone` |
| L6 | DISTRICT 6 OF 10 | Ikeja Along | Two wahala dey road today: LASTMA flag and KAI officers. Hold your change. | `bg_intro_L06` | `bg_intro_L06_phone` |
| L7 | DISTRICT 7 OF 10 | Ojota Intersect | Two wahala dey road today: LASTMA flag and KAI officers. Hold your change. | `bg_intro_L07` | `bg_intro_L07_phone` |
| L8 | DISTRICT 8 OF 10 | Third Mainland Bridge | Two wahala dey road today: LASTMA flag and KAI officers. Hold your change. | `bg_intro_L08` | `bg_intro_L08_phone` |
| L9 | DISTRICT 9 OF 10 | Lekki Toll Gate | Two wahala dey road today: LASTMA flag and KAI officers. Hold your change. | `bg_intro_L09` | `bg_intro_L09_phone` |
| L10 | DISTRICT 10 OF 10 | Ojuelegba Chaos | Two wahala dey road today: LASTMA flag and KAI officers. Hold your change. | `bg_intro_L10` | `bg_intro_L10_phone` |

Enforcement per `LevelManager`: L1–L4 none, L5 LASTMA only, L6–L10 LASTMA + KAI (no level is KAI-only; that line stays as written for future levels). " and " is coloured LASTMA pink `#E07CC0`.

## Code change in `DistrictIntroView.Show`
- `ScreenKit.ArtOrPlaceholder(root, $"bg_intro_L{f.LevelNumber:00}{(mobile ? "_phone" : "")}", …)` instead of `"bg_intro_blur"`.
- Lower the full-bleed `Dim` from 62% to **20%** (`#02030A` @ .20): the calm zone is baked, so the street stays visible around the card.

## Card layout (unchanged from PR #87 / `DistrictIntroRules`; inside `Screen.safeArea`, anchor + pivot centre)
Reference 1920×1080 = 1280×720 × 1.5. Card centre is 40 px (26.7 @720) **above** the safe-area centre.

| Element | 1280×720 safe coords | 1920×1080 (safe 1856×1016) | 2340×1080 (safe 2076×993) |
|---|---|---|---|
| Card (border 2 px gold @28%, fill ink @88%, radius 40) | 789 × 443, centre (0, +26.7) | 1184 × 664, centre (0, +40) → top-left (336, 168) in safe | 1184 × 664 → top-left (446, 125) in safe |
| Padding | 37 / 29 | PadX 56, PadY 44 | same |
| Kicker `DISTRICT N OF 10` | y 29, h 23 | y 44, 26 px, gold `#E8B21E`, tracking 12% | same |
| Title | y 56, h 57 | y 84, 72 px `#F5F5F0` | same |
| Subtitle (wraps, 2 lines max) | y 117, h 53 | y 176, 30 px `#9EA3AD` | same |
| 4 stat tiles (gap 16) | y 191, ≈ 170 × 87 each | y 286, ≈ 255 × 130 each (value 46 / 34 px `#FAE69E`, label 22 px) | same |
| Power-ups header + chips | y 295 / 321, chips h 29 | y 442 (24 px) / y 482, chips h 44, gap 10 | same |
| OYA, CROSS! (CTA) | right, 253 × 96 | 380 × 144, x = card − 56 − 380, bottom 44 − 30 | same |
| Base Camp (L2+) | 200 × 96, 11 left of CTA | 300 × 144, 16 px left of CTA | same |

Font Plus Jakarta Sans Bold (subtitle/labels Regular weight as in code). Touch targets 144 px. The calm zone is centred on the card for both widths, so it lines up with the card at any safe-area inset.

## Timing (unscaled time: the view sets `Time.timeScale = 0`)
| Step | Time | Ease |
|---|---|---|
| Background + dim fade in | 0–250 ms | linear |
| Card fade 0→1 + scale 0.96→1.0 | 80–300 ms | ease-out cubic |
| Stat tiles + chips fade/slide up 12 px, 40 ms stagger | 200–460 ms | ease-out |
| Hold | until the player taps OYA, CROSS! (no auto-dismiss) | — |
| Exit: card + bg fade out, then restore timeScale | 180 ms | ease-in |
Reduce motion: no scale/slide, fades only (150 ms). Buttons accept taps from 300 ms (avoid a carried-over tap skipping the card). Base Camp hides the card and restores it on return, no re-animation.

## Open questions
1. L1–L9 source captures came from the build with missing vehicle models (see Levels page note); swap in fresh captures when available (re-run `tools/gen_intro_bgs.py`).
2. Mobile switch rule: `isMobilePlatform` vs aspect ratio (tablets 4:3 would then use the desktop file, cropped by Envelope).
3. Dim 20%: confirm on device; raise to 30% if the subtitle feels weak on bright levels (L4, L9).
