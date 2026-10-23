// Opens every page of the built site in a headless browser and fails on any JavaScript error,
// failed request, or broken in-site link/anchor. Used by ./run.sh check.
import http from "http"; import fs from "fs"; import path from "path";
let chromium;
try { ({ chromium } = await import("playwright")); } catch { console.log("  pages: skipped (run `npm install` to enable browser checks)"); process.exit(0); }
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../docs");
const T = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json", ".md": "text/plain", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".png": "image/png", ".pdf": "application/pdf" };
const srv = http.createServer((q, r) => { let f = path.join(root, decodeURIComponent(q.url.split("?")[0].split("#")[0])); if (f.endsWith("/")) f += "index.html";
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { "content-type": T[path.extname(f)] || "application/octet-stream" }); r.end(d); } }); });
await new Promise((ok) => srv.listen(0, ok));
const base = `http://localhost:${srv.address().port}/`;
const pages = []; (function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walk(p); else if (f.endsWith(".html")) pages.push(path.relative(root, p)); } })(root);
const exe = ["/opt/pw-browsers/chromium"].find((p) => fs.existsSync(p));
const b = await chromium.launch(exe ? { executablePath: exe } : {});
let bad = 0;
for (const u of pages) {
  const p = await b.newPage(); const errs = [];
  p.on("pageerror", (e) => errs.push("JS error: " + e.message));
  p.on("response", (r) => { if (r.status() >= 400 && r.url().startsWith(base) && !r.url().endsWith("favicon.ico")) errs.push(`missing file: ${r.url().slice(base.length)}`); });
  await p.goto(base + u); await p.waitForTimeout(700);
  // every in-site link must point at a real file, and every #anchor at a real id
  const links = await p.evaluate(() => [...document.querySelectorAll("a[href]")].map((a) => a.href).filter((h) => h.startsWith(location.origin)));
  for (const h of new Set(links)) {
    const [file, hash] = h.slice(base.length).split("#");
    const f = path.join(root, decodeURIComponent((file || u).split("?")[0]) || u);
    const target = fs.existsSync(f) && fs.statSync(f).isDirectory() ? path.join(f, "index.html") : f;
    if (!fs.existsSync(target)) { errs.push(`broken link: ${h.slice(base.length)}`); continue; }
    if (hash && target.endsWith(".html") && !fs.readFileSync(target, "utf8").includes(`id="${decodeURIComponent(hash)}"`)) errs.push(`missing anchor: ${h.slice(base.length)}`);
  }
  if (errs.length) { bad++; console.log(`  ✗ ${u}\n    ${[...new Set(errs)].slice(0, 8).join("\n    ")}`); }
  await p.close();
}
console.log(`  pages: ${pages.length} checked, ${bad} with problems`);
await b.close(); srv.close();
process.exit(bad ? 1 : 0);
