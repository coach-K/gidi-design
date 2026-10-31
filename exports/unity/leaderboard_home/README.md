# GPP-LEADERBOARD-HOME: Home leaderboard tile + weekly L10 board (Global / Friends / Country)

- **v1:** Oct 31, 2026, commit `2a1cb93`.
- **v2:** Oct 31, 2026, after decisions Kehinde made (relayed by the dev).

Follows the RT-109 leaderboard spec (`exports/unity/README.md`, RT-109 section) and the d5577bd follow-ups. It answers the spec gaps listed in draft PR coach-K/G-Prototype#138 (`unity/l10-weekly-leaderboard`).

## Decided (Kehinde, via the dev, Oct 31)

| # | Decision | Replaces |
|---|---|---|
| D1 | **The Friends tab stays in v1.** Three tabs: Global, Friends, Country. | v1's "UGS Friends off, Friends hidden" |
| D2 | **The weekly L10 board resets Monday 00:00 UTC** (01:00 WAT). | v1 proposal Q2, now decided |
| D3 | **The Home label is "Ranks".** | v1 open question 3 |
| D4 | **Country boards are NG, GH, GB and US**, already created in UGS. | v1 open question 4 |

**Also fixed (not reopened):**
- UGS Leaderboards `gidi_L01_time` … `gidi_L10_time`, sorted ascending, score in ms, chips in metadata, times shown as `mm:ss.hh`.
- L10 ranks by clear time.
- Legacy `UI.Text`: Best Fit off, no Outline, one Shadow (0, −2) #000 at 60% over glass.
- Minimum tap target is 144 px.
- Canvas is 1920×1080, Scale With Screen Size, match height 1.0.

Anything still marked **PROPOSAL** needs Kehinde's OK.

**Generator:** `tools/gen_lb_home.py`.
- With no arguments it renders the v2 sprites and the leaderboard previews.
- `--all` also renders the v1 sprites and the Home previews.
- Manifest entries merge keyed by `file`, and no entry is ever dropped.
- Do **not** run `gen_unity.py`; it wipes `sprites@1x/@2x`. The definitions for `seg_filter_pressed` and `pill_week_reset` are also in `gen_unity.py`, and the SVGs `icons/svg/{country,friends}.svg` are picked up by its icon loop.

## Previews

| File | Shows |
|---|---|
| `exports/home-leaderboard-desktop.png`, `-annotated-desktop.png` | Home with the "Ranks" tile (1920×1080) |
| `exports/home-leaderboard-aspects-desktop.png` (+ `home-leaderboard-20x9.png`, `home-leaderboard-4x3.png`) | 16:9 / 20:9 / 4:3 |
| `exports/home-leaderboard-states-desktop.png` | Tile states |
| `exports/leaderboard-weekly-desktop.png` | **v2:** weekly L10, Global tab, 520 card with 3 tabs |
| `exports/leaderboard-weekly-4x3.png` | **v2:** the same at 1440×1080, chips column hidden |
| `exports/leaderboard-weekly-friends-desktop.png` | **v2:** Friends tab, v1 "coming soon" state |
| `exports/leaderboard-country-desktop.png` | Country tab (NG) |
| `exports/leaderboard-country-unavailable-desktop.png` | Country tab when the region has no board (KE) |
| `exports/leaderboard-country-empty-states-desktop.png` | **v2:** Friends v1 / Friends later / Country unavailable (known and unknown region) |
| `exports/leaderboard-tabs-desktop.png` | **v2:** three-tab row with coordinates, on and pressed states, and the "don't" option |

The HTML sources are in `mockups/` under the same names. All are 1920×1080 unless noted.

## 1. Home leaderboard button (label decided: "Ranks")

**Position and size.** 144×144 at `GameUiFactory.AnchorTopRight(rt, 732, 0, 144, 144)`, left of Souvenirs. Anchor and pivot are top-right (1,1); anchoredPosition is (−732, 0) in the safe-area rect.

| Layout | Canvas / safe area | Tile |
|---|---|---|
| 16:9 desktop | 1920×1080; safe x 32–1888, y 32–1048 | **x 1012–1156, y 32–176**. Souvenirs is at 1172–1316. |
| 20:9 phone | 2400×1080; 132 px notch inset each side, bottom 63 | **x 1392–1536, y 0–144** |
| 4:3 | 1440×1080; safe 1376×1016, aspect 1.35 | If `safe.width / safe.height < 1.5`, use a second row: Souvenirs at anchoredPosition (0, −160) → x 1264–1408; the tile at (−160, −160) → **x 1104–1248, y 192–336**. In one row the tile would overlap the tagline (which ends at x 558). |

**Icon.** `home/{1x,2x}/icon_trophy` (44 / 88 px, white) at (0, +16). The PR's `AddIcon` loads it untinted, so it needs no code change.

**Caption.** **"Ranks"** (decided, D3): 22 px #9EA3AD in a 144×30 rect at (0, −34). **Best Fit off.** The PR has `resizeTextForBestFit = true` on this caption, and it must be removed. Accessibility / tooltip name: "Leaderboard".

**States:**

| State | Frame | Look | Behaviour |
|---|---|---|---|
| Normal | `btn_glass_normal` | White icon | — |
| Pressed | `btn_glass_pressed` | Icon #FAE69E, caption #F5F5F0, scale 0.96 for 80 ms | — |
| Offline | Normal, plus `badge_tile_offline` 40×40 at top-right (−6, −6) | — | Still tappable; opens the RT-109 Offline card with the saved best |
| Disabled | `btn_glass_disabled` | 45% | Only when leaderboards are switched off |
| Focus | `btn_glass_highlight` | — | WebGL keyboard / controller |

**Target.** Opens weekly L10 (the PR's `LeaderboardEntryLevel`), since the weekly board is decided.

## 2. Weekly header on L10 (reset decided: Monday 00:00 UTC)

Side card, top to bottom (v2 card is **520 wide**; see Q3):

| # | Element | Spec |
|---|---|---|
| 1 | Kicker | `icon_trophy` 30 gold, then **"WEEKLY · L10 · W44"**, 22 px #E8B21E. W = ISO week in UTC. |
| 2 | Title | **"Ojuelegba Chaos"**, 46 px. Fits on one line in the 472 inner width. |
| 3 | "Same road" line | **"Same road for everybody this week. Fastest clear wins."** 24 px #F5F5F0. |
| 4 | Reset pill | `pill_week_reset` (height 44, border 22), with `icon_timer_white` 28 + Text 22 px #FAE69E. At 1920×1080: x 56, y 420–464. |
| 5 | Tabs | y 480–624 (Q3). |
| 6 | Stats | "Your best this week" / "Your rank" / "Players". |
| 7 | CTA | BEAT AM, x 56–528, y 876–1020. |

The pinned row in the list reads **"YOUR BEST THIS WEEK · PINNED"**.

**Countdown.** The PR's `ResetsIn`, rounded up:

| Time left | Shows |
|---|---|
| ≥ 1 day | "Resets in {d}d {h}h" |
| < 1 day | "Resets in {h}h {mm}m" |
| < 1 hour | "Resets in {m}m", minimum 1 |

- In the last hour, tint the pill #FF7A1A.
- At 0, refetch, then show toast **"New week, new road. W45 don start!"**
- The L10 level tab's sub-label reads "Weekly" (PROPOSAL).

**Backend.** Every weekly board needs the UGS reset schedule, cron `0 0 * * 1` (UTC) with archive on:
- `gidi_L10_time_weekly`;
- `gidi_L10_time_weekly_NG`, `_GH`, `_GB` and `_US` (D4 says these are created; **confirm the reset schedule is set on all five**).

The client WeekId (ISO week, UTC) and the seed `"gidi.L10."+weekId` must match the server's week. **Friends needs `GetScoresByPlayerIdsAsync`, which UGS does not support on bucketed (tiered) leaderboards, so these boards must stay unbucketed.**

## 3. Filter tabs: three tabs (decided, D1)

**Layout.** I kept my recommended **520 side card** (option A from v1). Inner width is 472 (24 padding each side, measured from the card edge; the 2 px glass border sits inside the padding). That gives **3 × 152 + 2 × 8**. The list panel moves to x 544 in the safe area.

Coordinates at 1920×1080 desktop (safe origin 32, 32), taken from the rendered mock:

| Element | Rect |
|---|---|
| Side card | x 32–552, y 208–1048 (RT-109 top 176 in the safe area) |
| Tab row | x 56–528, y 480–624 |
| List panel | x 576–1888 (1312 wide), y 208–1048 |

| Tab | Hit rect (Button) | Visible sprite (child Image) | Size |
|---|---|---|---|
| Global | x 56–213 | x 56–208 | hit 157 × 144 |
| Friends | x 213–371 | x 216–368 | hit 158 × 144 |
| Country | x 371–528 | x 376–528 | hit 157 × 144 |

The hit rects split the 8 px gaps between neighbours, so the row has no dead taps and the smallest tap area is **157 × 144** (≥ 144). Visible segments are 152 × 144, with insets of 0/5, 3/3 and 5/0 px on each tab's left/right edges.

In card-local units (Unity, card pivot top-left):
- tab x = 24, 181, 339, with widths 157 / 158 / 157;
- tab row top = 272 below the card top;
- the PR's `SegmentRect(left 24, total 392, gap 8)` becomes **total 472, three tabs, gap counted in the hit rects**.

**Other aspects:**

| Aspect | Canvas | Side card | List panel | Notes |
|---|---|---|---|---|
| 20:9 | 2400 | x 132–652 | x 676–2268 (1592) | Tab x 156–628 |
| 4:3 | 1440 | x 32–552 | x 576–1408, **832 wide** | Columns 88/60/1fr/250/210 leave the name only ~56 px |

**4:3 rule.** When the list panel is under 1100 px wide, **hide the CHIPS (RUN) column**. Columns become 88 / 60 / 1fr / 250; the name then gets about 286 px, and chips stay in the row's metadata. See `leaderboard-weekly-4x3.png`. The 520 card still fits on 4:3, so the layout gives no reason to change the recommendation.

**States** (each tab):

| State | Frame | Icon + label |
|---|---|---|
| Off | `seg_filter_off` | #9EA3AD |
| On | `seg_filter_on` | #FAE69E |
| Pressed | `seg_filter_pressed` | #F5F5F0 |

- Icons are 40 px, tinted with Image.color: `icon_trophy_white`, **`icon_friends_white`** (new) and `icon_country_white`.
- Label 28 px: "Global" (90 px), "Friends" (111 px, 20 px clear each side in 152), and the country ISO code ("NG", "GH", "GB", "US"). The country label is "Country" if the region is unknown.

**L1–L9 (PROPOSAL).** Global + Friends only, because country boards exist only for weekly L10:
- two tabs with hit rects 236 × 144 each (x 24–260 and 260–496 in the card);
- visible sprites 232, insets 0/4 and 4/0 px.

Friends on L1–L9 needs no new boards (`GetScoresByPlayerIdsAsync` on `gidi_L0x_time`). The PR currently shows Global only on L1–L9; see the open questions.

**Don't.** Three tabs in the 392 row gives 125 each, which is under the minimum. Icon-only 3 × 144 on a 496 card loses the country code; not used.

## 4. Empty states

### Friends tab, v1 (no add-friend flow)

**How friends get onto the board.**
- The Friends view is not its own board. It takes the player's **UGS Friends** relationships (`FriendsService.Instance.Friends`; it needs a signed-in player, and anonymous sign-in is fine) and asks the same weekly board for their entries with `GetScoresByPlayerIdsAsync(boardId, friendIds)`. Your own row is added to that list.
- A friendship only exists after one player sends a request (`AddFriendAsync` / `AddFriendByNameAsync`) and the other accepts it. **v1 has no screen that does this, so every v1 player has zero friends** and the tab always shows this state. The copy says so plainly.
- Nothing is imported from contacts or other platforms.

`exports/leaderboard-weekly-friends-desktop.png`, centred in the list panel:
- `icon_friends` 96, gold.
- Title 40 px: **"Friends board coming soon"**
- Body 30 px muted: **"You can't add friends in Gidi++ yet. When you can, the friends you add will show here with their times for this week."**
- CTA `btn_glass` 392×144: `icon_trophy` 44 + **"See Global"** (switches the tab).
- Caption 24 px: **"Your Gidi name: {name}#{4 digits}"**. The UGS player name is shown so players know it already; there is no share button in v1.
- Side card: "Your best this week" still shows the time; rank and players show "—".

**Later, once an add-friend flow ships:**
- Friends but no times this week: **"No friend times this week yet"** / "Clear Ojuelegba Chaos and set the time for them to chase." / OYA, CROSS!
- No friends: the RT-109 copy ("No friends on this board yet" / "Add friends with their Gidi name and race their times here." / Add friends · Share my name).

### Country not available (copy fixed: mentions Friends again)

- `icon_country` 96, #9EA3AD.
- Region known but not one of NG / GH / GB / US:
  - title **"No {CC} board yet"**;
  - body **"Country boards are open for Nigeria, Ghana, the UK and the US for now. Your time still counts on Global and Friends."**
- Region unknown:
  - title **"Country board no dey yet"**;
  - body **"We no fit tell your country from this device. Your time still counts on Global and Friends."**
  - The tab label reads "Country".
- CTA **"See Global"** (392×144).
- Caption **"Country comes from your device region ({CC})."**
- "Counts on Friends" is accurate: your weekly entry is the same row friends would see, even though v1 players have no friends yet.

### Country board open, no times this week

RT-109 Empty card: `icon_country` gold, "No times yet in NG this week" / "Clear Ojuelegba Chaos and your time goes up first." / OYA, CROSS!

## 5. Country source (PROPOSAL, unchanged)

- No country picker in v1.
- Country comes from `RegionInfo.CurrentRegion` or the UGS locale, normalised as in the PR.
- Show a country board only for NG, GH, GB and US; any other region gets the "not available" state.
- Keep the PlayerPrefs override `Gidi.LeaderboardCountry` for dev / QA only.
- Lock the country for the week in the score metadata.
- Cloud Code validation later.
- The add-friend flow is a separate later feature (see Q4).

## Sprites (manifest.json, PPU 100 at 1x / 200 at 2x, borders in 1x px)

| Name | Files | Size | 9-slice | Use |
|---|---|---|---|---|
| `icon_trophy` | `home/1x`, `home/2x` | 44 | — | Home tile icon, white |
| `badge_tile_offline` | `home/1x`, `home/2x` | 40 | — | Offline badge, pivot (1,1) at (−6, −6) |
| `icon_country` / `_white` | `sprites@{1x,2x}/icons/ui/` (+ `white/`) | 64 | — | Country tab and empty state |
| **`icon_friends` / `_white`** (v2) | `sprites@{1x,2x}/icons/ui/` (+ `white/`) | 64 | — | Friends tab and empty state. Two equal busts; not `icon_group`, which is the pickup passengers icon. SVG: `svg/icons/friends.svg`. Pressed = `seg_filter_pressed` + white icon tinted #F5F5F0. |
| `seg_filter_pressed` | `sprites@{1x,2x}/leaderboard/` | 80×80 | 36 | Pressed tab (all three) |
| `pill_week_reset` | `sprites@{1x,2x}/leaderboard/` | 80×44 | 22 | Weekly countdown |

## Open questions for Kehinde

1. Since v1 has no add-friend flow, the Friends tab will always show "coming soon". Keep it visible anyway (D1), or should the add-friend flow (by Gidi name, `AddFriendByNameAsync`) join v1?
2. L1–L9: Global + Friends (as RT-109 had), or Global only (as the PR has now)?
3. Keep an all-time L10 board as well as the weekly one?
4. A "new week" dot on the Home tile after the reset?
5. Dev to check:
   - remove Best Fit on the "Ranks" caption;
   - replace the Country copy with the text above;
   - the reset schedule is on all five weekly boards and none are bucketed;
   - `Random.InitState(seed)` alone makes the L10 road deterministic.
