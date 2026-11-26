#!/usr/bin/env python3
"""The 3AM Commit Message — make.fun bounty entry.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output):
the funniest one-line git commit message an AI coding agent types at
3am after a long night of fixing its own bugs.

Pure standard library, deterministic: the same bytes every run.
"""

import os
import sys

ENTRY = "fix: reverted my 2am fix, which fixed the 1am fix that broke the midnight fix"

MIN_CHARS = 1
MAX_CHARS = 139


def check_entry(text):
    """Gate: UTF-8 text, 1-139 characters, a single non-blank line."""
    if not isinstance(text, str):
        return "entry is not text"
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return "entry is %d characters, must be %d-%d" % (
            len(text),
            MIN_CHARS,
            MAX_CHARS,
        )
    if not text.strip():
        return "entry is only white space"
    if "\n" in text.rstrip("\n") or "\r" in text:
        return "entry must be a single line"
    return None


def main():
    problem = check_entry(ENTRY)
    if problem:
        print("invalid entry: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)

    # Read it back and verify the exact bytes we wrote.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != ENTRY:
        print("verify failed: entry.txt does not match the entry", file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(ENTRY), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
