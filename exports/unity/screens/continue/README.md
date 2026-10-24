# GPP-066 Continue modal: states (G-Prototype PR #109)

Mockups: `continue-*` (offer, existing), `continue-states-*` (all six), `continue-loading-*`, `continue-failed-*`, `continue-none-*`, `continue-countdown-*`. Source `tools/gen_continue.py`.
Code: `ContinueModalRules` (copy, button rules), `ContinueOfferPanel` (view, `SetBusy`, `RewardedChosen` / `ChipsChosen` / `Declined`), `ContinuePanelFit` (scales the 800-high design down when the safe height is smaller). **1 continue per run** (`MaxContinuesPerRun = 1`); the owner of that rule passes "continues remaining" in.

Layout is unchanged from PR #109: panel 1000 wide (`PanelWidth`), padding 48, kicker 40/34, title 56 px at 78, subtitle at 150, three buttons 144 high (`ButtonHeight`) with 20 gaps (`ButtonGap`) from y 220, footer under the buttons. Reuses `panel_glass`, `btn_cta_*`, `btn_glass_*`, `icon_ad`, `icon_chip`, `icon_wifi_off`, `spinner_arc` (RT-109). No new sprites.

| State | Trigger (code) | Kicker / title / subtitle | Watch ad | Chips | End run | Footer |
|---|---|---|---|---|---|---|
| 1 Offer | remaining 1, not busy | `ALMOST THERE` / `Continue this run?` / `Subtitle(level, location, endless=false)` | CTA on | glass, on if `wallet ≥ ContinueChipsCost(level)` (₦100 L1, ₦125 L2+) else 45% + grey | glass, muted text | `Footer(wallet, 1)` |
| 2 Countdown | **new (proposal)**: 10 s from open | kicker gets ` · 7s`; 12 px gold bar under the subtitle drains | as Offer | as Offer | as Offer | as Offer |
| 3 Ad loading | `SetBusy(true)` after Watch ad | unchanged | label `Loading ad…` + `spinner_arc` 44 px (1 rev/s), CTA at 85% | 45% grey, not interactable | 45% grey, not interactable | `Loading ad… · countdown paused` |
| 4 Ad unavailable / failed | ad not ready, or load/show fails or is closed early | unchanged | glass, dashed outline, `icon_wifi_off` + `Ad not available`, not interactable | gets focus (gold outline + 4 px glow) if affordable | on | `▲ Couldn't load an ad. Try again later or use chips.` in #FF9E57 (triangle = caution shape) |
| 5 Last 3 s | countdown ≤ 3 | kicker `◆ TIME UP · 2s` in orange; bar orange | on | on | on | `At 0 s the run ends (same as End run)` |
| 6 No continues left | remaining 0 | `RUN OVER` / `TitleNoneLeft` "Run over" / `SubtitleNoneLeft` | 45% grey, off | 45% grey, off | becomes CTA `See results ▷` → Game over | `1 of 1 continue used · Fair play: max 1 continue per run` |

Rules
- `AdEnabled(remaining, busy)` and `ChipsEnabled(remaining, busy, wallet, cost)` stay the source of truth; the visuals above are what "off" looks like (45% opacity + grayscale, `interactable = false`, label kept so the player sees why).
- Ad failed: no retry button (avoids ad spam); the ad slot comes back the next time the modal opens in a later run. Chips spend never needs a network.
- Countdown (proposal, not in PR #109): 10 s, pauses while busy (ad loading/showing) and while the app is backgrounded; at 0 → same path as `Declined` (End run). Reduce motion: bar steps per second, no pulse. If you don't want a timeout, drop states 2 and 5; the others don't depend on it.
- State 6 normally never shows (the modal isn't opened when remaining = 0); it covers the case where the run ends again after the one continue and the game still routes through this panel. If the game skips straight to Game over, ignore it.
- Back / Escape = End run (not while busy).
