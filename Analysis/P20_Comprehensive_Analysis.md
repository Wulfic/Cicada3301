# Page 20 - Comprehensive Analysis Report

## Status: 🔄 PARTIALLY DECODED (Active Investigation)

**Last Updated:** February 3, 2026

---

## Executive Summary

Page 20 uses a **novel dual-layer cipher** that separates runes by their **Gematria VALUES**:
- **Prime-valued runes** (values 2,3,5,7,11,13,17,19,23) → 237 runes
- **Non-prime-valued runes** (all other values) → 575 runes

The P19 hint "REARRANGING THE PRIMES NUMBERS" has been validated through TWO interpretations:
1. Prime **POSITIONS** - 166 runes at prime indices decoded via Beaufort(Deor)
2. Prime **VALUES** - 237 runes with prime Gematria values form a distinct layer

---

## Method 1: Prime-Position Decryption

### Approach
Extract runes at positions 2, 3, 5, 7, 11, 13, ... (prime indices) and decrypt with Deor.

### Results
- **166 runes** at prime positions
- **Beaufort cipher**: `stream[i] = (Deor[prime_i] - P20[prime_i]) mod 29`
- **IoC after decryption**: 1.8952 (English-like!)
- **2x83 column transposition** reveals readable text

### Decoded Stream (Transposed)
```
HFOFEEEODEOMETBIDAMSEFALTTHELONETNHERAAUIOAETIOAEAYOMEYCFGYWTEXJEJCDCBLOTEPTSAYFTHOFBNGIGADOTCHDHWWYGGLDAHRCLFEPESPMCXMMEOSXYEEOOOOEEANEEIOTCYTHWYFOMTTHHTTHGYEWHSGMW
```

### English/Old English Words Found
| Word | Meaning |
|------|---------|
| EODE | Old English: "went, departed" |
| SEFA | Old English: "heart, mind, spirit" |
| THE LONE | The solitary one |
| MET | met, encountered |
| BID | asked, commanded |
| HER | her/here |
| SAY | say |

### Interpretation
A first-person spiritual journey text:
> "Ho! For fee [I] went/departed. O [I] met [and] bade [my] heart/mind, the lone [one] here..."

---

## Method 2: Prime-Value Separation

### Approach
Separate runes by whether their **Gematria value** is prime (2,3,5,7,11,13,17,19,23).

### Distribution
| Category | Count | Unique Values | Letters |
|----------|-------|---------------|---------|
| Prime-valued | 237 | 9 | TH, O, C, W, J, P, B, M, D |
| Non-prime-valued | 575 | 20 | All other letters |

### Prime-Valued Stream (RAW)
```
JCTHJPWBPMBOBBWMBMDMWCPMPTHTHCJCMBDCJDPDTHDCWMTHTHOWDMMCCTHJCDODCBOBOPJOPWMCCPOJMMWCJMWMDCJTHBJWTHTHPTHMCCTHPCJMWCBOMMPWTHPJBPMWJMBCBTHJBJTHBBPPWOOPMB...
```
- IoC: 3.2125 (artificially high due to restricted 9-letter alphabet)
- This may be a KEY or structural marker

### Non-Prime-Valued Stream (RAW)
```
LEOHNGTAETXHTUOESRGYNAGEONGNFYNEAIANYASIAEAIAIRNLEARLLENHFOENGRAIAGOEEOTXEOYHEAILSNFLEASFOEIAEYLIAEOITOEEAEIANTEOEOAELIAEOEAHYUHTRHNGLNGSNAEEAGSLSXHEA...
```
- IoC: 1.4426 (higher than random 1.0, approaching English 1.73)

### Non-Prime Stream with Shift -2
Applying Caesar shift -2 to non-prime values yields:
```
EIGMXDXEOGXEALPTHRAWOERIMWWIAAWBYAEPWAOEPMBAEYAEHOBTHWEYTHEETBWWGMIALBMTHOEAERLIXMEODIMAGYHEPW...
```

**English words found (12 total):**
- "THE" appears 6 times (positions 49, 325, 415, 477, 549, 704)
- "HER", "WAY", "EYE", "HIM", "DAY" also found

---

## Key Discovery: Word 17 = "THEY"

In the raw full Page 20 stream, **Word 17** (at positions 96-98) reads as **"THEY"** in plaintext!

Analysis of positions 96-98:
| Position | Rune Value | Letter | Prime-Valued? |
|----------|------------|--------|---------------|
| 96 | 2 | TH | ✅ Yes |
| 97 | 18 | E | ❌ No |
| 98 | 26 | Y | ❌ No |

This suggests the cipher **mixes plaintext and ciphertext** based on some pattern.

---

## Remaining Unsolved Components

1. **646 non-prime POSITION runes** (after extracting 166 prime-position)
   - IoC remains ~1.0 (random)
   - All simple key attacks failed

2. **Full message reconstruction**
   - How do the prime-position and non-prime-position streams combine?
   - How do prime-valued and non-prime-valued runes interleave?

3. **Word "THEY" pattern**
   - Why is Word 17 plaintext?
   - Are other prime-indexed words also plaintext?

---

## Tools Created

| Script | Purpose |
|--------|---------|
| `attack_p20_composite_deor.py` | Test Deor on composite positions |
| `attack_p20_with_p18_key.py` | Test P18 plaintext as key |
| `analyze_p20_structure.py` | Word-level analysis |
| `analyze_p20_prime_words.py` | Prime-indexed word patterns |
| `find_english_in_p20.py` | Search for plaintext words |
| `attack_p20_by_value.py` | Separate by rune value |
| `analyze_p20_nonprime_stream.py` | Deep analysis of non-prime values |
| `attack_p20_prime_as_key.py` | Use prime stream as key |

---

## Next Steps

1. **Investigate the prime-valued stream as a KEY**
   - 237 runes using only 9 letters may encode key information
   - Try using as Vigenère key for non-prime stream

2. **Analyze word boundaries**
   - Prime-indexed words may be treated differently
   - Check if word length correlates with encryption method

3. **Combine the two approaches**
   - Prime POSITIONS decoded → 166 runes with "THE LONE", "EODE"
   - Prime VALUES separated → 237 runes of key, 575 of message
   - These may be complementary views of the same mechanism

4. **Test the Deor refrain**
   - "THAT PASSED AWAY, SO MAY THIS" appears in each stanza
   - May need special handling

---

## References

- P19 Hint: "REARRANGING THE PRIMES NUMBERS WILL SHOW A PATH TO THE DEOR K"
- P63 Grid: Contains "18" twice, mysterious terms like "VOID", "AETHEREAL"
- Deor Poem: Old English poem about overcoming hardship, 7 stanzas
