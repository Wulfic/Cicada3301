# Page 1 – Attack Playbook (Current Repo State)

This is a practical, evidence-driven checklist for iterating on Liber Primus Page 1 in this workspace.

**📖 For detailed breakthrough findings, see: [PAGE1_BREAKTHROUGH_SUMMARY.md](PAGE1_BREAKTHROUGH_SUMMARY.md)**

## 0) Use the right source

- Canonical Page 1 for tooling: `2014/Liber Primus/runes in text format.txt`
- Split delimiter: `%`
- Segment mapping: segment 0 => Page 1, segment 1 => Page 2, …, segment 56 => Page 57 (Parable)

Why: `RuneSolver.py` in this repo has `Page1 = ""` and cannot be used for Page 1 ciphertext.

## 1) Baseline: single-layer master-key variants

Run:
- `C:/Users/tyler/Repos/Cicada3301/.venv/Scripts/python.exe tools/page1_attack.py`

What it does:
- op ∈ {SUB, XOR, ADD}
- rot ∈ [0..94] (master key rotation)
- off ∈ [0..28] (constant offset added to each key element)

Scoring:
- Trigram language model trained from RuneSolver Page57 (the known Parable plaintext), plus a small capped keyword bonus.

Output:
- `tools/PAGE1_RESULTS.md`

Interpretation:
- Treat the top 10 as “seeds”, not solutions.
- If output is still token soup but repeatedly contains Parable-shaped fragments, that suggests the key family is relevant but an additional layer exists.

## 2) Test the “Page N gives key for Page N+1” hypothesis (lightweight)

Run:
- `C:/Users/tyler/Repos/Cicada3301/.venv/Scripts/python.exe tools/page1_chain_attack.py`

What it tests:
- Takes top Page 1 candidates and uses them as a running-key stream to decrypt Page 2.
- Includes a random-key null baseline so we can see whether “good Page 2” results are meaningful.

Current conclusion:
- No chaining rule tested (SUB/ADD/XOR) beats the random-key baseline, so there’s no evidence yet for a naïve “Page1 plaintext directly decrypts Page2” relationship.

## 3) Cheap second-layer check: constant mask

Run:
- `C:/Users/tyler/Repos/Cicada3301/.venv/Scripts/python.exe tools/page1_two_layer_attack.py`

What it tests:
- Second layer op2 ∈ {SUB, ADD, XOR} with constant k2 ∈ [0..28]

Current conclusion:
- No meaningful improvement vs k2=0; constant second layer is likely not the missing piece.

## 4) (Optional) Second-layer check: very short repeating key (len=3)

Run:
- `C:/Users/tyler/Repos/Cicada3301/.venv/Scripts/python.exe tools/page1_shortkey_secondlayer.py`

Current conclusion:
- The best len=3 repeating-key second layers score worse (LM-wise) than the best single-layer seeds.

## 5) Next experiments (highest value)

If we keep the “Page 1 uses master-key family” assumption:
- Expand to *structured* two-layer searches around the best seeds (not global brute force):
  - e.g., apply a second Vigenère-like key derived from Parable word positions, gematria, or page metadata.
- Verify transcription fidelity for Page 1 (compare rune counts and punctuation markers across sources); a single missing rune can destroy polyalphabetic decryptability.

If we drop the “master key applies to Page 1” assumption:
- Treat Page 1 as a fresh cipher instance:
  - estimate key length(s) by IoC on rune indices and on word-length-normalized streams
  - test alternative alphabets/mappings (CK vs C, J rune icon differences) only if mismatches are proven.

## 6) **BREAKTHROUGH: Key length 71 with XOR (Jan 2026)**

**What changed:**
- Index of Coincidence analysis revealed Page 1's IoC peaks at key length **71**, NOT 95
- The master key (length 95) assumption was incorrect for Page 1

**Current best result:**
- Run: `C:/Users/tyler/Repos/Cicada3301/.venv/Scripts/python.exe tools/page1_key71_attack.py`
- Key length: 71
- Operation: XOR
- Score: 801.50 (vs ~60 before)
- Output shows heavy English structure: frequent "THE", "OF", "AND", "WITH", "ING"
- Results in: `tools/PAGE1_KEY71_RESULTS.txt`

**Remaining issue:**
- Text is fragmented/interleaved, suggesting a **secondary layer** (likely transposition)
- Columnar transposition analysis showed width=3 improves readability
- Bigram analysis: TH=75, HE=42, AT=23 (strong English signal)

**Next steps:**
- Test refined columnar/rail-fence transpositions on the XOR-71 output
- Consider if Page 1 has a two-step process: XOR-71 decrypt → transpose/permute
- Verify the key-71 result against Page 2 (does a similar key work?)

## Quick links

- **NEW:** `tools/page1_key71_attack.py` ← **CURRENT BEST APPROACH**
- **NEW:** `tools/PAGE1_KEY71_RESULTS.txt`
- **NEW:** `tools/ioc_analysis_page1.py`
- **NEW:** `tools/analyze_xor71_output.py`
- `tools/page1_attack.py` (master key length 95 - likely wrong for Page 1)
- `tools/PAGE1_RESULTS.md`
- `tools/page1_chain_attack.py`
- `tools/page1_two_layer_attack.py`
- `tools/PAGE1_TWO_LAYER_RESULTS.md`
- `tools/page1_shortkey_secondlayer.py`
- `tools/PAGE1_SHORTKEY_LAYER_RESULTS.md`
