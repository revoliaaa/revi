// Render overlay.html (lapisan ilustrasi transparan) ke PDF A0 via Chromium.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(__dirname, 'overlay.html'));
  await p.pdf({ path: path.resolve(__dirname, 'build/overlay.pdf'), width: '33.11in', height: '46.81in', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
