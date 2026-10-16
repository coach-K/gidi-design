# Gidi++ Design System

Static HTML/CSS site, no build step, relative links only (works at a GitHub Pages project subpath). Open `index.html`.

**Landscape only (RT-106).** Sections: Brand, Guidelines, Palette, Typography, Icons, Logos & app icons, Screens (+ flow), Levels, Costumes, Souvenirs & perks, Devices.

- `mockups/` HTML sources · `exports/` PNG renders (screens, `hud/`, `costumes/`, `devices/`)
- `icons/svg/` icon set · `logos/` wordmarks, `logos/app/{ios,android,web}` app icons · `souvenirs/` medallions
- `assets/bg/` level backgrounds built from `reference/levels/L01–L10.png` (current build screenshots)

Regenerate (needs python3 + opencv/PIL/fontTools and google-chrome):
```
python3 tools/prep_levels.py          # backgrounds
python3 tools/brand.py                # icons
cd tools && python3 gen_hud.py && python3 gen_screens.py && python3 gen_more.py && cd ..
bash tools/shoot_all.sh               # screen PNGs
python3 tools/gen_costumes.py && python3 tools/gen_logos.py && python3 tools/gen_devices.py
cd tools && python3 gen_site.py
```
Numbers come from G-Prototype `Economy/GidiEconomyTables.cs` and `LevelManager.cs`; anything not in code is marked TBD. Font: Plus Jakarta Sans Bold (SIL OFL 1.1, `fonts/OFL.txt`).
