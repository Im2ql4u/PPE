// Run: node --test web/tests
import test from "node:test";
import assert from "node:assert/strict";
import {
  WHITE_COUNT, buildAnchors, isBlack, keyRect, labelAt, layoutLane, midiName, nearestSample, notesIn,
  sampleFile, spanOf, stepHarmony, toSeconds, whiteIndex, xAt, fifthsOf, nameOfFifths, transposeTonic,
} from "../js/util.js";

test("88-key geometry: 52 white keys, A0 first, C8 last", () => {
  assert.equal(WHITE_COUNT, 52);
  assert.equal(whiteIndex(21), 0);
  assert.equal(whiteIndex(108), 51);
  assert.equal(isBlack(22), true); // A#0
  assert.equal(isBlack(60), false); // C4
});

test("black keys sit between their white neighbours", () => {
  for (let m = 22; m < 108; m++) {
    if (!isBlack(m)) continue;
    const r = keyRect(m);
    const left = keyRect(m - 1), right = keyRect(m + 1);
    assert.ok(r.x > left.x && r.x + r.w < right.x + right.w, `key ${m}`);
  }
});

test("midiName spells C4 and A0", () => {
  assert.equal(midiName(60), "C4");
  assert.equal(midiName(21), "A0");
  assert.equal(midiName(61), "C♯4");
});

test("xAt interpolates between anchors and clamps at the ends", () => {
  const a = [{ t: 0, x: 10 }, { t: 2, x: 30 }, { t: 4, x: 50 }];
  assert.equal(xAt(a, 0), 10);
  assert.equal(xAt(a, 1), 20);
  assert.equal(xAt(a, 2), 30);
  assert.equal(xAt(a, 5), 50);
});

test("buildAnchors keeps the leftmost x per onset and adds measure bounds", () => {
  const pts = buildAnchors(4, 8, 100, 300, [{ t: 4, x: 120 }, { t: 4, x: 110 }, { t: 6, x: 200 }]);
  assert.deepEqual(pts, [{ t: 4, x: 110 }, { t: 6, x: 200 }, { t: 8, x: 300 }]);
});

test("buildAnchors adds the measure start when the first note is late, and stays monotone", () => {
  const pts = buildAnchors(0, 4, 0, 100, [{ t: 1, x: 40 }, { t: 2, x: 30 }]);
  assert.deepEqual(pts.map((p) => p.t), [0, 1, 2, 4]);
  assert.ok(pts.every((p, i) => i === 0 || p.x >= pts[i - 1].x));
});

test("harmony stepping moves to the next / previous label", () => {
  const labels = [{ on: 0, end: 2 }, { on: 2, end: 4 }, { on: 4, end: 8 }];
  assert.equal(stepHarmony(labels, 2, +1).on, 4);
  assert.equal(stepHarmony(labels, 2, -1).on, 0);
  assert.equal(stepHarmony(labels, 4, +1), null);
  assert.equal(labelAt(labels, 3).on, 2);
});

test("spans and note filtering", () => {
  const notes = [{ on: 0, dur: 1 }, { on: 1, dur: 2 }, { on: 4, dur: 1 }];
  assert.deepEqual(spanOf(notes.slice(0, 2)), { start: 0, end: 3 });
  assert.equal(notesIn(notes, 0, 4).length, 2);
});

test("lane layout pushes overlapping labels right and keeps free ones in place", () => {
  assert.deepEqual(layoutLane([{ x: 0, w: 20 }, { x: 10, w: 10 }, { x: 100, w: 5 }], 5), [0, 25, 100]);
});

test("tonics move along the line of fifths", () => {
  assert.equal(fifthsOf("C♯"), 7);
  assert.equal(fifthsOf("B♭"), -2);
  assert.equal(nameOfFifths(7), "C♯");
  assert.equal(nameOfFifths(-2), "B♭");
  assert.equal(transposeTonic("C♯", 2), "D♯"); // +M2: C# minor -> D# minor
  assert.equal(transposeTonic("B", -7), "B♭"); // -A1
  assert.equal(transposeTonic("E", 0), "E");
});

test("seconds from quarters", () => {
  assert.equal(toSeconds(1, 60), 1);
  assert.equal(toSeconds(2, 120, 0.5), 2);
});

test("nearest sample is within a tritone-free 1.5 semitones and files exist for every sample", () => {
  for (let m = 21; m <= 108; m++) {
    const { sample, rate } = nearestSample(m);
    assert.ok(Math.abs(m - sample) <= 1, `midi ${m} -> ${sample}`);
    assert.ok(rate > 0.94 && rate < 1.07);
    assert.match(sampleFile(sample), /^(C|Ds|Fs|A)\d\.mp3$/);
  }
});
