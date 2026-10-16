# Gidi++ Vision Brief (for design)

Source: internal vision doc v0.2 (12 Oct 2026, decisions locked), built on v0.1.

## What the game is
- **3D, not 2D.** Unity 6 URP, **perspective camera** looking down the road over Baba Gidi (see `levels/L01*.png`). **Landscape only.**
- Traffic-crossing runner: *"Be Baba Gidi, the street legend who gets Lagos home: weave crowds through keke, danfo and LASTMA chaos in 60-second runs."* Recruit commuters at the curb, cross the lanes, drop them at the goal.
- **Art direction: semi-real** (PBR, real proportions, no toy look), mobile budgets. Baked lighting + one sun, mild grade, colour-blind-safe lane telegraphs (danfo flashing headlights, LASTMA whistle cue). Bigger, bouncy HUD with numbers that count up.

## Cast & world
- **Baba Gidi** (hero; outfits: agbada, okada helmet, Ankara fits, generic jerseys).
- Traffic: **danfo** (yellow bus, paint jobs/back slogans), keke, taxi, okada, market lorry, sand tipper.
- Enforcement: **LASTMA** and **KAI** officers (flags, cones). Pedestrians: commuters, **Slay Queen**, Agbada Man.
- Reference renders and the art-direction board are kept in the team's internal art folder (not published).

## Districts (campaign)
L1 Agege Bus Stop (tutorial) · L2 Surulere · L3 Ikorodu Road · L4 Mushin Market · L5 Oshodi Expressway · L6 Ikeja Along · L7 Ojota · L8 Third Mainland · L9 Lekki Toll · **L10 Ojuelegba: truly endless** (no goal zone; score = distance + deliveries + combo; leaderboards + ghosts).

## Power-ups (next-gen set)
2-slot **"Gidi Bag"**, each item has its own Use button (two slot buttons). Owa! shout (free, 3/run), Pure Water (one-hit shield), Malta & Agege Roll (was “Maltina Break”; traffic slows to 50%), Change (auto on LASTMA/KAI, own pip), Danfo Ride, VIP Siren, Agbada Armour (earned only), Okada Dash, Gist Bomb. Agbero Whistle removed.

## Economy
Chips (earned only, never real money) for the shop; Naira in-run. Shop opens from L2. Rewarded ads only, opt-in.
**Decided (Kehinde, Oct 16):** Prices, caps and unlocks per vision doc (Kehinde, Oct 16); game-side changes in G-Prototype PR #51. Malta & Agege Roll 80 (renamed from Maltina & Gala), VIP Siren 120, Owa 80, Danfo Ride 150, Agbada Armour earned only (never sold).

## Tone
Millennials + Gen Z, 12+/Teen. Pidgin-first copy, adult Lagos in-jokes that never punch down ("Owa!", "We don reach!", "Chai!"). Afrobeats/amapiano energy. Cosmetics, ghost rivalry, vertical clips.
