#!/usr/bin/env python3
"""Align Liber Primus page sources.

Problem
-------
We currently have two competing sources of page text:

1) `EXTRA WIKI PAGES/.../RuneSolver.py` (used by many scripts)
   - in this repo, `Page1` is empty

2) `2014/Liber Primus/runes in text format.txt` (canonical transcription)
   - appears to contain 57 pages when split on `%` (segment i => page i+1)

We observed partial matches (e.g., first ~20 runes) but mismatches beyond that.
This script quantifies which transcription segment best matches a given
RuneSolver page by comparing rune-only streams.

What it does
------------
- Loads RuneSolver.py dynamically (no import path required)
- Extracts rune indices from a selected RuneSolver page (default Page0)
- Extracts rune indices for each `%` segment in the transcription
- Reports top matches by:
  - longest common prefix length
  - Hamming matches across aligned prefix (count of equal runes)

Usage
-----
`python tools/align_page_sources.py`  (defaults to RuneSolver Page0)
`python tools/align_page_sources.py 54`

This is a diagnostic tool; it doesn't modify any datasets.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}


@dataclass(frozen=True)
class Match:
    segment_index: int
    page_num: int
    seg_len: int
    page_len: int
    lcp: int
    aligned_matches: int
    aligned_len: int


def extract_rune_indices(text: str) -> List[int]:
    return [RUNE_TO_IDX[c] for c in text if c in RUNE_TO_IDX]


def load_runes_transcription_segments(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8")
    return text.split("%")


def load_runesolver_pages(runesolver_path: Path) -> Dict[int, str]:
    """Load PageNN assignments from RuneSolver.py *without executing it*.

    RuneSolver.py is interactive on import/run. We avoid that by parsing the file
    as Python syntax and extracting constant string assignments.
    """

    code = runesolver_path.read_text(encoding="utf-8")
    tree = ast.parse(code, filename=str(runesolver_path))

    pages: Dict[int, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        name = target.id
        if not name.startswith("Page"):
            continue
        suffix = name[4:]
        if not suffix.isdigit():
            continue

        try:
            value = ast.literal_eval(node.value)
        except Exception:
            continue
        if isinstance(value, str):
            pages[int(suffix)] = value

    return pages


def longest_common_prefix(a: List[int], b: List[int]) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


def aligned_match_count(a: List[int], b: List[int]) -> Tuple[int, int]:
    n = min(len(a), len(b))
    matches = sum(1 for i in range(n) if a[i] == b[i])
    return matches, n


def main() -> None:
    page_num = 0
    if len(sys.argv) >= 2:
        try:
            page_num = int(sys.argv[1])
        except ValueError:
            raise SystemExit("Usage: python tools/align_page_sources.py [page_num]")

    runesolver_path = Path(
        "EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/RuneSolver.py"
    )
    transcription_path = Path("2014/Liber Primus/runes in text format.txt")

    if not runesolver_path.exists():
        raise SystemExit(f"Missing: {runesolver_path}")
    if not transcription_path.exists():
        raise SystemExit(f"Missing: {transcription_path}")

    pages = load_runesolver_pages(runesolver_path)
    if page_num not in pages:
        available = ", ".join(str(n) for n in sorted(pages.keys())[:15])
        raise SystemExit(
            f"RuneSolver page {page_num} not found. Example available: {available} ..."
        )

    page_text = pages[page_num]
    page_idx = extract_rune_indices(page_text)

    segments = load_runes_transcription_segments(transcription_path)

    matches: List[Match] = []
    for i, seg in enumerate(segments):
        seg_idx = extract_rune_indices(seg)
        if not seg_idx:
            continue
        lcp = longest_common_prefix(page_idx, seg_idx)
        aligned_matches, aligned_len = aligned_match_count(page_idx, seg_idx)
        matches.append(
            Match(
                segment_index=i,
                page_num=i + 1,
                seg_len=len(seg_idx),
                page_len=len(page_idx),
                lcp=lcp,
                aligned_matches=aligned_matches,
                aligned_len=aligned_len,
            )
        )

    matches.sort(key=lambda m: (m.lcp, m.aligned_matches), reverse=True)

    print(f"RuneSolver Page{page_num}: rune_len={len(page_idx)}")
    print(
        "Top matches vs transcription % segments (segment i => page i+1):\n"
        "rank  page  seg_idx  lcp  aligned_matches/aligned_len"
    )

    for rank, m in enumerate(matches[:15], start=1):
        print(
            f"{rank:>4}  {m.page_num:>4}  {m.segment_index:>6}  {m.lcp:>3}  "
            f"{m.aligned_matches:>4}/{m.aligned_len:<4} (seg_len={m.seg_len})"
        )


if __name__ == "__main__":
    main()
