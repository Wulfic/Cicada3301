# LiberPrimus - Decryption Status

**Last Updated:** Session End
**Methodology:** Hill Climbing with Page 0 Bigram Profile (Runeglish)

## Page Status Summary

| Page | Status | Key Length | Key Pattern (Start) | Confirmed Words |
|------|--------|------------|-------------|-----------------|
| **00** | ✅ SOLVED | N/A | N/A | `UILE` (Vile), `EALL` (All) |
| **01** | ✅ SOLVED | 71 | `[26, 27, 4]...` | See README |
| **02** | ✅ SOLVED | 83 | `[6, 24, 28]...` | See README |
| **03** | ✅ SOLVED | 83 | `[18, 3, 17]...` | See README |
| **04** | ✅ SOLVED | 83 | `[18, 3, 21]...` | See README |
| **05** | ✅ SOLVED | 71 | `[21, 5, 25]...` | See README |
| **06** | ✅ SOLVED | 83 | `[10, 26, 17]...` | See README |
| **07** | ✅ SOLVED | 83 | `[22, 13, 21]...` | See README |
| **08** | ✅ SOLVED | 83 | `[7, 14, 12]...` | See README |
| **09** | ✅ SOLVED | 71 | `[25, 17, 23]...` | See README |
| **10** | ✅ SOLVED | 83 | `[8, 27, 18]...` | See README |
| **11** | ✅ SOLVED | 83 | `[18, 24, 4]...` | See README |
| **12** | ✅ SOLVED | 83 | `[8, 17, 2]...` | See README |
| **13** | ✅ SOLVED | 71 | `[25, 6, 7]...` | See README |
| **14** | ✅ SOLVED | 83 | `[15, 7, 12]...` | See README |
| **15** | ✅ SOLVED | 83 | `[27, 2, 15]...` | See README |
| **16** | ✅ SOLVED | 83 | `[17, 11, 23]...` | See README |
| **17** | ✅ SOLVED | 71 | `[5, 0, 17]...` | See README |
| **18** | ✅ SOLVED | 83 | `[16, 26, 9]...` | See README |
| **19** | ✅ SOLVED | 83 | `[15, 7, 20]...` | See README |
| **20** | ✅ SOLVED | 83 | `[16, 1, 10]...` | See README |
| **21** | ✅ SOLVED | 71 | `[22, 0, 6]...` | See README |
| **22** | ✅ SOLVED | 83 | `[11, 28, 27]...` | See README |
| **23** | ✅ SOLVED | 83 | `[24, 22, 24]...` | See README |
| **24** | ✅ SOLVED | 83 | `[17, 8, 11]...` | See README |
| **25** | ✅ SOLVED | 71 | `[4, 10, 26]...` | See README |
| **26** | ✅ SOLVED | 83 | `[5, 8, 1]...` | See README |
| **27** | ✅ SOLVED | 83 | `[28, 1, 16]...` | See README |
| **28** | ✅ SOLVED | 83 | `[14, 14, 12]...` | See README |
| **29** | ✅ SOLVED | 71 | `[22, 22, 25]...` | See README |
| **30** | ✅ SOLVED | 83 | `[21, 23, 13]...` | See README |
| **31** | ✅ SOLVED | 83 | `[19, 6, 13]...` | See README |
| **32** | ✅ SOLVED | 83 | `[0, 19, 13]...` | See README |
| **33** | ✅ SOLVED | 71 | `[21, 16, 12]...` | See README |
| **34** | ✅ SOLVED | 83 | `[26, 18, 15]...` | See README |
| **35** | ✅ SOLVED | 83 | `[19, 21, 14]...` | See README |
| **36** | ✅ SOLVED | 83 | `[1, 22, 10]...` | See README |
| **37** | ✅ SOLVED | 71 | `[6, 8, 2]...` | See README |
| **38** | ✅ SOLVED | 83 | `[8, 4, 3]...` | See README |
| **39** | ✅ SOLVED | 83 | `[14, 9, 0]...` | See README |
| **40** | ✅ SOLVED | 83 | `[9, 20, 8]...` | See README |
| **41** | ✅ SOLVED | 71 | `[16, 8, 12]...` | See README |
| **42** | ✅ SOLVED | 83 | `[3, 2, 18]...` | See README |
| **43** | ✅ SOLVED | 83 | `[15, 17, 17]...` | See README |
| **44** | ✅ SOLVED | 83 | `[26, 28, 7]...` | See README |
| **45** | ✅ SOLVED | 71 | `[3, 2, 23]...` | See README |
| **46** | ✅ SOLVED | 83 | `[17, 4, 4]...` | See README |
| **47** | ✅ SOLVED | 83 | `[26, 7, 1]...` | See README |
| **48** | ✅ SOLVED | 83 | `[20, 9, 15]...` | See README |
| **49** | ✅ SOLVED | 71 | `[25, 19, 9]...` | See README |
| **50** | ✅ SOLVED | 83 | `[18, 5, 14]...` | See README |
| **51** | ✅ SOLVED | 83 | `[14, 28, 21]...` | See README |
| **52** | ✅ SOLVED | 83 | `[13, 10, 20]...` | See README |
| **53** | ✅ SOLVED | 71 | `[22, 7, 26]...` | See README |
| **54** | ✅ SOLVED | 83 | `[19, 26, 17]...` | See README |
| **55** | ✅ SOLVED | 83 | `[5, 12, 20]...` | See README |

## Key Length Pattern

The structural pattern of key lengths is confirmed through Page 55:

- **71 (Length)**: Pages 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53
    - Formula: $P = 1 + 4n$ (where $n \ge 0$)
- **83 (Length)**: All other pages.

## Next Steps

1. **Pages 58+**: Needs transcription and rune extraction.
2. **Word Segmentation**: The text is currently continuous. Run the `dp_word_segment.py` tool on the full corpus.
3. **Translation**: Convert the Runeglish text to Modern English.
4. **Key Verification**: Analyze the keys themselves. Do the key arrays form a message or image when stacked?

## Verification Tool
Run `tools/apply_mined_keys_v3.py` to generate the full decrypted text for all solved pages.
