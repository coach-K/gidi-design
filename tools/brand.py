"""Gidi++ brand primitives: palette, SVG icon set (48x48 grid, 3px rounded stroke), wordmark/logo SVG."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = dict(ink="#0F1219", text="#F5F5F0", muted="#9EA3AD", naira="#FAE69E", gold="#E8B21E", cta="#2E7A68", ctad="#18493F",
         safe="#56B4E9", caution="#F0E442", danger="#FF7A1A", lastma="#E07CC0", train="#FFFFFF", dusk="#2B2F5C", horizon="#F28C4B")
S = 'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'

# inner markup per icon (viewBox 0 0 48 48). currentColor = line colour; accents use palette.
ICONS = {
 # power-ups (GidiEconomyTables.SoftPowerupIds)
 "owa": f'<path {S} d="M8 20v8h6l14 8V12l-14 8z"/><path {S} d="M34 18c2 2 2 10 0 12M38 14c4 4 4 16 0 20"/><path {S} d="M14 28l2 9h5l-2-8"/>',
 "maltina_gala": f'<path {S} d="M14 6h6v6l3 5v23a2 2 0 0 1-2 2h-8a2 2 0 0 1-2-2V17l3-5z"/><path {S} d="M11 24h12"/><rect {S} x="27" y="22" width="15" height="18" rx="5"/><path {S} d="M31 27h7M31 32h7"/>',
 "pure_water": f'<path {S} d="M8 14c0-3 3-4 6-4h20c3 0 6 1 6 4v20c0 3-3 4-6 4H14c-3 0-6-1-6-4z"/><path {S} d="M24 16c-4 6-6 8-6 11a6 6 0 0 0 12 0c0-3-2-5-6-11z"/>',
 "bribe_change": f'<rect {S} x="6" y="14" width="30" height="18" rx="3"/><path {S} d="M12 36h30V18"/><path {S} d="M16 28v-10l8 10v-10M14 21h12M14 25h12"/>',
 "siren": f'<path {S} d="M14 34v-10a10 10 0 0 1 20 0v10"/><rect {S} x="10" y="34" width="28" height="6" rx="2"/><path {S} d="M24 6v4M10 12l3 3M38 12l-3 3M4 24h4M40 24h4"/><path d="M19 24a5 5 0 0 1 5-5" stroke="{P["danger"]}" stroke-width="3" fill="none" stroke-linecap="round"/>',
 "danfo_ride": f'<path {S} d="M5 30V16a4 4 0 0 1 4-4h26l8 9v9a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/><path {S} d="M10 17h7v6h-7zM21 17h8v6h-8zM33 17l4 6"/><circle {S} cx="14" cy="33" r="4"/><circle {S} cx="34" cy="33" r="4"/><path d="M8 8c6-4 14-4 20 0" fill="none" stroke="{P["gold"]}" stroke-width="3" stroke-linecap="round"/>',
 "gist_bomb": f'<rect {S} x="6" y="16" width="36" height="24" rx="4"/><circle {S} cx="17" cy="28" r="6"/><path {S} d="M28 23h9M28 28h9M28 33h6M14 16l14-10"/><path d="M38 6c2 2 2 5 0 7M42 4c3 3 3 8 0 11" fill="none" stroke="{P["danger"]}" stroke-width="2.5" stroke-linecap="round"/>',
 "agbada_armour": f'<path {S} d="M24 6l15 6v11c0 9-6 15-15 19-9-4-15-10-15-19V12z"/><path {S} d="M17 18l7 5 7-5M24 23v12"/><path d="M36 6l1 3 3 1-3 1-1 3-1-3-3-1 3-1z" fill="{P["gold"]}"/>',
 "okada_dash": f'<circle {S} cx="11" cy="33" r="6"/><circle {S} cx="37" cy="33" r="6"/><path {S} d="M11 33l8-12h9l9 12M19 21l-3-6h-4M28 21l3-6h5"/><path {S} d="M2 18h7M1 24h6" opacity=".7"/>',
 "retry": f'<path {S} d="M38 24a14 14 0 1 1-4.1-9.9"/><path {S} d="M36 6v9h-9"/>',
 "iap_skins_pack": f'<path {S} d="M6 30V20a3 3 0 0 1 3-3h24l7 7v6a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z"/><circle {S} cx="13" cy="33" r="4"/><circle {S} cx="33" cy="33" r="4"/><path d="M30 6l5 5-9 9-6 1 1-6z" fill="none" stroke="{P["gold"]}" stroke-width="3" stroke-linejoin="round"/>',
 "iap_fits_pack": f'<path {S} d="M17 8l-9 5 4 8 4-2v21h16V19l4 2 4-8-9-5c-1 3-4 5-7 5s-6-2-7-5z"/><path d="M20 26h8M20 31h8" stroke="{P["gold"]}" stroke-width="3" stroke-linecap="round"/>',
 "iap_remove_ads": f'<rect {S} x="6" y="11" width="36" height="26" rx="5"/><path {S} d="M21 18l9 6-9 6z"/><path d="M8 40L40 8" stroke="{P["danger"]}" stroke-width="3.5" stroke-linecap="round"/>',
 # curb pickups / in-world
 "pickup_ring": f'<ellipse {S} cx="24" cy="34" rx="16" ry="6"/><path {S} d="M24 8v18M17 19l7 7 7-7"/>',
 "pickup_person": f'<circle {S} cx="24" cy="12" r="5"/><path {S} d="M16 40l3-14h10l3 14M18 30h12"/><path d="M8 40h32" stroke="{P["naira"]}" stroke-width="3" stroke-linecap="round"/>',
 "chip": f'<circle {S} cx="24" cy="24" r="17"/><circle {S} cx="24" cy="24" r="11" stroke-dasharray="3 4"/><path {S} d="M19 30V18l10 12V18M16 22h16M16 26h16"/>',
 # HUD
 "lives": f'<path {S} d="M24 40S7 30 7 18a8 8 0 0 1 17-3 8 8 0 0 1 17 3c0 12-17 22-17 22z"/>',
 "group": f'<circle {S} cx="17" cy="15" r="5"/><circle {S} cx="32" cy="17" r="4"/><path {S} d="M7 38c0-7 4-12 10-12s10 5 10 12M28 38c0-6 2-10 6-10s7 4 7 10"/>',
 "change": f'<ellipse {S} cx="20" cy="30" rx="12" ry="5"/><path {S} d="M8 30v6c0 3 5 5 12 5s12-2 12-5v-6"/><ellipse {S} cx="28" cy="14" rx="12" ry="5"/><path {S} d="M16 14v6c0 2 2 3 4 4M40 14v6c0 3-5 5-12 5"/>',
 "stats": f'<path {S} d="M8 40h32"/><rect {S} x="11" y="24" width="6" height="12" rx="1"/><rect {S} x="21" y="14" width="6" height="22" rx="1"/><rect {S} x="31" y="8" width="6" height="28" rx="1"/>',
 "pause": f'<rect {S} x="13" y="10" width="7" height="28" rx="2"/><rect {S} x="28" y="10" width="7" height="28" rx="2"/>',
 "settings": f'<circle {S} cx="24" cy="24" r="6"/><path {S} d="M24 5v6M24 37v6M5 24h6M37 24h6M10.5 10.5l4.2 4.2M33.3 33.3l4.2 4.2M10.5 37.5l4.2-4.2M33.3 14.7l4.2-4.2"/><circle {S} cx="24" cy="24" r="13"/>',
 "souvenirs": f'<path {S} d="M15 6h18l-6 13M15 6l6 13"/><circle {S} cx="24" cy="30" r="12"/><path {S} d="M24 23.5l2 4.2 4.5.6-3.3 3.1.8 4.5-4-2.2-4 2.2.8-4.5-3.3-3.1 4.5-.6z"/>',
 "map": f'<path {S} d="M6 12l11-4 14 4 11-4v28l-11 4-14-4-11 4z"/><path {S} d="M17 8v28M31 12v28"/>',
 "basecamp": f'<path {S} d="M10 18h28l-3 22H13z"/><path {S} d="M17 18v-4a7 7 0 0 1 14 0v4"/><path {S} d="M19 28h10"/>',
 "play": f'<path {S} d="M15 9l24 15-24 15z"/>',
 "back": f'<path {S} d="M30 8L14 24l16 16"/>',
 "close": f'<path {S} d="M12 12l24 24M36 12L12 36"/>',
 "ad": f'<rect {S} x="6" y="11" width="36" height="26" rx="5"/><path {S} d="M21 18l9 6-9 6z"/>',
 "timer": f'<circle {S} cx="24" cy="27" r="15"/><path {S} d="M24 27v-8M20 6h8M24 6v6"/>',
 "lock": f'<rect {S} x="10" y="22" width="28" height="20" rx="4"/><path {S} d="M16 22v-6a8 8 0 0 1 16 0v6"/>',
 # warning shapes (filled, colour fixed by state)
 "warn_safe": f'<rect x="4" y="16" width="40" height="16" rx="8" fill="{P["safe"]}"/><path d="M15 24l6 5 12-10" fill="none" stroke="#0F1219" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
 "warn_caution": f'<path d="M24 4L45 42H3z" fill="{P["caution"]}" stroke="#0F1219" stroke-width="2" stroke-linejoin="round"/><path d="M24 17v12" stroke="#0F1219" stroke-width="5" stroke-linecap="round"/><circle cx="24" cy="36" r="2.8" fill="#0F1219"/>',
 "warn_danger": f'<path d="M4 8l14 16L4 40h10l14-16L14 8z" fill="{P["danger"]}"/><path d="M22 8l14 16-14 16h10l14-16L32 8z" fill="{P["danger"]}"/>',
 "warn_lastma": f'<path d="M24 3l21 21-21 21L3 24z" fill="{P["lastma"]}"/><path d="M15 24h12l4-4 3 3-4 4" fill="none" stroke="#0F1219" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17" cy="24" r="3" fill="#0F1219"/>',
 "warn_train": f'<rect x="2" y="12" width="44" height="24" rx="3" fill="{P["train"]}"/><path d="M8 12v24M16 12v24M24 12v24M32 12v24M40 12v24" stroke="#0F1219" stroke-width="3"/><path d="M2 20h44M2 28h44" stroke="#0F1219" stroke-width="2"/>',
}
GROUPS = [("Power-ups", ["owa","maltina_gala","pure_water","bribe_change","siren","danfo_ride","gist_bomb"]),
          ("Earned &amp; curb-only (not sold)", ["agbada_armour","okada_dash"]),
          ("Shop extras", ["retry","iap_skins_pack","iap_fits_pack","iap_remove_ads"]),
          ("Curb pickups &amp; currency", ["pickup_ring","pickup_person","chip"]),
          ("HUD &amp; navigation", ["chip","lives","group","change","stats","pause","settings","map","basecamp","play","back","close","ad","timer","lock","souvenirs"]),
          ("Warning shapes (colour + shape)", ["warn_safe","warn_caution","warn_danger","warn_lastma","warn_train"])]
PU_ACCENT = {"owa":P["gold"],"maltina_gala":"#C8743A","pure_water":P["safe"],"bribe_change":"#7FD6A2","siren":P["danger"],"danfo_ride":"#F2C230","gist_bomb":"#E0443C","agbada_armour":P["naira"],"okada_dash":"#59D9B8"}

def icon(name, size=48, color=None):
    c = color or P["naira"]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="{size}" height="{size}" style="color:{c}" color="{c}">{ICONS[name]}</svg>'

def badge(name, size=96):
    """Power-up badge: ink glass disc, accent ring, gold glyph (used in Base Camp, HUD rings, pickups)."""
    a = PU_ACCENT.get(name, P["gold"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}" height="{size}" color="{P["naira"]}">'
            f'<circle cx="32" cy="32" r="29" fill="{P["ink"]}" fill-opacity=".86" stroke="{a}" stroke-width="3"/>'
            f'<circle cx="32" cy="32" r="24" fill="none" stroke="{P["naira"]}" stroke-opacity=".18" stroke-width="1"/>'
            f'<g transform="translate(8 8)">{ICONS[name]}</g></svg>')

def logo_mark(size=256, bg=True):
    """App mark: '++' crossing on a dusk tile with zebra stripes (crossing) and a gold plus pair."""
    g = (f'<defs><linearGradient id="dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["dusk"]}"/><stop offset=".62" stop-color="#6B4A6E"/><stop offset="1" stop-color="{P["horizon"]}"/></linearGradient></defs>'
         + (f'<rect width="256" height="256" fill="url(#dk)"/>' if bg else '')
         + '<g fill="#F5F5F0" opacity=".9">' + "".join(f'<rect x="{30+i*42}" y="188" width="26" height="40" rx="3"/>' for i in range(5)) + '</g>'
         + f'<g fill="{P["gold"]}" stroke="{P["ink"]}" stroke-width="6" stroke-linejoin="round"><path d="M58 92h28V64h28v28h28v28h-28v28H86v-28H58z" transform="translate(-20 0)"/><path d="M58 92h28V64h28v28h28v28h-28v28H86v-28H58z" transform="translate(68 0)"/></g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="{size}" height="{size}">{g}</svg>'

def wordmark(h=120, light=True, tagline=False):
    t = P["text"] if light else P["ink"]
    tl = f'<text x="0" y="168" font-family="Jakarta, Plus Jakarta Sans, sans-serif" font-weight="700" font-size="27" fill="{P["naira"] if light else P["ctad"]}" letter-spacing="1">Carry dem cross. Lagos no dey wait.</text>' if tagline else ''
    hh = 180 if tagline else 130
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 {hh}" height="{h}">'
            f'<text x="0" y="110" font-family="Jakarta, Plus Jakarta Sans, sans-serif" font-weight="700" font-size="128" letter-spacing="2" fill="{t}">GIDI</text>'
            f'<g fill="{P["gold"]}"><path d="M300 48h24V24h24v24h24v24h-24v24h-24V72h-24z"/><path d="M390 48h24V24h24v24h24v24h-24v24h-24V72h-24z"/></g>'
            + '<g fill="'+t+'" opacity=".85">' + "".join(f'<rect x="{6+i*44}" y="122" width="28" height="6" rx="2"/>' for i in range(11)) + '</g>' + tl + '</svg>')

if __name__ == "__main__":
    for n in ICONS:
        open(f"{ROOT}/icons/svg/{n}.svg", "w").write(icon(n).replace(' style="color:#FAE69E"', ''))
    for n in PU_ACCENT:
        open(f"{ROOT}/icons/svg/badge_{n}.svg", "w").write(badge(n))
    print(len(ICONS), "icons")

# --- outlined text (so exported logo SVGs don't depend on the font being installed) ---
_FONT = None
def text_path(txt, size, x=0, y=0, track=0):
    global _FONT
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    if _FONT is None: _FONT = TTFont(f"{ROOT}/fonts/PlusJakartaSans-Bold.ttf")
    gs, cmap, hmtx, upm = _FONT.getGlyphSet(), _FONT.getBestCmap(), _FONT["hmtx"], _FONT["head"].unitsPerEm
    sc = size/upm; d = []; cx = x
    for ch in txt:
        g = cmap.get(ord(ch));
        if g is None: continue
        pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (sc,0,0,-sc,cx,y))); d.append(pen.getCommands())
        cx += hmtx[g][0]*sc + track
    return " ".join(d), cx

def wordmark(h=120, light=True, tagline=False, mono=None):
    t = mono or (P["text"] if light else P["ink"]); acc = mono or P["gold"]
    gidi, end = text_path("GIDI", 128, 0, 110, 2)
    px = end + 14
    plus = lambda x0: f'<path d="M{x0} 48h24V24h24v24h24v24h-24v24h-24V72h-{24}z"/>'.replace(f"M{x0} 48", f"M{x0:.0f} 48")
    W = px + 192
    tl = ""
    if tagline:
        d,_ = text_path("Carry dem cross. Lagos no dey wait.", 27, 2, 168, 0.5)
        tl = f'<path d="{d}" fill="{mono or (P["naira"] if light else P["ctad"])}"/>'
    hh = 180 if tagline else 132
    stripes = "".join(f'<rect x="{6+i*44}" y="122" width="28" height="6" rx="2"/>' for i in range(int((W-10)//44)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {hh}" height="{h}">'
            f'<path d="{gidi}" fill="{t}"/><g fill="{acc}">{plus(px)}{plus(px+92)}</g>'
            f'<g fill="{t}" opacity=".85">{stripes}</g>{tl}</svg>')
