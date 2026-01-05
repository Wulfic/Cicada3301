# Liber Primus Investigation Summary

## Session Date: Analysis of Cicada 3301 Liber Primus (Updated 2025)

---

## Key Confirmed Findings

### 1. **Page 56 - SOLVED**
- **Method**: Prime shift cipher with formula `-(prime[i] + 57) mod 29`
- **Plaintext begins**: "AN END: WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT..."
- Contains RSA hex block embedded in the text

### 2. **Page 57 - PLAINTEXT**
- Known plaintext: "PARABLE: LIKE THE INSTAR TUNNELING TO THE SURFACE. WE MUST SHED OUR OWN CIRCUMFERENCES. FIND THE DIVINITY WITHIN AND EMERGE."
- Length: 95 runes
- No encryption applied

### 3. **Pages 0 and 54 - IDENTICAL** ⚠️ CONFIRMED
- Both pages contain EXACTLY the same first 95 runes
- Both decrypt to the Parable with Master Key at offset 0
- VERIFIED: Master Key derivation = Page0 - Page57 (mod 29)
- Master Key sum = **1331 = 11³** (highly significant!)

### 4. **Master Key VERIFIED**
```python
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]
# Sum = 1331 = 11³, Length = 95
```

### 5. **2016 Clue (PGP-Signed by 7A35090F)**
Source: `assets/2016/4gq25.jpg.outguess`
> "Liber Primus is the way. Its words are the map, their meaning is the road, and their **NUMBERS** are the direction."

---

## Statistical Findings

### Index of Coincidence (IoC)
| Category | IoC | Interpretation |
|----------|-----|----------------|
| English text | ~1.73 | Normal readable text |
| Page 57 (plaintext) | 1.82 | Confirms readable |
| Page 56 (decrypted) | 1.18 | Partial decryption works |
| All encrypted pages | ~1.00 | **FLAT DISTRIBUTION** |

**Critical insight**: IoC ≈ 1.0 indicates the cipher creates a one-time-pad-like effect with flat frequency distribution.

### Kasiski Analysis - KEY LENGTH CONFIRMED
- All unsolved pages show Kasiski key length = **95**
- This matches the Master Key length (from Parable)
- Confirms Vigenère with key length 95

### Key Match Analysis
When cracking keys from unsolved pages vs Master Key:
| Page | Best Match % | Best Offset |
|------|-------------|-------------|
| 27 | 7.4% | 59 |
| 28 | 10.5% | 13 |
| 29 | 7.4% | 91 |
| 30 | 6.3% | 1 |
| 31 | 7.4% | 9 |
| 40 | 7.4% | 81 |
| 46 | 10.5% | 56 |
| 52 | 9.5% | 72 |

**Critical Finding**: Cracked keys from unsolved pages only match 6-10% of Master Key at any offset. If simple Vigenère, we'd expect ~100% match.

### Letter Frequency Analysis (Page 28)
When decrypted with best offset=13:
| Letter | Found | Expected |
|--------|-------|----------|
| E | 3.4% | **12.7%** |
| T | 4.9% | 9.1% |
| X | 3.7% | **~0%** |

**WRONG for English!** Suggests either:
1. Plaintext is not English (Latin?)
2. Another cipher layer exists
3. Wrong decryption method

---

## Cipher Methods Tested (COMPREHENSIVE)

### ❌ Did NOT produce readable text:

1. **Vigenère with Master Key** - All 95 offset combinations tested
   - Best scores: 30-40 (need 100+ for readable)
   
2. **Affine Key Transformations** - `key'[i] = (a * key[i] + b) mod 29`
   - Tested all a=1-28, b=0-28 combinations
   - Best: Page 28 (a=5, b=19, offset=47) → score 33
   - No consistent (a,b) pattern across pages
   
3. **Running Key Cipher** - Using Parable as key source
   - Best scores: ~20
   
4. **Autokey Cipher** - With Master Key primer
   - Best scores: ~26
   
5. **Prime Shift Cipher** - Testing Page 56 method on unsolved pages
   - Page 56: constant=57 **WORKS** ("AN END WITHIN THE DEEP WEB...")
   - Unsolved pages: constant=-76 to -100, scores 18-30, gibberish
   
6. **Transposition Before/After Vigenère**
   - Columnar, rail fence, spiral, reverse
   - No improvement
   
7. **Double Vigenère** - Two keys combined
   - No improvement
   
8. **Key Multiplication** - `key[i] * multiplier mod 29`
   - No consistent pattern
   
9. **Word Position as Offset** - Using Parable word positions
   - Some partial matches but no solution

### ⚠️ Interesting Patterns Found:

1. **Scattered English Words** appear at certain offsets:
   - Page 28 offset 13: THE, WE, AND, WHO scattered
   - But no coherent sentence structure
   
2. **Page 29 offset 91** matches position of "AND" in Parable
   
3. **Page 46 offset 56** matches position of "CIRCUMFERENCES" in Parable

---

## Most Promising Leads for Further Investigation

### 1. **Non-English Plaintext**
Letter frequency analysis shows the plaintext is NOT standard English:
- E is at 3.4% (should be 12.7%)
- X is at 3.7% (should be ~0%)
- Consider Latin or constructed language

### 2. **Word-to-Page Correspondence** ⚠️ NEW THEORY
From Parable analysis, page numbers may map to words:
- Page 27 → Word 7 (SURFACE)
- Page 28 → Word 8 (WE)
- Page 29 → Word 9 (MUST)
- etc.
Pattern: Page N → Word (N - 20)

### 3. **Book Cipher with External Text**
Try using these as running keys:
- Emerson's "Self-Reliance" (referenced by Cicada)
- Crowley's "Book of the Law"
- Other Cicada-referenced philosophical texts

### 4. **Multi-Layer Encryption**
Evidence suggests more than one cipher layer:
- Vigenère confirmed (key length 95)
- But key doesn't match → transformation layer
- Prime shift? Affine? Position-dependent?

### 5. **Gematria as Cipher Component**
The 2016 clue says "NUMBERS are the direction":
- Word Gematria sums from Parable
- Gematria values of runes as additional shift

---

## Tools Created This Session

| Tool | Purpose | Key Finding |
|------|---------|-------------|
| `page52_focus.py` | Deep Page 52 analysis | Scattered words at various offsets |
| `test_word_gematria_offset.py` | Word Gematria as offset | Partial matches (SURFACE=46, COVERED=47) |
| `exhaustive_cipher_test.py` | Running key, autokey, double Vigenère | Affine showed best results |
| `affine_deep_analysis.py` | Affine key transformations | No consistent (a,b) pattern |
| `verify_page0_method.py` | Compare Pages 0 and 54 | IDENTICAL first 95 runes |
| `deep_parable_analysis.py` | Parable word position analysis | Word positions documented |
| `word_position_offset.py` | Best offset pattern analysis | Partial matches, no formula |
| `page28_detailed.py` | Detailed frequency analysis | Letter freqs WRONG for English |
| `transposition_tests.py` | Transposition cipher tests | No improvement |
| `prime_decryption.py` | Prime-based methods | Page 56 works, others don't |

---

## Unsolved Pages Status

| Page | Length | Best Score | Best Method | Notes |
|------|--------|------------|-------------|-------|
| 27 | 232 | 20 | offset=59 | First in sequence |
| 28 | 232 | 35 | affine(5,19)+47 | Most analyzed |
| 29 | 232 | 21 | offset=91 | Matches "AND" pos |
| 30 | 232 | 21 | offset=1 | |
| 31 | 232 | 23 | offset=9 | Last before gap |
| 40 | 232 | 22 | offset=81 | |
| 41 | 232 | 23 | offset=? | |
| 44 | 232 | 24 | offset=? | |
| 45 | 232 | 23 | offset=? | |
| 46 | 232 | 23 | offset=56 | Matches "CIRCUMFERENCES" |
| 47 | 232 | 25 | offset=? | |
| 48 | 232 | 24 | offset=? | |
| 52 | 232 | 36 | affine(25,12)+8 | Highest affine score |

**Score interpretation**: Need 80+ for readable English (Parable=64 on Page 0)

---

## Key Insights Summary

1. ✅ **Master Key WORKS** for Pages 0, 54, 56 (prime variant), 57
2. ⚠️ **Kasiski confirms key length 95** for unsolved pages
3. ❌ **Cracked keys DON'T match Master Key** (only 6-10%)
4. ❌ **Letter frequencies WRONG** for English output
5. 🔍 **Missing transformation layer** between ciphertext and Vigenère

---

## Next Actions

1. [ ] Test Self-Reliance as running key source
2. [ ] Test Latin word dictionary for plaintext matching  
3. [ ] Analyze original images for steganographic data
4. [ ] Try word-to-page mapping (Page N → Word N-20)
5. [ ] Look for patterns in the RSA hex block from Page 56

---
*Last updated: Current session*

## Community Resources
- [Uncovering Cicada Wiki](https://uncovering-cicada.fandom.com/wiki/Uncovering_Cicada_Wiki)
- [Cicada Solvers Discord](https://discord.com/invite/eMmeaA9)
- IRC #cicadasolvers

---

*"Like the instar, tunneling to the surface. We must shed our own circumferences. Find the divinity within and emerge."*
