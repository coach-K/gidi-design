// node shot.js <scene> <out.png> [w] [h]
const puppeteer = require('puppeteer-core');
(async () => {
  const [scene, out, w='1600', h='1200'] = process.argv.slice(2);
  const b = await puppeteer.launch({executablePath:'/usr/bin/google-chrome', headless:'new', args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const p = await b.newPage(); await p.setViewport({width:+w, height:+h});
  p.on('console', m => console.log('[page]', m.text())); p.on('pageerror', e => console.log('[err]', e.message));
  await p.goto(`http://127.0.0.1:8931/render.html?s=${scene}&w=${w}&h=${h}`);
  await p.waitForFunction('window.DONE===true', {timeout: 240000});
  await (await p.$('canvas')).screenshot({path: out});
  await b.close();
})();
