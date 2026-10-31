# GPP-SOUVENIR-CLEAR: souvenir row on Level Clear (G-Prototype PR #139)

Role: Game UI/UX. Screen: Level clear (`LevelClearView`, gidi-design `mockups/clear-desktop.html` / `clear-phone.html`). Landscape only.
Code read: PR #139 head `28cea96` (`LevelClearSouvenirRules`, `LevelClearView.BuildSouvenirRow`), `SouvenirCatalog`, `SouvenirCollection`, `SouvenirTracker`, `LagosMapRules.Districts`, `GameManager` cash-out and clear path.
Design read: `screens.html#s-clear`, `souvenirs.html`, `levels.html`, `reference/levels/README.md`, `reference/VISION_BRIEF.md`.

Preview: `clear-souvenir-preview.png` (the four renders on one sheet), in `GPP-SOUVENIR-CLEAR/mockups/` and gidi-design `exports/` (with `clear-souvenir-{new-desktop,owned-phone,new-4x3,hidden-desktop}.png`; HTML in `mockups/clear-souvenir-*.html`). Source `tools/gen_souvenir_clear.py` in gidi-design.

**Summary.** Keep the dev's row. It sits between the tiles and the buttons, is 150 high with a 30 gap (+180 on the panel), has the medal on the left, text in the middle and NEW on the right. Six changes:
1. Name text drops from 46 to **40 px**. At 46 px the longest name, "Ojuelegba Under-bridge Sticker", is 724 px wide, which overflows its 702 px rect.
2. Real 9-slice sprites replace the square `Image`s: a rounded pill and a gold-edged frame for NEW.
3. The text block becomes 3 lines: kicker, name, collection count.
4. The kicker reads **SOUVENIR FOUND** when NEW and **SOUVENIR** when owned.
5. Owned rows use the quiet `tile_stat_normal` frame.
6. NEW gets a one-time pop on unscaled time.

---

## 1. The row

### Position and size (1920×1080 reference, CanvasScaler match height 1)
The panel stays as it is in PR #139: `LevelClearRules.PanelWidth` 1180, inner 1068, centred in the safe area.

| | Panel-local (x, y from top-left, w × h) | Screen at 1920×1080 |
|---|---|---|
| Panel with row | 1180 × **742** (44+90+60+150+30+**150+30**+144+44) | x 370, y 169 |
| Panel, row hidden | 1180 × 562 | x 370, y 259 |
| Stat tiles | y 194, 4 × 251 × 150, gap 16 | y 363 |
| **SouvenirRow** | **56, 374, 1068 × 150** | **x 426–1494, y 543–693** |
| Buttons | y 554 (row shown) / 374 (hidden), 144 high | y 723 |

Inside the row (row-local, top-left):

| Child | Rect | Content |
|---|---|---|
| `SouvenirRow` (Image, Sliced) | 1068 × 150 | NEW: `clear_souvenir_frame_new` · owned: `tile_stat_normal` |
| `SouvenirMedal` | 12, 12, 126 × 126, preserveAspect | `souvenir_LNN` (gold rim baked). If the art is missing, the dev's gold circle with "L6" Text 40 px #0F1219 (keep) |
| `SouvenirLabel` (kicker) | x 166, y 20, w W, h 28 | 22 px. NEW: `SOUVENIR FOUND` #E8B21E · owned: `SOUVENIR` #9EA3AD |
| `SouvenirName` | x 166, y 50, w W, h 52 | **40 px** #FAE69E, Middle Left, `def.Title` (e.g. "Ikeja Along Phone Case") |
| `SouvenirCount` (new) | x 166, y 104, w W, h 28 | 22 px #9EA3AD. NEW: `Added to Lagos collection · 6/10` · owned: `Lagos collection · 6/10` (same string as `SouvenirBookRules.Header`) |
| `SouvenirNew` (pill) | x 904 (= 1068−24−140), y 47, 140 × 56 | `clear_pill_new` Sliced + child Text `NEW` 28 px #0F1219 Middle Center |

W (text width) is 714 with NEW (1068 − 166 − 24 − 140 − 24) and 878 when owned. The longest title at 40 px Jakarta Bold measures 629 px, so it fits with 85 px to spare. All other titles are ≤ 470 px.

**Legacy `UI.Text`** (no TMP). Plus Jakarta Sans Bold. **Best Fit off**, Rich Text off, Horizontal Overflow **Wrap** + Vertical Overflow **Truncate** on the name, so a bad string truncates instead of running under the pill. No `Outline`. One `Shadow` (#000 alpha 128, distance (0, −2), Use Graphic Alpha) on Name and Count only, because they sit on glass. The kicker is 22 px on a tinted frame and needs no shadow. NEW sits on a solid gold fill and gets no shadow. Raycast Target off on everything in the row: the row is not a button (see open question 4).

### Phone / 20:9 and 4:3
- With match height 1, the canvas is always 1080 tall, so the row is the same 1068 × 150 in canvas units everywhere.
- **20:9 / 19.5:9 phones** (2400×1080, mockup 2340×1080): the canvas is ~2340–2400 wide. Side notch insets (~132) and the home bar (63 bottom) leave a safe height of ≥ 1017, and the 742 panel fits with ≥ 137 spare. The row needs no change. The panel looks narrow on a wide phone; the site mockup uses 1600 wide. Widening is optional and separate (see open question 6).
- **4:3** (iPad 2048×1536 → canvas 1440×1080): 1180 leaves 130 per side, and the safe inset is ~14 canvas units. It fits as is. Don't drop below 22 px on the kicker/count. 22 px already matches the stat-tile labels and is the floor.
- If anyone changes `HudLandscapeConfig.canvasMatchWidthOrHeight` below 1, re-check 4:3. The numbers above assume 1.

### Wording
- Kicker: **SOUVENIR FOUND** (NEW) / **SOUVENIR** (owned). Today `LevelClearSouvenirRules.Label = "Souvenir"`. Add `LabelNew = "SOUVENIR FOUND"` and make `Label = "SOUVENIR"`.
- Name: `SouvenirDef.Title` (district + item), as in the collection book and the in-run toast "Souvenir found: … !".
- Count line: `Added to Lagos collection · {n}/10` / `Lagos collection · {n}/10` (`SouvenirTracker.Collection.CollectedCount`).
- All ten names are generic objects. No real brands. Keep it that way if names change; any brand on an item must be fictional.

### NEW badge style
- `clear_pill_new`: 56×56 source, border 28/28/28/28. Use it Sliced at 140 × 56, stretched horizontally only. Fill gold #E8B21E, 2 px #FAE69E rim, faint top highlight.
- Text `NEW` 28 px #0F1219.
- Gold rather than teal or orange: teal #59D9B8 means "info / active" (EARNED tag, Owa chip), and orange #FF7A1A means caution/time-up (Continue last 3 s). A collectible reward is gold, matching the medal rim and the gold edge.
- The badge is the word "NEW", not a colour dot, so it never relies on colour alone. The kicker also changes text.
- NEW row frame `clear_souvenir_frame_new`: 80×80 source, border 32, radius 24 like `tile_stat`, gold 10% fill, 2 px #E8B21E 80% edge.
- **Motion, NEW only.** The modal sets `Time.timeScale = 0`, so all of it must run on `Time.unscaledDeltaTime`:
  - The medal scales 0.9 → 1.0 over 0.25 s.
  - At +0.2 s the pill pops 0.6 → 1.12 → 1.0 over 0.35 s (ease-out back).
  - The frame edge alpha goes 0.8 → 1 → 0.8 once over 0.6 s.
  - Optional: a short chime.
  - Reduce motion: static.
  - Owned rows never animate.

## 2. States

| State | When (code) | Row |
|---|---|---|
| **NEW** | `collected && !seen` (`LevelClearSouvenirRules.IsNew`). `TakeForLevelClear` sets `gidi.souvenir.seen.LNN` | Shown: gold frame, SOUVENIR FOUND, NEW pill, pop |
| **Already owned** | `collected && seen` | Shown: `tile_stat_normal` frame, SOUVENIR kicker, no pill, no motion. Same height, so the buttons stay in the same place on every clear of that district |
| **Cleared, not earned** | `!collected` | **Hidden** (panel 562, as PR #139 does) |

**Not earned: hide it (keep the PR behaviour). Reasons:**
1. **The state can't happen with the current award rule.** The souvenir is awarded on the first cash-out (delivery) in the district (`SouvenirTracker.HandleCashOut` → `SouvenirCollection.OnCashOut`). A clear only fires after the delivery that empties the pool, and `NotifyCashOut` runs before `BeginPoolCleared`, so every real clear already holds the souvenir. The only runs that don't record it are autopilot/batch runs, and those never show this modal. A locked silhouette would be an asset, copy and QA path that no player sees.
2. **A hint would have nothing true to say.** The drop rule is still "TBD" on souvenirs.html. "Look for it at the curb" would be wrong today.
3. **The clear card is the payoff.** A "you missed it" row pushes NEXT down 180 px and competes with the reward. The tease for unfound souvenirs already lives in the collection book (dim `souvenir_LNN_dim` medallion, "L6 · not found yet").

**When to switch to the silhouette:** if Kehinde moves the award to something a clear can miss, such as a drop chance, a curb spawn, or "finish the last stop". Then the state becomes real and has an actionable hint. The variant is ready:
- `souvenir_LNN_dim` in the medal slot, kicker `SOUVENIR` #9EA3AD, name `???` 40 px #9EA3AD.
- Hint 22 px #9EA3AD, e.g. `Clear stop 3 of 3 to collect am`.
- `tile_stat_normal` frame, no pill.
- No new sprites needed.

## 3. Districts with several stops

`LagosMapRules.Districts` has 2 stops for L2, L4, L7 and L10, and 3 for L5 and L8. Later stops replay the same crossing with the same `CurrentLevelNumber`, and they unlock only after the previous stop is cleared.

- **How the code awards it.** On the district's first delivery on any stop, keyed by level, not stop. Stop 2 can't be played before stop 1 is cleared, so in practice the find always happens on stop 1.
- **How the vision awards it.** The vision brief (v0.2) doesn't mention souvenirs. souvenirs.html says "one per district, found once", drop rule TBD.
- **Spec (matches PR #139 as is):** the NEW row shows on the **first clear after the find**, which is **stop 1's first clear**. Every later clear in that district (stop 2, stop 3, replays) shows the owned row. If the player delivers on stop 1 and then crashes out, the in-run toast fires then. NEW waits for the next clear, which is still stop 1.
- L10 (2 stops, final clear "PLAY AGAIN", `GauntletCleared`) follows the same rule.

**Flag for Kehinde:** do you want the souvenir to be a "found on arrival" stamp (current: free on stop 1's first delivery, even in the L1 tutorial) or a **district-complete reward** (awarded on the final stop's clear, 2/2 or 3/3)?
- If district-complete: NEW lands on the last stop's clear. Stops 1 to n−1 show the locked silhouette with "Clear stop n of n to collect am" (section 2 variant).
- The code change would be in `SouvenirCollection.ShouldAwardOnCashOut` / the tracker hook, not in this view.

Recommendation: keep the current rule until a drop rule is decided. It gives the earliest reward, and finishing stops is already required to unlock the next district.

## Sprites (gidi-design `exports/unity/`, PPU 100 @1x / 200 @2x, in `manifest.json`, `screen: "clear"`)
| Name | 1x / 2x file | Size @1x | 9-slice border (L/R/T/B, 1x px) | Use |
|---|---|---|---|---|
| `clear_pill_new` | `sprites@1x/clear/clear_pill_new.png` / `sprites@2x/…` | 56×56 | 28/28/28/28 | NEW pill, Sliced 140×56 |
| `clear_souvenir_frame_new` | `sprites@1x/clear/clear_souvenir_frame_new.png` / `sprites@2x/…` | 80×80 | 32/32/32/32 | Row frame, NEW state, Sliced 1068×150 |
Reused: `tile_stat_normal` (owned frame), `souvenir_LNN` / `souvenir_LNN_dim` (`souvenirs/{1x,2x}`, already in `Resources/UI/Souvenirs`).
Import: Sprite (2D and UI), Single, Mesh Type Full Rect, Filter Bilinear, no mipmaps, Compression None (or high quality), borders as listed (double them on the 2x file).

## Dev deltas vs PR #139 (small)
1. `SouvenirName` 46 → 40 px, h 64 → 52, y 58 → 50, width `inner − tx − 188` when NEW (`inner − tx − 24` when owned), Wrap + Truncate.
2. Kicker y 22 → 20, h 30 → 28. Text switches between `SOUVENIR FOUND` (#E8B21E) and `SOUVENIR` (#9EA3AD).
3. Add `SouvenirCount` Text (y 104, h 28).
4. Row `Image`: Sliced `clear_souvenir_frame_new` (NEW) or `tile_stat_normal` (owned), instead of a flat `Tile` colour.
5. Pill: Sliced `clear_pill_new` with colour white (the gold is baked), instead of a flat `AccentGold` rect. Text 30 → 28 px.
6. NEW pop on unscaled time.

Unchanged: row height 150, gap 30, medal 126 at (12,12), pill 140×56 at (inner−164, 47), the show/hide rule, and seen-flag persistence.
Aside, not in scope: on the 1180 panel the "Cash-out grant (chips)" tile label wraps to 2 lines at 22 px (tile text width 207).

## Open questions for Kehinde
1. **Award timing in multi-stop districts:** first delivery on stop 1 (current) or the final stop's clear (district-complete reward)? This decides whether the "not earned" state ever appears and whether the silhouette variant ships.
2. **Real drop rule** (chance / curb spawn / guaranteed) is still TBD on souvenirs.html. Any rule that a clear can miss flips Q2 from "hide" to "silhouette + hint".
3. **Players who already own souvenirs** see NEW once on their next clear of each district (no migration in PR #139). OK, or mark existing ones as seen on first launch?
4. Should the row be tappable to open the Lagos collection book (`SouvenirBookPanel.Open()`)? This spec keeps it non-interactive so it doesn't compete with NEXT.
5. Double announcement: the in-run toast fires at the first delivery, and NEW shows again on the clear. Keep both (recommended: toast = moment, clear = recap)?
6. The panel is 1180 wide in code vs 1600 in the site mockup. Keep 1180 (this spec), or widen on phones?
