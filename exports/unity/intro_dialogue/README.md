> Copy of `/workspace/games/design/GPP-INTRO-DIALOGUE/README.md`. Paths here are relative to `exports/unity/intro_dialogue/`: UI sprites are in `sprites@{1x,2x}/ui/`, portraits in `sprites@{1x,2x}/portraits/`, mockups in `mockups/`. The `tools/` and `work/` folders stay in the design folder.

# GPP-INTRO-DIALOGUE: Baba Gidi intro dialogue (art + UI spec)

Design only. Shown once to first-time players before Level 1, replayable from Settings. Landscape only, uGUI with **legacy `UnityEngine.UI.Text`** (Best Fit off, no Outline, one `Shadow` over glass), CanvasScaler 1920×1080, match height 1.0. Style: the existing dusk glass (`gen_unity.py` GLASS recipe), teal `#59D9B8`, orange `#FF7A1A`, gold `#E8B21E`, Naira gold `#FAE69E`. Tap targets ≥ 144 px (canvas units).

Unity copy: `gidi-design/exports/unity/intro_dialogue/` (sprites in its own `sprites@1x/` and `sprites@2x/`, PPU 100 / 200, entries appended to `exports/unity/manifest.json`).

## Mockups
| Mockup | 16:9 (1920×1080) | 20:9 (2400×1080) |
|---|---|---|
| Line 1, Pedestrian speaking (Ped pleading, Baba neutral dimmed) | `mockups/intro-line1-16x9-1920x1080.png` | `mockups/intro-line1-20x9-2400x1080.png` |
| Line 2, Baba surprised (Ped pleading dimmed) | `mockups/intro-line2-16x9-1920x1080.png` | `mockups/intro-line2-20x9-2400x1080.png` |
| Line 8, Baba pointing "let's go" (Ped happy dimmed) | `mockups/intro-line8-16x9-1920x1080.png` | `mockups/intro-line8-20x9-2400x1080.png` |
| Line 8 + safe-area / layout guides | `mockups/intro-line8-16x9-1920x1080-guides.png` | `mockups/intro-line8-20x9-2400x1080-guides.png` |

Mockups are rendered from the exported sprites (9-slice borders as recorded below) and the portrait PNGs, over `gidi/characters/gidi-home-bg-v2.jpg` blurred 12 px at 55% brightness. In game, use the live L1 street (or `screens/intro/bg_intro_L01.png`) behind `dlg_scrim_bottom`; the blur is only so the mockup crowd doesn't compete.

## Layout
All positions are canvas units. Build everything except the scrim and the full-screen tap catcher under a `SafeArea` RectTransform fitted to `Screen.safeArea` (same as the HUD). Safe areas as in the HUD/Settings specs: **16:9 desktop** 32 px margin → safe rect x 32–1888, y 32–1048 (1856×1016). **20:9 phone** (2400×1080 ref) insets L/R 132, top 24, bottom 63 → x 132–2268, y 24–1017 (2136×993).

### Anchors (same on every aspect)
| Element | Parent | Anchor / pivot | anchoredPosition | Size |
|---|---|---|---|---|
| Scrim `dlg_scrim_bottom` | Canvas root (not safe) | bottom-stretch / (0.5, 0) | (0, 0) | stretch × 480 |
| Tap catcher (transparent `Image` α 0, raycast on, `Button`) | Canvas root | full stretch | 0 | full screen; sibling **below** Skip |
| Baba portrait (`Image`, Simple, Preserve Aspect) | SafeArea | (0, 0) / (0.5, 0) | (398, 104) | 700×800 |
| Ped 8 portrait | SafeArea | (1, 0) / (0.5, 0) | (−398, 104) | 700×800 |
| Dialogue box `dlg_box_normal` (Sliced) | SafeArea | (0.5, 0) / (0.5, 0) | (0, 24) | width `min(safeW − 96, 1760)` × 240 |
| Body Text | Box | full stretch | offsets L 64, R 112, T 52, B 32 | 1584×156 at 1760 wide |
| Name tag, Baba (`dlg_nametag_baba`, Sliced) | Box | (0, 1) / (0, 0) | (56, −16) | (text width + 64, min 220) × 64 |
| Name tag, Pedestrian (`dlg_nametag_ped`) | Box | (1, 1) / (1, 0) | (−56, −16) | (text width + 64, min 220; 240 for "Pedestrian") × 64 |
| Tap indicator `dlg_tap_indicator` | Box | (1, 0) / (1, 0) | (−40, 32) | 48×48 |
| Skip hit rect (transparent, raycast on) | SafeArea | (1, 1) / (1, 1) | (0, 0) | **264×144** |
| Skip visual `dlg_btn_skip_*` (Sliced) | Skip hit | centre | (0, 0) | 232×104; label "Skip" + `dlg_icon_skip` 40×40, 12 gap, centred |

Portraits sit behind the box (sibling order: scrim, portraits, box, tag, Skip). The portrait bottom is 160 below the box top, so the bottom fade of each portrait (and the waist crop on `baba_pointing`) is always under the box. Eye line in every portrait PNG is **y 250 from the top** (of 800), so both speakers share one eye line.

### Resolved positions (screen px, top-left origin)
| Element | 16:9 1920×1080 | 20:9 2400×1080 |
|---|---|---|
| Safe rect | 32, 32 → 1888, 1048 | 132, 24 → 2268, 1017 |
| Box | x 80–1840, y 784–1024 (1760×240) | x 320–2080, y 753–993 (1760×240) |
| Name tag (Baba / Ped) | y 736–800; Baba x 136–356, Ped x 1544–1784 | y 705–769; Baba x 376–596, Ped x 1784–2024 |
| Body text rect | x 144, y 836, 1584×156 | x 384, y 805, 1584×156 |
| Tap indicator | x 1752, y 944 (48×48) | x 1992, y 913 |
| Baba portrait | x 80–780, y 144–944 | x 180–880, y 113–913 |
| Ped 8 portrait | x 1140–1840, y 144–944 | x 1520–2220, y 113–913 |
| Shared eye line | y 394 | y 363 |
| Skip hit / visual | hit x 1624–1888, y 32–176; visual x 1640, y 52 | hit x 2004–2268, y 24–168; visual x 2020, y 44 |

On 20:9 the box stays capped at 1760 (readable line length) and the portraits move out to the safe edges, so they frame the box. **4:3 / tablets** (aspect of the safe rect < 1.5, same switch rule as the HUD): box = safeW − 96 (1280 on 1440×1080), portraits at scale 0.85 (595×680, same anchors, x offset 48 + 297) so they don't overlap in the middle.

## Type
| Text | Size | Colour | Shadow | Notes |
|---|---|---|---|---|
| Body line | **40 px** Bold, Line Spacing 1.0 (~52 px rows), Upper Left, wrap on, Vertical Overflow Truncate | `#F5F5F0` | yes | Follows the Settings **Text size** multiplier like subtitles: S 36 / M 40 / L 48. Longest line (8, 105 chars) is 2 rows at M and L; the 156 px rect holds 3 rows at M. Rich Text off (THAT stays plain caps from the script). |
| Name tag | **30 px** Bold, Middle Center | `#0F1219` on teal / gold | no (not over glass) | "Baba Gidi", "Pedestrian" (from the script) |
| Skip label | **32 px** Bold | `#F5F5F0`, pressed `#FAE69E` | yes | icon tinted the same |
| Everything | Plus Jakarta Sans Bold, **Best Fit off**, Raycast Target off on all Text | | `Shadow` #000 α 128, distance (0, −2), Use Graphic Alpha | no Outline anywhere |

## Colours
| Use | Value |
|---|---|
| Box fill / edge | ink `#0F1219` @ 82% / 2 px `#FFD873` @ 32%, radius 32, faint top sheen |
| Baba name tag | teal `#59D9B8`, 2 px white @ 35% edge |
| Pedestrian name tag | gold `#E8B21E` (picks up her brocade) |
| Neutral tag (spare) | glass ink 82% + gold edge 60%, text `#FAE69E` |
| Skip normal / pressed | glass ink 72% + gold edge 28% / ink 86% + gold edge 60% (= `btn_glass` normal/pressed) |
| Tap indicator | `#FAE69E` fill, `#E8B21E` stroke |
| Scrim | ink `#0F1219` 0% → 72% |
| Orange `#FF7A1A` | not used on this screen (kept for warnings/destructive, per the house rules) |

## Bright / dim and timing
| State | Image.color | Desaturation | Scale (pivot bottom-centre) | Sibling |
|---|---|---|---|---|
| **Speaker (bright)** | (1, 1, 1, 1) | 0 | 1.00 | last of the two |
| **Listener (dim)** | (0.55, 0.55, 0.58, 1) = `#8C8C94` (55% tint, slightly cool) | 35% (saturation 0.65) via an optional UI material `UI/GidiPortraitDim` with `_Saturation`; if no material, tint alone is fine | **0.95** | first |

- **Speaker change:** both portraits tween colour + scale together over **180 ms**, ease-out cubic, unscaled time. The new name tag swaps instantly and fades in over 120 ms with an 8 px slide from its own side. Text clears at the same moment and starts typing.
- **Expression change, same speaker:** swap the sprite and punch scale 1.00 → 1.03 → 1.00 over 140 ms.
- **Entry:** scrim + box fade in 200 ms; portraits slide 40 px in from their side and fade in 250 ms (Baba starts dim, line 1 is the Pedestrian); line 1 starts typing at 300 ms.
- **Exit:** after line 8 (or Skip), everything fades out 250 ms, then Level 1 loads.
- **Reduce motion** (pref hidden in v1, see Settings spec): no slides, scale or bob; colour changes in 120 ms; text appears whole.

## Tap to advance and Skip
- **Typewriter** 45 characters/s (unscaled). A tap while typing completes the line at once. A tap on a completed line advances. Ignore taps for 150 ms after a line completes so a double tap can't skip a line.
- `dlg_tap_indicator` shows only when the line is complete; it bobs 8 px down and back, 0.9 s loop, ease in-out.
- The whole screen is the tap area (tap catcher) except the Skip hit rect. Keyboard/WebGL: Space, Enter or click advance; **Esc = Skip**. Android Back = Skip.
- **Skip: one tap, no confirmation** (recommended). The dialogue is replayable from Settings and is short (8 lines), so a confirm only adds friction on the first-run path. Skip ends exactly like finishing line 8: mark seen, fade out, load Level 1. When replayed from Settings, finishing or Skip returns to Settings instead.
- Mark the intro as seen (suggested pref `gidi.intro.baba.seen`) when it ends or is skipped, so killing the app mid-dialogue replays it next time. Back it up with the other prefs in the cloud save.
- Skip states: normal → pressed (`SpriteSwap`, label/icon `#FAE69E`, scale 0.96 for 80 ms). No disabled state.

## Suggested expression per line
Each portrait keeps its last expression while it is dimmed.

| # | Speaker | Line | Speaker portrait | Listener (dim) |
|---|---|---|---|---|
| 1 | Pedestrian | Baba! Good morning sir. Abeg, I wan cross this road. | `ped8_pleading` | `baba_neutral` |
| 2 | Baba Gidi | Ah-ah, you wan cross THAT road? Una dey craze? | `baba_surprised` | `ped8_pleading` |
| 3 | Pedestrian | I no get choice o. I don late for owambe! | `ped8_pleading` | `baba_surprised` |
| 4 | Baba Gidi | Owambe? Why you no talk am first! Jollof no dey wait. | `baba_laughing` | `ped8_pleading` |
| 5 | Pedestrian | So you go help me? | `ped8_neutral` (hopeful) | `baba_laughing` |
| 6 | Baba Gidi | My green senator don ready, I don shine my sandals. I go carry you. | `baba_proud` | `ped8_neutral` |
| 7 | Pedestrian | Make you no knock anybody o! | `ped8_happy` (relieved, teasing; alt `ped8_pleading`) | `baba_proud` |
| 8 | Baba Gidi | Me? I be professional. I dey cross anybody for Lagos road. Pick people, cross safe, no wahala. Let's go! | `baba_pointing` | `ped8_happy` |

## Sprites
Import as the rest of `exports/unity` (Sprite 2D and UI, Full Rect, Bilinear, no mips, Compression None, Alpha Is Transparency). @1x PPU 100, @2x PPU 200. Borders are @1x px (double for @2x).

| Sprite | @1x size | 9-slice L/R/T/B | Pivot | Use |
|---|---|---|---|---|
| `dlg_box_normal` | 128×128 | 44 / 44 / 44 / 44 | 0.5, 0.5 | Dialogue box, Sliced, Fill Center on |
| `dlg_nametag_baba` | 96×64 | 28 / 28 / 28 / 28 | 0, 0 | Teal name tag (height fixed 64) |
| `dlg_nametag_ped` | 96×64 | 28 / 28 / 28 / 28 | 1, 0 | Gold name tag |
| `dlg_nametag_glass` | 96×64 | 28 / 28 / 28 / 28 | 0, 0 | Spare neutral tag |
| `dlg_btn_skip_normal` | 120×104 | 52 / 52 / 52 / 52 | 0.5, 0.5 | Skip pill (height fixed 104; horizontal stretch only) |
| `dlg_btn_skip_pressed` | 120×104 | 52 / 52 / 52 / 52 | 0.5, 0.5 | Skip pressed |
| `dlg_icon_skip` | 40×40 | – | 0.5, 0.5 | White double chevron, tint with Image.color |
| `dlg_tap_indicator` | 48×48 | – | 0.5, 0.5 | Gold ▼, baked colour |
| `dlg_scrim_bottom` | 16×256 | – (stretch Simple) | 0.5, 0 | Bottom scrim |
| `portrait_baba_{neutral,laughing,surprised,proud,pointing}` | 700×800 | – | 0.5, 0 | Baba, faces right, eye line y 250 |
| `portrait_ped8_{neutral,pleading,happy}` | 700×800 | – | 0.5, 0 | Ped 8, faces left, eye line y 250 |

Portraits: transparent PNG, waist-up, same head scale and eye line across all 8; the bottom ~80 px fades to transparent (hidden under the box). The @2x portraits (1400×1600) are upscaled about 1.3× from the 864×1152 generated source, so they are a little soft at full 2x; @1x is native-sharp. If 2x crispness matters on tablets, re-render the 3D characters at 2x and drop them into the same frames.

## Files
```
GPP-INTRO-DIALOGUE/
  README.md                       this spec
  portraits/sprites@1x/portrait_<name>.png   8 × 700×800
  portraits/sprites@2x/portrait_<name>.png   8 × 1400×1600
  ui/sprites@1x/<sprite>.png      9 UI sprites
  ui/sprites@2x/<sprite>.png      9 UI sprites
  ui/sprites.json                 manifest-shaped entries for the UI sprites
  mockups/intro-line{1,2,8}-16x9-1920x1080.png, intro-line8-16x9-1920x1080-guides.png
  mockups/intro-line{1,2,8}-20x9-2400x1080.png, intro-line8-20x9-2400x1080-guides.png
  tools/gen_ui.py                 UI sprites (headless Chrome, same method as gen_unity_settings.py)
  tools/cut.py, tools/compose.py  rembg cut-out (isnet-general-use) + edge clean + scale/eye-line normalise
  tools/gen_mockups.py            mockups and guide overlays
  work/raw, work/cut              generated source images and raw cut-outs
gidi-design/exports/unity/intro_dialogue/
  README.md (copy), sprites@1x/{ui,portraits}/, sprites@2x/{ui,portraits}/, mockups/
```
Names in `<name>`: baba_neutral, baba_laughing, baba_surprised, baba_proud, baba_pointing, ped8_neutral, ped8_pleading, ped8_happy.

## Notes on the art
- Baba Gidi keeps the reference's flat-faceted low-poly look in all five portraits (fila, white trim, gold chevrons). The pointing portrait was generated slightly closer, so it was scaled down to match head size; its waist crop sits under the box.
- Ped 8 matches her own reference, which is a smoother semi-real render than Baba's low-poly. The two therefore differ a little in finish, exactly as their reference renders do.
