# GPP-LEADERBOARD-HOME: Home leaderboard tile + weekly L10 / Country board

Oct 31, 2026. Follows the RT-109 leaderboard spec (`exports/unity/README.md`, RT-109 section) and the d5577bd follow-ups. It answers the spec gaps listed in draft PR coach-K/G-Prototype#138 (`unity/l10-weekly-leaderboard`).

**Fixed decisions (not reopened here):**
- UGS Leaderboards `gidi_L01_time` … `gidi_L10_time`, sorted ascending, score in ms, chips in metadata, times shown as `mm:ss.hh`.
- L10 ranks by clear time.
- UGS Friends is off in v1, so the Friends tab is hidden.
- Legacy `UI.Text`: Best Fit off, no Outline, one Shadow (0, −2) #000 at 60% over glass.
- Minimum tap target is 144 px.
- Canvas is 1920×1080, Scale With Screen Size, match height 1.0.

Items marked **PROPOSAL** need Kehinde's OK before they count as decided.

Generator: `tools/gen_lb_home.py`. It renders only these sprites and merges manifest entries keyed by `file`. Do **not** re-run `gen_unity.py` for this; it wipes `sprites@1x/@2x`. The definitions for `seg_filter_pressed` and `pill_week_reset` are also in `gen_unity.py`.

## Previews (1920×1080)

| File | Shows |
|---|---|
| `exports/home-leaderboard-desktop.png` | Home with the leaderboard tile (clean) |
| `exports/home-leaderboard-annotated-desktop.png` | Same, with coordinates |
| `exports/home-leaderboard-aspects-desktop.png` | 16:9 / 20:9 / 4:3. Source renders: `home-leaderboard-20x9.png` (2400×1080), `home-leaderboard-4x3.png` (1440×1080) |
| `exports/home-leaderboard-states-desktop.png` | Tile states: normal, pressed, offline, disabled, focus |
| `exports/leaderboard-weekly-desktop.png` | Weekly L10, Global tab |
| `exports/leaderboard-country-desktop.png` | Weekly L10, Country tab (NG) |
| `exports/leaderboard-country-unavailable-desktop.png` | Country tab when the region has no board (KE) |
| `exports/leaderboard-country-empty-states-desktop.png` | Country unavailable (known / unknown region), country board with no times, Friends empty (parked) |
| `exports/leaderboard-tabs-desktop.png` | Filter tabs: v1 two-up, and the options if Friends comes back |

The HTML sources are in `mockups/` under the same names.

## 1. Home leaderboard button

**Position.** Keep the dev's tile beside Souvenirs: `GameUiFactory.AnchorTopRight(rt, 732, 0, 144, 144)`, with anchor and pivot at the top-right (1,1) and anchoredPosition (−732, 0) in the safe-area rect. That puts it left of Souvenirs (572) with the same 16 px gap as the rest of the cluster.

| Layout | Canvas | Safe area | Leaderboard tile | Notes |
|---|---|---|---|---|
| 16:9 desktop | 1920×1080 | x 32–1888, y 32–1048 (32 px desktop margin) | **x 1012–1156, y 32–176** | Souvenirs 1172–1316, Chips 1332–1592, Lives 1608–1728, Settings 1744–1888. The tagline ends at x 558, leaving 454 px clear. |
| 20:9 phone | 2400×1080 | 132 px notch inset each side (symmetric), bottom 63 | **x 1392–1536, y 0–144** | Same offsets. Over 800 px free. |
| 4:3 (1024×768, iPad) | 1440×1080 | 1376×1016, aspect 1.35 | **Two rows.** Souvenirs at anchoredPosition (0, −160) → x 1264–1408, y 192–336. Leaderboard at (−160, −160) → **x 1104–1248, y 192–336**. | With one row the tile's left edge is at x 500, which overlaps the tagline (ends at 558, y 106–144). Rule: if `safe.width / safe.height < 1.5`, use the second row (the HUD uses the same threshold). The Map column top is at y 504, so row 2 is clear. |

**Size.** 144×144, the same as Settings and Souvenirs.

**Icon.**
- New sprite `home/1x/icon_trophy.png` (44 px) and `home/2x/icon_trophy.png` (88 px). White, 3 px / 48-grid stroke, matching `icon_settings` and `icon_souvenirs`.
- Position (0, +16).
- `HomeScreenView.AddIcon` already loads `UI/Home/{1x|2x}/icon_trophy` and shows it untinted, so copying it into `Resources/UI/Home/` replaces the AccentGold-tinted leaderboard fallback with no code change.

**Label.**
- **"Ranks"**: 22 px #9EA3AD in a 144×30 rect at (0, −34). Best Fit **off**.
- Accessibility / tooltip name: "Leaderboard".
- Why not "Leaderboard": it measures 139.5 px at 22 px, leaving 2 px per side in a 144 tile. The PR only fits it by turning on `resizeTextForBestFit` (16–22), which breaks the Best Fit rule. **Dev must remove Best Fit on this caption.**
- Fallback if Kehinde wants the full word: "Leaderboard" at a fixed 20 px (127 px).

**States** (`exports/home-leaderboard-states-desktop.png`):

| State | Frame | Icon / caption | Behaviour |
|---|---|---|---|
| Normal | `btn_glass_normal` (9-slice, border 36) | White / #9EA3AD | Tap opens the leaderboard |
| Pressed | `btn_glass_pressed` (SpriteSwap, as `MakeButton` already does) | Image.color #FAE69E / #F5F5F0. Scale 0.96 for 80 ms | — |
| Offline | Normal, plus child `badge_tile_offline` (40×40). Anchor and pivot top-right at (−6, −6) inside the tile | Unchanged | **Still interactable.** Opens the board, which shows the RT-109 Offline card with the saved best. Badge shows when UGS is unreachable or not signed in |
| Disabled | `btn_glass_disabled` | 45% alpha. `interactable = false` | Only when leaderboards are not in the build or are switched off remotely. Never used for offline |
| Focus (WebGL keyboard / controller) | `btn_glass_highlight` (24 px glow margin) | Unchanged | Enter = tap |

**Target.** Opens weekly L10 if the weekly board is confirmed (the PR's `LeaderboardEntryLevel`). Otherwise it opens the player's current level (highest unlocked).

## 2. Weekly header on L10 (PROPOSAL)

No weekly reset decision exists in the specs. RT-109 says only "a weekly view, if wanted, is a UGS reset schedule on a separate ID", and its open question 2 asks whether a weekly board is wanted. So everything below is a **proposal for Kehinde to confirm**. It matches the PR's `WeeklyLeaderboardRules`.

Side card, top to bottom (440 wide, inner 392, gap 14):

| # | Element | Spec |
|---|---|---|
| 1 | Kicker | `icon_trophy` 30 gold, then **"WEEKLY · L10 · W44"**, 22 px #E8B21E, letter-spacing as RT-109 (208 px wide). W = ISO week number in UTC, no year. |
| 2 | Title | **"Ojuelegba Chaos"**, 46 px #F5F5F0. Wraps to 2 lines (Horizontal Overflow Wrap), as RT-109 allows. |
| 3 | "Same road" line | **"Same road for everybody this week. Fastest clear wins."** 24 px #F5F5F0, 2 lines. This replaces RT-109's "Fastest clear time" subtitle. The PR's shorter `Subtitle` ("Same road for all · Resets in 1d 15h") becomes two elements: this line and the pill. |
| 4 | Reset pill | `pill_week_reset` (9-slice, height 44, border 22), with `icon_timer_white` 28 tinted #FAE69E and Text 22 px #FAE69E. |
| 5 | Filter tabs | See Q3. |
| 6 | Stats | `kv2` rows: **"Your best this week"** (shows "—" until you have a weekly entry), "Your rank", "Players". |
| 7 | CTA | BEAT AM. |

The pinned row label in the list reads **"YOUR BEST THIS WEEK · PINNED"**.

**Countdown format.** Uses the PR's `ResetsIn`, rounded up:

| Time left | Shows |
|---|---|
| ≥ 1 day | "Resets in {d}d {h}h", e.g. "Resets in 1d 19h" |
| < 1 day | "Resets in {h}h {mm}m" |
| < 1 hour | "Resets in {m}m", minimum 1 |

- In the last hour, tint the pill and icon #FF7A1A.
- At 0, refetch, then show toast **"New week, new road. W45 don start!"**
- Update once a minute.
- Times are UTC on the server and the client shows a relative time, so the player's timezone does not matter.
- Reset is Monday 00:00 UTC (01:00 WAT).

**L10 level tab.** When weekly is on, its sub-label reads "Weekly" instead of "Ojuelegba". PROPOSAL.

**Backend flag.** A weekly board needs a **UGS reset schedule**, and it is a new board ID beyond `gidi_L01..L10_time`:
- `gidi_L10_time_weekly`, plus one board per country (`gidi_L10_time_weekly_NG`, …).
- Each one needs Reset: cron `0 0 * * 1` (UTC) with **archive on** in the Dashboard / `.lb` config.
- The client WeekId (ISO week, UTC) and the seed `"gidi.L10."+weekId` must match the server schedule, or the "same road" claim breaks at the boundary.
- Do we keep an all-time L10 board as well? See open questions.

## 3. Filter tabs

**v1, weekly L10 only.** Two tabs, Global and Country:
- Each hit rect is **196×144** across the 392 row (x 24–220 and 220–416 inside the card).
- The visible segment sprite is inset 4 px on the inner edge, so the art still reads as 192 + 8 gap + 192, like RT-109.
- Sprites: `seg_filter_off`, `seg_filter_on`, and new **`seg_filter_pressed`** (80×80, border 36).
- This matches the PR's `SegmentRect` (left 24, total 392, gap 8) with the Friends tab removed. The difference is that the gap belongs to the hit area, so neither tab drops below 196.

**L1–L9.** Global only, so hide the row. In its place put a 22 px muted caption **"GLOBAL · ALL-TIME"**, which keeps the "Your best" block in the same place.

**Country tab style.**
- New **`icon_country`** (generic globe with a map pin; gold and `_white` versions, 64 px) at 40 px, over the ISO code in 28 px, e.g. **"NG"** (43 px wide).
- If the region is unknown, the label reads **"Country"** (111 px).
- Colours match Global: on #FAE69E, off #9EA3AD.
- No flags:
  - legacy UI.Text has no emoji glyphs;
  - about 250 flag sprites would need to ship;
  - some regions are disputed.
- On the Country board, the list panel shows a caption above the header: `icon_country` 28 + **"NG · NIGERIA · THIS WEEK"** (22 px muted). The name comes from `RegionInfo.EnglishName`; if that is unavailable on IL2CPP or WebGL, show the code only.

**If all three tabs return** (`exports/leaderboard-tabs-desktop.png`):

| Option | Card | Tabs | Effect |
|---|---|---|---|
| **A (recommended)** | 520 (inner 472) | 3 × 152 + 2 × 8 | List panel x 544, width 1312. Text labels still fit ("Friends" 111 px). |
| B | 496 (inner 448) | Icon-only, 3 × 144 + 2 × 8 | Plus a 22 px caption naming the selected tab. Loses the country code. |
| Don't | 440 (inner 392) | 3 × 125 | Below the 144 minimum. |

## 4. Empty states

**Country not available** (`leaderboard-country-unavailable-desktop.png`). This shows when the region is known but has no board, or when the region is unknown. It is centred in the list panel:
- `icon_country` 96, #9EA3AD.
- Title 40 px #F5F5F0:
  - known region: **"No {CC} board yet"**, e.g. "No KE board yet";
  - unknown region: **"Country board no dey yet"**.
- Body 30 px muted:
  - known region: **"Country boards are open for a few countries for now. Your time still counts on Global."**
  - unknown region: **"We no fit tell your country from this device. Your time still counts on Global."**
  - The PR's body ("Global and Friends still count…") mentions Friends, so replace it while Friends is off.
- CTA `btn_glass` 392×144: `icon_trophy` 44 + **"See Global"**. It switches the tab.
- Caption 24 px muted: **"Country comes from your device region ({CC})."**
- Side card: rank and players show "—"; "Your best this week" still shows the time, because it is a Global value.

**Country board open but no times this week.** Use the RT-109 Empty card:
- `icon_country` 96 gold.
- Title **"No times yet in NG this week"**.
- Body "Clear Ojuelegba Chaos and your time goes up first."
- CTA **OYA, CROSS!**

**No friends yet** (parked, not in v1). Keep the RT-109 / PR copy:
- `icon_group` 96 gold.
- Title "No friends on this board yet".
- Body "Add friends with their Gidi name and race their times here."
- CTA "Add friends" (392×144), plus `btn_glass` "Share my name".
- Caption "Your Gidi name: {name}#{4 digits}".
- Ship none of this until UGS Friends is on.

## 5. Country picker / add-friend (PROPOSAL)

- **No country picker and no add-friend flow in v1.**
- Country comes from the device region (`RegionInfo.CurrentRegion`) or the UGS / player locale, normalised as in the PR (`en-NG` → `NG`; reject ZZ / IV / AA / X* / QM–QZ).
- Keep the PlayerPrefs override `Gidi.LeaderboardCountry` for **dev / QA only**. Hide it in release builds.
- Lock the country for the week: write `country` into the score metadata on the first weekly submit, and reuse it for the rest of that week. Travelling or changing the device region then can't be used to farm several country boards.
- Later: validate the country in Cloud Code for anti-cheat.
- Add-friend waits for UGS Friends.

## New sprites (manifest.json, PPU 100 at 1x / 200 at 2x, borders in 1x px)

| Name | Files | Size | 9-slice | Use |
|---|---|---|---|---|
| `icon_trophy` | `home/1x`, `home/2x` | 44 | — | Home tile icon, white |
| `badge_tile_offline` | `home/1x`, `home/2x` | 40 | — | Offline badge, pivot (1,1) at (−6, −6) |
| `icon_country` / `icon_country_white` | `sprites@{1x,2x}/icons/ui/` (+ `white/`) | 64 | — | Country tab and empty state. SVG: `svg/icons/country.svg` |
| `seg_filter_pressed` | `sprites@{1x,2x}/leaderboard/` | 80×80 | 36 all sides | Pressed segment |
| `pill_week_reset` | `sprites@{1x,2x}/leaderboard/` | 80×44 | 22 all sides | Weekly reset countdown |

## Open questions for Kehinde

1. Is the weekly L10 board wanted at all? Is a Monday 00:00 UTC (01:00 WAT) reset OK?
2. Keep an all-time L10 board as well (e.g. behind "All-time" in the list), or weekly only?
3. Caption "Ranks", or "Leaderboard" at a fixed 20 px?
4. Which countries get boards? The PR has NG, GH, GB, US. Each one is a UGS board with its own reset.
5. Do L1–L9 get Country boards later? That would be 40 more boards for 4 countries.
6. Home tile: open weekly L10 or the current level?
7. A "new week" dot on the Home tile after a reset (unseen W45)?
8. Dev to fix: Best Fit on the caption; Country copy that mentions Friends. Also check that `Random.InitState(seed)` alone makes the L10 road deterministic (no other RNG sources).
