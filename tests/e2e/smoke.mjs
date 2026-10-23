// Browser interaction test over the Chrome DevTools Protocol, with no npm packages: Node ≥ 22 has
// WebSocket and fetch built in. Drives a real Chrome/Edge against a running server.
//
//   uv run python -m ppe serve --port 8765        (in another terminal)
//   node tests/e2e/smoke.mjs                      (CHROME=/path/to/chrome to override)
import { spawn } from "node:child_process";
import { existsSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = process.env.PPE_URL || "http://127.0.0.1:8765";
const PORT = 9333;
const CANDIDATES = [
  process.env.CHROME,
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "/usr/bin/google-chrome", "/usr/bin/chromium",
].filter(Boolean);
const browserPath = CANDIDATES.find((p) => existsSync(p));
if (!browserPath) { console.error("No Chrome/Edge found; set CHROME=..."); process.exit(2); }

const profile = mkdtempSync(join(tmpdir(), "ppe-e2e-"));
const browser = spawn(browserPath, [
  "--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run",
  "--autoplay-policy=no-user-gesture-required", "--window-size=1440,1000", "about:blank",
], { stdio: "ignore" });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws, nextId = 1;
const pending = new Map();
const errors = [];

async function connect() {
  for (let i = 0; i < 50; i++) {
    try {
      const targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = targets.find((t) => t.type === "page");
      if (page) {
        ws = new WebSocket(page.webSocketDebuggerUrl);
        await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
        ws.onmessage = (m) => {
          const msg = JSON.parse(m.data);
          if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
          if (msg.method === "Runtime.exceptionThrown") errors.push(msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text);
          if (msg.method === "Runtime.consoleAPICalled" && msg.params.type === "error") errors.push(msg.params.args.map((a) => a.value ?? a.description).join(" "));
        };
        return;
      }
    } catch { /* not up yet */ }
    await sleep(200);
  }
  throw new Error("could not connect to the browser");
}

const send = (method, params = {}) => new Promise((res) => {
  const id = nextId++;
  pending.set(id, res);
  ws.send(JSON.stringify({ id, method, params }));
});

async function js(expr) {
  const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result.exceptionDetails) throw new Error(`${expr}\n→ ${r.result.exceptionDetails.exception?.description}`);
  return r.result.result.value;
}

async function waitFor(expr, what, timeout = 15000) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeout) {
    if (await js(`!!(${expr})`)) return;
    await sleep(100);
  }
  throw new Error(`timed out waiting for ${what}: ${expr}`);
}

let passed = 0;
async function check(name, fn) {
  try {
    await fn();
    passed++;
    console.log(`  ✓ ${name}`);
  } catch (e) {
    console.log(`  ✗ ${name}\n    ${e.message}`);
    process.exitCode = 1;
  }
}

const text = (sel) => `(document.querySelector(${JSON.stringify(sel)})?.textContent || "")`;

try {
  await connect();
  await send("Runtime.enable");
  await send("Page.enable");
  console.log(`browser: ${browserPath}\napp: ${BASE}`);

  await check("loads Moonlight with score and analysis lanes", async () => {
    await send("Page.navigate", { url: `${BASE}/#piece=moonlight` });
    await waitFor(`document.querySelectorAll('.svg-host g.note').length > 1000`, "score notes");
    await waitFor(`document.querySelectorAll('.lane-label').length > 150`, "lane labels");
  });

  await check("clicking a lane label selects that harmony and explains both readings", async () => {
    await js(`[...document.querySelectorAll('.lane-label')].find(e => e.textContent.trim() === 'N⁶').click()`);
    await waitFor(`${text(".sel-head h2")} === 'm. 3, beat 2'`, "selection header");
    await waitFor(`document.querySelectorAll('.reading').length === 2`, "two readings");
    const figs = await js(`[...document.querySelectorAll('.reading .fig')].map(e => e.textContent)`);
    if (!figs.every((f) => f === "N⁶")) throw new Error(`figures ${figs}`);
  });

  await check("the keyboard shows the selected chord (D–F♯–A) with roles", async () => {
    await waitFor(`document.querySelectorAll('.keyboard .key.marked').length >= 3`, "marked keys");
    const roles = await js(`[...document.querySelectorAll('.keyboard .key.marked .role')].map(e => e.textContent)`);
    for (const r of ["R", "3", "5"]) if (!roles.includes(r)) throw new Error(`roles ${roles}`);
  });

  await check("selected notes are highlighted in the score", async () => {
    await waitFor(`document.querySelectorAll('.svg-host g.note.sel').length >= 6`, "highlighted notes");
  });

  await check("substitution candidates appear for a harmony", async () => {
    await waitFor(`document.querySelectorAll('.cand').length >= 4`, "candidates");
  });

  await check("arrow key steps to the next harmony", async () => {
    await js(`window.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight'}))`);
    await waitFor(`${text(".sel-head h2")} === 'm. 4'`, "next harmony (m. 4)");
  });

  await check("clicking a note selects it; double-click selects its chord", async () => {
    await js(`document.querySelector('.svg-host g.note').dispatchEvent(new MouseEvent('click', {bubbles: true}))`);
    await waitFor(`document.querySelectorAll('.svg-host g.note.sel').length === 1`, "single selected note");
    await js(`document.querySelector('.svg-host g.note').dispatchEvent(new MouseEvent('dblclick', {bubbles: true}))`);
    await waitFor(`${text(".sel-head h2")} === 'm. 1'`, "harmony of first note");
  });

  await check("transposing updates the key name and the lanes", async () => {
    await js(`[...document.querySelectorAll('.step')].find(b => b.textContent === '+').click()`);
    await waitFor(`${text(".transpose .value")}.includes('D minor')`, "D minor");
    await waitFor(`[...document.querySelectorAll('.lane-label i')].some(e => e.textContent.startsWith('d:'))`, "lane key d:");
    await js(`[...document.querySelectorAll('.step')].find(b => b.textContent === '−').click()`);
    await waitFor(`${text(".transpose .value")} === 'Original key'`, "back to original key");
  });

  await check("playback starts, lights notes, and stops", async () => {
    await js(`[...document.querySelectorAll('.mode')].find(b => b.textContent === 'Blocked chords').click()`);
    await js(`document.querySelector('.play').click()`);
    await waitFor(`${text(".play")}.includes('Stop')`, "stop button");
    await waitFor(`document.querySelectorAll('.svg-host g.note.playing').length > 0 || document.querySelectorAll('.key.sounding').length > 0`, "sounding notes", 8000);
    await js(`document.querySelector('.play').click()`);
    await waitFor(`${text(".play")}.includes('Play')`, "play button again");
  });

  await check("disagreement colouring marks disputed notes", async () => {
    await waitFor(`document.querySelectorAll('.svg-host g.note.disputed').length > 50`, "disputed notes");
  });

  await check("the Bach prelude opens with expert and automatic readings", async () => {
    await send("Page.navigate", { url: `${BASE}/#piece=bach-prelude-c&s=20&e=24` });
    await waitFor(`document.querySelectorAll('.reading').length === 2`, "two readings");
    await waitFor(`document.querySelector('.reading .tag')?.textContent === 'automatic'`, "automatic tag");
    await waitFor(`document.querySelector('.compare .badge')?.textContent === 'Different key'`, "key-frame comparison");
  });

  await check("no JavaScript errors", async () => {
    if (errors.length) throw new Error(errors.slice(0, 5).join("\n    "));
  });
} catch (e) {
  console.error(e);
  process.exitCode = 1;
} finally {
  console.log(`${passed} passed`);
  try { ws?.close(); } catch { /* ignore */ }
  browser.kill();
  await sleep(300);
  try { rmSync(profile, { recursive: true, force: true }); } catch { /* Edge may hold files briefly */ }
}
