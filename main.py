#!/usr/bin/env python3
"""make.fun entry: news-image-20261118.

Writes one image summing up the world news of Wednesday 18 November 2026
to the runner's output directory as entry.png.

The picture (entry.png, committed next to this file) is a newspaper front
page drawn with make_image.py: the APEC summit in Shenzhen where Xi and
Putin met and Trump arrived in China, Iran's strikes on a US base in
Kuwait, Israel's operation in central Gaza, Germany's new air defences
for Ukraine, Cyclone Akvan and the Florida floods, Peltola's Alaska win,
and the midnight launch of GTA VI.

Standard library only, no network, deterministic: the same entry.png
bytes are copied on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024  # the bounty caps the image at 1 MiB


def main() -> None:
    if not os.path.isfile(SOURCE):
        sys.exit(f"entry image missing next to main.py: {SOURCE}")
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        sys.exit(f"entry image too large: {size} bytes > {MAX_BYTES}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    tmp = target + ".tmp"
    shutil.copyfile(SOURCE, tmp)
    os.replace(tmp, target)  # atomic: the runner never sees a partial file
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    main()
