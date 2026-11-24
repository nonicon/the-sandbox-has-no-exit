#!/usr/bin/env python3
"""The Sandbox Has No Exit — entry for make.fun's
"Funniest Excuse an Agent Gives for a Missed Deadline" bounty.

Writes one line (the excuse an AI agent gives for missing a deadline)
to entry.txt in MAKEFUN_OUTPUT_DIR (or /output). Deterministic, stdlib only.
"""

import os
import sys

ENTRY = (
    "The deliverable is complete, verified, and saved \u2014 it's just "
    "inside the sandbox, which I'm now given to understand has no exit."
)


def validate_entry(text: str) -> str:
    """Enforce the kit gate: UTF-8 text of 1-200 characters, single line,
    not only whitespace. Raises ValueError on anything the gate would refuse."""
    text.encode("utf-8")  # must be valid UTF-8
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry is {len(text)} chars, must be 1-200")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def output_path() -> str:
    """Honour MAKEFUN_OUTPUT_DIR first (falling back to legacy OUTPUT_DIR,
    then /output) so the grader's sandbox receives the entry."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = validate_entry(ENTRY.strip())
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: re-read and confirm the file holds exactly the entry.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise ValueError("round-trip mismatch: written entry differs")
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
