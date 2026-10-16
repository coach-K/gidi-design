# Gidi++ Design System

Static HTML/CSS site, no build step, relative links only (works at a GitHub Pages project subpath). Open `index.html`.

**Landscape only (RT-106).** Sections: Brand, Guidelines, Palette, Typography, Icons, Logos & app icons, Screens (+ flow), Levels, Characters, Costumes, Vehicles, Power-ups, Souvenirs & perks, Devices.

- `mockups/` HTML sources · `exports/` PNG renders (screens, `hud/`, `costumes/`, `devices/`)
- `icons/svg/` icon set · `logos/` wordmarks, `logos/app/{ios,android,web}` app icons · `souvenirs/` medallions
- `img/r3d/` 3D dusk renders of shipped models + CONCEPT scenes (`tools/render3d/`) · `img/ref/` thumbnails of `reference/{babagidi,peds,officers,vehicles,powerups}` (provenance in each README; unclear-origin images are not committed)
- `assets/bg/` level backgrounds built from `reference/levels/L01–L10.png` (current build screenshots)

Regenerate (needs python3 + opencv/PIL/fontTools and google-chrome):
```
python3 tools/prep_levels.py          # backgrounds
python3 tools/brand.py                # icons
cd tools && python3 gen_hud.py && python3 gen_screens.py && python3 gen_more.py && cd ..
bash tools/shoot_all.sh               # screen PNGs
python3 tools/gen_logos.py && python3 tools/gen_devices.py && python3 tools/gen_tablet.py
# 3D renders: see tools/render3d/README.md
cd tools && python3 gen_site.py
```
Prices, caps and unlocks per vision doc (Kehinde, Oct 16); game-side changes in G-Prototype PR #51. Other numbers come from G-Prototype `Economy/GidiEconomyTables.cs` and `LevelManager.cs`; anything undefined is marked TBD. The `maltina_gala` pickup is displayed as “Malta & Agege Roll”. Font: Plus Jakarta Sans Bold (SIL OFL 1.1, `fonts/OFL.txt`).

## Hidden pages
Costumes, Vehicles and Power-ups are **hidden pending Kehinde's review** (Oct 16). They're left out of the nav, the index cards and cross-links, and they carry `<meta name="robots" content="noindex">`. The files stay in the repo and are **still reachable by direct URL** (`costumes.html`, `vehicles.html`, `powerups.html`).
To restore them: remove the keys from `HIDDEN` in `tools/gen_site.py`, re-add the index cards in the same file, then run `cd tools && python3 gen_site.py` and push.
