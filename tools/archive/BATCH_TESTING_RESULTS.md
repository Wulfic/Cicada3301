# 🔐 LIBER PRIMUS ANALYSIS - BATCH TESTING RESULTS

## Executive Summary

Extensive batch testing was performed on the unsolved pages of Liber Primus (pages 27-52) using the master key derived from the Page 0/54 = Parable relationship.

**Master Key**: 95 indices, Sum = 1331 = 11³
```
[11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5,
 20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27,
 17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14,
 5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7,
 14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23]
```

---

## 🏆 Top Results Summary

### Highest Scoring Combinations

| Rank | Page | Score | Method | Details |
|------|------|-------|--------|---------|
| 1 | 47 | 137 | Columnar width 29 + decrypt | Best with transposition |
| 2 | 47 | 137 | Rail fence 5 + decrypt | Confirms transposition layer |
| 3 | 31 | 139 | Parable pattern matching | rot=27, off=27 |
| 4 | 47 | 117 | gcd(page,95)=1 + XOR | Strong English indicators |
| 5 | 44 | 117 | Length-based key | rot=83, off=12 |
| 6 | 29 | 115 | Interleaved key | rot1=60, rot2=45 |

---

## 🔢 Prime Number Formulas Tested

### Cicada's Known Primes
- 3, 7, 11, 13, 17, 29, 31, 41, 59, 311, 1033, 3301

### Key Modular Values
| Prime | mod 29 | mod 95 |
|-------|--------|--------|
| 311 | 21 | 26 |
| 1033 | 17 | 83 |
| 3301 | 24 | 71 |

### Best Prime-Based Formulas
1. `311-page mod 95, 311-page mod 29` → Page 28 score 106
2. `page*311 mod 95, page*311 mod 29` → Page 45 score 103.5
3. `page mod 31, page mod 11` → Page 45 score 105.5
4. `3301-page mod 95` → Page 48 score 116.5

---

## 🏛️ Latin Text Detection

### Latin Words Found in Decryptions
Common Latin words appearing in high-scoring decryptions:
- **ET** (and) - very frequent
- **AD** (to, toward)
- **DE** (of, from)
- **IN** (in, into)
- **AB** (from, by)
- **EX** (out of)
- **UT** (as, so that)
- **NE** (not, lest)
- **SI** (if)
- **AC** (and)
- **DEO** (god)
- **SOL** (sun)
- **AER** (air)
- **HAEC/HOC/HIC** (this)
- **EST** (is)

This suggests **mixed Latin-English text** or purely Latin text.

---

## 🔀 Transposition Analysis

### Key Finding: Multi-Layer Encryption
The highest scores come from applying **transposition AFTER decryption**:

1. **Columnar Transposition**: Width 29 (number of runes) produces score 137
2. **Rail Fence**: 5 rails produces score 137
3. **Skip Cipher**: Reading every 2nd/3rd character shows patterns

This strongly suggests Cicada used **two encryption layers**:
- Layer 1: Gematria key substitution
- Layer 2: Transposition cipher

---

## 🔄 Interleaved Key Discovery

### Novel Finding
Using **two different rotation values** alternating between even/odd positions:

**Best Result**: Page 29 with rot1=60, rot2=45 → Score 115

This suggests the encryption may use:
- Position-dependent key rotation
- Even positions: one rotation
- Odd positions: different rotation

---

## 📊 Frequency Analysis

### Chi-Square Distance to Expected Distributions
- **Best English Match**: Page 55 (χ² = 44.8)
- **Best Latin Match**: Page 51 (χ² = 35.9)
- Pages 44-48 show mixed English/Latin characteristics

---

## 🎯 Page-Specific Recommendations

Based on pattern matching with the solved Parable:

| Page | Best Parameters | Score | Recommendation |
|------|-----------------|-------|----------------|
| 27 | rot=27*1, off=0 | 157 | Try transposition |
| 28 | rot=93, off=22 (311-page) | 106 | Strong Latin |
| 29 | Interleaved (60,45) | 115 | Dual key approach |
| 30 | rot=45, off=4 | 118 | Try skip cipher |
| 31 | rot=27, off=27 | 139 | Highest pattern match! |
| 44 | rot=37, off=15 | 112 | Check Latin |
| 45 | rot=15, off=14 | 129 | Very promising |
| 46 | rot=31, off=23 | 123 | Strong patterns |
| 47 | Columnar w=29 | 137 | Transposition key! |
| 48 | rot=53, off=7 | 108 | Contains "THING" |
| 52 | rot=11, off=17 | 118 | Check Latin |

---

## 💡 Hypotheses to Explore

1. **Multi-Layer Encryption**: Decrypt first, then apply columnar transposition
2. **Variable Key Rotation**: Each page may use `page * prime mod 95` for rotation
3. **Latin-First Pages**: Some pages may be fully in Latin, requiring translation
4. **Interleaved Keys**: Alternating rotation values for even/odd positions
5. **Skip Cipher**: Final plaintext may need character skipping

---

## 📁 Scripts Created

1. `tools/comprehensive_test_suite.py` - Main testing infrastructure
2. `tools/deep_dive_best_results.py` - Focused analysis on top results
3. `tools/extract_top_results.py` - Full text extraction
4. `tools/benchmark_analysis.py` - Comparison with solved Parable

---

## Next Steps

1. **Focus on Page 47**: Apply columnar transposition width 29 after decryption
2. **Investigate Page 31**: Has highest Parable pattern match (139)
3. **Try Latin Translation**: For pages with high Latin word counts
4. **Combine Layers**: Systematically try decrypt → transpose → score
5. **Variable Rotation per Page**: Test if each page uses different prime formula

---

*Analysis performed: Session date*
*Tools used: Python 3.12.10 with custom cipher analysis scripts*
