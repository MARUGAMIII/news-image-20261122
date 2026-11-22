# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/MARUGAMIII/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/MARUGAMIII/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One-page newspaper front page summing up the world's news of Sunday 22 November 2026: Iran's Revolutionary Guard says it struck two US Patriot radars at bases in Bahrain late Saturday, widening the Gulf war; COP31 runs into overtime in Antalya as a revised text is tabled at dawn, still omitting fossil fuels and the $120bn adaptation target; the EU and Indonesia sign their decade-in-the-making trade pact in Brussels; Hong Kong votes for the Election Committee that picks its leaders; Mexico flies captured cartel boss "El Chapo Isidro" to the capital after a deadly firefight in Sinaloa; and on the sports pages Ireland stun world champions South Africa 20–17 while England thrash the All Blacks 37–12. The page carries 50 sourced stories, a date check and a UTC timeline, so the image explains itself with no feed attached.

The image is drawn by `design.py` (Python + Pillow, DejaVu fonts, no network, no timestamps — fully reproducible) and rendered to a single 1024×1024 PNG; `main.ts` only copies it to the output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Node.js 22.18 or later, standard library only. The run copies `entry.png` to the output directory as `entry.png`, after checking it is a whole PNG of at most 1 MiB and 1024×1024 pixels, and is deterministic: two runs write the same bytes. To re-render the image from the story data:

```sh
python3 design.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
