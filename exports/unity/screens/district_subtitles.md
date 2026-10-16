# District-card subtitles (Level intro)

Source of voice: `Screens/DistrictIntroRules.Subtitle()` in coach-K/G-Prototype (PR #87). Approved mockup line for LASTMA + KAI:

> Two wahala dey road today: LASTMA flag and KAI officers. Hold your change.

The other three cases in the code are placeholders. Same shape below: "[count] wahala dey road today: [what]. [instruction]." Light Pidgin, short, ≤ ~75 characters so it fits the 30 px subtitle line. Note: `DistrictIntroView` colours " and " in LASTMA pink, so these lines avoid the word "and".

| Case | Option A | Option B | Pick |
|---|---|---|---|
| LASTMA only | One wahala dey road today: LASTMA flag. Hold your change. | LASTMA dey flag lanes today. Hold your change. *(current placeholder)* | **A** |
| KAI only | One wahala dey road today: KAI officers. Hold your change. | KAI officers dey patrol today. Hold your change. | **A** |
| No enforcement | No wahala for road today: no LASTMA, no KAI. Just find your gap. | Road free today, no officer for sight. Read the road, find the gap. | **A** |

Why A: it mirrors the approved line word for word ("One wahala…" vs "Two wahala…"), so the three enforced cases read as one family, and "Hold your change" stays tied to LASTMA/KAI (the Change power-up settles them). The no-enforcement line drops "Hold your change" because there's nobody to pay, and keeps the game's "find the gap" instruction.

Drop-in for `Subtitle(DistrictFacts f)`:
```csharp
if (f.Lastma && f.Kai) return "Two wahala dey road today: LASTMA flag and KAI officers. Hold your change.";
if (f.Lastma)          return "One wahala dey road today: LASTMA flag. Hold your change.";
if (f.Kai)             return "One wahala dey road today: KAI officers. Hold your change.";
return "No wahala for road today: no LASTMA, no KAI. Just find your gap.";
```
(Copy only; the game repo is not changed from here. The PR #87 test pins only the LASTMA + KAI line.)
