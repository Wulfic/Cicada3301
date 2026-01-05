#!/usr/bin/env python3
"""Page 1 -> Page 2 chaining experiment.

Goal
----
Test the hypothesis: "previous page provides a clue/key for the next page".

We already have a 1-layer search for Page 1 (`tools/page1_attack.py`) that
tries master-key variants (rot/off) and simple ops (SUB/XOR/ADD), but the
scoring can be gamed by repetitive 'THE'.

This script:
1) Re-runs the same Page 1 search space.
2) Re-scores candidates with a slightly more conservative scorer.
3) For the best Page 1 candidates, tries a *running-key* decrypt of Page 2
   using the Page 1 candidate plaintext indices as the key stream.

If any Page 1 candidate is "real", it should tend to make Page 2 look *more*
English-like under a reasonable chaining rule.

Dataset
-------
Uses `2014/Liber Primus/runes in text format.txt` split on `%`.
Segment 0 => Page 1, segment 1 => Page 2.

Outputs
-------
Prints a ranked shortlist with (score_page1, score_page2, combined).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
from typing import List, Tuple


RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_IDX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F",
    "U",
    "TH",
    "O",
    "R",
    "C",
    "G",
    "W",
    "H",
    "N",
    "I",
    "J",
    "EO",
    "P",
    "X",
    "S",
    "T",
    "B",
    "E",
    "M",
    "L",
    "NG",
    "OE",
    "D",
    "A",
    "AE",
    "Y",
    "IA",
    "EA",
]

TOKEN_TO_CHAR = {
    "F": "F",
    "U": "U",
    "TH": "T",
    "O": "O",
    "R": "R",
    "C": "C",
    "G": "G",
    "W": "W",
    "H": "H",
    "N": "N",
    "I": "I",
    "J": "J",
    "EO": "E",
    "P": "P",
    "X": "X",
    "S": "S",
    "T": "T",
    "B": "B",
    "E": "E",
    "M": "M",
    "L": "L",
    "NG": "N",
    "OE": "O",
    "D": "D",
    "A": "A",
    "AE": "A",
    "Y": "Y",
    "IA": "I",
    "EA": "E",
}


MASTER_KEY: List[int] = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23,
]


COMMON_WORDS = {
    # ultra-common
    "THE",
    "AND",
    "THAT",
    "THIS",
    "WITH",
    "FROM",
    "FOR",
    "NOT",
    "ARE",
    "YOU",
    "WE",
    "OUR",
    "OWN",
    "WILL",
    "THERE",
    "THEY",
    "HAVE",
    "HAS",
    "HAD",
    "BE",
    "IN",
    "ON",
    "TO",
    "OF",
    "AS",
    # cicada-ish
    "INSTAR",
    "PARABLE",
    "DIVINITY",
    "EMERGE",
    "SURFACE",
    "CIRCUMFERENCES",
    "CICADA",
    "LIBER",
    "PRIMUS",
    "TRUTH",
    "WISDOM",
}


@dataclass(frozen=True)
class PageData:
    page_num: int
    raw: str
    cipher_idx: List[int]


@dataclass(frozen=True)
class Candidate:
    score1: float
    score2: float
    combined: float
    op: str
    chain_op: str
    rot: int
    off: int
    preview1: str
    preview2: str


def load_pages_from_runes_file(path: Path) -> List[PageData]:
    text = path.read_text(encoding="utf-8")
    segments = text.split("%")

    pages: List[PageData] = []
    for i, seg in enumerate(segments):
        cipher_idx = [RUNE_TO_IDX[c] for c in seg if c in RUNE_TO_IDX]
        if not cipher_idx:
            continue
        pages.append(PageData(page_num=i + 1, raw=seg, cipher_idx=cipher_idx))

    return pages


def roll_key(key: List[int], rot: int) -> List[int]:
    rot = rot % len(key)
    if rot == 0:
        return list(key)
    return key[-rot:] + key[:-rot]


def extend_key(key: List[int], length: int) -> List[int]:
    out = [0] * length
    n = len(key)
    for i in range(length):
        out[i] = key[i % n]
    return out


def apply_op(c: int, k: int, op: str) -> int:
    if op == "SUB":
        return (c - k) % 29
    if op == "ADD":
        return (c + k) % 29
    if op == "XOR":
        return (c ^ k) % 29
    raise ValueError(f"unknown op: {op}")


def render_with_formatting(raw: str, plaintext_idx: List[int]) -> str:
    out: List[str] = []
    rune_pos = 0

    for ch in raw:
        if ch in RUNE_TO_IDX:
            if rune_pos >= len(plaintext_idx):
                break
            out.append(LETTERS[plaintext_idx[rune_pos] % 29])
            rune_pos += 1
            continue

        if ch == "-":
            out.append(" ")
        elif ch == "/":
            out.append("\n")
        elif ch == ".":
            out.append(". ")
        else:
            out.append(ch)

    return "".join(out)


def compact_preview(text: str, n: int = 160) -> str:
    t = text.replace("\n", " ")
    t = " ".join(t.split())
    return t[:n]


def to_ascii_stream(rendered: str) -> str:
    # Pull out our rune tokens and map them to a single-letter-ish stream.
    # This makes frequency scoring less exploitable by TH/EO etc.
    out: List[str] = []
    i = 0
    while i < len(rendered):
        # tokens include "TH", "EO", "NG", "OE", "AE", "IA", "EA" or single letters.
        if rendered[i].isalpha():
            # Try digraph tokens first
            if i + 1 < len(rendered):
                two = rendered[i : i + 2]
                if two in TOKEN_TO_CHAR:
                    out.append(TOKEN_TO_CHAR[two])
                    i += 2
                    continue
            one = rendered[i]
            if one in TOKEN_TO_CHAR:
                out.append(TOKEN_TO_CHAR[one])
        i += 1
    return "".join(out)


ENGLISH_FREQ = {
    "E": 0.127,
    "T": 0.091,
    "A": 0.082,
    "O": 0.075,
    "I": 0.070,
    "N": 0.067,
    "S": 0.063,
    "H": 0.061,
    "R": 0.060,
    "D": 0.043,
    "L": 0.040,
    "U": 0.028,
    "W": 0.024,
    "M": 0.024,
    "F": 0.022,
    "C": 0.022,
    "G": 0.020,
    "Y": 0.020,
    "P": 0.019,
    "B": 0.015,
    "V": 0.010,
    "K": 0.008,
    "J": 0.002,
    "X": 0.002,
    "Q": 0.001,
    "Z": 0.001,
}


def chi2_english(ascii_stream: str) -> float:
    # lower is better
    if not ascii_stream:
        return 1e9
    total = len(ascii_stream)
    counts = {ch: 0 for ch in ENGLISH_FREQ}
    for ch in ascii_stream:
        if ch in counts:
            counts[ch] += 1
    chi2 = 0.0
    for ch, exp in ENGLISH_FREQ.items():
        expected = exp * total
        if expected <= 0:
            continue
        diff = counts[ch] - expected
        chi2 += (diff * diff) / expected
    return chi2


def score_text(rendered: str) -> float:
    t = rendered.upper()

    # Dictionary-ish hits, but cap the contribution per word to reduce "THE" spam.
    word_score = 0.0
    for w in COMMON_WORDS:
        c = t.count(w)
        if not c:
            continue
        capped = min(c, 6)
        word_score += capped * (len(w) ** 1.1)

    # N-gram boosters
    ng = 0.0
    for bg in ("TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND", "OU", "EA"):
        ng += 0.6 * t.count(bg)
    for tg in ("THE", "AND", "ING", "ION", "ENT", "FOR", "THA", "ERE", "HAT"):
        ng += 1.0 * t.count(tg)

    # Penalty for extreme repetition (a typical failure mode)
    the_count = t.count("THE")
    rep_penalty = 0.0
    if the_count > 40:
        rep_penalty += (the_count - 40) * 0.8

    ascii_stream = to_ascii_stream(rendered)
    chi2 = chi2_english(ascii_stream)

    # Convert chi2 to a positive score (higher is better)
    freq_score = 120.0 / (1.0 + chi2)

    return word_score + ng + freq_score - rep_penalty


def decrypt_master_variant(cipher_idx: List[int], op: str, rot: int, off: int) -> List[int]:
    base_key = roll_key(MASTER_KEY, rot)
    final_key = [(k + off) % 29 for k in base_key]
    extended = extend_key(final_key, len(cipher_idx))
    return [apply_op(c, extended[i], op) for i, c in enumerate(cipher_idx)]


def decrypt_running_key(cipher_idx: List[int], key_stream: List[int], chain_op: str) -> List[int]:
    # Simple running-key model with selectable combine op.
    # Treat key_stream as the per-position key indices.
    extended = extend_key(key_stream, len(cipher_idx))
    if chain_op == "SUB":
        return [(c - extended[i]) % 29 for i, c in enumerate(cipher_idx)]
    if chain_op == "ADD":
        return [(c + extended[i]) % 29 for i, c in enumerate(cipher_idx)]
    if chain_op == "XOR":
        return [(c ^ extended[i]) % 29 for i, c in enumerate(cipher_idx)]
    raise ValueError(f"unknown chain_op: {chain_op}")


def null_baseline_scores(cipher_idx: List[int], trials: int, chain_op: str, seed: int = 1337) -> List[float]:
    rng = random.Random(seed)
    scores: List[float] = []
    for _ in range(trials):
        key_stream = [rng.randrange(29) for _ in range(95)]
        p_idx = decrypt_running_key(cipher_idx, key_stream, chain_op=chain_op)
        rendered = render_with_formatting(page2_raw_for_scoring, p_idx)
        scores.append(score_text(rendered))
    scores.sort(reverse=True)
    return scores


def main() -> None:
    pages = load_pages_from_runes_file(Path("2014/Liber Primus/runes in text format.txt"))
    page1 = next((p for p in pages if p.page_num == 1), None)
    page2 = next((p for p in pages if p.page_num == 2), None)
    if page1 is None or page2 is None:
        raise SystemExit("Could not locate Page 1/2")

    # Used by null_baseline_scores without threading raw through all calls.
    global page2_raw_for_scoring
    page2_raw_for_scoring = page2.raw

    # Phase 1: score all Page 1 master-key variants, keep top N
    scored: List[Tuple[float, str, int, int, List[int], str]] = []
    for op in ("SUB", "XOR", "ADD"):
        for rot in range(95):
            for off in range(29):
                p1_idx = decrypt_master_variant(page1.cipher_idx, op=op, rot=rot, off=off)
                r1 = render_with_formatting(page1.raw, p1_idx)
                s1 = score_text(r1)
                scored.append((s1, op, rot, off, p1_idx, r1))

    scored.sort(key=lambda x: x[0], reverse=True)
    top1 = scored[:60]

    # Phase 2: chaining test into Page 2
    candidates: List[Candidate] = []
    for s1, op, rot, off, p1_idx, r1 in top1:
        for chain_op in ("SUB", "ADD", "XOR"):
            p2_idx = decrypt_running_key(page2.cipher_idx, p1_idx, chain_op=chain_op)
            r2 = render_with_formatting(page2.raw, p2_idx)
            s2 = score_text(r2)

            combined = s1 + 0.85 * s2
            candidates.append(
                Candidate(
                    score1=s1,
                    score2=s2,
                    combined=combined,
                    op=op,
                    chain_op=chain_op,
                    rot=rot,
                    off=off,
                    preview1=compact_preview(r1),
                    preview2=compact_preview(r2),
                )
            )

    candidates.sort(key=lambda c: c.combined, reverse=True)

    print("=" * 90)
    print("PAGE 1 -> PAGE 2 CHAINING RESULTS")
    print("=" * 90)
    print("Top candidates where Page 1 (master-key variant) also makes Page 2 look good under a running key")
    print()

    # Null baseline: how good can Page 2 look with a random key stream?
    # This helps detect whether our "best" results are just scorer noise.
    print("Null baseline (random 95-length key stream; 400 trials):")
    for chain_op in ("SUB", "ADD", "XOR"):
        base = null_baseline_scores(page2.cipher_idx, trials=400, chain_op=chain_op)
        p95 = base[int(0.05 * len(base))]
        p99 = base[int(0.01 * len(base))]
        best = base[0]
        print(f"  chain_op={chain_op}: best={best:6.2f}  ~99%={p99:6.2f}  ~95%={p95:6.2f}")
    print()

    for i, c in enumerate(candidates[:15], start=1):
        print(
            f"#{i:02d} combined={c.combined:7.2f}  p1={c.score1:7.2f}  p2={c.score2:7.2f}  "
            f"op={c.op:>3} rot={c.rot:02d} off={c.off:02d}  chain={c.chain_op}"
        )
        print(f"  P1: {c.preview1}")
        print(f"  P2: {c.preview2}")
        print()


if __name__ == "__main__":
    main()
