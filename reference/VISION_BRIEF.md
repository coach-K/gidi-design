# Gidi++ Vision Brief (for design)

Source: `/workspace/games/reports/vision-nextgen-v2.md` (v0.2, 12 Oct 2026, decisions locked), built on `/workspace/games/reports/vision-nextgen.md` (v0.1).

## What the game is
- **3D, not 2D.** Unity 6 URP, **perspective camera** looking down the road over Baba Gidi (see `levels/L01*.png`). **Landscape only.**
- Traffic-crossing runner: *"Be Baba Gidi, the street legend who gets Lagos home: weave crowds through keke, danfo and LASTMA chaos in 60-second runs."* Recruit commuters at the curb, cross the lanes, drop them at the goal.
- **Art direction: semi-real** (PBR, real proportions, no toy look), mobile budgets. Baked lighting + one sun, mild grade, colour-blind-safe lane telegraphs (danfo flashing headlights, LASTMA whistle cue). Bigger, bouncy HUD with numbers that count up.

## Cast & world
- **Baba Gidi** (hero; outfits: agbada, okada helmet, Ankara fits, generic jerseys).
- Traffic: **danfo** (yellow bus, paint jobs/back slogans), keke, taxi, okada, market lorry, sand tipper.
- Enforcement: **LASTMA** and **KAI** officers (flags, cones). Pedestrians: commuters, **Slay Queen**, Agbada Man.
- Renders for reference: `/workspace/games/trellis-regen/v2/render/`, `/workspace/games/optimize-run/render/png/`, `/workspace/games/reports/review-s1/r6-renders/`, art board `/workspace/games/reports/art-direction/art-direction-board.png`.

## Districts (campaign)
L1 Agege Bus Stop (tutorial) · L2 Surulere · L3 Ikorodu Road · L4 Mushin Market · L5 Oshodi Expressway · L6 Ikeja Along · L7 Ojota · L8 Third Mainland · L9 Lekki Toll · **L10 Ojuelegba: truly endless** (no goal zone; score = distance + deliveries + combo; leaderboards + ghosts).

## Power-ups (next-gen set)
2-slot **"Gidi Bag"**, each item has its own Use button (two slot buttons). Owa! shout (free, 3/run), Pure Water (one-hit shield), Maltina Break (traffic slows to 50%), Change (auto on LASTMA/KAI, own pip), Danfo Ride, VIP Siren, Agbada Armour (earned only), Okada Dash, Gist Bomb. Agbero Whistle removed.

## Economy
Chips (earned only, never real money) for the shop; Naira in-run. Shop opens from L2. Rewarded ads only, opt-in.
**Open question for Kehinde:** vision prices differ from code (`G-Prototype/Economy/GidiEconomyTables.cs`). E.g. Maltina **80** in the vision vs **60** in code, VIP Siren 120 vs 100, Owa free vs 80; the code still has Agbero Whistle (120). **For now, follow the code** for names and prices in mockups.

## Tone
Millennials + Gen Z, 12+/Teen. Pidgin-first copy, adult Lagos in-jokes that never punch down ("Owa!", "We don reach!", "Chai!"). Afrobeats/amapiano energy. Cosmetics, ghost rivalry, vertical clips.
