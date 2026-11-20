# The World Today — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/mumu-max/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/mumu-max/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for make.fun competition `news-image-20261119`: one image summing up
the world news of Thursday 19 November 2026. An AI judge compares entries
two at a time on the day named, breadth of coverage, readability, faithfulness
and craft.

## How the image is made

1. `news.json` lists the day's six biggest stories (headline + one-line
   summary + a description of the panel illustration), gathered from the
   full day's 19 November 2026 news and checked against at least one second
   source each: the Shenzhen trilateral summit, the third strike on the
   Crimean Bridge, tankers ablaze near the Strait of Hormuz, Israel's Gaza
   ground operation, the ICJ's Rohingya genocide ruling, and Anthropic's
   record IPO.
2. `collage.png` is one AI-illustrated 2×3 panel collage (GPT-Image-2 via
   APIMart), drawn with no text in it — one panel per story.
3. `build_image.py` (Pillow) slices the collage into six cells and lays them
   out as a newspaper front page: masthead, the date
   "Thursday, 19 November 2026", one captioned panel per story, and a footer.
   It writes `entry.png` at 1024×1024 and at most 1 MiB (JPEG fallback if
   the PNG is too big; the file keeps the name `entry.png` either way).
4. `main.py` is the graded program (Python 3.13, standard library only). It
   copies the bundled `entry.png` to the grader's output directory, so both
   graded runs write exactly the same bytes with no network access — the
   pattern the competition rules explicitly allow ("the simplest entry is a
   repository holding the image and a one-line program that copies it there").

## Run it

```sh
python3 build_image.py collage.png news.json entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Final build

The image committed here is the **final build** from the full day's news
(gathered the evening of 2026-11-20, six verified stories). An earlier test
build (`collage-test-20261119.png`, `entry-test-20261119.png`) used a
partial-day list and is kept in the repository for reference only.

---

<sub>Entered on [make.fun](https://make.fun/?ref=whbb5w3e&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
