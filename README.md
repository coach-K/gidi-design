# Gidi++ Design System

Static HTML/CSS site with no build step (works on GitHub Pages once approved). Open `index.html`.

**Landscape only (RT-106).** The four approval mockups for M1 (Oct 30) are in `mockups/` (HTML) and `exports/` (PNG). The HUD spec is in `exports/hud/`.

Regenerate:
```
cd tools && python3 gen_hud.py && python3 gen_screens.py && cd .. && python3 tools/gen_site.py
tools/shoot.sh "$PWD/mockups/hud-desktop.html" exports/hud-desktop.png 1920 1080   # needs google-chrome
```
The font is Plus Jakarta Sans Bold (SIL OFL 1.1, `fonts/OFL.txt`). Economy values are copied from G-Prototype `Economy/GidiEconomyTables.cs`.
