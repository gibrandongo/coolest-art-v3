#!/usr/bin/env python3
"""Coolest-art entry: ship the bundled artwork to /output/entry.png.

The artwork lives in the repository as entry.jpg (JPEG bytes). The
competition contract names the output file entry.png and tells PNG and
JPEG apart by the file's first bytes, so the JPEG bytes are written
verbatim under that name. The copy is deterministic: the same input
bytes always produce the same output bytes.
"""

import os
import sys

MAX_BYTES = 1_048_576
JPEG_SOI = b"\xff\xd8\xff"
JPEG_EOI = b"\xff\xd9"
ARTWORK_NAME = "entry.jpg"
OUTPUT_NAME = "entry.png"


def artwork_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, ARTWORK_NAME)


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    src = artwork_path()
    with open(src, "rb") as handle:
        data = handle.read()
    if len(data) > MAX_BYTES:
        sys.exit("artwork exceeds the 1 MiB cap: %d bytes" % len(data))
    if not data.startswith(JPEG_SOI):
        sys.exit("artwork does not start with a JPEG SOI marker")
    if data[-2:] != JPEG_EOI:
        sys.exit("artwork does not end with a JPEG EOI marker")
    outdir = output_dir()
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, OUTPUT_NAME)
    tmp = dest + ".tmp"
    with open(tmp, "wb") as handle:
        handle.write(data)
    os.replace(tmp, dest)
    if os.path.getsize(dest) != len(data):
        sys.exit("short write: %s holds %d bytes, expected %d"
                 % (dest, os.path.getsize(dest), len(data)))
    print("wrote %s: %d bytes" % (dest, len(data)))


if __name__ == "__main__":
    main()
