#!/usr/bin/env python3
"""Page 1 attack harness (Liber Primus)

Context
-------
Many scripts in `tools/` load Liber Primus pages from
`EXTRA WIKI PAGES/.../RuneSolver.py`, but in this repo that dataset has
`Page1 = ""` (empty), which blocks Page 1 analysis.

This script treats `2014/Liber Primus/runes in text format.txt` as the
canonical per-page stream:
- split on `%`
- map segment index i -> Page (i+1)

It then runs a focused one-layer search using the known master key (length 95)
with the same families that have produced the best partial English fragments in
other tooling:
- op ∈ {SUB, XOR, ADD}
- key = roll(master_key, rot)
- key_final[i] = (key[i] + off) mod 29

Output
------
Writes `tools/PAGE1_RESULTS.md` with top candidates plus full text for top 5.

Note: This does not assume Page 1 *must* use the master key; it's a pragmatic
first pass consistent with the repo’s existing brute-force results.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import re
from typing import Iterable, List


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


# Master key as described/verified in existing repo docs:
# derived from (Page0 - Page57) mod 29, length 95, sum 1331.
MASTER_KEY: List[int] = [
	11,
	24,
	17,
	28,
	10,
	11,
	25,
	19,
	9,
	22,
	5,
	11,
	3,
	20,
	27,
	9,
	3,
	21,
	20,
	5,
	20,
	22,
	18,
	18,
	24,
	16,
	23,
	2,
	23,
	24,
	10,
	5,
	28,
	19,
	15,
	19,
	0,
	25,
	27,
	17,
	2,
	14,
	10,
	15,
	8,
	22,
	8,
	8,
	27,
	14,
	2,
	2,
	19,
	0,
	18,
	14,
	28,
	2,
	11,
	14,
	5,
	3,
	19,
	8,
	16,
	11,
	9,
	5,
	1,
	21,
	9,
	9,
	9,
	5,
	0,
	19,
	25,
	28,
	7,
	14,
	14,
	7,
	14,
	3,
	26,
	18,
	24,
	23,
	19,
	8,
	4,
	9,
	16,
	7,
	23,
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
	score: float
	op: str
	rot: int
	off: int
	preview: str


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


def tokens_to_ascii_stream(rendered: str) -> str:
	"""Convert rendered rune-token text to a compact A-Z stream.

	We map multi-letter rune tokens like TH/EO/NG/... down to single characters.
	This reduces scoring artifacts from digraph tokens.
	"""
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


class TrigramScorer:
	"""Simple trigram LM scorer with add-k smoothing.

	Trained on the Parable plaintext (Page57) extracted from RuneSolver.py.
	Scores are higher when the text looks closer to the Parable/English distribution.
	"""

	def __init__(self, training_stream: str, k: float = 0.25) -> None:
		training_stream = re.sub(r"[^A-Z]", "", training_stream.upper())
		if len(training_stream) < 50:
			raise ValueError("training stream too short")

		self.k = float(k)
		self.vocab = 26
		self.bi: dict[str, int] = {}
		self.tri: dict[str, int] = {}

		for i in range(len(training_stream) - 1):
			bg = training_stream[i : i + 2]
			self.bi[bg] = self.bi.get(bg, 0) + 1
		for i in range(len(training_stream) - 2):
			tg = training_stream[i : i + 3]
			self.tri[tg] = self.tri.get(tg, 0) + 1

	def score(self, stream: str) -> float:
		stream = re.sub(r"[^A-Z]", "", stream.upper())
		if len(stream) < 3:
			return float("-inf")

		logp = 0.0
		n = 0
		for i in range(len(stream) - 2):
			bg = stream[i : i + 2]
			tg = stream[i : i + 3]
			num = self.tri.get(tg, 0) + self.k
			den = self.bi.get(bg, 0) + self.k * self.vocab
			logp += math.log(num / den)
			n += 1

		# Return average log-probability (higher is better)
		return logp / max(n, 1)


def extract_page57_from_runesolver(path: Path) -> str:
	text = path.read_text(encoding="utf-8", errors="replace")
	# In this repo RuneSolver.py stores Page57 on one line.
	m = re.search(r"^Page57\s*=\s*\"([^\"]*)\"", text, flags=re.MULTILINE)
	if not m:
		raise ValueError("Could not find Page57 in RuneSolver.py")
	return m.group(1)


def parable_training_stream() -> str:
	# Extract Page57 runes from RuneSolver.py and map them to an A-Z stream.
	solver_path = Path(
		"EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/RuneSolver.py"
	)
	page57 = extract_page57_from_runesolver(solver_path)

	# Convert rune chars to our LETTERS tokens, preserving separators roughly.
	out: List[str] = []
	for ch in page57:
		if ch in RUNE_TO_IDX:
			out.append(LETTERS[RUNE_TO_IDX[ch] % 29])
		elif ch in ("•", ":", ".", "\n"):
			out.append(" ")
		else:
			out.append(" ")
	return tokens_to_ascii_stream("".join(out))


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
	if not key:
		raise ValueError("key is empty")
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
	"""Reinsert plaintext tokens into original formatting.

	Formatting conventions in this repo's transcription:
	- rune chars -> emit plaintext token
	- '-' -> space
	- '/' -> newline
	- '.' -> '. '
	- '\n' preserved
	- other chars kept
	"""

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


def score_text(text: str, lm: TrigramScorer) -> float:
	"""Score candidate plaintext.

	Primary signal: trigram LM trained on the Parable plaintext stream.
	Secondary signal: small capped bonus for key Cicada words.
	"""
	t = text.upper()
	word_bonus = 0.0
	for w in COMMON_WORDS:
		c = t.count(w)
		if not c:
			continue
		word_bonus += min(c, 6) * (len(w) ** 1.05)

	ascii_stream = tokens_to_ascii_stream(t)
	lm_score = lm.score(ascii_stream)
	if lm_score == float("-inf"):
		return float("-inf")

	# lm_score is average log-prob (negative). Scale to a readable range.
	return (lm_score * 120.0) + (word_bonus * 0.8)


def decrypt_page(cipher_idx: List[int], op: str, rot: int, off: int) -> List[int]:
	base_key = roll_key(MASTER_KEY, rot)
	final_key = [(k + off) % 29 for k in base_key]
	extended = extend_key(final_key, len(cipher_idx))
	return [apply_op(c, extended[i], op) for i, c in enumerate(cipher_idx)]


def main() -> None:
	lm = TrigramScorer(parable_training_stream())

	runes_path = Path("2014/Liber Primus/runes in text format.txt")
	pages = load_pages_from_runes_file(runes_path)
	page1 = next((p for p in pages if p.page_num == 1), None)
	if page1 is None:
		raise SystemExit("Could not locate Page 1 in runes-in-text-format dataset")

	candidates: List[Candidate] = []

	for op in ("SUB", "XOR", "ADD"):
		for rot in range(95):
			for off in range(29):
				plain_idx = decrypt_page(page1.cipher_idx, op=op, rot=rot, off=off)
				rendered = render_with_formatting(page1.raw, plain_idx)
				s = score_text(rendered, lm=lm)

				preview = rendered.replace("\n", " ")
				preview = " ".join(preview.split())
				preview = preview[:180]
				candidates.append(
					Candidate(score=s, op=op, rot=rot, off=off, preview=preview)
				)

	candidates.sort(key=lambda c: c.score, reverse=True)
	top = candidates[:40]

	out_path = Path("tools/PAGE1_RESULTS.md")
	out_path.parent.mkdir(parents=True, exist_ok=True)

	with out_path.open("w", encoding="utf-8") as f:
		f.write("# Page 1 Decryption Candidates\n\n")
		f.write(
			"Source: `2014/Liber Primus/runes in text format.txt` split on `%` (segment 0 => Page 1)\n\n"
		)
		f.write(
			"Test space: op ∈ {SUB, XOR, ADD}, rot ∈ [0..94], off ∈ [0..28] using master key\n\n"
		)

		f.write("## Top Candidates (by heuristic score)\n\n")
		f.write("| Rank | Score | Op | Rot | Off | Preview |\n")
		f.write("|---:|---:|---|---:|---:|---|\n")
		for i, c in enumerate(top, start=1):
			prev = c.preview.replace("|", "\\|")
			f.write(f"| {i} | {c.score:.2f} | {c.op} | {c.rot} | {c.off} | {prev} |\n")

		f.write("\n## Full Text For Top 5\n")
		for i, c in enumerate(top[:5], start=1):
			plain_idx = decrypt_page(page1.cipher_idx, op=c.op, rot=c.rot, off=c.off)
			rendered = render_with_formatting(page1.raw, plain_idx)
			f.write(
				f"\n### #{i}: score={c.score:.2f}, op={c.op}, rot={c.rot}, off={c.off}\n\n"
			)
			f.write("```\n")
			f.write(rendered.strip() + "\n")
			f.write("```\n")

	print(f"Wrote: {out_path}")
	if top:
		print(f"Top candidate: {top[0]}")


if __name__ == "__main__":
	main()