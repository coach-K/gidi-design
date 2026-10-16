#!/bin/bash
# renders every mockups/*.html (except hud*, handled by gen_hud) to exports/
cd "$(dirname "$0")/.."
for f in mockups/*.html; do b=$(basename $f .html); case $b in *phone*) W=2340;; *) W=1920;; esac
  out=exports/$b.png; case $b in hud-desktop*|hud-phone*) out=exports/hud/$b.png;; esac
  bash tools/shoot.sh "$PWD/$f" "$PWD/$out" $W 1080 & 
  while [ $(jobs -r | wc -l) -ge 6 ]; do sleep 0.3; done
done; wait
