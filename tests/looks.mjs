// Picture comparison: a safety net for style changes. Photographs a fixed set of screens (clock frozen, motion off)
// and compares each with the picture saved in tests/looks/. A screen that changed is listed, so a style edit meant for
// one place cannot quietly alter another.
//   node tests/looks.mjs          compare and report (used by ./run.sh check; reports, never blocks)
//   node tests/looks.mjs accept   the new look is intended: save it as the reference
import http from "http"; import fs from "fs"; import path from "path";
let chromium;
try { ({ chromium } = await import("playwright")); } catch { console.log("  looks: skipped (run `npm install` to enable browser checks)"); process.exit(0); }
const here = path.dirname(new URL(import.meta.url).pathname), root = path.resolve(here, "../docs"), store = path.join(here, "looks");
const accept = process.argv[2] === "accept";
const T = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".png": "image/png", ".wasm": "application/wasm" };
const srv = http.createServer((q, r) => { let f = path.join(root, decodeURIComponent(q.url.split("?")[0].split("#")[0])); if (f.endsWith("/")) f += "index.html";
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { "content-type": T[path.extname(f)] || "application/octet-stream" }); r.end(d); } }); });
await new Promise((ok) => srv.listen(0, ok));
const base = `http://localhost:${srv.address().port}/`;

// name, page, what to bring into view, [width, colour scheme]
const SHOTS = [
  ["home", "index.html"], ["home-week", "index.html", ".first-screen + .section"], ["home-dark", "index.html", null, 1280, "dark"], ["home-phone", "index.html", null, 390],
  ["lecture-top", "L09/index.html"], ["lecture-part", "L09/index.html", ".part-sec"], ["lecture-part-dark", "L09/index.html", ".part-sec", 1280, "dark"],
  ["lecture-part-phone", "L09/index.html", ".part-sec .rd", 390], ["lecture-summary", "L05/index.html", "#summary"], ["lecture-cram", "L05/index.html", "#cram"],
  ["lecture-selftest", "L05/index.html", "#selftest"], ["figure", "L07/index.html", "figure[data-viz]"], ["drugs", "drugs/index.html"], ["drugs-dark", "drugs/index.html", null, 1280, "dark"],
  ["practice", "practice/index.html"], ["insight", "review/index.html"], ["syllabus", "syllabus/index.html"], ["grades", "syllabus/index.html", "#calc"], ["class-stats", "syllabus/index.html", "#class"],
  ["exam", "exams/unit3/index.html"], ["anki", "anki/index.html"],
];
const FROZEN = new Date("2026-11-09T15:00:00Z").getTime();
const exe = ["/opt/pw-browsers/chromium"].find((p) => fs.existsSync(p));
const b = await chromium.launch(exe ? { executablePath: exe } : {});
fs.mkdirSync(store, { recursive: true });
const cmp = await (await b.newContext()).newPage();
const changed = [], fresh = [];
for (const [name, url, sel, w = 1280, scheme = "light"] of SHOTS) {
  const ctx = await b.newContext({ viewport: { width: w, height: 900 }, colorScheme: scheme, reducedMotion: "reduce" });
  const p = await ctx.newPage();
  await p.addInitScript((t) => {
    const D = Date; // eslint-disable-next-line no-global-assign
    Date = class extends D { constructor(...a) { if (a.length) super(...a); else super(t); } static now() { return t; } };
    try { localStorage.setItem("prefs", JSON.stringify({ motion: "off" })); } catch {}
    document.addEventListener("DOMContentLoaded", () => { const s = document.createElement("style"); s.textContent = ".tipcard,.sk-fab,.dotd,.dx-mol,canvas{visibility:hidden!important}*{caret-color:transparent!important}"; document.head.append(s); });
  }, FROZEN);
  await p.goto(base + url); await p.waitForTimeout(1200);
  if (sel) { await p.evaluate((s) => document.querySelector(s)?.scrollIntoView({ block: "start" }), sel); await p.waitForTimeout(900); }
  const shot = await p.screenshot({ type: "jpeg", quality: 60 });
  await ctx.close();
  const file = path.join(store, `${name}.jpg`);
  if (accept || !fs.existsSync(file)) { fs.writeFileSync(file, shot); if (!accept) fresh.push(name); continue; }
  // share of pixels that differ clearly (moving dots in a figure stay far below the limit)
  const share = await cmp.evaluate(async ([a, c]) => {
    const load = (s) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = "data:image/jpeg;base64," + s; });
    const [x, y] = await Promise.all([load(a), load(c)]);
    if (x.width !== y.width || x.height !== y.height) return 1;
    const px = (i) => { const k = new OffscreenCanvas(i.width, i.height), g = k.getContext("2d"); g.drawImage(i, 0, 0); return g.getImageData(0, 0, i.width, i.height).data; };
    const A = px(x), B = px(y); let n = 0;
    for (let i = 0; i < A.length; i += 4) if (Math.abs(A[i] - B[i]) + Math.abs(A[i + 1] - B[i + 1]) + Math.abs(A[i + 2] - B[i + 2]) > 90) n++;
    return n / (A.length / 4);
  }, [fs.readFileSync(file).toString("base64"), shot.toString("base64")]);
  if (share > 0.025) { changed.push(`${name} (${(share * 100).toFixed(1)}%)`); fs.writeFileSync(path.join(store, `${name}.new.jpg`), shot); }
  else if (fs.existsSync(path.join(store, `${name}.new.jpg`))) fs.unlinkSync(path.join(store, `${name}.new.jpg`));
}
await b.close(); srv.close();
if (accept) { for (const f of fs.readdirSync(store)) if (f.endsWith(".new.jpg")) fs.unlinkSync(path.join(store, f)); console.log(`  looks: ${SHOTS.length} reference pictures saved`); }
else console.log(`  looks: ${SHOTS.length} screens compared, ${changed.length} look different${changed.length ? ": " + changed.join(", ") + " — open tests/looks/<name>.new.jpg beside <name>.jpg; if intended, run ./run.sh looks accept" : ""}${fresh.length ? ` (${fresh.length} new references saved)` : ""}`);
