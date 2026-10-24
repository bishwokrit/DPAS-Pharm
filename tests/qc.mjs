// Deep quality check: every page on desktop and phone, light and dark, plus the main interactions.
// Fails on JS errors, failed requests, sideways overflow, broken images, duplicate ids, or visible "undefined"/"NaN".
// Used by ./run.sh check (after pages.mjs, which covers links and anchors).
import http from "http"; import fs from "fs"; import path from "path";
let chromium;
try { ({ chromium } = await import("playwright")); } catch { console.log("  qc: skipped (run `npm install` to enable browser checks)"); process.exit(0); }
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../docs");
const T = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml",
  ".jpg": "image/jpeg", ".png": "image/png", ".pdf": "application/pdf", ".wasm": "application/wasm", ".xlsx": "application/octet-stream" };
const srv = http.createServer((q, r) => { let f = path.join(root, decodeURIComponent(q.url.split("?")[0].split("#")[0])); if (f.endsWith("/")) f += "index.html";
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { "content-type": T[path.extname(f)] || "application/octet-stream" }); r.end(d); } }); });
await new Promise((ok) => srv.listen(0, ok));
const base = `http://localhost:${srv.address().port}/`;
const pages = []; (function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walk(p); else if (f.endsWith(".html")) pages.push(path.relative(root, p)); } })(root);
const exe = ["/opt/pw-browsers/chromium"].find((p) => fs.existsSync(p));
const b = await chromium.launch(exe ? { executablePath: exe } : {});
const problems = {};
const add = (k, m) => (problems[k] ||= new Set()).add(m);

const VIEWS = [["desktop", { viewport: { width: 1280, height: 860 } }], ["phone", { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }]];
for (const [vname, vopt] of VIEWS) for (const scheme of ["light", "dark"]) {
  const ctx = await b.newContext({ ...vopt, colorScheme: scheme });
  await ctx.addInitScript(() => { localStorage.setItem("tip:welcome", "true"); localStorage.setItem("sketch", "true"); });
  for (const u of pages) {
    const p = await ctx.newPage(), tag = `${u} [${vname}, ${scheme}]`;
    p.on("pageerror", (e) => add(tag, "JS error: " + e.message));
    p.on("console", (m) => { if (m.type() === "error" && !/favicon|ERR_FILE/.test(m.text())) add(tag, "console error: " + m.text().slice(0, 140)); });
    p.on("response", (r) => { if (r.status() >= 400 && r.url().startsWith(base) && !r.url().endsWith("favicon.ico")) add(tag, `missing file: ${r.url().slice(base.length)}`); });
    await p.goto(base + u); await p.waitForTimeout(500);
    // scroll through so lazy content renders and reveals run
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 25)); } scrollTo(0, 0); });
    await p.waitForTimeout(400);
    const r = await p.evaluate(() => {
      const out = [];
      const w = document.documentElement.scrollWidth, vw = innerWidth;
      if (w > vw + 1) out.push(`page scrolls sideways (${w}px wide in a ${vw}px window)`);
      document.querySelectorAll("img").forEach((i) => { if (i.complete && i.naturalWidth === 0 && i.getAttribute("src")) out.push("broken image: " + i.getAttribute("src")); });
      const ids = {}; document.querySelectorAll("[id]").forEach((e) => (ids[e.id] = (ids[e.id] || 0) + 1));
      Object.entries(ids).filter(([, n]) => n > 1).slice(0, 5).forEach(([id]) => out.push("duplicate id: " + id));
      const txt = document.body.innerText;
      const m = txt.match(/.{0,30}\b(undefined|NaN|\[object Object\])\b.{0,30}/);
      if (m) out.push("visible junk text: …" + m[0].replace(/\s+/g, " ") + "…");
      return out;
    });
    r.forEach((m) => add(tag, m));
    await p.close();
  }
  await ctx.close();
}

// interactions: drug sheet, a quiz, an interactive figure, Sidekick, Anki build, Insight
const ctx = await b.newContext({ viewport: { width: 1280, height: 860 }, acceptDownloads: true });
await ctx.addInitScript(() => localStorage.setItem("tip:welcome", "true"));
const p = await ctx.newPage(); const tag = "interactions";
p.on("pageerror", (e) => add(tag, "JS error: " + e.message));
try {
  await p.goto(base + "drugs/index.html"); await p.waitForTimeout(500);
  await p.locator(".dx-tile").first().click(); await p.waitForTimeout(900);
  if (!(await p.locator("#dx-sheet.open").count())) add(tag, "drug sheet did not open");
  await p.goto(base + "L01/index.html"); await p.waitForTimeout(500);
  const fig = p.locator("figure[data-viz]").first(); await fig.scrollIntoViewIfNeeded(); await p.waitForTimeout(600);
  if (!(await fig.locator(".viz svg *").count())) add(tag, "interactive figure did not render");
  else { await fig.locator("[data-step]").first().click(); await p.waitForTimeout(1100); }
  await p.locator(".q .opt").first().click(); await p.waitForTimeout(200);
  if (!(await p.locator(".q.answered").count())) add(tag, "self-test answer did not register");
  await p.locator(".sk-fab").click(); await p.waitForTimeout(700);
  if (!(await p.locator(".sk-panel.open").count())) add(tag, "Sidekick did not open");
  await p.goto(base + "anki/index.html"); await p.waitForTimeout(1200);
  const [dl] = await Promise.all([p.waitForEvent("download", { timeout: 20000 }), p.locator("[data-go]").click()]);
  const f = await dl.path(); if (!f || fs.statSync(f).size < 5000) add(tag, "Anki package looks empty");
  await p.goto(base + "review/index.html"); await p.waitForTimeout(1200);
  for (const id of ["act", "stats", "cover", "fade", "pat", "streak"]) if (!(await p.locator("#" + id).innerHTML()).trim()) add(tag, `Insight section #${id} is empty`);
  await p.goto(base + "index.html"); await p.waitForTimeout(1200);
  if (await p.locator("#dotd[hidden]").count()) add(tag, "Drug of the day did not appear");
} catch (e) { add(tag, "interaction failed: " + e.message.split("\n")[0]); }

await b.close(); srv.close();
const n = Object.keys(problems).length;
for (const [k, v] of Object.entries(problems)) console.log(`  ✗ ${k}\n    ${[...v].slice(0, 6).join("\n    ")}`);
console.log(`  qc: ${pages.length} pages × 2 sizes × 2 themes + interactions, ${n} with problems`);
process.exit(n ? 1 : 0);
