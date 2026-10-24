# RT-117 In-run HUD: consolidated support spec (current HUD + bag)

Full detail stays in `HUD_Landscape_Spec.md`; this page is the one-screen build list for G-Prototype PR #106 (Stats/Pause row + level-card title) and what's left after it. Reference 1920×1080, CanvasScaler match height 1.0, everything inside `Screen.safeArea`, touch targets ≥ 144. Mockups: `hud-bag-*` (the target HUD), `hud-owa-*` (power-up active), `hud-warn-*`, `hud-toast-*`, tablet `tablet-hud*`.

| # | Element | Anchor (safe rect) | Size | Status vs PR #106 |
|---|---|---|---|---|
| 1 | Level card `L5 · Oshodi Expressway` / `Saved N · Best N` (`HudTextRules` title; L10 is `L10 · Ojuelegba Chaos`, no endless form) | top-left 0,0 | 400×144 | title done in #106; drop the L10 endless branch (RT-108) |
| 2 | Stock panel GROUP · CHANGE (pips) | top row, centred between 1 and 3 | ≈396×144 | built; no OWA! cell |
| 3 | Chips `₦12,450` / `NAIRA CHIPS` | top-right row | ≥240×144 | built (`NairaCounterView`) |
| 4 | Lives `♥ 3` | top-right row, 16 gap | ~120×144 | built (`CapacityPipsView`) |
| 5 | Stats | top-right, `StatsRightInset` = Pause + 16 | 144×144, icon 44, caption 22 | **done in #106** (`HudStatsPauseButtons`, `icon_stats_white`) |
| 6 | Pause | top-right outermost, `PauseRightInset` | 144×144 | **done in #106** (`icon_pause_white`) |
| 7 | PICK UP | bottom-left, centre (360, 786) desktop / (492, 723) phone | 216 Ø | built (PR #59); nothing above it now |
| 8 | D-pad | centre (86.1% W, 70.2% H), r 16.7% H | 360 Ø | built |
| 9 | **Bag row** (4 slots, `BAG · TAP TO USE` label 44 above) | bottom-right: right = safe right − 32, bottom = d-pad top − 24 | 612×144 (slots 144, gap 12); desktop x 1276–1888, phone x 1564–2176, y 410–554 | **to build** (GPP-021 section) |
| 10 | Timer chips (Malta / Pure Water / Siren) | top-centre, y 198–368 | 140 badge + 170 ring | built (#85) |
| 11 | Owa freeze ring | on the Owa bag slot, 124 | — | **move** from the OWA! button (#107) to the bag slot (RT-118 section) |
| 12 | Toasts | top-centre, y 420 band, left edge ≥ 744 when the bag-full toast shows | auto × 72 | built (#90) |
| – | ~~OWA! button~~ | removed Oct 24 | — | **remove/hide** `MobileControlsView` OWA! (`_owaRoot`, rim, label, pips, `FreezeTimer`) |
| – | ~~Endless score strip~~ | removed (L10 timed) | — | **remove** |

Sorting / z-order: 3D → world telegraphs → HUD panels (canvas 100) → touch controls (PICK UP, bag, d-pad: never overlapping) → toasts → onboarding coach (115) → Pause (124) → level intro (125) → splash (130). Modals (continue, stats) sit on the Pause layer with the 62% `#02030A` dim.

Clearances to keep (1080): top row ends y 176; chips/ring band 198–368 at x 875–1045; bag starts y 410 / x ≥ 1276 (desktop); d-pad top y 578; PICK UP top y 678. Tablet 4:3 (aspect < 1.5): two-row top HUD per the tablet section; the bag keeps its rule (right − 32, d-pad top − 24).

Wiring the dev needs: `HudStatsPauseButtons.PauseHandler = PauseScreenView.Open`, `StatsHandler = StatsScreenView.Open` (set by those screens, as in #106). Pause also opens on app background. Stats/Pause are disabled (45%) while the continue modal or level intro is up.
