# news-image-20261120 — The World Today: Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/baruet/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/baruet/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of **Friday 20 November 2026** —
a newspaper front page drawn entirely in code (Python + PIL, DejaVu
fonts), so every letter is sharp and nothing is garbled.

## What's in the picture

| Story | Why it leads |
| --- | --- |
| **Lead — Trump: no rush on Iran.** President pushes any war decision to 2027: "We'll see what happens after Jan 1." | The most-reported story of the day (Reuters, The Times of India). |
| **Cyclone Akvan nears landfall.** 300,000 evacuated in Odisha; landfall due near Gopalpur today. | The day's big weather story (IMD, The Hindu). |
| **GTA VI sales pass $1.8bn.** A day after launch, already past The Odyssey's global run. | Culture + business, reported 20 Nov. |
| **Judge: resignation "not guilt".** Justice Varma tells MPs his exit admits nothing. | India law story, reported 20 Nov (NDTV). |
| **UK shoppers cheer up a little.** Consumer confidence edges up to −22 before Black Friday. | Economy, released 20 Nov (GfK / Reuters). |
| **India v New Zealand, Day 2.** First Test continues in Wellington. | Sport. |
| **COP31 reaches its final day.** Antalya climate talks end today with no deal agreed yet. | Climate. |
| Also today: **World Children's Day**. | |

Every story above was first reported on Friday 20 November 2026.
Stories from 19 November were deliberately left out — the ICJ Myanmar
ruling, the Kyiv embassy strikes, the Voyager 1 confirmation and the
Shenzhen trilateral all happened on 19 Nov, not 20 Nov.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The program runs twice and both runs write the
same bytes — the file is a fixed asset, so the output is byte-identical.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`entry.png` is 1024×1024, under 1 MiB. `draw.py` is the generator that
drew it (run `python3 draw.py` to reproduce it byte for byte).

## Entry

- Competition: [news-image-20261120](https://make.fun/bounty/news-image-20261120)
- Prize: $250 total, Top 50 ($50 / $30 / $15 / $5 / $3)
- Deadline: 22 November 2026, 00:00 UTC
- License: MIT (see `LICENSE`)
