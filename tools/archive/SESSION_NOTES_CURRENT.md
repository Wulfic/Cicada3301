# Liber Primus Analysis Session Summary
## Date: Session following 2026-01-04 analysis

---

## 🔑 KEY VERIFIED FACTS

### The Master Key (LENGTH=95, SUM=1331=11³)
```python
MASTER_KEY = [
    11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
    20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
    17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
    5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
    14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23
]
```

### Which Pages Work With Master Key?
| Page Range | Status | Method |
|------------|--------|--------|
| Pages 0-24 | ✅ SOLVED | Vigenère with master key |
| Pages 25-26 | ⚠️ UNCLEAR | May need investigation |
| Pages 27-31 | ❌ UNSOLVED | Different key/method |
| Pages 32-39 | ⚠️ UNCLEAR | Some may be solved |
| Pages 40-41 | ❌ UNSOLVED | Different key/method |
| Pages 42-43 | ⚠️ UNCLEAR | May need investigation |
| Pages 44-48 | ❌ UNSOLVED | Different key/method |
| Pages 49-53 | ⚠️ UNCLEAR | Some may be solved |
| Page 54 | ✅ SOLVED | IDENTICAL to Page 0 |
| Pages 55 | ⚠️ UNCLEAR | May need investigation |
| Page 56 | ✅ SOLVED | Prime+57 shift cipher |
| Page 57 | ✅ PLAINTEXT | "The Parable" - no encryption |

### Circular Nature
- **Pages 0 and 54 are IDENTICAL** (ciphertext matches exactly)
- This confirms the Liber Primus has circular structure

---

## 📊 STATISTICAL ANALYSIS RESULTS

### Index of Coincidence
| Page | IC Value | Interpretation |
|------|----------|----------------|
| Random | 0.0345 (1/29) | Polyalphabetic/random |
| English | ~0.0667 | Natural language |
| Unsolved pages | 0.0344-0.0356 | ≈ RANDOM → confirms polyalphabetic |

### Kasiski Test Results
- Only 3 repeated sequences found in Page 27
- GCD of distances = 1
- **Conclusion**: Key is very long or non-repeating

### Entropy Analysis
- Maximum (29 symbols): 4.858 bits
- Solved pages (decrypted): 4.79 bits
- Unsolved pages (ciphertext): 4.73-4.76 bits

---

## 🔍 WHAT WE TESTED ON UNSOLVED PAGES

### Cipher Methods Tested
1. ❌ **All 95 key offsets** - None produce readable text
2. ❌ **All 29 Caesar shifts** - Best scores 50-63, still gibberish
3. ❌ **Key reversals/inversions** - No improvement
4. ❌ **Key XOR with various values** - No improvement
5. ❌ **Autokey cipher** (master key + previous ciphertext) - Failed
6. ❌ **Gematria-based key modifications** - Failed
7. ❌ **Page number as key modifier** - Failed
8. ❌ **Word positions as key offsets** - Failed

### Key Recovery Attempts
- Used frequency analysis to recover "most likely" key for each page
- **CRITICAL FINDING**: Recovered keys are DIFFERENT from master key
- Recovered keys don't match each other either (0-8/95 random matches)

### Recovered Keys (First 20 Positions)
```
Page 27: [10, 3, 11, 17, 1, 8, 6, 9, 13, 5, 3, 8, 21, 4, 17, 2, 20, 10, 24, 20]
Page 28: [26, 25, 0, 1, 21, 20, 11, 12, 3, 13, 1, 18, 5, 4, 6, 8, 19, 13, 20, 5]
Page 29: [13, 7, 17, 28, 0, 4, 10, 8, 21, 26, 11, 2, 1, 23, 23, 17, 16, 21, 6, 28]
Page 44: [10, 15, 17, 15, 7, 12, 20, 28, 18, 0, 2, 6, 27, 7, 15, 10, 15, 6, 3, 11]
Master:  [11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5]
```

---

## 💡 KEY INSIGHTS

### 1. The 2016 Clue: "NUMBERS are the direction"
We discovered the page-to-word mapping:
- Page N → Word (N-20) in the Parable
- Example: Page 27 → Word 7 ("SURFACE")
- This may hint at key derivation, but didn't crack the cipher

### 2. Why Master Key Doesn't Work
- The differences between recovered keys and master key are **inconsistent**
- No simple transformation (add, XOR, multiply) maps master key to unsolved key
- Unsolved pages likely use:
  - A completely different key derivation
  - OR an additional encryption layer
  - OR external key sources (steganography, book cipher, etc.)

### 3. Pattern in Unsolved Pages
- Pages 27-31 are consecutive → possibly a section
- Pages 44-48 are consecutive → possibly another section
- Pages 40-41 are adjacent to solved pages
- Pages 52 is isolated

---

## 🚀 RECOMMENDED NEXT STEPS

### High Priority
1. **Steganography Analysis**
   - Run outguess on original LP images for unsolved pages
   - Check for LSB hidden data
   - The original images at `2014/Liber Primus/A drop box of all unmodified files/` may contain keys

2. **Book Cipher Investigation**
   - Test "Book of the Law" by Aleister Crowley
   - Test "Self-Reliance" by Emerson
   - Use word/letter positions as key elements

3. **Latin Plaintext Testing**
   - Rerun frequency analysis assuming LATIN vocabulary
   - Test common Latin words as cribs: "ET", "IAM", "SED", "NON"

### Medium Priority
4. **Two-Layer Encryption**
   - Try decrypting with master key THEN applying another cipher
   - Test transposition after Vigenère
   - Test substitution after Vigenère

5. **External Key Sources**
   - Analyze the MIDI file puzzle
   - Check the phone recording for hidden data
   - Look for keys in PGP messages

6. **Community Research**
   - Check Uncovering Cicada wiki for recent discoveries
   - Review Discord/IRC findings since 2014

---

## 📁 TOOLS CREATED THIS SESSION

| File | Purpose |
|------|---------|
| `tools/numbers_analysis.py` | Analyze 2016 "NUMBERS" clue |
| `tools/page_word_mapping.py` | Map pages to Parable words |
| `tools/page_number_tests.py` | Test page numbers as key modifiers |
| `tools/page_plus_one_test.py` | Test (pg+1) as shift |
| `tools/optimal_caesar.py` | Find best Caesar shift per page |
| `tools/caesar_full_output.py` | View full Caesar decryptions |
| `tools/advanced_analysis.py` | Word boundaries, autokey, running key |
| `tools/gematria_cipher_test.py` | Test Gematria-based keys |
| `tools/solved_analysis.py` | Analyze solved page patterns |
| `tools/key_recovery.py` | Try to recover key fragments |
| `tools/offset_analysis.py` | IC, Kasiski, offset patterns |
| `tools/second_layer.py` | Crib dragging, XOR variations |
| `tools/key_relationship.py` | Compare recovered keys to master |
| `tools/final_analysis.py` | Entropy, statistical summary |

---

## 📝 FINAL ASSESSMENT

### What We Know For Certain
1. ✅ Master key (length=95, sum=1331) is CORRECT for solved pages
2. ✅ Pages 0 and 54 are IDENTICAL (circular structure)
3. ✅ Page 57 is plaintext (The Parable)
4. ✅ Page 56 uses prime+57 shift cipher
5. ✅ Unsolved pages are polyalphabetic (IC ≈ 0.035)

### What We Strongly Suspect
1. 🔶 Unsolved pages use a DIFFERENT key than master key
2. 🔶 Each unsolved page may have its own unique key
3. 🔶 Key derivation method involves external information
4. 🔶 The plaintext is likely English (word lengths match)

### What Remains Unknown
1. ❓ How the key for unsolved pages is derived
2. ❓ Whether there's a second encryption layer
3. ❓ What external sources (steganography, books) provide keys
4. ❓ The full extent of which pages are "solved" vs "unsolved"

---

*"Like the instar, tunneling to the surface. We must shed our own circumferences. Find the divinity within and emerge."*
— The Parable
