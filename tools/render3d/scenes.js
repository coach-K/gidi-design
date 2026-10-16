import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { DecalGeometry } from 'three/addons/geometries/DecalGeometry.js';
let KTX = null;
export function setRenderer(rd) { KTX = new KTX2Loader().setTranscoderPath('./node_modules/three/examples/jsm/libs/basis/').detectSupport(rd); }
const gltf = p => new Promise((r, j) => { const l = new GLTFLoader(); if (KTX) l.setKTX2Loader(KTX); l.load(p, g => r(g.scene), undefined, j); });
const fbx = p => new Promise((r, j) => new FBXLoader().load(p, r, undefined, j));
const img = p => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = p; });
const P = 'gp/Art/L1_Agege/';
const CH = { baba: ['Characters/Baba-Gidi_/BGidi@Idle.fbx', 'Characters/Baba-Gidi_/Textures/BGidi_BaseColor.png'] };
for (const n of ['Ped', 'Ped1', 'Ped2', 'Ped3', 'Ped4', 'Ped5', 'Ped6', 'Ped7', 'Ped8', 'Ped9', 'Ped10']) CH[n] = [`Characters/Pedestrians/Commuter/${n}@Idle.fbx`, `Characters/Pedestrians/Commuter/Textures/${n}_BaseColor.png`];
for (const n of ['AgbadaMan', 'AgbadaMan1', 'AgbadaMan2']) CH[n] = [`Characters/Pedestrians/AgbadaMan/${n}@Idle.fbx`, `Characters/Pedestrians/AgbadaMan/Textures/${n}_BaseColor.png`];
for (const n of ['SlayQueen', 'SlayQueen1']) CH[n] = [`Characters/Pedestrians/SlayQueen/${n}@Idle.fbx`, `Characters/Pedestrians/SlayQueen/Textures/${n}_BaseColor.png`];
for (const n of ['KAI', 'LASTMAN']) CH[n] = [`Characters/Pedestrians/Officials/${n}@Idle.fbx`, `Characters/Pedestrians/Officials/Textures/${n}_BaseColor.png`];

export function fit(obj, height) { obj.updateMatrixWorld(true); const b = new THREE.Box3().setFromObject(obj); const s = height / (b.max.y - b.min.y); obj.scale.multiplyScalar(s); obj.updateMatrixWorld(true); const b2 = new THREE.Box3().setFromObject(obj); obj.position.y -= b2.min.y; obj.position.x -= (b2.min.x + b2.max.x) / 2; obj.position.z -= (b2.min.z + b2.max.z) / 2; return obj; }

// recolour: replace clothing hue range in the base-colour texture, keep shading (luminance) and fine details
function recolour(image, fn) {
  const c = document.createElement('canvas'); c.width = image.width; c.height = image.height; const g = c.getContext('2d'); g.drawImage(image, 0, 0);
  const d = g.getImageData(0, 0, c.width, c.height), a = d.data;
  for (let i = 0; i < a.length; i += 4) { const r = a[i], gg = a[i + 1], b = a[i + 2]; const o = fn(r, gg, b, (i / 4) % c.width, (i / 4 / c.width) | 0); if (o) { a[i] = o[0]; a[i + 1] = o[1]; a[i + 2] = o[2]; } }
  g.putImageData(d, 0, 0); return c;
}
const isGreen = (r, g, b) => g > 60 && g > r * 1.25 && g > b * 1.25;
const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const shade = (col, r, g, b, k = 1.6) => { const l = Math.min(1.25, (0.3 * r + 0.59 * g + 0.11 * b) / 255 * k + 0.25); return col.map(v => Math.min(255, v * l)); };
function patternFn(kind) {
  if (kind === 'ankara') { const A = hex('#1F4FB5'), B = hex('#E8B21E'), C = hex('#C8102E'), D = hex('#111111');
    return (x, y) => { const u = x % 48, v = y % 48; const dx = u - 24, dy = v - 24, r = Math.hypot(dx, dy); if (r < 7) return D; if (r < 14) return B; if (Math.abs(dx) + Math.abs(dy) > 30) return C; return A; }; }
  if (kind === 'lace') { const A = hex('#3B2A7A'), B = hex('#8E7CE0'); return (x, y) => ((Math.sin(x * 0.5) * Math.sin(y * 0.5) > 0.6) ? B : A); }
  if (kind === 'stripe') { const A = hex('#C8102E'), B = hex('#F2F2EE'); return (x, y) => ((x % 40) < 12 ? B : A); }
  return null;
}
export async function character(name, { recol, anim = 0.8 } = {}) {
  const [f, t] = CH[name]; const o = await fbx(P + f); const im = await img(P + t);
  let src = im;
  if (recol) src = recolour(im, recol);
  const tex = new THREE.CanvasTexture(src); tex.colorSpace = THREE.SRGBColorSpace; tex.flipY = true; tex.anisotropy = 8;
  o.traverse(m => { if (m.isMesh) { m.material = new THREE.MeshStandardMaterial({ map: tex, roughness: .78, metalness: 0 }); m.frustumCulled = false; } });
  if (o.animations && o.animations.length) { const mx = new THREE.AnimationMixer(o); mx.clipAction(o.animations[0]).play(); mx.update(anim); }
  return o;
}
function bone(o, n) { let b = null; o.traverse(x => { if (x.isBone && x.name.toLowerCase().endsWith(n.toLowerCase())) b = b || x; }); return b; }
function attach(o, boneName, mesh) { const b = bone(o, boneName); if (!b) { console.log('no bone ' + boneName); return; } o.updateMatrixWorld(true); const inv = new THREE.Matrix4().copy(b.matrixWorld).invert(); b.add(mesh); mesh.applyMatrix4(inv); }

function textTex(lines, { w = 1024, h = 256, bg = null, fg = '#111', font = 'bold 120px Jakarta, Arial', stroke = null } = {}) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); if (bg) { g.fillStyle = bg; g.fillRect(0, 0, w, h); }
  g.font = font; g.textAlign = 'center'; g.textBaseline = 'middle'; const L = Array.isArray(lines) ? lines : [lines];
  L.forEach((s, i) => { const y = h * (i + 0.5) / L.length; if (stroke) { g.lineWidth = 10; g.strokeStyle = stroke; g.strokeText(s, w / 2, y); } g.fillStyle = fg; g.fillText(s, w / 2, y); });
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
function decal(target, pos, rot, size, tex, opts = {}) {
  const meshes = []; target.traverse(m => m.isMesh && meshes.push(m)); const grp = new THREE.Group();
  for (const m of meshes) { if (!m.geometry.attributes.normal) m.geometry.computeVertexNormals(); const g = new DecalGeometry(m, pos, rot, size); if (!g.attributes.position.count) continue;
    grp.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ map: tex, transparent: true, depthTest: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, roughness: .5, ...opts }))); }
  return grp;
}
function hueShift(obj, target, opts = {}) { // repaint yellow body paint on KTX2 vehicles via shader
  const T = new THREE.Color(target);
  obj.traverse(m => { if (!m.isMesh) return; const mat = m.material.clone(); m.material = mat;
    mat.onBeforeCompile = s => { s.uniforms.uT = { value: T }; s.fragmentShader = 'uniform vec3 uT;\n' + s.fragmentShader.replace('#include <map_fragment>', `#include <map_fragment>
      { vec3 c = diffuseColor.rgb; float y = smoothstep(0.08, 0.25, min(c.r, c.g) - c.b) * step(c.b * 1.2, c.g); float l = dot(c, vec3(.3,.59,.11));
        diffuseColor.rgb = mix(c, uT * (l * 1.9 + 0.08), y); }`); }; mat.needsUpdate = true; });
}
const M = (c, r = .5, m = 0, e = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m, ...e });
function wheel(r = .42, w = .28) { const g = new THREE.Group(); const tyre = new THREE.Mesh(new THREE.TorusGeometry(r * .78, r * .24, 16, 40), M('#141414', .9)); g.add(tyre);
  const rim = new THREE.Mesh(new THREE.CylinderGeometry(r * .58, r * .58, w * .7, 28), M('#9aa0a8', .3, .9)); rim.rotation.x = Math.PI / 2; g.add(rim);
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(r * .18, r * .18, w * .8, 16), M('#555', .4, .8)); hub.rotation.x = Math.PI / 2; g.add(hub); return g; }

// --- props
function agbadaRobe(fabricTex, color = '#F2EAD8') {
  const pts = []; for (let i = 0; i <= 20; i++) { const t = i / 20; pts.push(new THREE.Vector2(0.15 + 0.40 * Math.pow(t, 0.9) + 0.02 * Math.sin(t * 9), -t * 1.05)); }
  const geo = new THREE.LatheGeometry(pts, 96, -Math.PI * 0.86, Math.PI * 1.72);
  const pos = geo.attributes.position; for (let i = 0; i < pos.count; i++) { const x = pos.getX(i), z = pos.getZ(i), y = pos.getY(i); const a = Math.atan2(z, x); const k = 1 + 0.06 * Math.sin(a * 14) * (-y); pos.setX(i, x * k); pos.setZ(i, z * k * 0.62); }
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({ color, map: fabricTex || null, roughness: .62, side: THREE.DoubleSide });
  return new THREE.Mesh(geo, mat);
}
function embroideryTex(base = '#F2EAD8', thread = '#C9A227') {
  const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d'); g.fillStyle = base; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 4000; i++) { g.fillStyle = `rgba(0,0,0,${Math.random() * .04})`; g.fillRect(Math.random() * 512, Math.random() * 512, 1, 3); }
  g.strokeStyle = thread; g.lineWidth = 6; for (let k = 0; k < 4; k++) { g.beginPath(); for (let y = 0; y < 512; y += 4) g.lineTo(256 + (k - 1.5) * 18 + Math.sin(y / 18) * 10, y); g.stroke(); }
  g.lineWidth = 3; for (let y = 40; y < 512; y += 90) { g.beginPath(); g.arc(256, y, 26, 0, Math.PI * 2); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(2, 1); return t;
}
function helmet() { const g = new THREE.Group(); const shell = new THREE.Mesh(new THREE.SphereGeometry(0.15, 40, 24, 0, Math.PI * 2, 0, Math.PI * 0.62), M('#E8B21E', .25, .1, { envMapIntensity: 1.5 })); g.add(shell);
  const stripe = new THREE.Mesh(new THREE.SphereGeometry(0.152, 40, 24, -0.25, 0.5, 0, Math.PI * 0.6), M('#111', .3)); g.add(stripe);
  const visor = new THREE.Mesh(new THREE.SphereGeometry(0.155, 40, 16, Math.PI * 0.15, Math.PI * 0.7, Math.PI * 0.32, Math.PI * 0.2), M('#1b2638', .05, .6, { transparent: true, opacity: .85 })); visor.rotation.y = Math.PI; g.add(visor); return g; }

function sprite(text, color, size = 1, stroke = '#0F1219', w = 1024) { const t = textTex(text, { w, fg: color, stroke, font: 'bold 150px Jakarta, Arial' }); const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, transparent: true, depthTest: false })); s.scale.set(4 * size, 1 * size, 1); s.renderOrder = 10; return s; }
function ring(r, color, op = .9, w = .05) { const m = new THREE.Mesh(new THREE.TorusGeometry(r, w, 12, 120), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: op, toneMapped: false })); m.rotation.x = Math.PI / 2; return m; }
function laneMarks(scene, n = 4, z0 = 0) { for (let i = 0; i < n; i++) for (let k = -10; k < 10; k++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(1.4, .12), M('#e8e2d0', .8)); m.rotation.x = -Math.PI / 2; m.position.set(k * 2.6, .005, z0 - i * 3.4); scene.add(m); } }
function kerb(scene, z) { const k = new THREE.Mesh(new THREE.BoxGeometry(60, .18, .5), M('#8a8578', .9)); k.position.set(0, .09, z); scene.add(k); const w = new THREE.Mesh(new THREE.BoxGeometry(60, .16, 4), M('#6d6a62', .95)); w.position.set(0, .08, z + 2.25); scene.add(w); }

// --- vehicles from primitives
function okada() {
  const g = new THREE.Group(); const red = M('#B3121F', .22, .25, { envMapIntensity: 1.4 }), chrome = M('#d5d9de', .12, 1), black = M('#121212', .55), alloy = M('#7d838c', .3, .9);
  const V = (x, y, z = 0) => new THREE.Vector3(x, y, z);
  const tube = (a, b, r = .022, mat = chrome) => { const v = new THREE.Vector3().subVectors(b, a); const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, v.length(), 12), mat); m.position.copy(a).add(b).multiplyScalar(.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), v.normalize()); g.add(m); return m; };
  const wh = (x) => { const w = new THREE.Group(); w.add(new THREE.Mesh(new THREE.TorusGeometry(.29, .055, 18, 48), M('#161616', .85)));
    w.add(new THREE.Mesh(new THREE.TorusGeometry(.24, .012, 8, 48), alloy)); for (let i = 0; i < 18; i++) { const sp = new THREE.Mesh(new THREE.CylinderGeometry(.003, .003, .47, 4), chrome); sp.rotation.z = i * Math.PI / 18; w.add(sp); }
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(.045, .045, .09, 16), alloy); hub.rotation.x = Math.PI / 2; w.add(hub); w.position.set(x, .35, 0); g.add(w); };
  wh(.74); wh(-.66);
  const tank = new THREE.Mesh(new THREE.SphereGeometry(.2, 32, 20), red); tank.scale.set(1.45, .62, .7); tank.position.set(.2, .88, 0); g.add(tank);
  const pnl = new THREE.Mesh(new RoundedBoxGeometry(.38, .16, .22, 4, .05), red); pnl.position.set(-.28, .74, 0); g.add(pnl);
  const seat = new THREE.Mesh(new RoundedBoxGeometry(.62, .09, .24, 5, .045), M('#1d1a17', .65)); seat.position.set(-.26, .87, 0); g.add(seat);
  const eng = new THREE.Mesh(new RoundedBoxGeometry(.34, .28, .2, 4, .05), M('#2f3236', .35, .8)); eng.position.set(.08, .5, 0); g.add(eng);
  for (let i = 0; i < 5; i++) { const f = new THREE.Mesh(new THREE.BoxGeometry(.3, .012, .24), alloy); f.position.set(.1, .44 + i * .03, 0); g.add(f); }
  tube(V(.74, .35, .06), V(.52, 1.0, .06), .02); tube(V(.74, .35, -.06), V(.52, 1.0, -.06), .02);
  tube(V(.5, 1.03, .33), V(.5, 1.03, -.33), .016, black); tube(V(.52, 1.0, 0), V(.5, 1.03, 0), .03, black);
  for (const z of [.33, -.33]) { const gr = new THREE.Mesh(new THREE.CylinderGeometry(.022, .022, .1, 12), black); gr.rotation.x = Math.PI / 2; gr.position.set(.5, 1.03, z * 1.08); g.add(gr); tube(V(.48, 1.03, z * .8), V(.45, 1.15, z * .95), .008, chrome); const mir = new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, .012, 20), chrome); mir.rotation.z = Math.PI / 2; mir.position.set(.45, 1.17, z * .95); g.add(mir); }
  tube(V(-.66, .35, .07), V(-.1, .6, .07), .02, black); tube(V(-.66, .35, -.07), V(-.1, .6, -.07), .02, black);
  tube(V(-.55, .42, .07), V(-.4, .83, .1), .02, M('#B38B2A', .3, .8)); tube(V(.05, .38, .14), V(-.72, .5, .15), .03, chrome);
  const muf = new THREE.Mesh(new THREE.CylinderGeometry(.045, .04, .3, 16), chrome); muf.rotation.z = Math.PI / 2 - .12; muf.position.set(-.65, .5, .15); g.add(muf);
  const ff = new THREE.Mesh(new THREE.TorusGeometry(.33, .03, 8, 28, Math.PI * .55), red); ff.position.set(.74, .35, 0); ff.rotation.z = Math.PI * .25; g.add(ff);
  const rf = new THREE.Mesh(new THREE.TorusGeometry(.33, .03, 8, 28, Math.PI * .5), red); rf.position.set(-.66, .35, 0); rf.rotation.z = Math.PI * .45; g.add(rf);
  const lamp = new THREE.Mesh(new THREE.SphereGeometry(.075, 24, 16, 0, Math.PI), M('#fff7d6', .05, 0, { emissive: '#ffe9a8', emissiveIntensity: 2.5 })); lamp.rotation.y = Math.PI / 2; lamp.position.set(.6, .96, 0); g.add(lamp);
  const lb = new THREE.Mesh(new THREE.CylinderGeometry(.08, .065, .09, 24), chrome); lb.rotation.z = Math.PI / 2; lb.position.set(.56, .96, 0); g.add(lb);
  const tl = new THREE.Mesh(new RoundedBoxGeometry(.04, .05, .12, 2, .01), M('#ff3030', .2, 0, { emissive: '#ff2020', emissiveIntensity: 1.5 })); tl.position.set(-.62, .86, 0); g.add(tl);
  const rack = new THREE.Mesh(new THREE.BoxGeometry(.3, .015, .26), black); rack.position.set(-.62, .88, 0); g.add(rack);
  return g;
}
function tanker() {
  const g = new THREE.Group(); const cabC = M('#B3121F', .28, .3, { envMapIntensity: 1.3 }), glassM = M('#4a5f86', .08, .4, { envMapIntensity: 2.5 }), chrome = M('#d5d9de', .12, 1);
  const cab = new THREE.Mesh(new RoundedBoxGeometry(1.8, 1.25, 2.3, 6, .16), cabC); cab.position.set(3.45, 1.2, 0); g.add(cab);
  const top = new THREE.Mesh(new RoundedBoxGeometry(1.5, .95, 2.24, 6, .22), cabC); top.position.set(3.3, 2.2, 0); g.add(top);
  const ws = new THREE.Mesh(new RoundedBoxGeometry(.08, .72, 2.0, 3, .05), glassM); ws.position.set(4.05, 2.22, 0); ws.rotation.z = -.12; g.add(ws);
  for (const z of [1.13, -1.13]) { const sw = new THREE.Mesh(new RoundedBoxGeometry(.8, .6, .04, 3, .02), glassM); sw.position.set(3.5, 2.25, z); g.add(sw);
    const mr = new THREE.Mesh(new RoundedBoxGeometry(.06, .34, .14, 2, .02), M('#111', .3)); mr.position.set(4.25, 2.1, z * 1.18); g.add(mr); }
  const strip = new THREE.Mesh(new THREE.BoxGeometry(1.82, .1, 2.32), M('#F5F5F0', .4)); strip.position.set(3.45, 1.45, 0); g.add(strip);
  const grille = new THREE.Mesh(new RoundedBoxGeometry(.06, .55, 1.3, 2, .02), chrome); grille.position.set(4.36, 1.05, 0); g.add(grille);
  for (let i = 0; i < 6; i++) { const bar = new THREE.Mesh(new THREE.BoxGeometry(.07, .025, 1.25), M('#222', .4, .6)); bar.position.set(4.37, .84 + i * .08, 0); g.add(bar); }
  for (const z of [.85, -.85]) { const hl = new THREE.Mesh(new RoundedBoxGeometry(.06, .18, .32, 2, .03), M('#fff', .05, 0, { emissive: '#fff1c8', emissiveIntensity: 2.5 })); hl.position.set(4.37, 1.05, z); g.add(hl); }
  const bump = new THREE.Mesh(new RoundedBoxGeometry(.25, .28, 2.4, 3, .06), M('#1d1d1d', .5, .4)); bump.position.set(4.42, .6, 0); g.add(bump);
  const chassis = new THREE.Mesh(new THREE.BoxGeometry(7.4, .28, 1.5), M('#1a1a1a', .7)); chassis.position.set(.5, .66, 0); g.add(chassis);
  const tank = new THREE.Mesh(new THREE.CapsuleGeometry(1.0, 4.3, 16, 48), M('#dfe3e8', .16, .95, { envMapIntensity: 1.4 })); tank.rotation.z = Math.PI / 2; tank.position.set(-.35, 1.82, 0); tank.scale.set(1, 1, .92); g.add(tank);
  const band = (x, c) => { const b = new THREE.Mesh(new THREE.CylinderGeometry(1.012, 1.012, .2, 48), M(c, .45, .1)); b.rotation.z = Math.PI / 2; b.position.set(x, 1.82, 0); b.scale.set(1, 1, .92); g.add(b); };
  band(-2.3, '#FF7A1A'); band(1.65, '#FF7A1A');
  for (const x of [-1.6, -.35, .9]) { const h = new THREE.Mesh(new THREE.CylinderGeometry(.22, .22, .12, 24), chrome); h.position.set(x, 2.84, 0); g.add(h); }
  const rail = new THREE.Mesh(new THREE.BoxGeometry(4.0, .04, .04), chrome); rail.position.set(-.35, 3.0, .32); g.add(rail); const rail2 = rail.clone(); rail2.position.z = -.32; g.add(rail2);
  const ladder = new THREE.Mesh(new THREE.BoxGeometry(.05, 1.6, .4), chrome); ladder.position.set(-2.95, 1.6, .5); g.add(ladder);
  for (const x of [3.55, -1.45, -2.6]) for (const z of [1.02, -1.02]) { const w = wheel(.5, .34); w.position.set(x, .5, z); g.add(w); }
  for (const z of [1.15, -1.15]) { const mud = new THREE.Mesh(new THREE.BoxGeometry(1.8, .05, .45), M('#111', .6)); mud.position.set(-2.0, 1.05, z); g.add(mud); }
  return g;
}

function brt() {
  const g = new THREE.Group(); const body = new THREE.Mesh(new RoundedBoxGeometry(11, 3.0, 2.55, 8, .35), M('#1F4FB5', .32, .3)); body.position.set(0, 1.85, 0); g.add(body);
  const skirt = new THREE.Mesh(new RoundedBoxGeometry(11.02, .7, 2.57, 4, .2), M('#C8102E', .35, .3)); skirt.position.set(0, .75, 0); g.add(skirt);
  const win = new THREE.Mesh(new RoundedBoxGeometry(9.6, 1.15, 2.6, 4, .12), M('#4a5f86', .08, .4, { envMapIntensity: 2.5 })); win.position.set(-.5, 2.35, 0); g.add(win);
  for (let i = 0; i < 9; i++) { const pl = new THREE.Mesh(new THREE.BoxGeometry(.12, 1.17, 2.62), M('#1F4FB5', .32, .3)); pl.position.set(-5.2 + i * 1.15, 2.35, 0); g.add(pl); }
  for (const x of [1.6, -2.0]) { const dr = new THREE.Mesh(new THREE.BoxGeometry(1.0, 2.0, 2.58), M('#3a4d72', .1, .5, { envMapIntensity: 2 })); dr.position.set(x, 1.65, 0); g.add(dr); }
  const ac = new THREE.Mesh(new RoundedBoxGeometry(3.2, .3, 1.6, 4, .1), M('#e6e8ea', .4, .2)); ac.position.set(.5, 3.45, 0); g.add(ac);
  const ws = new THREE.Mesh(new RoundedBoxGeometry(.1, 1.7, 2.3, 3, .05), M('#4a5f86', .06, .4, { envMapIntensity: 2.5 })); ws.position.set(5.5, 2.1, 0); g.add(ws);
  const stripe = new THREE.Mesh(new THREE.BoxGeometry(11.04, .16, 2.59), M('#E8B21E', .4)); stripe.position.set(0, 1.55, 0); g.add(stripe);
  for (const x of [-3.8, -2.6, 3.6]) for (const z of [1.15, -1.15]) { const w = wheel(.55, .34); w.position.set(x, .55, z); g.add(w); }
  for (const z of [.85, -.85]) { const l = new THREE.Mesh(new THREE.BoxGeometry(.06, .18, .45), M('#fff', .1, 0, { emissive: '#fff4d0', emissiveIntensity: 3 })); l.position.set(5.52, .95, z); g.add(l); }
  const dest = new THREE.Mesh(new THREE.PlaneGeometry(1.9, .35), new THREE.MeshBasicMaterial({ map: textTex('OSHODI ▸ CMS', { w: 1024, h: 190, fg: '#FF9F2E', bg: '#120a02', font: 'bold 120px Jakarta, Arial' }), toneMapped: false })); dest.rotation.y = Math.PI / 2; dest.position.set(5.57, 3.0, 0); g.add(dest);
  g.userData.sideZ = 1.29; return g;
}
function hawkerTray(goods = 'water') { const g = new THREE.Group(); const tray = new THREE.Mesh(new THREE.CylinderGeometry(.34, .3, .07, 40), M('#c2c8cc', .25, .9)); g.add(tray);
  if (goods === 'water') { for (let i = 0; i < 14; i++) { const s = new THREE.Mesh(new RoundedBoxGeometry(.13, .04, .09, 3, .018), M('#cfe9ff', .05, 0, { transparent: true, opacity: .75, envMapIntensity: 2 })); const a = i * 2.4; s.position.set(Math.cos(a) * (.08 + (i % 3) * .07), .06 + (i % 4) * .03, Math.sin(a) * (.08 + (i % 3) * .07)); s.rotation.y = a; g.add(s); } }
  else { for (let i = 0; i < 16; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(.05, 16, 12), M(i % 5 ? '#F08A1C' : '#7BB34A', .5)); const a = i * 2.4; s.position.set(Math.cos(a) * (.06 + (i % 3) * .08), .07 + (i % 3) * .05, Math.sin(a) * (.06 + (i % 3) * .08)); g.add(s); } }
  const pad = new THREE.Mesh(new THREE.TorusGeometry(.09, .035, 8, 20), M('#7a1f2b', .8)); pad.rotation.x = Math.PI / 2; pad.position.y = -.05; g.add(pad); return g; }

// ---------------- scenes ----------------
const camChar = (camera, h = 1.75, side = 1) => { camera.fov = 26; camera.updateProjectionMatrix(); camera.position.set(1.7 * side, 1.25, 4.6); camera.lookAt(0, h * .52, 0); };
const charScene = (name, extra) => async (ctx) => { const o = await character(name); fit(o, 1.75); ctx.scene.add(o); camChar(ctx.camera); if (extra) await extra(ctx, o); };
export const SCENES = {};
for (const n of Object.keys(CH)) SCENES['ch_' + n] = charScene(n);

// Baba Gidi outfits (CONCEPT): recolour the shipped texture + add garment geometry
SCENES.baba_agbada = async (ctx) => { const o = await character('baba', { recol: (r, g, b) => isGreen(r, g, b) ? shade(hex('#EFE6D2'), r, g, b, 1.3) : null }); fit(o, 1.75); ctx.scene.add(o);
  const robe = agbadaRobe(embroideryTex()); robe.position.set(0, 1.39, 0); robe.scale.set(1, 1, 1); ctx.scene.add(robe); camChar(ctx.camera); };
SCENES.baba_ankara = async (ctx) => { const pf = patternFn('ankara'); const o = await character('baba', { recol: (r, g, b, x, y) => isGreen(r, g, b) ? shade(pf(x, y), r, g, b, 1.4) : null }); fit(o, 1.75); ctx.scene.add(o); camChar(ctx.camera); };
SCENES.baba_okada = async (ctx) => { const o = await character('baba', { recol: (r, g, b, x, y) => isGreen(r, g, b) ? shade(hex('#FF6A13'), r, g, b, 1.4) : null }); fit(o, 1.75); ctx.scene.add(o);
  o.updateMatrixWorld(true); const hb = bone(o, 'HeadTop_End') || bone(o, 'Head'); const hp = new THREE.Vector3(); hb.getWorldPosition(hp);
  const h = helmet(); h.position.set(hp.x, hp.y - 0.17, hp.z + 0.01); h.scale.setScalar(1.25); ctx.scene.add(h); console.log('head ' + hp.toArray().map(v=>v.toFixed(2)));
  for (const y of [1.18, 1.02]) { const s = new THREE.Mesh(new THREE.CylinderGeometry(.205, .19, .045, 40, 1, true), M('#e8e8e8', .2, .6, { emissive: '#666', side: THREE.DoubleSide })); s.position.set(0, y, 0.0); s.scale.z = .7; ctx.scene.add(s); }
  const bike = okada(); bike.position.set(-1.0, 0, -1.4); bike.rotation.y = 0.5; ctx.scene.add(bike); camChar(ctx.camera); ctx.camera.position.set(1.9, 1.35, 5.2); ctx.camera.lookAt(-0.3, 0.85, -0.3); };
SCENES.baba_owambe = async (ctx) => { const pf = patternFn('lace'); const o = await character('baba', { recol: (r, g, b, x, y) => isGreen(r, g, b) ? shade(pf(x, y), r, g, b, 1.5) : (r > 150 && g > 120 && b < 90 ? [240, 196, 60] : null) }); fit(o, 1.75); ctx.scene.add(o);
  const robe = agbadaRobe(embroideryTex('#4B2C8C', '#E8B21E'), '#ffffff'); robe.position.set(0, 1.39, 0); robe.scale.set(1.03, 1, 1.03); ctx.scene.add(robe);
  for (let i = 0; i < 40; i++) { const s = new THREE.Mesh(new THREE.PlaneGeometry(.05, .03), new THREE.MeshBasicMaterial({ color: ['#FAE69E', '#56B4E9', '#E07CC0'][i % 3], side: THREE.DoubleSide, toneMapped: false })); s.position.set((Math.random() - .5) * 2.2, .3 + Math.random() * 2.2, (Math.random() - .5) * 1.5 - .4); s.rotation.set(Math.random() * 3, Math.random() * 3, 0); ctx.scene.add(s); }
  camChar(ctx.camera); ctx.bloom = .2; };
SCENES.baba_jersey = async (ctx) => { const pf = patternFn('stripe'); const o = await character('baba', { recol: (r, g, b, x, y) => isGreen(r, g, b) ? shade(pf(x, y), r, g, b, 1.4) : null }); fit(o, 1.75); ctx.scene.add(o); camChar(ctx.camera); };
SCENES.baba_default = async (ctx) => { const o = await character('baba'); fit(o, 1.75); ctx.scene.add(o); camChar(ctx.camera); };

// Hawkers (CONCEPT): shipped commuter models + head trays
SCENES.hawker_water = async (ctx) => { const o = await character('Ped9'); fit(o, 1.68); ctx.scene.add(o); const t = hawkerTray('water'); t.position.set(0, 1.74, 0); ctx.scene.add(t); camChar(ctx.camera); ctx.camera.lookAt(0, 1.0, 0); };
SCENES.hawker_orange = async (ctx) => { const o = await character('Ped2'); fit(o, 1.66); ctx.scene.add(o); const t = hawkerTray('orange'); t.position.set(0, 1.72, 0); ctx.scene.add(t); camChar(ctx.camera); ctx.camera.lookAt(0, 1.0, 0); };

// Vehicles
const camVeh = (camera, d = 9, y = 2.6, lx = 0) => { camera.fov = 30; camera.updateProjectionMatrix(); camera.position.set(d * .75 + lx, y, d * .8); camera.lookAt(lx, 1.1, 0); };
for (const [k, p] of [['danfo', 'Vehicles/Danfo_2/DanfoNew.glb'], ['keke', 'Vehicles/Keke/LagKeke.glb'], ['taxi', 'Vehicles/Taxi/LagTaxi.glb']])
  SCENES['veh_' + k] = async (ctx) => { const o = await gltf(P + p); fit(o, k === 'danfo' ? 2.0 : k === 'keke' ? 1.75 : 1.45); ctx.scene.add(o); laneMarks(ctx.scene, 1, -2.2); camVeh(ctx.camera, k === 'danfo' ? 8 : 6.5); };
SCENES.veh_okada = async (ctx) => { const b = okada(); b.scale.setScalar(1.0); ctx.scene.add(b); laneMarks(ctx.scene, 1, -1.5); ctx.camera.fov = 30; ctx.camera.updateProjectionMatrix(); ctx.camera.position.set(2.2, 1.25, 2.6); ctx.camera.lookAt(0, .62, 0); };
SCENES.veh_tanker = async (ctx) => { const t = tanker(); ctx.scene.add(t);
  const txt = textTex(['EKO FUEL LOGISTICS', 'FLAMMABLE · NO SMOKING'], { w: 2048, h: 400, bg: '#F5F5F0', fg: '#B3121F', font: 'bold 120px Jakarta, Arial' });
  txt.center.set(.5, .5); txt.rotation = -Math.PI / 2;
  const lab = new THREE.Mesh(new THREE.CylinderGeometry(1.008, 1.008, 3.0, 48, 1, true, -0.34, 0.68), new THREE.MeshStandardMaterial({ map: txt, roughness: .45 })); lab.rotation.z = Math.PI / 2; lab.scale.set(1, 1, .92); lab.position.set(-.35, 1.82, 0); ctx.scene.add(lab);
  ctx.scene.add(decal(t, new THREE.Vector3(1.0, 1.4, .9), new THREE.Euler(0, 0, Math.PI / 4), new THREE.Vector3(.5, .5, 1.0), textTex('1203', { w: 256, h: 256, bg: '#FF7A1A', fg: '#111', font: 'bold 90px Jakarta, Arial' })));
  laneMarks(ctx.scene, 1, -2.5); camVeh(ctx.camera, 10.5, 2.8, 0.4); };
SCENES.veh_brt = async (ctx) => { const b = brt(); ctx.scene.add(b);
  const side = new THREE.Mesh(new THREE.PlaneGeometry(5, .7), new THREE.MeshStandardMaterial({ map: textTex('EKO RAPID · BRT', { w: 2048, h: 290, fg: '#F5F5F0', font: 'bold 200px Jakarta, Arial' }), transparent: true })); side.position.set(-.8, 1.1, 1.292); ctx.scene.add(side);
  laneMarks(ctx.scene, 1, -2.6); camVeh(ctx.camera, 15, 3.4, .5); };
const SLOGANS = { classic: ['NO FOOD FOR', 'LAZY MAN'], godstime: ["GOD'S TIME", 'IS THE BEST'], detty: ['DETTY', 'DECEMBER'], eko: ['EKO O NI', 'BAJE O!'] };
const PAINT = { classic: null, godstime: '#1E7A4A', detty: '#5B2A86', eko: '#C8102E' };
for (const k of Object.keys(SLOGANS)) SCENES['danfo_' + k] = async (ctx) => {
  const o = await gltf(P + 'Vehicles/Danfo_2/DanfoNew.glb'); fit(o, 2.0); if (PAINT[k]) hueShift(o, PAINT[k]); ctx.scene.add(o); o.updateMatrixWorld(true);
  const bb = new THREE.Box3().setFromObject(o); const sz = bb.getSize(new THREE.Vector3()); const longX = sz.x > sz.z;
  // rear slogan + stripes as projected decals (rear = -X end if long axis is X)
  const rear = longX ? new THREE.Vector3(bb.min.x, bb.min.y + sz.y * .42, (bb.min.z + bb.max.z) / 2) : new THREE.Vector3((bb.min.x + bb.max.x) / 2, bb.min.y + sz.y * .42, bb.min.z);
  const rot = longX ? new THREE.Euler(0, -Math.PI / 2, 0) : new THREE.Euler(0, Math.PI, 0);
  const fg = k === 'classic' ? '#111' : '#FAE69E';
  ctx.scene.add(decal(o, rear, rot, new THREE.Vector3((longX ? sz.z : sz.x) * .8, .55, 1.2), textTex(SLOGANS[k], { w: 1024, h: 512, fg, font: 'bold 118px Jakarta, Arial', stroke: k === 'classic' ? null : '#111' })));
  const sideP = longX ? new THREE.Vector3((bb.min.x + bb.max.x) / 2, bb.min.y + sz.y * .36, bb.max.z) : new THREE.Vector3(bb.max.x, bb.min.y + sz.y * .36, (bb.min.z + bb.max.z) / 2);
  const srot = longX ? new THREE.Euler(0, 0, 0) : new THREE.Euler(0, Math.PI / 2, 0);
  const st = document.createElement('canvas'); st.width = 1024; st.height = 128; const sg = st.getContext('2d'); sg.fillStyle = k === 'detty' ? '#E8B21E' : '#111'; sg.fillRect(0, 10, 1024, 34); sg.fillRect(0, 84, 1024, 34);
  const stt = new THREE.CanvasTexture(st); stt.colorSpace = THREE.SRGBColorSpace; ctx.scene.add(decal(o, sideP, srot, new THREE.Vector3((longX ? sz.x : sz.z) * .95, .32, 1.2), stt));
  laneMarks(ctx.scene, 1, -2.4);
  // rear 3/4 view
  ctx.camera.fov = 30; ctx.camera.updateProjectionMatrix(); const c = new THREE.Vector3((bb.min.x + bb.max.x) / 2, 1.0, (bb.min.z + bb.max.z) / 2);
  if (longX) ctx.camera.position.set(c.x - 6.2, 2.4, c.z + 5.6); else ctx.camera.position.set(c.x + 5.6, 2.4, c.z - 6.2); ctx.camera.lookAt(c);
  ctx.info = { longX, sz: [sz.x, sz.y, sz.z] }; console.log('danfo bbox ' + JSON.stringify(ctx.info));
};

// Power-up GLBs (in game)
for (const [k, f] of [['pu_maltina', 'ColdMaltinaGala'], ['pu_purewater', 'PureWater'], ['pu_siren', 'VIPEscortSiren'], ['pu_change', 'ChangeBundle'], ['pu_whistle', 'AgberoWhistle']])
  SCENES[k] = async (ctx) => { const o = await gltf(P + 'PowerUps/' + f + '.glb'); fit(o, .9); ctx.scene.add(o); const r = ring(.5, '#E8B21E', .7, .012); r.position.y = .03; ctx.scene.add(r); ctx.bloom = .4; ctx.camera.fov = 28; ctx.camera.updateProjectionMatrix(); ctx.camera.position.set(1.7, 1.25, 2.4); ctx.camera.lookAt(0, .45, 0); };

// Power-up CONCEPTS
SCENES.pu_owa = async (ctx) => { const o = await character('baba', { anim: 0.3 }); fit(o, 1.75); ctx.scene.add(o);
  const hb = bone(o, 'RightArm'), fa = bone(o, 'RightForeArm'); if (hb) { hb.rotation.x -= 0.0; hb.rotation.z -= 1.0; } if (fa) fa.rotation.z -= 1.6;
  for (let i = 0; i < 5; i++) { const r = ring(.12 + i * .16, '#FAE69E', .95 - i * .15, .012 + i * .004); r.rotation.set(0, Math.PI / 2, 0); r.position.set(.35 + i * .38, 1.58 - i * .05, -.15 - i * .3); r.lookAt(3.2, .9, -2.4); ctx.scene.add(r); }
  const s = sprite('OWA!', '#E8B21E', .8); s.position.set(.6, 2.35, 0); ctx.scene.add(s);
  laneMarks(ctx.scene, 2, -1.5);
  const car = await gltf(P + 'Vehicles/Taxi/LagTaxi.glb'); fit(car, 1.45); car.position.set(3.2, 0, -2.4); car.rotation.y = Math.PI / 2; ctx.scene.add(car);
  const ice = new THREE.Mesh(new RoundedBoxGeometry(3.9, 1.7, 2.2, 4, .2), new THREE.MeshStandardMaterial({ color: '#9fd8ff', transparent: true, opacity: .22, roughness: .05, emissive: '#56B4E9', emissiveIntensity: .4 })); ice.position.set(3.2, .85, -2.4); ctx.scene.add(ice);
  ctx.bloom = .5; ctx.camera.fov = 32; ctx.camera.updateProjectionMatrix(); ctx.camera.position.set(-1.6, 1.9, 5.0); ctx.camera.lookAt(1.3, 1.0, -1.0); };
SCENES.pu_danforide = async (ctx) => { const o = await gltf(P + 'Vehicles/Danfo_2/DanfoNew.glb'); fit(o, 2.0); ctx.scene.add(o);
  o.traverse(m => { if (m.isMesh) { m.material = m.material.clone(); m.material.emissive = new THREE.Color('#E8B21E'); m.material.emissiveIntensity = 0.12; } });
  laneMarks(ctx.scene, 3, 1.5); kerb(ctx.scene, 3.4);
  const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(-2.2, .2, 3.2), new THREE.Vector3(-1.2, 2.9, 0), new THREE.Vector3(.4, 2.9, -3.6), new THREE.Vector3(1.4, .2, -6.6)]);
  const arc = new THREE.Mesh(new THREE.TubeGeometry(curve, 80, .06, 10), new THREE.MeshBasicMaterial({ color: '#FAE69E', toneMapped: false })); ctx.scene.add(arc);
  const head = new THREE.Mesh(new THREE.ConeGeometry(.22, .5, 20), new THREE.MeshBasicMaterial({ color: '#FAE69E', toneMapped: false })); head.position.set(1.4, .45, -6.6); head.rotation.x = Math.PI; ctx.scene.add(head);
  const s = sprite('ENTER WITH YOUR CHANGE!', '#FAE69E', .55, '#0F1219', 2400); s.scale.set(5.6, .6, 1); s.position.set(-.4, 3.5, -1.2); ctx.scene.add(s);
  ctx.bloom = .5; ctx.camera.fov = 34; ctx.camera.updateProjectionMatrix(); ctx.camera.position.set(8.5, 5.0, 6.5); ctx.camera.lookAt(-.2, .8, -1.5); };
SCENES.pu_agbada_armour = async (ctx) => { const o = await character('baba', { recol: (r, g, b) => isGreen(r, g, b) ? shade(hex('#E8B21E'), r, g, b, 1.3) : null }); fit(o, 1.75); ctx.scene.add(o);
  const robe = agbadaRobe(embroideryTex('#D9A520', '#FFF4C8'), '#ffffff'); robe.position.set(0, 1.39, 0); robe.material.metalness = .35; robe.material.roughness = .4; ctx.scene.add(robe);
  const sh = new THREE.Mesh(new THREE.SphereGeometry(1.15, 64, 40), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, side: THREE.DoubleSide, uniforms: { c: { value: new THREE.Color('#FFD36B') } },
    vertexShader: 'varying vec3 n; varying vec3 v; void main(){ vec4 mv = modelViewMatrix*vec4(position,1.); n = normalize(normalMatrix*normal); v = normalize(-mv.xyz); gl_Position = projectionMatrix*mv; }',
    fragmentShader: 'uniform vec3 c; varying vec3 n; varying vec3 v; void main(){ float f = pow(1.-abs(dot(n,v)), 2.6); gl_FragColor = vec4(c*1.1, f*.6+.02); }' }));
  sh.scale.set(.8, 1.0, .8); sh.position.y = 1.0; ctx.scene.add(sh);
  for (let i = 0; i < 60; i++) { const s = new THREE.Mesh(new THREE.OctahedronGeometry(.018), new THREE.MeshBasicMaterial({ color: '#FFF1B8', toneMapped: false })); const a = Math.random() * 6.28, y = Math.random() * 2; s.position.set(Math.cos(a) * .95, y, Math.sin(a) * .95); ctx.scene.add(s); }
  ctx.bloom = .25; camChar(ctx.camera); ctx.camera.position.set(1.9, 1.3, 5.2); };
