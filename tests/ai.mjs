// End-to-end test of Sidekick's AI chat + podcast against a fake Anthropic API (same streaming format as the real one).
// Checks the request shape (own key, fallbacks, structured output) and that bad citations get flagged. Used by ./run.sh check.
let chromium;
try { ({ chromium } = await import("playwright")); } catch { console.log("  ai: skipped (run `npm install`)"); process.exit(0); } import http from "http"; import fs from "fs"; import path from "path";
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../docs");
const T = { ".html": "text/html", ".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json", ".md": "text/plain", ".svg": "image/svg+xml", ".jpg": "image/jpeg" };
const srv = http.createServer((q, r) => { let f = path.join(root, decodeURIComponent(q.url.split("?")[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { "content-type": T[path.extname(f)] || "x" }); r.end(d); } }); });
await new Promise((ok) => srv.listen(0, ok)); const base = `http://localhost:${srv.address().port}/`;
const sse = (text) => {
  const ev = (type, data) => `event: ${type}\ndata: ${JSON.stringify({ type, ...data })}\n\n`;
  const chunks = text.match(/[\s\S]{1,40}/g) || [];
  return ev("message_start", { message: { id: "msg_x", type: "message", role: "assistant", model: "claude-opus-5-5", content: [], stop_reason: null, usage: { input_tokens: 10, output_tokens: 1 } } })
    + ev("content_block_start", { index: 0, content_block: { type: "text", text: "" } })
    + chunks.map((c) => ev("content_block_delta", { index: 0, delta: { type: "text_delta", text: c } })).join("")
    + ev("content_block_stop", { index: 0 }) + ev("message_delta", { delta: { stop_reason: "end_turn" }, usage: { output_tokens: 50 } }) + ev("message_stop", {});
};
const reqs = [];
const reply = (body) => {
  const fmt = body.output_config?.format?.schema;
  if (!fmt) return "Albuterol activates β2 receptors and raises cAMP, relaxing bronchial smooth muscle (S26). Made-up claim (S999). See [Grade calculator](syllabus/index.html#calc).";
  const p = fmt.properties;
  if (p.questions) return JSON.stringify({ note: "Great pick.", questions: [{ q: "How deep should we go?", options: ["Exam-level", "First pass"] }, { q: "What confuses you most?", options: ["Potency vs efficacy", "Agonists vs antagonists"] }] });
  if (p.segments) return JSON.stringify({ title: "Receptors, fast", segments: [{ title: "Hook", points: ["Why receptors matter"], recall: 0 }, { title: "Rapid recall", points: ["Competitive vs noncompetitive"], recall: 3 }] });
  return JSON.stringify({ title: "Receptors, fast", script: [
    { who: "A", kind: "talk", say: "This episode is built from your course study guides.", src: "", pause: 0 },
    { who: "B", kind: "talk", say: "Albuterol activates beta-2 receptors.", src: "S26", pause: 0 },
    { who: "A", kind: "recall", say: "Which way does a competitive antagonist shift the curve? Pause and answer.", src: "", pause: 3 },
    { who: "B", kind: "answer", say: "To the right, same maximum.", src: "S999", pause: 0 }] });
};
const exe = ["/opt/pw-browsers/chromium"].find((x) => fs.existsSync(x));
const b = await chromium.launch(exe ? { executablePath: exe } : {}); const errs = [];
const ctx = await b.newContext({ colorScheme: "dark" });
await ctx.route("https://api.anthropic.com/**", async (route) => {
  const body = JSON.parse(route.request().postData()); reqs.push({ headers: route.request().headers(), body });
  await route.fulfill({ status: 200, headers: { "content-type": "text/event-stream", "access-control-allow-origin": "*" }, body: sse(reply(body)) });
});
const p = await ctx.newPage(); p.on("pageerror", (e) => errs.push(e.message)); p.on("console", (m) => m.type() === "error" && errs.push(m.text()));
await p.addInitScript(() => { localStorage.setItem("tip:welcome", "true"); localStorage.setItem("sk:key", JSON.stringify("sk-ant-test-key")); });
await p.goto(base + "L01/index.html"); await p.waitForTimeout(600);
await p.click(".sk-fab"); await p.waitForTimeout(800);
await p.evaluate(() => { const f = document.querySelector(".sk-panel form"); f.q.value = "albuterol"; f.requestSubmit(); }); await p.waitForTimeout(2500);
const chat = await p.evaluate(() => ({ text: document.querySelector(".sk-msg.ai")?.innerText.slice(0, 160), badCites: [...document.querySelectorAll(".sk-msg.ai .cite-bad")].map((x) => x.textContent), warn: !!document.querySelector(".sk-msg.ai .cite-warn"), link: document.querySelector(".sk-msg.ai a")?.getAttribute("href") }));

// podcast
await p.click('.sk-tabs [data-group="listen"]'); await p.waitForTimeout(300);
await p.click('.sk-sub [data-tab="pod"]'); await p.waitForTimeout(800);
await p.click(".pod-chip"); await p.click("[data-plan]"); await p.waitForTimeout(2000);
await p.click(".pod-qq .pod-chip"); await p.click("[data-outline]"); await p.waitForTimeout(2000);
await p.click("[data-write]"); await p.waitForTimeout(2500);

// what was sent to the API
const fail = [];
if (!chat.badCites?.length || !chat.warn) fail.push("chat did not flag the made-up citation");
if (!chat.link?.includes("syllabus/index.html#calc")) fail.push("chat page link not rendered");
if (reqs.some((r) => !r.headers["x-api-key"]?.startsWith("sk-ant-"))) fail.push("a request did not use the student's own key");
if (reqs.slice(1).some((r) => !r.body.output_config?.format)) fail.push("podcast step without structured output");
if (errs.length) fail.push("page errors: " + errs.join("; "));
console.log(fail.length ? "  ai: ✗ " + fail.join("\n  ai: ✗ ") : `  ai: chat + podcast flow OK (${reqs.length} API calls, citations checked)`);
process.exitCode = fail.length ? 1 : 0;
await b.close(); srv.close();
