#!/usr/bin/env node
// DRAFT (not exercised in CI): open a built web app, click through entry screens until the largest
// canvas is big enough, screenshot that canvas.
// usage: node capture.mjs http://localhost:8080/ out.png   (requires: npm i playwright)
import { chromium } from 'playwright';
const [url, out] = process.argv.slice(2);
if (!url || !out) { console.error('usage: capture.mjs <url> <out.png>'); process.exit(2); }
const MIN = 200;
const CLICKABLE = 'button, a[href], [role=button], [class*="cursor-pointer"]'; // cards are often <div>s
const SKIP = /help|settings|credits|back|close|reset|share|ranking/i;           // tune for your UI
const START = /start|play|enter|go|continue|stage|mode/i;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 720, height: 1280 } });
const biggest = async () => {
  const s = await p.locator('canvas').evaluateAll((els) => els.map((e) => e.clientWidth * e.clientHeight)).catch(() => []);
  let best = -1, area = 0; s.forEach((a, i) => { if (a > area) { area = a; best = i; } });
  return area >= MIN * MIN ? best : -1;
};
try {
  await p.goto(url, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(1800);
  for (let i = 0; i < 6 && (await biggest()) < 0; i++) {
    const c = p.locator(CLICKABLE); const n = Math.min(await c.count(), 40); const rows = [];
    for (let j = 0; j < n; j++) { const t = (await c.nth(j).innerText().catch(() => '')).trim(); if (t && !SKIP.test(t)) rows.push({ j, s: START.test(t) }); }
    const pick = rows.find((r) => r.s) || rows[0]; if (!pick) break;
    await c.nth(pick.j).click({ timeout: 3000 }).catch(() => {}); await p.waitForTimeout(2000);
  }
  await p.waitForTimeout(2500);
  const idx = await biggest();
  if (idx < 0) { console.error('UNMEASURED: no play canvas reached'); process.exit(3); }
  await p.locator('canvas').nth(idx).screenshot({ path: out }); console.log('saved', out);
} finally { await b.close(); }
