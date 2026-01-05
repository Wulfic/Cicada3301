# Liber Primus Solving Plan

> A comprehensive guide for approaching the unsolved Liber Primus puzzle from Cicada 3301 (2014)

---

## Table of Contents
1. [Overview](#overview)
2. [Current Status](#current-status)
3. [The Cryptographic System](#the-cryptographic-system)
4. [Resources in This Repository](#resources-in-this-repository)
5. [Solved Pages Analysis](#solved-pages-analysis)
6. [Approaches Already Tried](#approaches-already-tried)
7. [Proposed Solving Strategy](#proposed-solving-strategy)
8. [Action Items & Experiments](#action-items--experiments)
9. [Tools to Build](#tools-to-build)
10. [Research Leads](#research-leads)

---

## Overview

The **Liber Primus** ("First Book") is a 58-page cryptographic document written in **Anglo-Saxon Futhorc runes**. It was discovered through the 2014 Cicada 3301 puzzle series and represents the final major unsolved puzzle. The book was released via hidden .onion websites and contains the central mystery that the community has been working on since 2014.

### Key Facts
- **Total Pages**: 58 (Pages 0-57)
- **Alphabet**: 29 Anglo-Saxon Futhorc runes
- **Gematria System**: Each rune maps to a consecutive prime number
- **Status**: Mostly unsolved (~2-3 pages confirmed decoded)

---

## Current Status

### ✅ SOLVED PAGES

| Page | Method | Content |
|------|--------|---------|
| **Page 56** | Prime number shift cipher (`-(prime + 57) mod 29`) | Contains RSA hex block + runic text |
| **Page 57** | Plaintext (no encryption) | The "Parable" - a philosophical message about emergence |

### ⏳ PARTIALLY ANALYZED
- Pages 0-14, 27-32, 40-55 - Have runic data transcribed but not decrypted
- Various pattern analyses exist but no successful decryption

### ❌ UNSOLVED
- The vast majority of the 58 pages remain encrypted
- The encryption method(s) for most pages are unknown

---

## The Cryptographic System

### The Gematria Primus (Rune Alphabet)

The 29-character Anglo-Saxon Futhorc alphabet with prime number gematria values:

| # | Rune | English | Gematria (Prime) | Shift Value |
|---|------|---------|------------------|-------------|
| 0 | ᚠ | F | 2 | 0 |
| 1 | ᚢ | U/V | 3 | 1 |
| 2 | ᚦ | TH | 5 | 2 |
| 3 | ᚩ | O | 7 | 3 |
| 4 | ᚱ | R | 11 | 4 |
| 5 | ᚳ | C/K | 13 | 5 |
| 6 | ᚷ | G | 17 | 6 |
| 7 | ᚹ | W | 19 | 7 |
| 8 | ᚻ | H | 23 | 8 |
| 9 | ᚾ | N | 29 | 9 |
| 10 | ᛁ | I | 31 | 10 |
| 11 | ᛂ | J | 37 | 11 |
| 12 | ᛇ | EO | 41 | 12 |
| 13 | ᛈ | P | 43 | 13 |
| 14 | ᛉ | X | 47 | 14 |
| 15 | ᛋ | S | 53 | 15 |
| 16 | ᛏ | T | 59 | 16 |
| 17 | ᛒ | B | 61 | 17 |
| 18 | ᛖ | E | 67 | 18 |
| 19 | ᛗ | M | 71 | 19 |
| 20 | ᛚ | L | 73 | 20 |
| 21 | ᛝ | NG/ING | 79 | 21 |
| 22 | ᛟ | OE | 83 | 22 |
| 23 | ᛞ | D | 89 | 23 |
| 24 | ᚪ | A | 97 | 24 |
| 25 | ᚫ | AE | 101 | 25 |
| 26 | ᚣ | Y | 103 | 26 |
| 27 | ᛡ | IA/IO | 107 | 27 |
| 28 | ᛠ | EA | 109 | 28 |

### Text Formatting Symbols
- `•` = Word separator (space)
- `-` = Word break/hyphen
- `%` = Line/section marker
- `&` and `$` = Page/chapter markers
- `:` = Special section delimiter

### Confirmed Decryption Method (Page 56)

```python
# Page 56 uses a prime-based shift cipher
def decrypt_page_56(rune_text):
    for each rune character:
        prime = next_prime()  # Consecutive primes: 2, 3, 5, 7, 11...
        shift_amount = -(prime + 57)
        new_position = (current_position + shift_amount) % 29
        output = rune_at(new_position)
```

---

## Resources in This Repository

### Primary Source Files

| Resource | Location | Description |
|----------|----------|-------------|
| Raw Runic Text | `2014/Liber Primus/runes in text format.txt` | 690 lines of runic ciphertext |
| English Transcript | `2014/Liber Primus/lp-full-english transcript.docx` | Transliterated text |
| Original Images | `2014/Liber Primus/liber primus images full/` | Source images |
| Enhanced Runes | `2014/Liber Primus/Enhanced Rune Images/` | Cleaned up rune images |
| Stacked Pages | `2014/Liber Primus/Stacked Pages/` | Layered analysis |
| Gematria Analysis | `EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/Liber primus in gematria values by mortlach.txt` | Mathematical breakdown |

### Tools & Scripts

| Tool | Location | Purpose |
|------|----------|---------|
| RuneSolver.py | `EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/` | Comprehensive decoder with multiple cipher modes |
| runes.py | `2014/additional docs/scripts/` | Vigenère-style operations with offset sequences |
| Page 56 Decoder | `2014/additional docs/scripts/page 56 script decoder.txt` | Working decoder for Page 56 |
| DetectJPG_v2.py | `2014/additional docs/scripts/` | Image steganography detection |
| RSA Decrypt (Perl) | `2014/additional docs/scripts/Program to decrypt RSA message in perl.txt` | RSA decryption attempt |

### Reference Materials

| Material | Location |
|----------|----------|
| Vigenère Tables | `EXTRA WIKI PAGES/useful tools/` |
| 5x5 Magic Squares | `2014/additional docs/5x5 Magic Squares based on numbers from onion5 portrait.jpg.txt` |
| Pattern Analysis Logs | `EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/PFb6eQiD - logs.txt` |
| Wiki Discussion Logs | `2014/additional docs/logs from the wiki.txt` |

---

## Solved Pages Analysis

### Page 57 - The Parable (Plaintext)

This is the **only confirmed plaintext** in the Liber Primus:

> *"Parable: Like the instar, tunneling to the surface. We must shed our own circumferences. Find the divinity within and emerge."*

**Key Observations:**
- References **"instar"** - a stage in insect development (cicada lifecycle)
- Themes of **transformation**, **emergence**, and **inner divinity**
- The gematria sum of each line, multiplied together = **1,595,277,641**
- This message likely provides thematic clues to the rest of the book

### Page 56 - Prime Shift Cipher

**Method**: Each rune is shifted by `-(prime_n + 57) mod 29` where prime_n is the nth consecutive prime.

**Contents**:
- Runic text
- Embedded **hex block** (possibly RSA-encrypted):
  ```
  36367763ab73783c7af284446c
  59466b4cd653239a311cb7116
  d4618dee09a8425893dc7500b
  464fdaf1672d7bef5e891c6e227
  4568926a49fb4f45132c2a8b4
  ```

---

## Approaches Already Tried

### Cipher Methods Attempted

1. **Vigenère Cipher** (with runic alphabet)
   - Standard Vigenère with various keywords
   - Two Vigenère tables exist in the repository
   
2. **Alberti Cipher** (variant of Vigenère)
   - Tested with different rotor settings
   
3. **Stream Ciphers**
   - Combined with Vigenère
   - Skip cipher + stream combinations

4. **Prime-Based Shifts**
   - Page 56 method extended to other pages (unsuccessful)
   - Totient sequences
   - Totient of primes sequences

5. **Mathematical Sequences (OEIS)**
   - Various integer sequences tested as keys
   - Community consensus: "text is not enciphered with an OEIS stream"

### Pattern Analysis Attempts

From the IRC logs (`PFb6eQiD - logs.txt`):

1. **Cyclical Gap Patterns**
   - Identified patterns like `11, -18, 11, 11, -18` for key generation
   - Formula: `X1 = K2 - K1` (base gap pattern)
   - "Low doubles" generation using base gap of 11

2. **Difference Patterns**
   - X1, X2, X3, X4 difference calculations between key elements
   - Cyclical patterns observed but not exploited

### Why These Failed

- Simple substitution doesn't work
- The key or method remains unknown
- Different pages may use different encryption methods
- The cipher may be more complex than single-pass encryption

---

## Proposed Solving Strategy

### Phase 1: Data Preparation & Verification

**Goal**: Ensure we have accurate, machine-readable data

1. **[ ] Verify Transcriptions**
   - Cross-reference `runes in text format.txt` with original images
   - Check for transcription errors
   - Standardize separator symbols

2. **[ ] Create Clean Datasets**
   - Page-by-page runic text files
   - Corresponding gematria value files
   - Frequency analysis per page

3. **[ ] Catalog All Clues**
   - Extract all PGP-signed messages
   - Document all onion addresses and their contents
   - Map the complete 2014 puzzle flow

### Phase 2: Statistical Analysis

**Goal**: Identify patterns that reveal the encryption method

4. **[ ] Frequency Analysis**
   - Compare rune frequencies against expected English (transliterated)
   - Identify pages with similar frequency distributions
   - Look for pages that might share the same key

5. **[ ] Index of Coincidence**
   - Calculate IoC for each page
   - Identify polyalphabetic vs monoalphabetic sections
   - Determine probable key lengths for Vigenère-like ciphers

6. **[ ] N-gram Analysis**
   - Common bigrams/trigrams in runic English
   - Compare against ciphertext patterns
   - Look for repeated sequences

### Phase 3: Key Discovery

**Goal**: Find the key(s) needed for decryption

7. **[ ] Known-Plaintext Attacks**
   - The Parable provides vocabulary Cicada uses
   - Try common words: "instar", "emerge", "divinity", "cicada", "3301"
   - Test headers/footers that might be consistent

8. **[ ] Page 56 Method Extension**
   - Vary the `+57` constant
   - Try different starting primes
   - Test other prime-based formulas

9. **[ ] Image Steganography**
   - Re-analyze original images with Outguess
   - Check for hidden data in enhanced images
   - Look for LSB steganography

10. **[ ] Mathematical Clues**
    - 5x5 Magic Squares analysis
    - Gematria sum patterns
    - Fibonacci/prime relationships

### Phase 4: Cryptanalysis

**Goal**: Apply discovered keys/methods

11. **[ ] Systematic Cipher Testing**
    - Build automated testing framework
    - Test all common cipher combinations
    - Score outputs by English-likeness

12. **[ ] Layered Encryption**
    - Consider multi-pass encryption
    - Test: Vigenère → Shift → Substitution chains
    - Vary layer order

13. **[ ] Book Cipher Possibility**
    - Check references in the puzzle (Emerson's "Self-Reliance", etc.)
    - Test numerical references as book cipher keys

### Phase 5: Validation & Documentation

14. **[ ] Verify Solutions**
    - Check for grammatically correct English
    - Verify thematic consistency with solved pages
    - Look for Cicada's characteristic style

15. **[ ] Document Methods**
    - Record all successful techniques
    - Update this plan with findings
    - Share with community

---

## Action Items & Experiments

### Immediate Actions (Week 1)

- [ ] **Transcription Audit**: Manually verify first 5 pages against images
- [ ] **Build Frequency Analyzer**: Script to count rune frequencies per page
- [ ] **Calculate IoC**: Determine polyalphabetic characteristics
- [ ] **Catalog Reference Texts**: List all books/works mentioned in the puzzles

### Short-Term Experiments (Week 2-3)

- [ ] **Known-Plaintext Test**: Use "PARABLE", "INSTAR", "CICADA" as potential cribs
- [ ] **Page 56 Variations**: Test -(prime + N) for N = 0 to 100
- [ ] **Cross-Page Analysis**: Look for identical ciphertext sequences across pages
- [ ] **Gematria Factoring**: Factor page totals, look for meaningful patterns

### Medium-Term Research (Month 1-2)

- [ ] **RSA Analysis**: Attempt to factor/decrypt the hex block on Page 56
- [ ] **Image Re-Analysis**: Fresh steganography analysis on all images
- [ ] **Historical Context**: Research any new discoveries since 2014
- [ ] **Discord/Community Check**: Verify current state of community knowledge

---

## Tools to Build

### 1. Universal Rune Decoder (`rune_decoder.py`)
```
Features:
- Input: Runic text file
- Output: Decrypted text
- Modes: Vigenère, Caesar, Prime-shift, Stream, Custom
- Key input: Text, numeric sequence, or mathematical formula
- Scoring: English word detection, frequency analysis
```

### 2. Frequency Analyzer (`freq_analyzer.py`)
```
Features:
- Per-page rune frequency
- Compare against expected English frequencies
- Index of Coincidence calculation
- Kappa test for key length detection
```

### 3. Pattern Matcher (`pattern_match.py`)
```
Features:
- Find repeated n-grams
- Cross-page sequence detection
- Known-word pattern matching
- Report suspicious regularities
```

### 4. Automated Cipher Tester (`cipher_tester.py`)
```
Features:
- Brute-force key space
- Multi-cipher combinations
- Parallel processing
- English language scoring (dictionary + bigram frequency)
- Save promising results
```

### 5. Steganography Scanner (`steg_scanner.py`)
```
Features:
- Outguess detection
- LSB analysis
- Metadata extraction
- Comparison with known hidden messages
```

---

## Research Leads

### Mathematical Leads
- [ ] The number **1,595,277,641** (Parable gematria product) - factor and analyze
- [ ] 5x5 Magic Squares with A+C relationships
- [ ] Prime number patterns in page gematria totals
- [ ] Fibonacci sequence appearances

### Cryptographic Leads
- [ ] The `+57` constant in Page 56 - why 57? (57 = 3 × 19)
- [ ] RSA hex block analysis - public key discovery
- [ ] Possible asymmetric encryption requiring private key
- [ ] Time-locked cryptography (see `futorcap` in 2012 folder)

### Textual Leads
- [ ] Emerson's "Self-Reliance" - present in repository, likely a reference text
- [ ] The Book of the Law (Aleister Crowley) - referenced in 2013 puzzle
- [ ] Instar emergence / cicada lifecycle symbolism
- [ ] Gnostic/mystical themes

### Community Resources
- [ ] [Uncovering Cicada Wiki](https://uncovering-cicada.fandom.com/wiki/Uncovering_Cicada_Wiki)
- [ ] [Cicada Solvers Discord](https://discord.com/invite/eMmeaA9)
- [ ] IRC #cicadasolvers on Freenode
- [ ] Historical solving logs in repository

---

## Appendix A: Quick Reference

### Rune → English Lookup
```
ᚠ=F  ᚢ=U  ᚦ=TH  ᚩ=O  ᚱ=R  ᚳ=C  ᚷ=G  ᚹ=W  ᚻ=H  ᚾ=N
ᛁ=I  ᛂ=J  ᛇ=EO  ᛈ=P  ᛉ=X  ᛋ=S  ᛏ=T  ᛒ=B  ᛖ=E  ᛗ=M
ᛚ=L  ᛝ=ING ᛟ=OE ᛞ=D  ᚪ=A  ᚫ=AE ᚣ=Y  ᛡ=IA ᛠ=EA
```

### Gematria (Primes) Lookup
```
F=2   U=3   TH=5  O=7   R=11  C=13  G=17  W=19  H=23  N=29
I=31  J=37  EO=41 P=43  X=47  S=53  T=59  B=61  E=67  M=71
L=73  ING=79 OE=83 D=89 A=97  AE=101 Y=103 IA=107 EA=109
```

### File Paths
```
Main Text:      2014/Liber Primus/runes in text format.txt
Images:         2014/Liber Primus/liber primus images full/
RuneSolver:     EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/RuneSolver.py
Gematria Data:  EXTRA WIKI PAGES/Liber Primus Ideas and Suggestions/Liber primus in gematria values by mortlach.txt
Scripts:        2014/additional docs/scripts/
```

---

## Appendix B: Page 56 Decoder (Working Example)

```python
# -*- coding: utf-8 -*-
import itertools as it

gematriaprimus = (
    ('ᚠ', 'f', 2), ('ᚢ', 'u', 3), ('ᚦ', 'th', 5), ('ᚩ', 'o', 7),
    ('ᚱ', 'r', 11), ('ᚳ', 'c', 13), ('ᚷ', 'g', 17), ('ᚹ', 'w', 19),
    ('ᚻ', 'h', 23), ('ᚾ', 'n', 29), ('ᛁ', 'i', 31), ('ᛂ', 'j', 37),
    ('ᛇ', 'eo', 41), ('ᛈ', 'p', 43), ('ᛉ', 'x', 47), ('ᛋ', 's', 53),
    ('ᛏ', 't', 59), ('ᛒ', 'b', 61), ('ᛖ', 'e', 67), ('ᛗ', 'm', 71),
    ('ᛚ', 'l', 73), ('ᛝ', 'ing', 79), ('ᛟ', 'oe', 83), ('ᛞ', 'd', 89),
    ('ᚪ', 'a', 97), ('ᚫ', 'ae', 101), ('ᚣ', 'y', 103), ('ᛡ', 'io', 107),
    ('ᛠ', 'ea', 109)
)

runes = [x[0] for x in gematriaprimus]
letters = [x[1] for x in gematriaprimus]

def primegen():
    D = {}
    yield 2
    for q in it.islice(it.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q*q] = q
            yield q
        else:
            x = q + 2*p
            while x in D:
                x += 2*p
            D[x] = p

def shift(offset, direction): 
    return (offset + direction) % len(gematriaprimus)

def decrypt_page_56(page_text):
    pg = primegen()
    result = ''
    n = 0
    for c in page_text:
        if c == '•':
            result += ' '
            continue
        if c not in runes:
            result += c
            continue
        o = runes.index(c)
        if n != 56:  # 57th rune is unencrypted
            np = next(pg)
            o = shift(o, -(np + 57))
        result += letters[o]
        n += 1
    return result
```

---

## Progress Log

| Date | Action | Result |
|------|--------|--------|
| *Start* | Created this solving plan | - |
| 2026-01-04 | Built analysis toolkit (`tools/liber_primus_analyzer.py`) | Comprehensive frequency/IoC analysis |
| 2026-01-04 | Ran full statistical analysis | IoC=1.0356 confirms polyalphabetic cipher |
| 2026-01-04 | Verified Page 56 decryption | Prime+57 produces "an end: within the deep web..." |
| 2026-01-04 | Verified Page 57 (Parable) | Confirmed plaintext, IoC=1.82 |
| 2026-01-04 | Built advanced solver (`tools/advanced_solver.py`) | Tests 6 cipher methods with scoring |
| 2026-01-04 | Tested all pages individually | All encrypted pages have IoC ≈ 1.0 |

---

## Analysis Results (2026-01-04)

### Key Statistical Findings

```
Full Liber Primus Statistics:
- Total runes: 12,683
- Unique runes: 28 (missing J rune ᛂ in many sections)
- Index of Coincidence: 1.0356 (very close to random 1.0)
- Gematria sum: 659,573

Frequency Distribution: FLAT (all runes ≈ 3.2-3.9%)
This indicates strong encryption that flattens letter frequencies
```

### Confirmed Decryptions

**Page 57 (The Parable)** - PLAINTEXT
```
parable: like the instar tunneling to the surface.
we must shed our own circumferences.
find the divinity within and emerge.
```
- IoC: 1.82 (confirms readable English)
- No encryption applied

**Page 56** - Prime+57 Shift Cipher
```
an end: within the deep web, there exists a page that hashes to:
it is the duty [partial corruption after hex block]
```
- Method: Shift each rune by `-(prime_n + 57) mod 29`
- Confirmed working for first portion of page
- Contains embedded hex block (possible RSA data)

### Tools Created

| Tool | Path | Purpose |
|------|------|---------|
| `liber_primus_analyzer.py` | `tools/` | Frequency analysis, IoC, n-grams |
| `verify_page56.py` | `tools/` | Page 56 decryption verification |
| `page_analysis.py` | `tools/` | Individual page analysis |
| `advanced_solver.py` | `tools/` | Multi-method cipher testing |

### Next Investigation Leads

1. **The flat frequency distribution** suggests:
   - Running key cipher (using another text as key)
   - OR multiple layers of encryption
   - OR a one-time pad style cipher

2. **Factor 29 appears in spacing analysis** - The alphabet size appearing suggests the cipher incorporates modular arithmetic related to the alphabet

3. **Page 56 partial decryption** - Need to investigate why decryption degrades after hex block

---

*"Like the instar, tunneling to the surface. We must shed our own circumferences. Find the divinity within and emerge."*

— The Parable, Liber Primus Page 57
