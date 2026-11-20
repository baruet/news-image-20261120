// news-image-20261120 entry (Node 22, standard library only).
// The image beside this file is the entry: copy it to the output path
// the grader reads, /output/entry.png. No network, no dependencies,
// and the same bytes every run, so both grader runs match.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL("./entry.png", import.meta.url),
  join(outDir, "entry.png"),
);
