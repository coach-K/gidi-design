# GPP-063 Onboarding 1–4: support note (G-Prototype PR #104)

**Already fully specified; not duplicated here.** Screens `onboard1..4-{desktop,phone}` (site: Screens › Onboarding) and PR #104 (`OnboardingRules`, `OnboardingCoachView`) match each other: coach pill (56 px step disc, 36 px copy, gold 2 px border, safe top 200, height 100), Skip glass button 200×144 at safe top-right 170 (steps 2–4 only), 4 step dots at bottom 30 (on = 48×18 gold, off = 18×18 #555), level card meta `Tutorial · step n/4`, step 3 glows the GROUP/CHANGE panel, step 4 shows `GOAL · far curb`, sorting order 115, advance rules 1→2 first pick-up, 2→3 after 6 s, 3→4 after 5 s, 4→done first delivery, `PlayerPrefs gidi.onboarding.gpp063.done`.

Only what the dev needs to change:
1. **Step 3 copy** (OWA! button removed, Oct 24): replace `Your stock: GROUP and CHANGE up top, OWA! above PICK UP` with **`Your stock: GROUP and CHANGE up top. Power-ups go in your bag from L2`** (`OnboardingRules` case 3). Mockup `onboard3-*` already shows it.
2. No OWA! button is drawn on L1 any more (mockups updated); nothing in the coach points at it.
3. The bag row isn't shown on L1 (no power-ups yet), so onboarding never overlaps it. The first bag hint is the L2 Owa unlock toast (`hud-toast`).
