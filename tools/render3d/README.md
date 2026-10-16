# 3D dusk renders (three.js, headless Chrome)
Renders the **shipped** game models (FBX/GLB from the game repo) on a Lagos-dusk stage, plus the CONCEPT scenes (outfits, hawkers, okada/tanker/BRT, danfo paint jobs, Owa!/Danfo Ride/Agbada Armour).
Setup: `npm i three@0.160.0 puppeteer-core@22`, symlink the game repo checkout as `gp/`, serve this folder (`python3 -m http.server 8931`), then `bash batch.sh <scene…>` (writes PNGs to /tmp/r3d; the site uses JPGs in `img/r3d/` with a CONCEPT / IN-GAME MODEL tag added).
Scene list: see `SCENES` in `scenes.js`.
