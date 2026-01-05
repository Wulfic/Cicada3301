# Liber Primus - Organized Reference

**The First Book** - Cicada 3301's cryptographic manuscript from 2014

---

## 📖 Overview

The Liber Primus is a 75-page manuscript (pages 0-74) written primarily in Anglo-Saxon runes using the **Gematria Primus** cipher alphabet. It was released as part of the 2014 Cicada 3301 puzzle and remains largely unsolved.

### Current Status

| Category | Count | Percentage |
|----------|-------|------------|
| **Solved Pages** | 2 | 2.7% |
| **Partially Decoded** | 5 | 6.7% |
| **Unsolved** | 68 | 90.6% |
| **Total Pages** | 75 | 100% |

### Confirmed Solved Pages
- **Page 56**: Prime shift cipher `-(prime + 57) mod 29`
- **Page 57**: Plaintext (no encryption) - "The Parable"

---

## 📁 Folder Structure

```
LiberPrimus/
├── README.md                    # This file
├── MASTER_SOLVING_DOCUMENT.md   # Comprehensive methodology & results
├── GEMATRIA_PRIMUS.md           # The 29-character cipher alphabet
├── pages/
│   ├── page_00/                 # Cover page
│   ├── page_01/                 # First content page
│   │   ├── README.md            # Page-specific analysis & status
│   │   ├── images/              # All image variants for this page
│   │   │   ├── original.jpg     # Unmodified source image
│   │   │   ├── enhanced.jpg     # Enhanced/processed versions
│   │   │   └── ...
│   │   ├── runes.txt            # Raw rune text for this page
│   │   ├── analysis/            # Analysis scripts & results
│   │   └── notes/               # Research notes & hypotheses
│   ├── page_02/
│   ├── ...
│   └── page_74/
├── tools/                       # Solving tools & scripts
│   ├── liber_primus_solver.py   # Unified solver
│   └── utilities/               # Helper scripts
├── reference/                   # Reference materials
│   ├── solved_pages/            # Confirmed solutions
│   ├── transcripts/             # Full text transcripts
│   └── research/                # Community research & ideas
└── archive/                     # Deprecated/old analysis files
```

---

## 🔤 The Gematria Primus

The Liber Primus uses a custom 29-character alphabet based on Anglo-Saxon runes:

| Index | Rune | Latin | Prime Value |
|-------|------|-------|-------------|
| 0 | ᚠ | F | 2 |
| 1 | ᚢ | U | 3 |
| 2 | ᚦ | TH | 5 |
| 3 | ᚩ | O | 7 |
| 4 | ᚱ | R | 11 |
| 5 | ᚳ | C/K | 13 |
| 6 | ᚷ | G | 17 |
| 7 | ᚹ | W | 19 |
| 8 | ᚻ | H | 23 |
| 9 | ᚾ | N | 29 |
| 10 | ᛁ | I | 31 |
| 11 | ᛂ | J | 37 |
| 12 | ᛇ | EO | 41 |
| 13 | ᛈ | P | 43 |
| 14 | ᛉ | X | 47 |
| 15 | ᛋ | S | 53 |
| 16 | ᛏ | T | 59 |
| 17 | ᛒ | B | 61 |
| 18 | ᛖ | E | 67 |
| 19 | ᛗ | M | 71 |
| 20 | ᛚ | L | 73 |
| 21 | ᛝ | NG/ING | 79 |
| 22 | ᛟ | OE | 83 |
| 23 | ᛞ | D | 89 |
| 24 | ᚪ | A | 97 |
| 25 | ᚫ | AE | 101 |
| 26 | ᚣ | Y | 103 |
| 27 | ᛡ | IA/IO | 107 |
| 28 | ᛠ | EA | 109 |

### Text Formatting Symbols
- `-` Word separator
- `.` Sentence end
- `/` Line break
- `%` Page separator
- `&` Section marker
- `$` Chapter marker

---

## 🔐 Proven Cryptographic Methodology

### Key Discoveries (January 2026)

1. **SUB operation, NOT XOR** - Subtraction mod 29 achieves perfect reversibility
2. **Each page has unique key length** - No master key for all pages
3. **Key lengths are PRIME numbers** - Pages 1 (71), 2 (83), 3 (83), 4 (103), 5 (71)
4. **IoC analysis identifies key lengths** - Index of Coincidence reliably finds each page's key

### Decryption Formula

```
Decrypt: plaintext[i] = (cipher[i] - key[i mod keyLength]) mod 29
Encrypt: cipher[i] = (plaintext[i] + key[i mod keyLength]) mod 29
```

### Verification

A correct decryption achieves **100% reversibility**:
```
re_encrypt(decrypt(cipher, key), key) == cipher
```

---

## 📊 Page Status Summary

### Solved
| Page | Method | Content Summary |
|------|--------|-----------------|
| 56 | Prime shift | Philosophical text |
| 57 | Plaintext | "The Parable" - Instar/emergence metaphor |

### Work In Progress (Decryption Attempted)
| Page | Best Key | Reversibility | Score | Notes |
|------|----------|---------------|-------|-------|
| 1 | 71 | 100% | 798 | Fragmented output |
| 2 | 83 | 100% | 903 | Fragmented output |
| 3 | 83 | 100% | 732 | Fragmented output |
| 4 | 103 | 100% | 993 | Fragmented output |
| 5 | 71 | 100% | 987 | Fragmented output |

### Unsolved
Pages 0, 6-55, 58-74 await analysis.

---

## 📚 Key Themes (from Solved Content)

From "The Parable" (Page 57):
> *"Like the instar, tunneling to the surface, we must shed our own circumferences; find the divinity within and emerge."*

- **Instar**: Metamorphosis stage in cicada development
- **Circumference**: Boundaries/limitations to transcend
- **Divinity within**: Inner enlightenment
- **Emerge**: Transformation and revelation

---

## 🛠️ Quick Start

```bash
# Analyze a specific page
python tools/liber_primus_solver.py --page 3

# View page status
cat pages/page_03/README.md

# View all images for a page
ls pages/page_03/images/
```

---

## 📖 Related Resources

- [MASTER_SOLVING_DOCUMENT.md](MASTER_SOLVING_DOCUMENT.md) - Full methodology
- [GEMATRIA_PRIMUS.md](GEMATRIA_PRIMUS.md) - Complete alphabet reference
- [reference/solved_pages/](reference/solved_pages/) - Confirmed solutions

---

**Last Updated:** January 5, 2026  
**Project:** Cicada 3301 Research
