# Splash (RT-115) + Lagos map (GPP-060): repaired resources for G-Prototype #95–#99

Generator: `gidi-design/tools/gen_splash_map.py`. Font: Plus Jakarta Sans Bold. Reference: 1920×1080, CanvasScaler match height 1.0. Scale `s = H/1080` (1024×450 → s = 0.4167). Sprites come at 1x and 2x (2x = double the px and double the 9-slice borders).
Previews (checked by eye): `preview/splash_{1920x1080,1024x450}.png` and `preview/map_{1024x450,1920x1080,2340x1080}.png`.

## Splash
| File | Size | Use |
|---|---|---|
| splash/bg_splash_1920x1080.png, bg_splash_2340x1080.png | opaque | Lagos dusk skyline, Third Mainland bridge, danfos, zebra crossing. **Replaces bg_splash_*_blur (the bokeh).** Pick 2340 when aspect ≥ 2.0. Cover-fit, centred. |
| splash/logo_gidi_master.png | 2400×720, transparent | Master logo (mark + GIDI++ + tagline) |
| sprites@1x/logo_gidi.png (2x: 1600×480) | 800×240 | Splash logo |
| loader_track / loader_fill | 64×20, 9-slice L/R 10, T/B 0 | Bar, Image type Sliced; drive fill width (or Filled Horizontal) |
| loader_glint | 48×20 | Optional sweep over the fill, 1.2 s loop |
| badge_rating | 72×48 | 12+ |
| splash_scrim | 64×256, stretch | Bottom 45% of the screen, ink 0→85%, behind the bar/text |

Layout (1920 ref, ×s elsewhere): logo 800×240 centred, top = 0.30·H − 120. Bar 720×20 centred, top = H − 200. Loading text 28 px, muted #9EA3AD, tip in #FAE69E, centred, top = H − 160. Badge bottom-left at (40 + safeL, 40 from the bottom).
At 1024×450: logo 333×100 at (345,85); bar 300×8 at (362,367); text 11.7 px at y 383; badge 30×20 at (17,410).

Timing (all eased):
- 0.00–0.40 s: scene fades from black (#0F1219) to the bg, ease-out cubic.
- 0.15–0.55 s: logo alpha 0→1 and scale 0.96→1.0, ease-out back (overshoot 1.2).
- 0.55 s: bar and text fade in over 0.25 s. The fill follows `SplashRules.BarFill`, lerped at ≤ 1.5/s so it never jumps.
- Hold: minimum total display **2.2 s** (allowed range 2.0–2.5; replaces MinSeconds 1.2 / 1.6). Cap at 8 s as in #99.
- Fade out: 0.40 s, ease-in-out sine, over Home.

## Lagos map
Opaque backgrounds: `map/bg_map_1920x1080.png` and `bg_map_2340x1080.png` (ink city blocks, expressways, Lagos Lagoon, Atlantic, gold dashed road baked through the node positions below, top 160 px darkening band). **Replaces bg_map_*_blur; gameplay must not show through.** For other aspects, either draw the road at runtime from `layout.json` or use the closest bg.

Sprites in `map/sprites@1x|2x/`:
- map_node_done 128 (teal ✓), map_node_open 128, map_node_locked 128 (lock), map_node_current 168 (gold ring + glow, 24 px glow pad). Disc diameter 120 at 1x; fills are opaque so the road never shows through. Text "L5" / "∞" drawn on top at 44 px.
- map_star_filled / map_star_empty: 48.
- map_stopdot_done / open / locked / selected: 32 (28 disc).
- map_panel: 96×96, 9-slice 36 all sides. Ink 90%, 2 px gold 55% outline, radius 28.
- map_tab_on / map_tab_off: 64×64, 9-slice 20.
- map_label_plate: 48×48, 9-slice 16, optional backing behind labels.

### Rules
- **The panel has its own column on the right.** Nodes live only in the map area to its left, so the panel can never cover a node or label (it fixes L9 being hidden).
- Ten nodes snake in 2 rows × 5 columns: L1→L5 left to right on top, L6→L10 right to left below. The road links L5 to L6 down the right side.
- Under each node, centred on its x: stop dots, then the label (centred, max 2 lines, width = column − 24 px, so neighbouring labels can't touch: ≥ 24 px gap).
- Shrink-to-fit: if a label needs a 3rd line, the font steps down to 0.85×.
- Stack below the node centre: dots top = +72 px, label top = +110 px, label ≤ 2×32 px. The stack ends at +174, well inside the 422 px row pitch.
- Safe area: the margin is 40 px plus the device insets (2340×1080 assumes a 132 px notch each side). Nothing comes closer than 40·s to an edge.
- Stop dots: d 28 with 8 px gap, the row centred on the node x (1 stop = a single dot right under the node).

### Formulas (s = H/1080, inset = safe-area side inset)
```
m = 40s; topbar = 160s
panel: w = 640s, x = W − inset − m − w, y = 160s, h = H − 160s − m
area:  x0 = inset + m, x1 = panel.x − m, y0 = 160s, y1 = H − m; col = (x1 − x0)/5
row y: y0 + 0.10(y1−y0) + 60s  and  y0 + 0.58(y1−y0) + 60s
node cx = x0 + col·(c + 0.5)   (c = 0..4; bottom row reversed)
```
Normalized node positions are in `map/layout.json` (each resolution, px + all sizes).

| Res | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9 | L10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1024×450 px | 87,128 | 229,128 | 370,128 | 512,128 | 653,128 | 653,304 | 512,304 | 370,304 | 229,304 | 87,304 |
| 1920×1080 px | 156,308 | 388,308 | 620,308 | 852,308 | 1084,308 | 1084,730 | 852,730 | 620,730 | 388,730 | 156,730 |
| 2340×1080 px | 304,308 | 567,308 | 830,308 | 1093,308 | 1356,308 | 1356,730 | 1093,730 | 830,730 | 567,730 | 304,730 |
| 1920 normalized | .0813,.2852 | .2021 | .3229 | .4437 | .5646 | .5646,.6763 | .4437 | .3229 | .2021 | .0813 |

### Every element at 1024×450 (x, y, w, h in px; s = 0.4167)
| Element | Rect / value |
|---|---|
| Back button | 17,12, 43×43 (9-slice panel) |
| Title "Lagos map" | x 70, y 22, 20 px |
| Naira chip | 794,12, 110×43; text #FAE69E 12.5 px |
| Lives | 911,12, 43×43 |
| Settings | 964,12, 43×43 |
| Map area | 17,67 → 724,433 (col 141.5) |
| Node disc | Ø 50 centred on the table above (current sprite 70, others 53) |
| Stop dots | Ø 11.7 (sprite 13.3), gap 3.3, top = cy + 30 |
| Label | w 131.5 centred on cx, top = cy + 45.8, 11.7 px, line-height 1.15, max 2 lines; #F5F5F0 (locked #9EA3AD) |
| Info panel | **741,67, 267×367**; map_panel 9-slice (border 15 at this scale), padding 13 |
| Panel title | 18.3 px #F5F5F0 (e.g. "L5 · Oshodi Expressway"); single line, auto-size down to 14 |
| Stop tabs | 3 equal in a row, h 26.7, gap 5, top = title + 8; 10.8 px; on = gold tab |
| KV rows | key col 62.5 wide #9EA3AD, value #F5F5F0 10.8 px, row gap 5.8; Crowd wraps ≤ 2 lines (#97) |
| Stars | 15 px stars, gap 6.7 |
| OYA, CROSS! | bottom of panel: 241×50 at (754,371), 18.3 px |
| Lock toast | centred in the map area: x 17–724, y 395, h 29 (keeps clear of the row-2 labels, which end at y 376) |

At 1920×1080, multiply by 1/s (panel 1240,160,640×880; padding 32; title 44; tabs 64; KV 26; CTA 120 high; label font 28).

### Notes for the consolidated PR
- Load art from `Resources/UI/Screens/{1x,2x}/`. Suggested names are the file names here; backgrounds go as `bg_splash_desktop`/`bg_splash_phone` and `bg_map_desktop`/`bg_map_phone` (non-blur) and drop the `_blur` variants.
- Remove the dim overlay on top of the map bg (it's opaque now). On the splash, use only the scrim.
