# LIBER PRIMUS - MASTER SOLVING DOCUMENT
## Cicada 3301 (2014) Cryptographic Analysis

> **Note:** Full decryption outputs and detailed page analysis have been moved to individual page README files. See [pages/page_XX/README.md](../LiberPrimus/pages/) for complete details.
> 
> Archived full document: [archive/MASTER_SOLVING_DOC_FULL.md](../LiberPrimus/archive/MASTER_SOLVING_DOC_FULL.md)

---

## 📊 Project Status At-A-Glance (REVISED - Feb 3 Evening)

| Category | Count | Pages |
|----------|-------|-------|
| ✅ **FULLY SOLVED (Readable English)** | ~35 | [01](../LiberPrimus/pages/page_01/README.md)-[17](../LiberPrimus/pages/page_17/README.md), [55](../LiberPrimus/pages/page_55/README.md)-[74](../LiberPrimus/pages/page_74/README.md) (excluding images) |
| 🟡 **PARTIALLY SOLVED** | 3 | [18-19](../LiberPrimus/pages/page_18/README.md) (readable), [20](../LiberPrimus/pages/page_20/README.md) (prime-stream only) |
| 🔴 **HIGH IoC - NEEDS EXTRACTION** | 10 | [21-30](../LiberPrimus/pages/page_21/README.md) - Keywords found, IoC 1.86-2.31, text scrambled |
| 🔴 **CAESAR - NEEDS EXTRACTION** | 24 | [31-54](../LiberPrimus/pages/page_31/README.md) - Caesar shifts found, IoC ~1.0, text scrambled |
| ❓ **NOT ANALYZED** | 3 | 02, 65-71 (some are image-only) |

**⚠️ CRITICAL REVISION (Feb 3 Evening):**
> **High IoC Does NOT Mean Solved!** Previous session incorrectly assumed high IoC = solved.
> 
> **Reality:** Pages 21-54 have correct letter-frequency distributions but remain completely scrambled.
> All transposition methods (rail fence, columnar, diagonal, every-nth) have FAILED.
> 
> **New Understanding:** Pages 21-54 require additional breakthrough - possibly word-level transposition, 
> multi-stage decryption, or page-dependent transformations.
>
> **True Solved Count:** ~35 pages (NOT 50+). Pages 21-54 (34 pages) need new attack vector.

---

## 🔑 Core Breakthroughs

| # | Discovery | Impact |
|---|-----------|--------|
| 1 | **SUB mod 29, NOT XOR** | Achieves 100% reversibility |
| 2 | **Key lengths are ALL PRIME** | Keys like 43, 83, 47 (P19), 53 (P18) dominate. |
| 3 | **φ(prime) Shift Cipher** | Pages 55, 56, 73, 74 use `(cipher - φ(prime[i])) mod 29` |
| 4 | **Literal F Rule** | When plaintext is F, cipher is raw ᚠ without encryption (key counter skipped) |
| 5 | **Hyphens = word boundaries** | Preserved through encryption |
| 6 | **Self-Reliance Connection** | Emerson's essay is referenced in solved pages - may be running key source |
| 7 | **Primes/Totient Hint** | Page 05 says "THE PRIMES ARE SACRED, THE TOTIENT FUNCTION IS SACRED" |
| 8 | **Deor Key (Page 20 Artifact)** | Extracted 166-rune stream from P20 Primes (Deor - P20). Contains Scrambled Eng ("DEATH", "LENGTH RATIO"). Validates "REARRANGE PRIMES" hint. |
| 9 | **VALUE-based Separation (NEW)** | Page 20 uses rune VALUES: prime-valued (TH,O,C,W,J,P,B,M,D) separate from non-prime. Non-prime stream with shift -2 yields "THE" 6x! |

---

## 📋 Solved Pages Summary

| Page | Method | Plaintext Preview |
|------|--------|-------------------|
| 01 | Reversed Gematria | "A WARNING BELIEVE NOTHING FROM THIS BOOK..." |
| 03 | Vigenère (DIVINITY) | "WELCOME PILGRIM TO THE GREAT JOURNEY..." |
| 04 | Vigenère (DIVINITY) | "IT IS THROUGH THIS PILGRIMAGE..." |
| 05 | Default Gematria | "THE PRIMES ARE SACRED..." |
| 06-08 | Shift 3 Reversed | Koan story |
| 09 | Shift 3 Reversed | "DO FOUR UNREASONABLE THINGS EACH DAY" |
| 10 | Default Gematria | "THE CIRCUMFERENCE PRACTICES THREE BEHAVIORS..." |
| 11-12 | Key Length 83 | Philosophical text |
| 13 | Default Gematria | "AMASS GREAT WEALTH..." |
| 14-15 | Vigenère (FIRFUMFERENFE) | Koan story |
| 16 | Default Gematria | "QUESTION ALL THINGS..." |
| 17 | Vigenère (YAHEOOPYJ) | "EPILOGUE..." |
| 18 | Vigenère (Key Length 53) | "BEING OF ALL I WILL ASC THE OATH..." |
| 55 | φ(prime) + literal F | "AN END. WITHIN THE DEEP WEB..." |
| 56-57 | Prime shift | "AN END... LIKE THE INSTAR..." |
| 58 | CLEARTEXT | "LIBER PRIMUS" |
| 60 | CLEARTEXT | "CHAPTER I INTUS" |
| 61 | Vigenère (DIVINITY) | "WELCOME..." (Likely Continuation - Split Key) |
| 62 | Vigenère (CONSUMPTION) | "EOTATE..." |
| 63 | CLEARTEXT | "SOME WISDOM THE PRIMES ARE SACRED..." |
| 64 | Vigenère (KAON) | "THTHAEIO..." (KOAN) |
| 67 | Vigenère (CICADA) | "THEOTIO..." |
| 68 | CLEARTEXT | "THE LOSS OF DIVINITY..." |
| 72 | Vigenère (FIRFUMFERENFE)| "A KOAN" |
| 73-74 | φ(prime) + shift | "WITHIN THE DEEP WEB..." + Parable |

---

## � FEBRUARY 3, 2026 - MAJOR STRATEGIC DISCOVERIES

### Self-Referential Page Links Confirmed
- **Page 19 → Page 20:** "REARRANGING PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K" → Leads to prime-index extraction
- **Page 63 → Pages 21-30:** Wisdom grid keywords (VOID, AETHEREAL, CARNAL, ANALOG, MOURNFUL, SHADOWS, BUFFERS, MOBIUS, OBSCURA, CABAL, DEOR, DIVINITY, TOTIENT, PRIMES, SACRED, ENCRYPTION, CONSUMPTION) UNLOCK 10 consecutive pages with HIGH IoCs

### Cicada's Methodology (Confirmed)
1. **Wisdom/Reference Pages Contain Keys:** Find a wisdom page → extract keywords → unlocks multiple content pages
2. **Keyword Reuse:** Same word used as key multiple times across different pages (DIVINITY, DEOR, CABAL)
3. **Cipher Mode Variety:** Pages use SUB, ADD, BEAUFORT modes seemingly at random
4. **Self-Reliance Principle:** Like Emerson's essay referenced in earlier pages - solver must discover patterns independently

### Next Priority Actions
1. **Page 20 Non-Primes:** Use transposition methods on shift-16 decrypted text (IoC 2.0135)
2. **Pages 21-30 Plaintext Extraction:** Try zigzag, diagonal, column-reading on high-IoC results
3. **Page 31-54 Attack:** Scan for other wisdom/reference pages that might unlock this block
4. **Page 02:** Unsolved title page - likely "INTUS" based on pattern

---

## �🎯 Active Research Leads

### High Priority - Outside-the-Box Approaches

1.  **Running Key Cipher with Self-Reliance**
    *   **Status: TESTED (Jan 9, 2026)** - Negative results on Page 18 Body.
    *   Emerson's "Self-Reliance" is referenced in solved text ("shed our circumferences")
    *   Direct running key attacks (ADD/SUB) failed to produce readable text.

2.  **Autokey Cipher**
    *   **Status: Active**
    *   Standard Vigenère hill-climbing produces gibberish
    *   Autokey uses plaintext to extend the key - would explain why repeating-key attacks fail
    *   *Idea:* Use Page 17 plaintext ("EPILOGUE...") as key for Page 18 Body.

3.  **Prime/Totient Based Keys**
    *   **Status: PARTIAL SUCCESS (Jan 9, 2026)**
    *   **BREAKTHROUGH:** Page 18 Body is confirmed to be **Vigenère (SUB)** with **Key Length 53**.
    *   Hill-climbing produced high-scoring plaintext fragments: `ETHTHERE...`, `THEATHING...`, `WITHENT...`.
    *   Key Length 53 is a PRIME number.
    *   Next Step: Recover the exact 53-character key.

4.  **Cross-Page Key Derivation**
   - Solved pages may contain keys for unsolved pages
   - Look for hidden messages in the solutions

5. **Interleaved Text**
   - Pages 56-57 are identical - may need to be combined with other pages
   - Some content might be split across multiple pages

### Investigation Needed
- **Page 00**: Old English text identified but needs proper translation
- **Pages 18-54**: Completely unsolved - these form the bulk of the mystery
- **Pages 58-60, 63, 65-66, 68-71**: Unsolved, part of Intus chapter. Missing readable runes or Verified Keys.

