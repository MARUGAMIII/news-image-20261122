// THE WORLD TODAY — Sunday 22 November 2026.
//
// The entry image lives in this repository as entry.png: a one-page
// newspaper front page summing up the day's world news, drawn by design.py
// (Pillow, DejaVu fonts, no network, no timestamps) and saved as a
// deterministic PNG. This program does nothing but copy that file to the
// output directory, so both grader runs write exactly the same bytes.
//
// The program first checks the image is a whole PNG inside the limits:
// at most 1 MiB, at most 1024x1024, PNG magic up front and a complete IEND
// chunk at the end. If any check fails it throws instead of writing.
//
// Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22.18 or later, standard library only.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const IEND_CHUNK = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

const sourcePath = new URL("./entry.png", import.meta.url);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const targetPath = join(outputDir, "entry.png");

function checkPng(bytes, label) {
  if (bytes.length === 0) {
    throw new Error(`${label} is empty`);
  }
  if (bytes.length > MAX_BYTES) {
    throw new Error(
      `${label} is ${bytes.length} bytes, over the ${MAX_BYTES} byte limit`,
    );
  }
  if (!bytes.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)) {
    throw new Error(`${label} does not start with the PNG signature`);
  }
  if (!bytes.subarray(bytes.length - IEND_CHUNK.length).equals(IEND_CHUNK)) {
    throw new Error(`${label} does not end with a complete IEND chunk`);
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(
      `${label} is ${width}x${height}, over the ${MAX_SIDE}x${MAX_SIDE} limit`,
    );
  }
  return { width, height };
}

const size = statSync(sourcePath).size;
const original = readFileSync(sourcePath);
const dims = checkPng(original, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourcePath, targetPath);

const written = readFileSync(targetPath);
if (written.length !== size || !written.equals(original)) {
  throw new Error("the copied entry.png does not match the repository copy");
}
checkPng(written, "copied entry.png");
console.log(
  `wrote ${targetPath} (${size} bytes, ${dims.width}x${dims.height})`,
);
