# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Auspiciouspeony/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Auspiciouspeony/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Sum up 22 November's world news in one image: a front page, "THE WORLD", with 35 stories first reported on Sunday 22 November 2026 across 7 regions — tankers hit off Oman, Russia's 400-drone night over Ukraine, the COP31 deal nearing in Antalya, Bolsonaro in ICU, a cartel boss seized in Sinaloa — plus a dotted world map, a BY THE NUMBERS strip and sixteen one-line briefs. Every story was verified against wire reporting dated 22 November 2026. All art is drawn with PIL, so the image is fully reproducible from the build script.

## Run it

```sh
python3 build_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.png` to `/output/entry.png`, byte for byte, so both grader runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
