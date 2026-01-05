# Liber Primus – Aggregated Results (Repo State)

This document consolidates what the current `tools/` work has already tested, what is confirmed solved, what repeatedly “almost works”, and what is currently blocking a clean page-by-page workflow.

## Canonical Facts (Confirmed)

- Alphabet: 29-rune Gematria Primus (`mod 29` arithmetic)
- Page 57: plaintext Parable (95 runes)
- Page 56: solved via prime-shift style method (per repo notes)
- Pages 0 and 54 (RuneSolver dataset): decrypt to the Parable with the derived master key

### Master Key (Confirmed)
Derived as:
- `K = (Page0 - Page57) mod 29`
- Decrypt as: `P = (C - K) mod 29`

Properties:
- Length: 95
- Sum of indices: 1331 (= 11^3)

## Data Sources and the Current Blocker

There are two competing page sources:

1) `EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/RuneSolver.py`
- Widely used by the existing scripts.
- **Problem**: `Page1 = ""` (empty), so Page 1 cannot be attacked with the older loaders.

2) `2014/Liber Primus/runes in text format.txt`
- Splitting on `%` yields **57 segments** (segment `i` maps cleanly to Page `i+1`).
- Segment 56 contains the Parable runes (Page 57).

### Alignment status between sources
Using [tools/align_page_sources.py](tools/align_page_sources.py):
- RuneSolver `Page0` best matches transcription segment index 53 (Page 54) by longest common prefix (LCP=45).
- Match is **not** perfect: transcription Page 54 rune-only length is 223 vs RuneSolver 232.

Interpretation:
- The sources likely differ by transcription omissions, page-boundary decisions, or included/excluded glyphs/markers.
- Until we standardize on one canonical loader, “page numbers” can silently drift.

## What’s Been Tried (and Outcomes)

### 1) Straight master-key application (Vigenère-like)
Tested extensively across pages using:
- operations: SUB / ADD / XOR
- rotations: 0..94
- offsets: 0..28

Outcome:
- Produces **word-like fragments** on some pages, but not readable text.
- XOR variants appear disproportionately often among best-scoring candidates.

### 2) Affine transforms of the key
Tested:
- `k'[i] = (a*k[i] + b) mod 29` for many/all `a,b`

Outcome:
- No consistent (a,b) pattern across pages.

### 3) Running-key and autokey variants
Tested:
- Parable as running key
- Autokey with master-key primer

Outcome:
- Scores stay low; no coherent plaintext.

### 4) Prime-shift methods
- Page 56 method works (per repo notes), but does not generalize cleanly to unsolved pages.

### 5) Transposition (before/after decrypt)
Tested:
- columnar, rail fence, spiral-ish permutations, reverse

Outcome:
- Some scoring improvements but no stable readable plaintext.

### 6) Multi-layer operations
Tested (coarse grids and targeted refinement):
- XOR→XOR, XOR→SUB, ADD→XOR, etc.

Outcome:
- Higher “English-word coverage” on certain pages.
- Example highlight (from repo summaries): Page 28 double XOR yields the highest word-coverage, but still not clean sentences.

### 7) Page-number-based formulas
Tested:
- rot/off as functions of page number (including `page`, `page+1`, `95-page`, `page*3`, `page*11`, etc.)

Outcome:
- Yields the highest heuristic scores (e.g., Page 47 scoring ~102 in repo notes), but still not readable.

## Page 1: Now Attackable via Transcription Source

A new harness [tools/page1_attack.py](tools/page1_attack.py) extracts Page 1 from `runes in text format.txt` (split on `%`) and runs the standard single-layer search:
- op ∈ {SUB, XOR, ADD}
- rot ∈ [0..94]
- off ∈ [0..28]

Results written to:
- [tools/PAGE1_RESULTS.md](tools/PAGE1_RESULTS.md)
- [tools/PAGE1_PLAYBOOK.md](tools/PAGE1_PLAYBOOK.md)

**⚠️ MAJOR UPDATE (Jan 2026): Master key length 95 assumption was WRONG for Page 1**

### Breakthrough: Key Length 71 with XOR

Index of Coincidence analysis revealed Page 1's true key length is **71, not 95**.

Current best result:
- Tool: [tools/page1_key71_attack.py](tools/page1_key71_attack.py)
- Method: XOR with optimized key length 71
- Score: 801.50 (massive improvement from ~60 under old assumptions)
- Output: [tools/PAGE1_KEY71_RESULTS.txt](tools/PAGE1_KEY71_RESULTS.txt)
- Strong English signal: "THE" appears 41 times, "ATH" 21 times, common bigrams present
- Status: **Partially readable but fragmented** - suggests possible secondary layer or non-standard plaintext structure

Supporting tools:
- [tools/ioc_analysis_page1.py](tools/ioc_analysis_page1.py): IoC peaks at 71, 93, 138 (NOT 95)
- [tools/page1_alternative_keylength.py](tools/page1_alternative_keylength.py): tested IoC-suggested lengths
- [tools/page1_two_layer_final.py](tools/page1_two_layer_final.py): tested transpositions on XOR-71 output; no improvement
- [tools/extract_patterns_xor71.py](tools/extract_patterns_xor71.py): pattern analysis suggests possible interleaving

### What this means for the repo's approach:

1. **The master key (length 95) does NOT apply uniformly to all pages**
2. Different pages may use different key lengths (71, 93, 102, etc.)
3. IoC analysis should be run on each unsolved page individually
4. The "previous page gives key to next page" hypothesis needs revision

### Older Page 1 experiments (pre-breakthrough, likely incorrect):

- [tools/page1_attack.py](tools/page1_attack.py): master-key-95 variants with LM scoring
- [tools/PAGE1_RESULTS.md](tools/PAGE1_RESULTS.md): results from key-95 assumption
- [tools/page1_chain_attack.py](tools/page1_chain_attack.py): chaining hypothesis test
- [tools/page1_two_layer_attack.py](tools/page1_two_layer_attack.py): constant second-layer with key-95
- [tools/page1_shortkey_secondlayer.py](tools/page1_shortkey_secondlayer.py): repeating-key second layer with key-95

## What This Suggests (High-level)

Based on the repo’s own evidence:
- It is **unlikely** the book is solved by a simple “Page N gives exact key for Page N+1” rule in a single consistent cipher.
- It is **plausible** pages share a *family* of related keys (rotations/offsets/derived transforms) while also requiring:
  - an additional preprocessing layer (re-ordering / stripping / formatting), and/or
  - a second crypto layer (multi-step XOR/SUB style), and/or
  - non-English plaintext (or plaintext in a constrained vocabulary).

## Recommended Next Steps (Practical)

1) Standardize page loading
- Decide whether we treat the transcription file as canonical for analysis, and build a shared loader for tools.

2) Reconcile page boundary mismatch
- Identify exactly what rune(s) are missing/extra between RuneSolver Page0/54 and transcription Page 54.
- Once aligned, we can safely “reuse” older scripts on Page 1 without dataset drift.

3) Push Page 1 beyond the single-layer search
- Run the same multi-layer grid used on Page 28/44/52 against Page 1.
- Consider scoring not just by word hits, but by language-model-ish constraints (digraph/trigraph distribution) or dictionary coverage.

4) Re-test the “page-by-page” hypothesis with evidence
- If you want “Page N implies key schedule for Page N+1”, we should define a measurable claim (e.g., `K_{n+1} = rotate(K_n, f(n)) + g(n)`), then fit `f,g` against several pages that show strong partial English under rotated keys.
