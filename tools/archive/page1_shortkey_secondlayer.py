#!/usr/bin/env python3
"""Page 1: second-layer *short repeating key* search.

What this does
--------------
1) Scores all one-layer master-key variants using the Parable-trained trigram LM.
2) Takes the top N seeds.
3) For each seed, applies a second layer using a repeating key of length 3:
   - chain_op ∈ {SUB, XOR}
   - key = (k0,k1,k2) with each ki ∈ [0..28]

Why
---
Constant second-layer offsets don't help. A very short repeating key is the next
cheapest plausible "extra layer" that still keeps search feasible.

Output
------
Writes tools/PAGE1_SHORTKEY_LAYER_RESULTS.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import itertools
import math
import re
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

MASTER_KEY: List[int] = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23,
]

COMMON_WORDS = {
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

IDX_TO_CHAR = [TOKEN_TO_CHAR[tok] for tok in LETTERS]


@dataclass(frozen=True)
class PageData:
    page_num: int
    raw: str
    cipher_idx: List[int]


@dataclass(frozen=True)
class Seed:
    score: float
    op1: str
    rot: int
    off: int
    idx: List[int]


@dataclass(frozen=True)
class Result:
    score: float
    op1: str
    rot: int
    off: int
    op2: str
    k0: int
    k1: int
    k2: int
    preview: str


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


def tokens_to_ascii_stream(rendered: str) -> str:
    out: List[str] = []
    i = 0
    while i < len(rendered):
        ch = rendered[i]
        if not ch.isalpha():
            i += 1
            continue

        if i + 1 < len(rendered):
            two = rendered[i : i + 2].upper()
            if two in TOKEN_TO_CHAR:
                out.append(TOKEN_TO_CHAR[two])
                i += 2
                continue

        one = ch.upper()
        if one in TOKEN_TO_CHAR:
            out.append(TOKEN_TO_CHAR[one])
        i += 1

    return "".join(out)


def indices_to_ascii_stream(idx: List[int]) -> str:
    # Fast path: score without re-rendering rune tokens.
    return "".join(IDX_TO_CHAR[x % 29] for x in idx)


class TrigramScorer:
    def __init__(self, training_stream: str, k: float = 0.25) -> None:
        training_stream = re.sub(r"[^A-Z]", "", training_stream.upper())
        if len(training_stream) < 50:
            raise ValueError("training stream too short")

        self.k = float(k)
        self.vocab = 26

        # Counts over 26 letters.
        self.bi_counts = [0] * (26 * 26)  # a*26 + b
        self.tri_counts = [0] * (26 * 26 * 26)  # a*26*26 + b*26 + c

        letters = [ord(c) - 65 for c in training_stream]
        for i in range(len(letters) - 1):
            a = letters[i]
            b = letters[i + 1]
            self.bi_counts[a * 26 + b] += 1
        for i in range(len(letters) - 2):
            a = letters[i]
            b = letters[i + 1]
            c = letters[i + 2]
            self.tri_counts[a * 26 * 26 + b * 26 + c] += 1

        # Precompute log-probabilities for every trigram.
        self.tri_logp = [0.0] * (26 * 26 * 26)
        for a in range(26):
            for b in range(26):
                den = self.bi_counts[a * 26 + b] + self.k * self.vocab
                base = a * 26 * 26 + b * 26
                for c in range(26):
                    num = self.tri_counts[base + c] + self.k
                    self.tri_logp[base + c] = math.log(num / den)

    def score_ints(self, letters: List[int]) -> float:
        if len(letters) < 3:
            return float("-inf")

        logp = 0.0
        n = 0
        for i in range(len(letters) - 2):
            a = letters[i]
            b = letters[i + 1]
            c = letters[i + 2]
            logp += self.tri_logp[a * 26 * 26 + b * 26 + c]
            n += 1
        return logp / max(n, 1)


def extract_page57_from_runesolver(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^Page57\s*=\s*\"([^\"]*)\"", text, flags=re.MULTILINE)
    if not m:
        raise ValueError("Could not find Page57 in RuneSolver.py")
    return m.group(1)


def parable_training_stream() -> str:
    solver_path = Path("EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/RuneSolver.py")
    page57 = extract_page57_from_runesolver(solver_path)

    out: List[str] = []
    for ch in page57:
        if ch in RUNE_TO_IDX:
            out.append(IDX_TO_CHAR[RUNE_TO_IDX[ch] % 29])
    return "".join(out)


def score_indices(idx: List[int], lm: TrigramScorer) -> float:
    # Inner-loop scorer: LM only for speed.
    letters = [ord(IDX_TO_CHAR[x % 29]) - 65 for x in idx]
    lm_score = lm.score_ints(letters)
    if lm_score == float("-inf"):
        return float("-inf")
    return lm_score * 120.0


def decrypt_master_variant(cipher_idx: List[int], op: str, rot: int, off: int) -> List[int]:
    base_key = roll_key(MASTER_KEY, rot)
    final_key = [(k + off) % 29 for k in base_key]
    extended = extend_key(final_key, len(cipher_idx))
    return [apply_op(c, extended[i], op) for i, c in enumerate(cipher_idx)]


def compact_preview(text: str, n: int = 180) -> str:
    t = text.replace("\n", " ")
    t = " ".join(t.split())
    return t[:n]


def apply_shortkey_layer(idx: List[int], op2: str, key3: Tuple[int, int, int]) -> List[int]:
    k0, k1, k2 = key3
    out = [0] * len(idx)
    for i, x in enumerate(idx):
        k = (k0, k1, k2)[i % 3]
        out[i] = apply_op(x, k, op2)
    return out


def main() -> None:
    lm = TrigramScorer(parable_training_stream())

    pages = load_pages_from_runes_file(Path("2014/Liber Primus/runes in text format.txt"))
    page1 = next((p for p in pages if p.page_num == 1), None)
    if page1 is None:
        raise SystemExit("Could not locate Page 1")

    seeds: List[Seed] = []
    for op1 in ("SUB", "XOR", "ADD"):
        for rot in range(95):
            for off in range(29):
                idx = decrypt_master_variant(page1.cipher_idx, op=op1, rot=rot, off=off)
                s = score_indices(idx, lm)
                seeds.append(Seed(score=s, op1=op1, rot=rot, off=off, idx=idx))

    seeds.sort(key=lambda s: s.score, reverse=True)
    seeds = seeds[:10]

    results: List[Result] = []

    keys = list(itertools.product(range(29), repeat=3))
    for seed in seeds:
        for op2 in ("SUB", "XOR"):
            best_for_seed: Result | None = None
            for k0, k1, k2 in keys:
                idx2 = apply_shortkey_layer(seed.idx, op2=op2, key3=(k0, k1, k2))
                s = score_indices(idx2, lm)
                if best_for_seed is None or s > best_for_seed.score:
                    best_for_seed = Result(
                        score=s,
                        op1=seed.op1,
                        rot=seed.rot,
                        off=seed.off,
                        op2=op2,
                        k0=k0,
                        k1=k1,
                        k2=k2,
                        preview="",
                    )

            if best_for_seed is not None:
                results.append(best_for_seed)

    # Build previews only for the best results.
    results.sort(key=lambda r: r.score, reverse=True)
    results = results[:25]
    with_previews: List[Result] = []
    for r in results:
        seed = next(
            (s for s in seeds if s.op1 == r.op1 and s.rot == r.rot and s.off == r.off),
            None,
        )
        if seed is None:
            continue
        idx2 = apply_shortkey_layer(seed.idx, op2=r.op2, key3=(r.k0, r.k1, r.k2))
        rendered = render_with_formatting(page1.raw, idx2)
        with_previews.append(
            Result(
                score=r.score,
                op1=r.op1,
                rot=r.rot,
                off=r.off,
                op2=r.op2,
                k0=r.k0,
                k1=r.k1,
                k2=r.k2,
                preview=compact_preview(rendered),
            )
        )

    results = with_previews
    out_path = Path("tools/PAGE1_SHORTKEY_LAYER_RESULTS.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        f.write("# Page 1: Short-key Second Layer (len=3)\n\n")
        f.write("Seeds: top 10 one-layer master-key variants (LM-scored)\n\n")
        f.write("Second layer: op2 ∈ {SUB, XOR}, repeating key length 3 (k0,k1,k2)\n\n")
        f.write("| Rank | Score | Op1 | Rot | Off | Op2 | k0 | k1 | k2 | Preview |\n")
        f.write("|---:|---:|---|---:|---:|---|---:|---:|---:|---|\n")
        for i, r in enumerate(results[:20], start=1):
            prev = r.preview.replace("|", "\\|")
            f.write(
                f"| {i} | {r.score:.2f} | {r.op1} | {r.rot} | {r.off} | {r.op2} | {r.k0} | {r.k1} | {r.k2} | {prev} |\n"
            )

    print(f"Wrote: {out_path}")
    if results:
        print(f"Top: {results[0]}")


if __name__ == "__main__":
    main()
