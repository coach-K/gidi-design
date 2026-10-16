import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { SCENES, setRenderer } from './scenes.js';
const q = new URLSearchParams(location.search), W = +q.get('w'), H = +q.get('h');
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H); renderer.setPixelRatio(1);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
// dusk sky gradient background
const c = document.createElement('canvas'); c.width = 8; c.height = 512; const g = c.getContext('2d');
const gr = g.createLinearGradient(0, 0, 0, 512); gr.addColorStop(0, '#1d2048'); gr.addColorStop(.45, '#4a3a66'); gr.addColorStop(.72, '#b8606a'); gr.addColorStop(.9, '#f28c4b'); gr.addColorStop(1, '#f6b077');
g.fillStyle = gr; g.fillRect(0, 0, 8, 512); const bg = new THREE.CanvasTexture(c); bg.colorSpace = THREE.SRGBColorSpace; scene.background = bg;
const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.35;
scene.fog = new THREE.Fog(0x4a3a66, 18, 60);
const hemi = new THREE.HemisphereLight(0x8a90d0, 0x5a3424, 0.9); scene.add(hemi);
const key = new THREE.DirectionalLight(0xffb070, 3.2); key.position.set(-6, 5, 7); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 0.5, far: 40 }); key.shadow.bias = -0.0004; key.shadow.radius = 4; scene.add(key);
const rim = new THREE.DirectionalLight(0x9fb4ff, 2.0); rim.position.set(6, 4, -6); scene.add(rim);
// asphalt ground with subtle noise + kerb line
const gc = document.createElement('canvas'); gc.width = gc.height = 512; const gg = gc.getContext('2d'); gg.fillStyle = '#2b2c33'; gg.fillRect(0, 0, 512, 512);
for (let i = 0; i < 9000; i++) { const v = 30 + Math.random() * 40 | 0; gg.fillStyle = `rgba(${v + 10},${v + 8},${v + 12},${Math.random() * .5})`; gg.fillRect(Math.random() * 512, Math.random() * 512, 2, 2); }
const gt = new THREE.CanvasTexture(gc); gt.wrapS = gt.wrapT = THREE.RepeatWrapping; gt.repeat.set(8, 8); gt.colorSpace = THREE.SRGBColorSpace;
const ground = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), new THREE.MeshStandardMaterial({ map: gt, roughness: .92, metalness: 0 }));
ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
const camera = new THREE.PerspectiveCamera(30, W / H, 0.05, 200);
window.T = THREE; setRenderer(renderer);
const ctx = { THREE, scene, camera, renderer, key, rim, hemi, ground, bloom: 0 };
try {
  await SCENES[q.get('s')](ctx);
} catch (e) { console.log('scene error ' + e.stack); }
scene.traverse(o => { if (o.isMesh) { o.castShadow = true; if (o !== ground) o.receiveShadow = true; } });
const comp = new EffectComposer(renderer); comp.addPass(new RenderPass(scene, camera));
if (ctx.bloom) comp.addPass(new UnrealBloomPass(new THREE.Vector2(W, H), ctx.bloom, 0.5, 0.85));
comp.addPass(new OutputPass());
for (let i = 0; i < 2; i++) comp.render();
window.DONE = true;
