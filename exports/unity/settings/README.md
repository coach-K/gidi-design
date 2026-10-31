> Copy of `/workspace/games/design/GPP-SETTINGS/README.md`. The `previews/`, `mockups/` and `gen_previews.py` paths below are in that design folder, not in this repo. Sprite paths are relative to `exports/unity/settings/`; regenerate them with `python3 tools/gen_unity_settings.py`.

# GPP-SETTINGS: Settings screen spec (G-Prototype PR #136)

Landscape only, uGUI with **legacy `UnityEngine.UI.Text`** (no TMP), CanvasScaler 1920×1080, match height 1.0. Style: the existing dark glass (`panel_glass`, ink 72% with a 28% gold edge), gold for navigation (selected tab, Back), **teal `#59D9B8` for set values** (slider fill, toggle on, selected segment), **warning `#FF7A1A`** for destructive or offline states.

- Code read: PR #136 head `d0439e1` (`feat/settings-audio-screen`, stacked on #135 → #134): `SettingsRules`, `SettingsScreenLayout`, `SettingsPersistence`, `SettingsScreenView`, `SettingsStore` (`GidiSettingsBridge`). Also on the game repo: `UgsBootstrap` (anonymous sign-in, `PlayerId`), `LeaderboardRules.FriendsEnabled = false`, `OnboardingRules.PrefsDoneKey`, `WebPerformanceBootstrap` battery saver.
- Design read: `exports/hud/HUD_Landscape_Spec.md`, `screens.html` › Settings, `mockups/settings-*.html` + `css/more.css`, `exports/unity/manifest.json`, `exports/unity/README.md` (legacy Text rules), `tools/gen_unity.py`.
- Sprites: `gidi-design/exports/unity/settings/sprites@{1x,2x}/` (16 × 2), made by `gidi-design/tools/gen_unity_settings.py`, entries merged into `exports/unity/manifest.json`.
- Previews (rendered from the exported sprites and their 9-slice borders): `previews/` here, source HTML in `mockups/`, generator `gen_previews.py`.

| Preview | File |
|---|---|
| Audio | `previews/settings-audio-1920x1080.png` |
| Controls | `previews/settings-controls-1920x1080.png` |
| Display | `previews/settings-display-1920x1080.png` |
| Accessibility | `previews/settings-accessibility-1920x1080.png` |
| Account | `previews/settings-account-1920x1080.png` |
| Account › Reset confirm | `previews/settings-account-reset-confirm-1920x1080.png` |
| Controls on WebGL/desktop (Haptics greyed) | `previews/settings-controls-webgl-desktop-1920x1080.png` |
| Audio at 20:9 (2400×1080 ref) | `previews/settings-audio-20x9-2400x1080.png` |
| Audio at 4:3 (1024×768 → 1440×1080 ref) | `previews/settings-audio-4x3-1440x1080.png` |

Previews show a touch device with sample values. Real defaults: every volume 100%, Haptics on, **Subtitles on**, Text size M, the rest off.

---

## Q1 + Q2: where every control goes (8 controls, 5 rows per tab, no scrolling)

All five tabs fit without scrolling. Audio is the fullest, with exactly 5 rows. The desktop body has 768 px inside the padding, which fits 5 rows of 132 (`RowsThatFit(1016) = 5`). The same holds on 20:9 and 4:3 (see Q7).

The eight `SettingsControl` values from PR #136:

| Control | Tab | Row # | Kind | Label | Caption | Default |
|---|---|---|---|---|---|---|
| MasterVolume | Audio | 1 | slider | `Master` | `Everything at once` | 100% |
| MusicVolume | Audio | 2 | slider | `Music` | `Afrobeats / amapiano loop` | 100% |
| SfxVolume | Audio | 3 | slider | `SFX` | `Horns, danfo, crowd` | 100% |
| VoiceVolume | Audio | 4 | slider | `Voice` | `Owa!, conductor calls` | 100% |
| AmbienceVolume | Audio | 5 | slider | `Ambience` | `Street buzz, hawkers, generators` | 100% |
| Haptics | Controls | 1 | toggle | `Haptics` | `Buzz on bag taps, pickups, hits` (no haptics hardware: `Phones and tablets only`, row at 45%, not interactable) | on |
| Language | Display | 1 | read-only value `English` (v1, see Q5) | `Language` | `Menus and subtitles` | `en` |
| Subtitles | Accessibility | 1 | toggle | `Subtitles` | `Text for voice lines and calls` | **on** (`DefaultSubtitles = true`, vision v2 §5) |

Music, SFX and Voice keep their mockup copy. Master goes first because it scales the four below it. Captions are 32 characters or fewer so they fit the narrowest label column (4:3, Q7) with Best Fit off.

**Code change (one line per tab in `SettingsScreenLayout.Rows`):**
```
Audio:         MasterVolume, MusicVolume, SfxVolume, VoiceVolume, AmbienceVolume
Controls:      Haptics
Display:       Language, BatterySaver*
Accessibility: Subtitles, TextSize*, ColourBlind*
Account:       PlayerName*, PlayerId*, SignIn*, ResetData*
AwaitingDesign: (empty)
HiddenV1:      ReplayTutorial*, ReduceMotion*   (designed, not shown in v1; see "Hidden for later")
```
Visible row counts in v1: **Audio 5, Controls 1, Display 2, Accessibility 3, Account 4.**
`*` are new `SettingsControl` values (Q3/Q4). Add `SettingsControlKind.Button` (Copy, Retry, Reset), `Value` (read-only text, also used for Language in v1), `Status`, and `Segment` (Text size). Keep `Choice` for Language: the view draws it as a read-only value while `Languages.Length == 1` and as the stepper (Q5) once a second language ships. The existing layout test, "5 rows fit, every control placed or awaiting, never both", still passes with `AwaitingDesign` empty.

## Q3: Controls, Display, Accessibility and Account (v1)

**Controls** (1 row in v1)
| Row | Control | Behaviour |
|---|---|---|
| `Haptics` / `Buzz on bag taps, pickups, hits` | toggle → `GidiAudioSettings.Current.HapticsEnabled` (exists) | Turning it on plays one light haptic as a preview. Where there's no haptics hardware (WebGL, desktop, `!SystemInfo.supportsVibration`): row at 45% (CanvasGroup alpha 0.45, `interactable = false`, RT-117 grey-out), caption `Phones and tablets only` |

No keyboard map and no control remapping in v1: the HUD spec has no keyboard hints, and there's nothing to remap on touch.

**Display** (2 rows)
| Row | Control | Behaviour |
|---|---|---|
| `Language` / `Menus and subtitles` | read-only value `English`, Text 30 px `#F5F5F0`, Middle Right, ending at the row's right edge | **v1 decision: show the row as a single value, not hidden.** No arrows, no hit area, no sub-line. It tells players the game knows about language without offering a choice that does nothing. It becomes the stepper (Q5) when `SettingsRules.Languages` has 2+ entries |
| `Battery saver` / `Lower resolution, cooler phone` | toggle → `WebPerformanceBootstrap` battery saver (`gidi.perf.battery_saver`, -1 unset / 0 / 1; already built "for a future Settings screen") | Default comes from `FramePacingRules.DefaultBatterySaver` (on for phones with ≤ 4096 MB RAM, `LowMemoryMb`). On desktop/WebGL it does nothing, so the row is at 45% with caption `Phones and tablets only` |

No graphics-quality or FPS picker in v1: frame pacing is rule-driven (RT-105) and phones already run the lean URP asset.

**Accessibility** (3 rows in v1, Q4)
| Row | Control | Behaviour |
|---|---|---|
| `Subtitles` / `Text for voice lines and calls` | toggle → `GidiAudioSettings.Current.SubtitlesEnabled` (exists, **default on**) | `SubtitleOverlay` picks it up live |
| `Text size` / `Subtitles, tips and toasts` | segment `S` `M` `L` (left / mid / right) | New pref `gidi.a11y.text_size` (0/1/2, default 1). Font-size multiplier **0.9 / 1.0 / 1.2**, rounded to whole px, on subtitles, toasts, coach pills and the Continue/Game Over body copy only. HUD numbers, buttons and Settings keep their sizes, so nothing overflows with Best Fit off |
| `Colour-blind mode` / `Bolder danger colour + chevrons` | toggle | New pref `gidi.a11y.colour_blind` (default off). Danger telegraph `#FF7A1A` → Okabe-Ito vermilion `#D55E00`, chevron stroke ×1.5. Caution ▲ / LASTMA ◆ / Safe shapes unchanged (the shapes already carry meaning) |

**Account** (4 rows; UGS Friends stays off in v1 (`LeaderboardRules.FriendsEnabled = false`), so there's no friends, add-friend or share row)
| Row | Control | Behaviour |
|---|---|---|
| `Player name` / `Shown on leaderboards` | value, Text 30 px `#F5F5F0`, right | `AuthenticationService.Instance.PlayerName` (UGS `Name#1234`). Read-only in v1. Not loaded yet: `—`, caption `Appears once you're online` |
| `Player ID` / `Quote this if you contact us` | value (30 px `#9EA3AD`, middle-ellipsis: first 6 + `…` + last 4) + `Copy` (`btn_glass` 240×96) | `UgsBootstrap.PlayerId`. Copy → `GUIUtility.systemCopyBuffer` = full ID, toast `Player ID copied`. WebGL can block clipboard writes; if so, the toast shows the full ID for 4 s instead |
| `Sign-in` / `Guest account on this device` | status, 30 px, right | Ready: `● Signed in · guest`, teal. Initialising: `Connecting…` in `#9EA3AD` + `spinner_arc` 32 px. Failed or offline: `▲ Offline` in `#FF7A1A`, plus `Retry` (`btn_glass` 240×96) → `UgsBootstrap.EnsureSignedInAsync()`. Dot or triangle shape plus colour, never colour alone. No platform sign-in (Google/Apple) in v1 |
| `Reset game data` / `Wipes this device and cloud save` | `Reset` (`settings_btn_danger_normal`, 240×96, text `#FF7A1A` 28 px) | Opens the confirm modal below |

**Reset confirm modal** (preview `settings-account-reset-confirm-1920x1080.png`)
- Dim `rgba(2,3,5,.62)`, `panel_modal_normal` 1000×560 centred, padding 48.
- Kicker `▲ CAN'T UNDO`: 26 px `#FF7A1A`, tracking 8%.
- Title `Reset game data?`: 56 px `#F5F5F0`.
- Body, 28 px `#9EA3AD`, wraps to 3 lines at 904 px (**Kehinde decision: reset wipes device and cloud**):
  "This wipes your game progress on this device and in your cloud save: levels, Naira chips, bag, souvenirs and tutorial. You can't undo this. Your settings and player name stay."
  - Legacy Text has Rich Text off, so the emphasis is three Text runs, or turn Rich Text on for this one Text only: "and in your cloud save" in `#F5F5F0`, "You can't undo this." in `#FF7A1A`. Plain `#9EA3AD` all through is also acceptable.
- Buttons 392×144: **`Cancel`** (`btn_glass`, left; **default selection**; Esc and Back do the same) and **`Reset`** (`settings_btn_danger_*`, right). Reset is at 45% and not interactable for the first **1.0 s** after the modal opens, so a double-tap can't confirm it.
- On Reset:
  - Clear `PlayerProgress` on the device **and** delete/overwrite the Cloud Save `progress_v1` key, plus the bag, souvenirs, wallet and `gidi.onboarding.*`, both local and cloud. If offline, the reset is refused with the toast `Go online to reset your cloud save` so the cloud copy can't come back on the next sign-in.
  - Keep `gidi.audio.*`, `gidi.settings.*`, `gidi.a11y.*`, `gidi.perf.*` and the UGS account.
  - Close Settings, reload into Home, toast `Game data reset`.

**Locked tab** (`settings_tab_locked`): use it for a tab whose rows are all unavailable in this build. In v1 that's only **Account in a build without UGS** (no `UgsBootstrap` / services off). It also covers the interim state while a tab's rows aren't built yet, replacing PR #136's non-interactable plain tab.
- Look: `icon_lock_white` 30 px tinted `#9EA3AD` left of the label, label at 45%.
- It's still tappable and shows the toast `Account needs an online build` (or `Coming soon`).

## Q4: Colour-blind mode and Text size

Both are removed from Audio and now sit in **Accessibility** as rows 3 and 2 (table above). Audio only holds the five volume sliders. Neither has an owner or API yet (PR #136 gap 4).

Proposal: put both in `SettingsRules` / `SettingsPersistence`, with new keys `gidi.a11y.colour_blind` and `gidi.a11y.text_size` and a `GidiSettingsBridge.AccessibilityChanged` event that the danger-telegraph views, `SubtitleOverlay` and the toast and coach views listen to.

## Q5: language list (v1 ships **English only**; the other names are a **proposal for later**, for Kehinde to confirm)

Each language is shown in its own name, in this order, on the later Display › Language stepper:

| Code (BCP-47) | Button text (autonym) | English name | Notes |
|---|---|---|---|
| `en` | **English** | English | default (`SettingsRules.DefaultLanguage`) |
| `pcm` | **Naijá** | Nigerian Pidgin | alternative button text: `Pidgin`. Kehinde to pick |
| `yo` | **Yorùbá** | Yoruba | ù = U+00F9, á = U+00E1 (precomposed). Long form `Èdè Yorùbá` if preferred |
| `ha` | **Hausa** | Hausa | Long form `Harshen Hausa` |
| `ig` | **Igbo** | Igbo | Long form `Asụsụ Igbo` (ụ = U+1EE5) |

- **v1 ships English only (Kehinde decision).** `SettingsRules.Languages` exposes only `en`. Keep the other four in code as a hidden list (e.g. `SettingsRules.HiddenLanguages`, or entries with `Visible = false`) so they can be switched on per language when its strings land. The Display row shows the single value `English` (Q3).
- Font check (Plus Jakarta Sans Bold):
  - It has every glyph in these five names, plus ẹ ọ ṣ ụ and the combining grave, acute and dot below.
  - It **lacks Hausa's hooked letters ɓ ɗ ƙ ƴ** (U+0253, U+0257, U+0199, U+01B4). Full Hausa copy needs a fallback font, e.g. Noto Sans in the Font asset's fallback list.
  - Legacy `UI.Text` does no mark positioning. Yorùbá letters that only exist as base + combining mark (e.g. ẹ́, ọ̀) will render badly, so translated Yorùbá text must use precomposed characters where they exist, or the screen moves to TMP. The button names above are all precomposed and safe.
- Stepper metrics (**later, when a second language ships**; not in v1): left and right 120×96 (`settings_seg_left/right_normal` with `icon_back_white` 40 px tinted `#F5F5F0`; the right one flipped with scaleX −1), mid 360×96 (`settings_seg_mid_normal`). Name 30 px `#F5F5F0`, sub-line `{i} of {n}` 18 px `#9EA3AD`. Wraps around at the ends. Selecting saves at once and fires `LanguageChanged`.

## Q6: top-right cluster

Removed. The Settings screen has **only Back (top-left) and the title `Settings`**: no ₦ chip, no ♥ lives, no Settings button (a Settings button on Settings is a dead end). This confirms what PR #136 already does. Back, Esc and Android back close the screen and return to Home or Pause.

## Q7: layout

### 1920×1080 (desktop, safe margin 32 on all sides → safe rect x 32–1888, y 32–1048, 1856×1016)
Screen px, top-left origin. Code uses offsets from the safe rect (= `SettingsScreenLayout` constants).

| Element | Rect (x, y, w, h) | Notes |
|---|---|---|
| Back button | 32, 32, 144, 144 | `btn_glass_normal` (sliced 36). `icon_back_white` 44 px at (0, +16) from centre; caption `Back` 22 px `#9EA3AD` at (0, −34) |
| Title `Settings` | 196, 32, 600, 144 | 48 px `#F5F5F0`, Middle Left (safe x 164 = 144 + 20 gap) |
| Tab rail | 32, 208, 340, 816 | `panel_glass_normal`. Grid top = safe 176, bottom gap 24 |
| Tabs 1–5 | x 48, w 308, h 120; y **224 / 356 / 488 / 620 / 752** | pad 16, gap 12. Label 30 px at x +24 (lock icon variant: icon at +24, label at +64) |
| Body panel | 396, 208, 1492, 816 | `panel_glass_normal`, gap 24 from the rail |
| Rows 1–5 | x 436–1848 (w 1412), h 132; y **232 / 364 / 496 / 628 / 760** | padding 40 / 24. Divider 1 px white 8% at the row bottom. Bottom 108 px of the body stay empty |
| Row label / caption | x 436, label 32 px in the top half (Lower Left), caption 22 px in the bottom half (Upper Left, 4 px gap) | label column ends 24 px before the control |
| Slider | x 1328–1848 (520), track 16 high, centred on the row | `settings_slider_track` + `settings_slider_fill` (sliced 8/8/0/0), handle `settings_slider_knob` 80×80 (56 visible). **Handle Slide Area inset 28 px each side** so the knob stays in the row. Value read-out `70%`: 26 px `#9EA3AD`, right-aligned, 80 wide, ending 24 px left of the track |
| Toggle | x 1716–1848, 132×72 | `settings_toggle_on/off`, Image Simple, swapped on state |
| Segment S/M/L | x 1488–1848, 3 × 120×96 | left / mid / right pieces, `_selected` on the chosen one. Text 28 px: `#9EA3AD`, selected `#0F1219` |
| Language value (v1) | x 1148–1848 (700 wide), 48 high, centred on the row | Middle Right. Stepper later: x 1248–1848, 120 + 360 + 120, h 96 (Q5) |
| Row button (Copy, Retry, Reset) | x 1608–1848, 240×96 | Value text (Player ID) ends at x 1584 |
| Reset modal | 460, 260, 1000, 560 | buttons at y 628, 392×144 each, 48 from the panel edges |

Hit areas: the visible controls are 72–96 px high, but each control's raycast rect is the **full row height (132 px = 44 dp at 3x)**, and tabs and buttons stay ≥ 120 / 96 px with 132 px row spacing. Toggles flip when the whole row is tapped.

### 20:9 phone (2400×1080 ref; safe insets L/R 132, top 24, bottom 63, as in the HUD phone spec → safe 2136×993)
- Same constants. Back at (132, 24). Rail x 132–472, y 200–993. Body x 496–2268 (1772 wide), rows y 224 / 356 / 488 / 620 / 752, controls right-aligned to x 2228.
- Body inner height 745 → still **5 rows, no scroll**. The extra width goes to the label column. 19.5:9 (2340) is the same with 60 px less body width.
- Preview: `settings-audio-20x9-2400x1080.png`.

### 4:3 tablet (1024×768 physical → **1440×1080 ref**; safe 32 sides/top, 40 bottom → 1376×1008)
- Switch rule as on the HUD: `Screen.safeArea.width / height < 1.5` → narrow variant.
- Rail unchanged (x 32–372). Body x 396–1408 (1012 wide), rows x 436–1368, y 232 … 760 (inner 760 → **5 rows, no scroll**).
- **Slider 400** (x 968–1368) instead of 520. Language stepper (later) 96 + 312 + 96 (x 864–1368). Toggle, segment and buttons unchanged.
- Narrowest label column is 404 px (next to the later stepper; in v1 the short `English` value leaves far more): the 32-character caption limit is what keeps captions on one line at 22 px.
- 1 ref px = 0.71 physical px at 1024×768, so a 132-row is about 94 px, still above 44 pt.
- Preview: `settings-audio-4x3-1440x1080.png`.

Fallback: if `RowsThatFit(safeHeight)` < a tab's row count on some odd device (split screen, very tall insets), wrap the body in a vertical `ScrollRect` (clamped, no elastic, scrollbar 8 px teal at 60%). No v1 target device needs it.

## Legacy Text settings (no TMP)

Font: Plus Jakarta Sans Bold (Dynamic, Include Font Data).
- On every Text: **Best Fit off**, Rich Text off, Horizontal Overflow Overflow on single-line labels, Vertical Overflow Truncate, Raycast Target off.
- **No `Outline` component anywhere.** PR #136 currently adds `Outline` to the selected tab, to the language segment frame and to the glass fallback. Replace those with `settings_tab_selected`, the segment pieces and `panel_glass_normal`.
- One **`Shadow`** (#000 alpha 128, distance (0, −2), Use Graphic Alpha) only on text over glass: title, tab labels, row labels, values, button labels. Captions, segment text and danger-button text get no shadow.

| Text | Size | Colour | Align |
|---|---|---|---|
| Title | 48 | #F5F5F0 | Middle Left |
| Back caption | 22 | #9EA3AD | Middle Center |
| Tab label | 30 | #9EA3AD, selected #FAE69E, locked #9EA3AD @45% | Middle Left |
| Row label | 32 | #F5F5F0 | Lower Left |
| Row caption | 22 | #9EA3AD | Upper Left |
| Slider value `70%` | 26 | #9EA3AD | Middle Right |
| Segment | 28 | #9EA3AD, selected #0F1219 | Middle Center |
| Language value (v1) | 30 | #F5F5F0 | Middle Right |
| Stepper name / sub-line (later) | 30 / 18 | #F5F5F0 / #9EA3AD | Middle Center |
| Account values | 30 | name #F5F5F0, ID #9EA3AD, status teal / #9EA3AD / #FF7A1A | Middle Right |
| Row buttons | 28 | #F5F5F0, Reset #FF7A1A | Middle Center |
| Modal kicker / title / body / buttons | 26 / 56 / 28 / 36 | #FF7A1A / #F5F5F0 / #9EA3AD / #F5F5F0 (Reset #FF7A1A) | Left / Left / Upper Left (wrap) / Center |

## Sprites (exports/unity/settings/, PPU 100 @1x and 200 @2x, borders in px at 1x, double for @2x)

Import: Sprite (2D and UI), Mesh Type Full Rect, Bilinear, Clamp, no mips, Compression None (or a Sprite Atlas: ASTC 4×4 / BC7).

| Sprite | Size @1x | 9-slice L/R/T/B | Use |
|---|---|---|---|
| `settings_slider_track` | 48×16 | 8/8/0/0 | slider background, #333846 |
| `settings_slider_fill` | 48×16 | 8/8/0/0 | teal fill (hide at value 0) |
| `settings_slider_knob` | 80×80 | none | 56 Ø cream knob, teal dot, shadow baked |
| `settings_toggle_off` | 132×72 | none (knob baked) | grey track, knob left |
| `settings_toggle_on` | 132×72 | none (knob baked) | teal track and edge, knob right with a check |
| `settings_seg_left_normal` / `_selected` | 64×96 | 24/4/24/24 | first segment |
| `settings_seg_mid_normal` / `_selected` | 64×96 | 4/4/4/4 | middle segment (divider baked on its left) |
| `settings_seg_right_normal` / `_selected` | 64×96 | 4/24/24/24 | last segment (divider baked on its left) |
| `settings_tab_normal` | 96×96 | 30/30/30/30 | tab, white 3% |
| `settings_tab_selected` | 96×96 | 30/30/30/30 | gold 15% + 2 px gold 50% edge |
| `settings_tab_locked` | 96×96 | 30/30/30/30 | dashed 3 px #9EA3AD 45% (dashes stretch slightly) |
| `settings_btn_danger_normal` / `_pressed` | 96×96 | 36/36/36/36 | Reset row button and modal Reset |

Reused from the existing export: `panel_glass_normal`, `panel_modal_normal`, `btn_glass_*`, `icon_back_white`, `icon_lock_white`, `spinner_arc`.

The folder sits outside `sprites@*` on purpose: `tools/gen_unity.py` deletes `exports/unity/sprites@1x|2x` when it runs, and it keeps manifest entries whose files are elsewhere.

## Other notes for the PR #136 dev
- PR gap 9 (source of truth), **Kehinde decision: all settings are backed up to the cloud save.**
  - Every setting (all five volumes, haptics, subtitles, text size, colour-blind, language, battery saver; the hidden reduce-motion pref too) is written to PlayerPrefs at once, and then backed up to UGS Cloud Save.
  - Proposal for the dev: use a separate Cloud Save key `settings_v1`, not `progress_v1`, so Reset game data can wipe progress without wiping settings. Drop the stray `PlayerProgress.musicVolume / sfxVolume / hapticsEnabled / language` copies or migrate them into `settings_v1` once.
  - Upload is debounced: 2 s after the last change, plus once when Settings closes. On sign-in, if the cloud copy is newer (compare a `savedAt` stamp), apply it and refresh PlayerPrefs. Offline changes stay local and upload on the next sign-in.
  - Battery saver's default is per device (RAM rule), so a phone only takes the cloud value if the player set it on purpose (saved choice 0/1, not -1).
- PR gap 10: a 5% slider step is fine. Add the `70%` read-out so the step is visible.
- Every change saves at once, so there's no Apply button. Moving the SFX slider plays a short existing SFX (e.g. `SFX_hop`) once per step (throttled to 8/s). The Voice slider plays one short voice line when released, so the player hears the level.

## Hidden for later (designed, not shown in v1; Kehinde decision)
Keep the enum values and prefs in code. Leave them out of `SettingsScreenLayout.Rows` (list them in `HiddenV1`). Adding them back is a one-line change per tab, and both tabs stay within 5 rows.

| Row | Would go | Control | Behaviour when shown |
|---|---|---|---|
| `Replay tutorial` / `Show the coach steps on L1 again` | Controls, row 2 | button `Replay` (`btn_glass`, 240×96) | Deletes `OnboardingRules.PrefsDoneKey` (`gidi.onboarding.gpp063.done`). Toast `Tutorial will play next time you start L1` (2 s). `ShouldRun` only fires on L1 |
| `Reduce motion` / `Fewer shakes, pulses, shimmer` | Accessibility, row 4 | toggle | New pref `gidi.a11y.reduce_motion` (default off). Turns off bag shake (keeps the orange frame), the 1 Hz last-second pulse (colour change stays), leaderboard skeleton shimmer, and the Continue bar pulse (it steps once a second instead). The leaderboard, intro and continue specs already define this reduced-motion ("ln") variant, so this row is the switch for it |

Language stepper (Q5) is in the same state: designed, shown only when a second language ships.

## Decisions (Kehinde, relayed by the dev, Oct 31)
1. Reset game data wipes the device **and** the cloud save. The confirm copy says so and says it can't be undone. Cancel is the default and Reset waits 1 s.
2. Reduce motion and Replay tutorial are hidden in v1. Controls has 1 row, Accessibility 3.
3. English only. The Language row shows the single value `English`; the other languages stay in code, hidden.
4. All settings are backed up to the cloud save.

## Open for Kehinde
1. Language names for later (`Naijá` or `Pidgin`; short or long autonyms) and when localisation lands.
2. Reset keeps settings and player name (the spec assumes yes; settings live in `settings_v1`, separate from progress). Confirm.
