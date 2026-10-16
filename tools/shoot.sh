#!/bin/bash
# usage: shoot.sh page.html out.png W H   (renders taller, then crops: avoids headless viewport clipping)
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --virtual-time-budget=3000 --window-size=$3,$(($4+300)) --screenshot="$2" "file://$1" 2>/dev/null
python3 -c "from PIL import Image;im=Image.open('$2');im.crop((0,0,$3,$4)).save('$2')"
