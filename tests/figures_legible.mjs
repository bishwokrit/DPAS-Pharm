// Legibility sweep of every interactive figure: opens each one (as drawn, then with each drug added) and measures the
// picture itself: labels that run off the canvas, labels that collide with each other, and script errors.
//   node tests/figures_legible.mjs [L07 L08 …]     (default: every lecture)
import http from "http"; import fs from "fs"; import path from "path";
let chromium;
try { ({ chromium } = await import("playwright")); } catch { console.log("  figures: skipped (run `npm install` to enable browser checks)"); process.exit(0); }
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../docs");
const T = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".png": "image/png" };
const srv = http.createServer((q, r) => { let f = path.join(root, decodeURIComponent(q.url.split("?")[0].split("#")[0])); if (f.endsWith("/")) f += "index.html";
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { "content-type": T[path.extname(f)] || "application/octet-stream" }); r.end(d); } }); });
await new Promise((ok) => srv.listen(0, ok));
const base = `http://localhost:${srv.address().port}/`;
const lecs = process.argv.slice(2).length ? process.argv.slice(2) : fs.readdirSync(root).filter((d) => /^L\d\d$/.test(d)).sort();
const exe = ["/opt/pw-browsers/chromium"].find((p) => fs.existsSync(p));
const b = await chromium.launch(exe ? { executablePath: exe } : {});
const p = await b.newPage({ viewport: { width: 1280, height: 900 }, reducedMotion: "reduce" });
let err = ""; p.on("pageerror", (e) => (err = e.message));
await p.addInitScript(() => { try { localStorage.setItem("prefs", JSON.stringify({ motion: "off" })); } catch {} document.addEventListener("DOMContentLoaded", () => { const s = document.createElement("style"); s.textContent = ".tipcard,.sk-fab{display:none!important}"; document.head.append(s); }); });
const measure = (f) => f.evaluate((fig) => {
  const svg = fig.querySelector(".viz svg"); if (!svg) return { off: [], hit: [] };
  const box = svg.getBoundingClientRect(), vis = (e) => { const c = getComputedStyle(e); return c.display !== "none" && c.visibility !== "hidden" && +c.opacity > 0.05 && !e.closest(".vz-hide"); };
  const ts = [...svg.querySelectorAll("text")].filter((t) => t.textContent.trim() && vis(t)).map((t) => ({ s: t.textContent.trim().slice(0, 34), r: t.getBoundingClientRect() })).filter((t) => t.r.width > 2 && [...t.s].length > 3);  // moving particles (H⁺, Na⁺, a drop) are short and are not labels
  const off = ts.filter((t) => t.r.left < box.left - 3 || t.r.right > box.right + 3 || t.r.top < box.top - 3 || t.r.bottom > box.bottom + 3).map((t) => t.s);
  const hit = [];
  for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) {
    const a = ts[i].r, c = ts[j].r, w = Math.min(a.right, c.right) - Math.max(a.left, c.left), h = Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top);
    if (ts[i].s !== ts[j].s && w > 6 && h > 5 && w * h > 0.22 * Math.min(a.width * a.height, c.width * c.height)) hit.push(`"${ts[i].s}" × "${ts[j].s}"`);
  }
  return { off, hit };
});
let n = 0, bad = 0;
for (const L of lecs) {
  await p.goto(base + L + "/index.html"); await p.waitForTimeout(500);
  const count = await p.$$eval("figure[data-viz]", (x) => x.length);
  for (let i = 0; i < count; i++) {
    const f = (await p.$$("figure[data-viz]"))[i]; n++;
    await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(650);
    const name = await f.evaluate((e) => `${e.dataset.viz} ${e.querySelector("img")?.getAttribute("src") || ""}`);
    const issues = new Set(); err = "";
    const take = async (state) => { const m = await measure(f); m.off.forEach((s) => issues.add(`off the canvas: "${s}" (${state})`)); m.hit.forEach((s) => issues.add(`overlap: ${s} (${state})`)); if (err) { issues.add(`script error: ${err}`); err = ""; } };
    if (!(await f.$(".viz svg"))) issues.add("no picture drawn");
    await take("start");
    const chips = await f.$$(".viz .vz-chip");
    for (let k = 0; k < chips.length; k++) {
      await chips[k].click().catch(() => {}); await p.waitForTimeout(420); await take(`drug ${k + 1}`);
      await chips[k].click().catch(() => {}); await p.waitForTimeout(120);
    }
    if (issues.size) { bad++; console.log(`  ✗ ${L} ${name}`); [...issues].slice(0, 6).forEach((s) => console.log(`      ${s}`)); }
  }
}
await b.close(); srv.close();
console.log(`  figures: ${n} drawn and exercised, ${bad} with legibility problems`);
