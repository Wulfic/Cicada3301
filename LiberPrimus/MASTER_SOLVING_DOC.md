# LIBER PRIMUS - MASTER SOLVING DOCUMENT
## Cicada 3301 (2014) Cryptographic Analysis

> **Note:** Full decryption outputs and detailed page analysis have been moved to individual page README files. See [pages/page_XX/README.md](pages/) for complete details.
> 
> Archived full document: [archive/MASTER_SOLVING_DOC_FULL.md](archive/MASTER_SOLVING_DOC_FULL.md)

---

## 📊 Project Status At-A-Glance

| Category | Count | Pages |
|----------|-------|-------|
| ✅ **FULLY SOLVED** | 2 | [56](pages/page_56/README.md), [57](pages/page_57/README.md) |
| 🔄 **FIRST-LAYER COMPLETE** | 6 | [0](pages/page_00/README.md)-[5](pages/page_05/README.md) |
| ❌ **UNSOLVED** | 51 | 6-55 |
| 📝 **NEEDS TRANSCRIPTION** | 16 | 58-74 |

**Bottom Line:** ~97% unsolved. First-layer decryption complete for pages 0-5. Output is **Runeglish** (Old English transliterated from runes), not garbled text. Requires translation.

---

## 🔑 Core Breakthroughs

| # | Discovery | Impact |
|---|-----------|--------|
| 1 | **SUB mod 29, NOT XOR** | Achieves 100% reversibility |
| 2 | **Key lengths are ALL PRIME** | 71 (P1, P5), 83 (P2, P3, P4), 113 (P0) |
| 3 | **Each page has unique key** | Hill climbing found unique optimal keys per page. |
| 4 | **Output is Runeglish** | `feadaþ`, `eþeia`, `dæþ` - Old English vocabulary. |
| 5 | **Hyphens = word boundaries** | Preserved through encryption |
| 5 | **Pages 56 & 57 identical** | Calibration reference |
| 6 | **Multi-layer encryption** | First-layer ≠ final plaintext |
| 7 | **"IP" primer [10,13] helps** | +59% to +145% score improvement |

---

## 📋 Page Quick Reference

### Key Length Distribution

| Key | Prime# | Pages | Count |
|-----|--------|-------|-------|
| **71** | 20th | 1,5,8,9,13,15,17,18,21-23,27,29,31-33,36,48,54,55 | 20 |
| **83** | 23rd | 2,3,6,7,11,24,38,41,42 | 9 |
| **79** | 22nd | 14,28,30,39,46,50,53 | 7 |
| **89** | 24th | 16,25,26,40,43,51 | 6 |
| **103** | 27th | 4,12,19,34 | 4 |
| **101** | 26th | 35,37,47,52 | 4 |
| **97** | 25th | 20,44 | 2 |
| **113** | 30th | 0 | 1 |
| **137** | 33rd | 10 | 1 |
| **107** | 28th | 45 | 1 |

### Output Pattern Types

| Type | Characteristics | Pages |
|------|-----------------|-------|
| **Type A** | THE-heavy (28% TH), Old English patterns | 0, 1, 5 |
| **Type B** | EMB prefix, transitions to English-like | 2, 3, 4, 6-11 |

---

## 🔬 Proven Methodology

### Decryption Formula
```
plaintext[i] = (cipher[i] - key[i mod keylen]) mod 29
```

### Verification (MANDATORY)
```
re_encrypted[i] = (plaintext[i] + key[i mod keylen]) mod 29
MUST match original cipher 100%
```

### Process
1. **IoC analysis** → Find prime key length
2. **Frequency attack** → Initialize key (assume common rune → E)
3. **SUB decryption** → Apply subtraction mod 29
4. **Verify reversibility** → Must be 100%
5. **Hill-climb** → Optimize key for English score
6. **Check interleaving** → Test every-Nth patterns

---

## 🔎 Key Discoveries Summary

### From Solved Pages (56-57)

| Discovery | Details |
|-----------|---------|
| **Page 56 cipher** | `plaintext = (cipher - (prime + 57)) mod 29` |
| **Deep web hash** | SHA-512 pointing to undiscovered onion page |
| **Word preservation** | Hyphen structure maps 1:1 to English |
| **Section marker §** | May indicate "Section 6" of numbered sections |

→ Full details: [pages/page_56/README.md](pages/page_56/README.md)

### From First-Layer Analysis (Pages 0-5)

| Discovery | Details |
|-----------|---------|
| **TH anomaly** | 28% TH is actually 28% Rune `ᚦ` (Thorn) - consistent with Old English usage |
| **Runeglish Text** | Decrypted output is NOT garbled but transliterated Old English |
| **Identified Words** | `FLETH` (Dwelling), `HATHEN` (Heathen), `DOETH`, `GOETH`, `THAT` |
| **Word Boundaries** | Hyphens in original runes mark actual word boundaries |
| **Autokey "PI"** | Starts with "TH" - promising (likely incorrect - Vigenère confirmed) |
| **EMB prefix** | Pages 2-4 have E/M/B heavy start |

→ Full details: [pages/page_00/README.md](pages/page_00/README.md)

### From Community Research

| Discovery | Source |
|-----------|--------|
| **Totient sacred** | "Some Wisdom" onion page |
| **Gap of 11** | IRC (Profetul, Mortlach) |
| **Magic square 1033** | Solved pages |
| **Skip indices** | F-rune skipping at specific positions |

---

## 📚 The Gematria Primus

### 29-Character Cipher Alphabet

| Idx | Rune | Letter | Prime | | Idx | Rune | Letter | Prime |
|-----|------|--------|-------|---|-----|------|--------|-------|
| 0 | ᚠ | F | 2 | | 15 | ᛋ | S | 53 |
| 1 | ᚢ | U/V | 3 | | 16 | ᛏ | T | 59 |
| 2 | ᚦ | TH | 5 | | 17 | ᛒ | B | 61 |
| 3 | ᚩ | O | 7 | | 18 | ᛖ | E | 67 |
| 4 | ᚱ | R | 11 | | 19 | ᛗ | M | 71 |
| 5 | ᚳ | C/K/Q | 13 | | 20 | ᛚ | L | 73 |
| 6 | ᚷ | G | 17 | | 21 | ᛝ | NG | 79 |
| 7 | ᚹ | W | 19 | | 22 | ᛟ | OE | 83 |
| 8 | ᚻ | H | 23 | | 23 | ᛞ | D | 89 |
| 9 | ᚾ | N | 29 | | 24 | ᚪ | A | 97 |
| 10 | ᛁ | I | 31 | | 25 | ᚫ | AE | 101 |
| 11 | ᛂ | J | 37 | | 26 | ᚣ | Y | 103 |
| 12 | ᛇ | EO | 41 | | 27 | ᛡ | IA/IO | 107 |
| 13 | ᛈ | P | 43 | | 28 | ᛠ | EA | 109 |
| 14 | ᛉ | X/Z | 47 | | | | | |

### Key Digraphs
- **ᚦ** = TH (THE, THAT)
- **ᛝ** = NG/ING (THING, BEING)
- **ᛠ** = EA (EACH, IDEA)
- **ᛡ** = IA/IO (RATIO, MEDIA)

### Text Symbols
| Symbol | Meaning |
|--------|---------|
| `-` | Word separator (**CRITICAL**) |
| `.` | Sentence end |
| `&` | Section marker |
| `§` | Page/section end |

---

## 🎯 Active Research Leads

### High Priority
1. **Translation of Pages 0-5** - Decrypted text is Old English/Runeglish. Needs translation.
   - Page 0: `æþatæyeþ-esþes...` -> Contains `FLETH` (Dwelling), `HATHEN` (Heathen).
2. **Interleaving** - Every-2nd-char shows promise
3. **Old English segmentation** - DOETH, GOETH, HATH patterns confirmed.

### Medium Priority
5. **Skip indices via Fibonacci-Lucas** - F-rune positions
6. **Gap of 11 pattern** - Key derivation
7. **Totient-based transformations** - φ(p) = p-1

### Low Priority (Long Shots)
8. **Magic square 1033** - Transposition key?
9. **Cross-page relationships** - Same key lengths
10. **Section 6 theory** - Pages 56-57 as missing section

---

## 📁 Repository Structure

```
LiberPrimus/
├── MASTER_SOLVING_DOC.md      ← You are here
├── GEMATRIA_PRIMUS.md         ← Alphabet reference
├── pages/
│   ├── page_00/README.md      ← Full page analysis
│   ├── page_01/README.md
│   ├── ...
│   └── page_74/README.md
├── reference/
│   ├── research/              ← Source materials
│   ├── solved_pages/          ← Confirmed solutions
│   └── transcripts/           ← IRC logs, etc.
├── tools/                     ← Python analysis scripts
└── archive/
    └── MASTER_SOLVING_DOC_FULL.md  ← Original detailed doc
```

---

## 🔗 Quick Links

| Resource | Location |
|----------|----------|
| Page 0 (Cover) | [pages/page_00/README.md](pages/page_00/README.md) |
| Page 56 (Solved) | [pages/page_56/README.md](pages/page_56/README.md) |
| Page 57 (Solved) | [pages/page_57/README.md](pages/page_57/README.md) |
| Full Gematria | [GEMATRIA_PRIMUS.md](GEMATRIA_PRIMUS.md) |
| All Tools | [tools/](tools/) |
| Full Archive | [archive/MASTER_SOLVING_DOC_FULL.md](archive/MASTER_SOLVING_DOC_FULL.md) |

---

**Last Updated:** January 8, 2026
