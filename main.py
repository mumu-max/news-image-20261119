"""news-image-20261119 entrypoint (Python 3.13, standard library only).

The entry image is built offline by build_image.py from news.json and an
AI-illustrated collage, and is committed to this repository as entry.png.
This program only copies that image to the grader's output directory, so
both graded runs write exactly the same bytes with no network access.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print(f"missing bundled image: {src}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
