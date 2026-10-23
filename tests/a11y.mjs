// Automated accessibility audit (axe-core, WCAG 2 A/AA) of every page in light and dark mode. Used by ./run.sh check.
import http from "http"; import fs from "fs"; import path from "path"; import { createRequire } from "module";
let chromium; try { ({ chromium } = await import("playwright")); } catch { console.log("  a11y: skipped (run `npm install`)"); process.exit(0); }
const axePath = createRequire(import.meta.url).resolve("axe-core/axe.min.js");
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../docs");
const T = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json", ".md": "text/plain", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".png": "image/png" };
const srv = http.createServer((q, r) => { let f = path.join(root, decodeURIComponent(q.url.split("?")[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { "content-type": T[path.extname(f)] || "x" }); r.end(d); } }); });
await new Promise((ok) => srv.listen(0, ok)); const base = `http://localhost:${srv.address().port}/`;
const pages = []; (function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walk(p); else if (f.endsWith(".html")) pages.push(path.relative(root, p)); } })(root);
const exe = ["/opt/pw-browsers/chromium"].find((x) => fs.existsSync(x));
const b = await chromium.launch(exe ? { executablePath: exe } : {});
const found = new Map();
for (const scheme of ["light", "dark"]) for (const u of pages) {
  const p = await b.newPage({ colorScheme: scheme, reducedMotion: "reduce" });
  await p.addInitScript(() => { localStorage.setItem("tip:welcome", "true"); localStorage.setItem("prefs", JSON.stringify({ motion: "off" })); });
  await p.goto(base + u); await p.waitForTimeout(600);
  await p.evaluate(() => document.querySelectorAll(".appear").forEach((e) => e.classList.add("in")));
  await p.addScriptTag({ path: axePath });
  const audit = async (label) => {
    const res = await p.evaluate(async () => (await axe.run(document, { runOnly: ["wcag2a", "wcag2aa"] })).violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.slice(0, 400).map((n) => n.target.join(" ") + (n.any[0]?.data?.contrastRatio ? ` (${n.any[0].data.contrastRatio}:1 ${n.any[0].data.fgColor} on ${n.any[0].data.bgColor})` : "")) })));
    for (const v of res) { const e = found.get(v.id) || { ...v, where: new Set(), nodes: new Set() }; e.where.add(`${scheme}:${label}`); v.nodes.forEach((n) => e.nodes.add(n)); found.set(v.id, e); }
  };
  // also audit the panels people open: Sidekick, settings, a drug sheet
  if (u === "L01/index.html" || u === "drugs/index.html") {
    await p.click(".sk-fab"); await p.waitForTimeout(900); await audit(u + " +sidekick");
    await p.keyboard.press("Escape"); await p.click(".set-btn"); await p.waitForTimeout(400); await audit(u + " +settings"); await p.keyboard.press("Escape");
    if (u === "drugs/index.html") { await p.click(".dx-tile"); await p.waitForTimeout(900); await audit(u + " +drug sheet"); }
  }
  const res = await p.evaluate(async () => (await axe.run(document, { runOnly: ["wcag2a", "wcag2aa"] })).violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.slice(0, 400).map((n) => n.target.join(" ") + (n.any[0]?.data?.contrastRatio ? ` (${n.any[0].data.contrastRatio}:1 ${n.any[0].data.fgColor} on ${n.any[0].data.bgColor})` : "")) })));
  for (const v of res) { const k = `${v.id}`; const e = found.get(k) || { ...v, where: new Set(), nodes: new Set() }; e.where.add(`${scheme}:${u}`); v.nodes.forEach((n) => e.nodes.add(n)); found.set(k, e); }
  await p.close();
}
for (const v of found.values()) console.log(`  ✗ [${v.impact}] ${v.id}: ${v.help}\n      pages: ${[...v.where].slice(0, 4).join(", ")}${v.where.size > 4 ? ` +${v.where.size - 4}` : ""}\n      e.g. ${[...v.nodes].join("\n           ")}`);
console.log(`  a11y: ${pages.length} pages × 2 themes, ${found.size} kinds of problems`);
await b.close(); srv.close(); process.exitCode = found.size ? 1 : 0;
