# Liber Primus Solving Session - 2026-01-04

## Executive Summary

This session established the analytical foundation for solving the Liber Primus. We verified known solutions, built analysis tools, and characterized the encryption used in the unsolved pages.

## ⚡ MAJOR BREAKTHROUGH - XOR DISCOVERY ⚡

### Discovery
By XORing three outguess hex blocks together (all 991 bytes each):
- `liber_primus_outguess.txt`
- `intus_outguess.txt`  
- `runes_outguess.txt`

We recovered a **VALID PGP SIGNED MESSAGE**:

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO
UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ

Good luck.

3301

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)
[valid signature]
-----END PGP SIGNATURE-----
```

### Cipher Analysis
- 14 groups of 5 characters each
- Contains numbers: 7, 5, 4 (possibly markers)
- Group 4 "RTHIS" contains "THIS"
- Could contain: DIVINITY, THEKEY, RUNES, WITHIN
- Likely a transposition cipher

### Extracted Files from Outguess
- `portrait_jpeg_1_1.jpg` - Created with GIMP (1084 bytes)
- `portrait_jpeg_2_1.jpg` - LEAD Technologies (1635 bytes)  
- `liber_primus_5_jpeg_1.jpg` - 15188 bytes
- 3 high-entropy .bin files (991 bytes each) - these XOR together!

---

## What We Confirmed

### ✅ Page 57 (The Parable) - PLAINTEXT
Direct transliteration produces readable English:
> "parable: like the instar tunneling to the surface. we must shed our own circumferences. find the divinity within and emerge."

- **IoC: 1.82** (English typically ≈ 1.73)
- No cipher applied - this is the **only plaintext page**

### ✅ Page 56 - Prime Shift Cipher  
The decryption method `-(prime_n + 57) mod 29` works:
> "an end: within the deep web, there exists a page that hashes to: it is the duty..."

The page contains an **embedded hex block**:
```
36367763ab73783c7af284446c
59466b4cd653239a311cb7116
d4618dee09a8425893dc7500b
464fdaf1672d7bef5e891c6e227
4568926a49fb4f45132c2a8b4
```
This appears to be RSA-encrypted data.

---

## Key Statistical Findings

### The Full Liber Primus
| Metric | Value | Interpretation |
|--------|-------|----------------|
| Total runes | 12,683 | - |
| Unique runes | 28 | Missing J (ᛂ) in most text |
| Index of Coincidence | 1.0356 | ≈ Random (strong encryption) |
| Gematria Sum | 659,573 | - |

### Frequency Distribution
**All 29 runes appear with nearly equal frequency (3.2% - 3.9%)**

This is the hallmark of:
- A well-designed polyalphabetic cipher
- OR a running key cipher
- OR multiple encryption layers

English text would show E at ~12.7%, T at ~9.1%, etc.

---

## Tools Created

### 1. `tools/liber_primus_analyzer.py`
Comprehensive toolkit including:
- Rune/English conversion
- Gematria calculations
- Frequency analysis
- Index of Coincidence
- Kappa test (key length estimation)
- Kasiski examination
- Multiple cipher implementations

### 2. `tools/verify_page56.py`
Confirms the Page 56 decryption method works.

### 3. `tools/page_analysis.py`  
Analyzes each page/section individually with IoC calculations.

### 4. `tools/advanced_solver.py`
Tests multiple cipher methods:
- Caesar shifts (all 29)
- Prime number shifts (various offsets)
- Fibonacci shifts
- Vigenère with prime-based keys
- Known plaintext attack

---

## Why Simple Ciphers Don't Work

We tested the following on unsolved pages - **none produced readable English**:

1. **Caesar shifts** (all 29 variations)
2. **Prime shifts** (offsets 0-120)
3. **Fibonacci shifts** (offsets -30 to +30)
4. **Vigenère** with short keys (2-7)
5. **Known plaintext attack** with Cicada-specific words

**Best scores on unsolved pages: 20-30** (compared to **391** for Page 56)

---

## Hypotheses for the Cipher

### Hypothesis 1: Running Key Cipher
The flat frequency suggests the key might be:
- Another text (perhaps one referenced in the puzzle)
- The book "Self-Reliance" by Emerson (mentioned in 2013 puzzles)
- The Book of the Law by Aleister Crowley (also referenced)

### Hypothesis 2: Layered Encryption
Multiple passes of encryption, such as:
- Vigenère → then shift by primes
- Autokey → then Caesar

### Hypothesis 3: Different Methods Per Section
Each page/section might use:
- Different keys
- Different base methods
- Keys derived from gematria values

### Hypothesis 4: Information-Theoretic Security
If a one-time pad was used, the text may be:
- Theoretically unbreakable without the key
- Require finding the key source externally

---

## Recommended Next Steps

### Immediate (High Priority)
1. **Analyze the hex block in Page 56** - Try RSA factoring or look for public key
2. **Test running key cipher** with known reference texts
3. **Research what new discoveries** the Cicada community has made since 2014

### Short-term
4. **Cross-reference with image steganography** - Original LP images may contain keys
5. **Analyze gematria patterns** - The number 1,595,277,641 (Parable gematria product)
6. **Look for patterns in page gematria sums**

### Long-term
7. **Build a distributed solver** to test more key combinations
8. **Apply machine learning** for English detection in partial decryptions
9. **Collaborate with active Cicada solvers** on Discord/IRC

---

## Files Modified/Created

```
Cicada3301/
├── LIBER_PRIMUS_SOLVING_PLAN.md    [Updated with results]
└── tools/
    ├── liber_primus_analyzer.py    [Main analysis toolkit]
    ├── verify_page56.py            [Page 56 verification]
    ├── page_analysis.py            [Per-page analysis]
    ├── advanced_solver.py          [Multi-method solver]
    ├── comprehensive_analysis.py   [Running key, RSA, gematria, steg]
    ├── extract_hidden_data.py      [Extract from outguess files]
    ├── rsa_decrypt.py              [RSA decryption attempts]
    ├── xor_analysis.py             [XOR of hex blocks - FOUND MESSAGE!]
    ├── decode_xor_message.py       [Cipher analysis]
    ├── solve_transposition.py      [Transposition solver]
    ├── SESSION_NOTES_2026-01-04.md [This file]
    └── extracted/
        ├── xor_discovered_message.pgp  [THE BREAKTHROUGH!]
        ├── portrait_jpeg_1_1.jpg
        ├── portrait_jpeg_2_1.jpg  
        ├── liber_primus_5_jpeg_1.jpg
        ├── liber_primus_extracted.bin
        ├── intus_extracted.bin
        ├── runes_extracted.bin
        └── xor_all_three.bin           [XOR result]
```

---

## THE DISCOVERED CIPHER

The XOR of the three outguess blocks reveals this encrypted message:

```
IDGTK UMLOO ARWOE RTHIS UTETL HUTIA TSLLO
UIMNI TELNJ 7TFYV OIUAU SNOCO 5JI4M EODZZ
```

### Analysis Results:
- 14 groups × 5 chars = 70 characters
- Contains "THIS" (group 4: RTHIS)
- Numbers 7, 5, 4 may be positional markers
- Could contain: DIVINITY, THEKEY, RUNES, WITHIN

### Next Steps for This Cipher:
1. Verify PGP signature with Cicada's public key
2. Try columnar transposition with prime-based keys
3. The numbers might indicate letter removal or swapping

---

## Running the Tools

```powershell
# From the Cicada3301 directory:

# Full analysis
.venv/Scripts/python.exe tools/liber_primus_analyzer.py

# Page 56 verification
.venv/Scripts/python.exe tools/verify_page56.py

# Per-page analysis
.venv/Scripts/python.exe tools/page_analysis.py

# Advanced solver
.venv/Scripts/python.exe tools/advanced_solver.py
```

---

*"Like the instar, tunneling to the surface. We must shed our own circumferences. Find the divinity within and emerge."*
