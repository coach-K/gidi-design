for s in "$@"; do
  case $s in ch_*|baba_*|hawker_*|pu_agbada_armour) WH="1000 1250";; pu_malta|pu_purewater|pu_siren|pu_change|pu_whistle) WH="1000 1000";; *) WH="1600 1000";; esac
  timeout 280 node shot.js $s /tmp/r3d/$s.png $WH 2>&1 | grep -i "error" ; echo "done $s"
done
