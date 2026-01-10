# LiberPrimus - Decryption Status

**Last Updated:** Jan 2026
**Status:** 🔍 **AUDIT COMPLETE** - False positives identified and corrected

## ⚠️ CRITICAL AUDIT FINDING (Jan 2026)

> **Page 54 "theatheatheatheath" was a FALSE POSITIVE!**
> 
> The hill-climbing solution produced gibberish and has been reverted to UNSOLVED status.
> 
> **Data Integrity Note:** RuneSolver.py has incorrect content for Page 54 (contains Page 0 duplicate). The `runes.txt` files in page folders are the authoritative source.

## 📊 Summary

| Category | Pages | Notes |
|----------|-------|-------|
| ✅ **SOLVED** | 00, 01, 03-17, 55, 56, 57, **59**, **63**, **64**, **68**, 73, 74 | Verified plaintext. |
| ❌ **UNSOLVED** | 02, 18-54, 58, 60-62, 65-67, 69-72 | No verified solution yet. |
| 📄 **IMAGE ONLY** | 65, 66, 69, 70 | No runes to decrypt. |

> **Note:** Pages 18-54 (37 pages) form the main unsolved block with IoC ≈ 0.034, suggesting running key cipher.

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

