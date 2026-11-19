# The World Today — 19 November 2026

Entry for make.fun competition `news-image-20261119`: one image summing up
the world news of Thursday 19 November 2026. An AI judge compares entries
two at a time on the day named, breadth of coverage, readability, faithfulness
and craft.

## How the image is made

1. `news.json` lists the day's six biggest stories (headline + one-line
   summary + a description of the panel illustration), gathered from the
   19 November 2026 editions of the Japan Times, NDTV, The Hindu and the
   Manila Times, and checked against at least one second source each.
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

## Reproduce

```sh
python3 build_image.py collage.png news.json entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Test build vs final build

The image committed here is a **test build** from a partial-day news list
(gathered 2026-11-19 ~15:15 CST, while the day was still running). The final
build on the evening of 2026-11-20 replaces `news.json` with the full day's
news and regenerates `entry.png` before submission.
