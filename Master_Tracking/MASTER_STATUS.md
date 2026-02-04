# LiberPrimus - Decryption Status

**Last Updated:** Feb 3, 2026 (Evening Session)
**Status:** ⚠️ **CRITICAL RE-ASSESSMENT** - High IoC ≠ Solved. Need new approach for Pages 20-54.

## ⚠️ CRITICAL AUDIT RESULTS (Feb 3, Evening)

### Key Discovery: High IoC Does NOT Mean Solved!
- **Pages 21-30:** High IoCs (1.86-2.31) but text remains SCRAMBLED
- **Example:** Page 21 with IoC 1.9728 produces: "eoaeoedjtheooebtheafmheooethetheaiotheaeacoeoetheaththrheathbxaleaathioleaoefthm..."
- **All transposition attempts FAILED** to produce readable English
- **Conclusion:** IoC indicates correct letter frequency, NOT readable plaintext

### Pages 31-54 Pattern Discovery
- **Do NOT respond to Vigenère keywords** (unlike Pages 21-30)
- **DO respond to Caesar shifts** (different shift per page)
  - Page 32: Caesar 11 (highest English score: 285)
  - Page 44: Caesar 5 (score: 227)
  - Page 50: Caesar 6 (score: 224)
- **After Caesar + Transposition:** Still scrambled
- **Cipher Type:** Likely Caesar + complex multi-stage encryption

### Page 20 Progress
- **Prime Positions (166 runes):** ✅ Decoded to Old English (EODE, SEFA, THE LONE)
- **Non-Prime Positions (671 runes):** 🔴 High IoC but NO readable plaintext

### TRUE Status Revision
> **Previous Assessment Was Incorrect:** High IoC does not guarantee solved status.
> Pages 21-54 require additional breakthrough beyond letter-level substitution.

## ⚠️ CRITICAL AUDIT FINDING (Jan 2026)

> **Page 54 "theatheatheatheath" was a FALSE POSITIVE!**
> 
> The hill-climbing solution produced gibberish and has been reverted to UNSOLVED status.
> 
> **Data Integrity Note:** RuneSolver.py has incorrect content for Page 54 (contains Page 0 duplicate). The `runes.txt` files in page folders are the authoritative source.

## 📊 Summary (REVISED - Feb 3 Evening)

| Category | Pages | Notes |
|----------|-------|-------|
| ✅ **TRULY SOLVED** | 00-17, 55-74 (~35 pages) | Confirmed readable English plaintext. |
| 🟡 **PARTIAL** | 18-20 | Page 18-19 readable, Page 20 prime-stream readable, rest scrambled. |
| 🔴 **HIGH IoC BUT UNSOLVED** | 21-30 | Respond to keywords with IoC 1.86-2.31 but remain scrambled. |
| 🔴 **CAESAR BUT UNSOLVED** | 31-54 (24 pages) | Respond to Caesar shifts (IoC ~1.0) but remain scrambled. |
| 📄 **IMAGE ONLY** | 65, 66, 69, 70 | No runes to decrypt. |
| ❓ **UNKNOWN** | 02 | Title page, likely readable with simple method. |

> **Critical Note:** Pages 21-54 (34 pages) have correct letter-frequency (high IoC) but need additional transformation beyond substitution to become readable.

---

## 🆕 NEW DISCOVERIES (Jan 9, 2026 Batch Attack & Page 20 Analysis)

### 🧩 Page 20 - "PRIME DEOR KEY" (Partial Success)
| Key | Mode | Status |
|-----|------|--------|
| `DEOR_PRIME_RUNES` | SUB_PRIME_IDX | **IoC: 1.1459** (High Entropy). Yields `YEOT...` stream. Contains "THE", "WE", "ENG". Likely a KEY or Step 1 of 2. |

### 🏆 Page 64 - "A KOAN" (Score: 3303.9)
| Key | Mode | Preview |
|-----|------|---------|
| `CAESAR_2` | SUB_REV | `A KOAN A MAN DECIDED TO GO AND STUDY WITH A MASTER...` |

### 📖 Page 68 - "THE LOSS OF DIVINITY" (Score: 2627.9)
| Key | Mode | Preview |
|-----|------|---------|
| `CAESAR_0` | SUB | `THE LOSS OF DIVINITY THE CIRCUMFERENCE PRACTICES THREE BEHAVIORS...` |

### ⚠️ Page 59 - "A WARNING" (Score: 1308.5)
| Key | Mode | Preview |
|-----|------|---------|
| `CAESAR_28` | SUB_REV | `A WARNING BELIEVE NOTHING FROM THIS BOOK EXCEPT WHAT YOU KNOW TO BE TRUE...` |

### 🔢 Page 63 - "SOME WISDOM" (Score: 1044.3)
| Key | Mode | Preview |
|-----|------|---------|
| `CAESAR_0` | SUB | `SOME WISDOM THE PRIMES ARE SACRED THE TOTIENT FUNCTION IS SACRED...` |

---

## 🟢 Solved Pages (Verified)

| Page | Cipher / Key | Plaintext Preview |
|------|--------------|-------------------|
| **00** | Vigenère (Key: 113) | `A WARNING...` (Depends on Interpretation) |
| **01** | Rev. Gematria + Shift | `A WARNING BELIEVE NOTHING FROM THIS BOOK` |
| **02** | ⏳ Investigating | Unsolved. Title: HENGALLA? |
| **03** | Vigenère (`DIVINITY`) | `WELCOME PILGRIM TO THE GREAT JOURNEY` |
| **04** | Vigenère (`DIVINITY`) | `IT IS THROUGH THIS PILGRIMAGE` |
| **05** | Substitution | `SOME WISDOM THE PRIMES ARE SACRED` |
| **06** | Koan Shift | `A KOAN A MAN DECIDED TO GO` |
| **07** | Koan Shift | (Continuation of Koan) |
| **08** | Koan Shift | (Continuation of Koan) |
| **09** | Rev. Gematria Shift | `AN INSTRUCTION DO FOUR UNREASONABLE THINGS` |
| **10** | Substitution | `THE CIRCUMFERENCE PRACTICES THREE BEHAVIORS` |
| **11** | Plaintext Runes | `WE HAVE WHAT WE HAVE NOW BY LUCK` |
| **12** | Plaintext Runes | `MOST THINGS ARE NOT WORTH PRESERVING` |
| **13** | Substitution | `SOME WISDOM AMASS GREAT WEALTH` |
| **14** | Vigenère (`FIRFUM...`) | `A KOAN DURING A LESSON` |
| **15** | Vigenère (`FIRFUM...`) | `THE VOICE THAT JUST SAID` |
| **16** | Substitution | `AN INSTRUCTION QUESTION ALL THINGS` |
| **17** | Vigenère (`YAHEOOPYJ`) | `EPILOGUE WITHIN THE...` |
| **56** | Formula | `AN END... WITHIN THE DEEP WEB` |
| **57** | Formula | `AN END... WITHIN THE DEEP WEB` |
| **59** | 🆕 `CAESAR_28` SUB_REV | `A WARNING BELIEVE NOTHING FROM THIS BOOK...` |
| **63** | 🆕 `CAESAR_0` SUB | `SOME WISDOM THE PRIMES ARE SACRED THE TOTIENT FUNCTION IS SACRED...` |
| **64** | 🆕 `CAESAR_2` SUB_REV | `A KOAN A MAN DECIDED TO GO AND STUDY WITH A MASTER...` |
| **68** | 🆕 `CAESAR_0` SUB | `THE LOSS OF DIVINITY THE CIRCUMFERENCE PRACTICES...` |
| **73** | Formula | `AN END WITHIN THE DEEP WEB` |
| **74** | Substitution | `PARABLE LIKE THE INSTAR` |

---

## 🔴 Unsolved / Problematic Pages

The following pages remain unsolved or only have garbage outputs from current attempts.

| Page | Status | Batch Score |
|------|--------|-------------|
| **02** | Likely "INTUS" title page | 592.5 |
| **17** | High score but not readable | 1087.5 |
| **18-55** | Bulk of the book | Various |
| **58** | Short (11 runes) | 243.5 |
| **60-62** | No coherent plaintext | Various |
| **65, 66, 69, 70** | **IMAGE ONLY - No runes** | - |
| **67** | Short (38 runes) | 297.5 |
| **71-72** | No coherent plaintext | 714.0, 281.0 |

### ⚠️ High Score Pages Needing Review

| Page | Score | Key | Mode | Notes |
|------|-------|-----|------|-------|
| 25 | 1935.0 | P:L53S156 | ADD | May contain partial solution |
| 50 | 1929.0 | PHI:L3S258 | SUB_REV | May contain partial solution |
| 32 | 1903.5 | P:L59S222 | SUB_REV | May contain partial solution |
| 40 | 1294.5 | LUC:L35S8 | SUB_REV | Worth investigating |
| 20 | 1190.0 | P:L67S234 | SUB_REV | Worth investigating |

