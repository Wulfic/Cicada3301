# Batch Testing Summary - Liber Primus

## Overview

This document summarizes the comprehensive batch testing conducted on the Liber Primus cipher.

## Tests Conducted

### 1. Basic Batch Key Attack (`batch_key_attack.py`)
- **Tested**: ~320 key variants per page
- **Transformations**: 95 rotations, 29 offsets, reversed, negated
- **Operations**: Subtraction, XOR, Addition
- **Threshold**: Score ≥ 40
- **Result**: Found scores up to 75

### 2. Intensive Batch Attack (`intensive_batch_attack.py`)
- **Tested**: ALL 5510 combinations per page (95 rotations × 29 offsets × 2 operations)
- **Operations**: Subtraction, XOR
- **Threshold**: Score ≥ 60
- **Result**: 666 qualifying results, max score 101

### 3. Deep Pattern Analysis (`deep_pattern_analysis.py`)
- Tested page-number-based rotation
- Tested page-number-based offset
- Tested Fibonacci-based key selection
- Tested Prime-position key selection
- Tested Autokey cipher variant

### 4. Alternative Key Sources (`alternative_keys_test.py`)
- Tested Pi digits as key
- Tested Fibonacci numbers as key
- Tested Self-Reliance text as key
- Tested Prime numbers as key
- **Result**: Pi digits on Page 31 scored 70

### 5. Page-Number Formula Testing (`page_formula_test.py`)
- Tested 11 different formulas based on page number
- **BEST RESULT**: Page 47 scored 102 with rot=page, off=page mod 29

## Key Findings

### Top Scoring Pages

| Page | Best Score | Best Formula | Operation |
|------|------------|--------------|-----------|
| 47   | 102        | rot=page, off=page | Subtraction |
| 29   | 99         | rot=page+1, off=page+1 | Subtraction |
| 28   | 95         | rot=95-page, off=page | XOR |
| 45   | 89         | rot=page, off=page*3 | Subtraction |
| 44   | 87         | rot=page, off=0 | XOR |
| 31   | 87         | rot=page*11, off=page*11 | Subtraction |
| 52   | 87         | rot=page, off=page | Subtraction |
| 30   | 86         | rot=page, off=0 | Subtraction |

### Special Finding: "TRUTH" in Page 52
Page 52 decrypted with (xor, rot=21, off=11) produces:
```
GULTHINGTRUTHGYTHJOECJCFOEMBOEYXURIAEOFMALIFMFFTHSNTHEAAEADO...
```
The word "TRUTH" appears at position 8!

### Pattern Observations

1. **XOR outperforms subtraction** in many cases
2. **Page-number-based formulas** produce the highest scores
3. **The number 11 is significant**: Key sum = 1331 = 11³
4. Different pages may use different cipher formulas
5. Despite high scores, text is not readable English

## Master Key Reference

```python
MASTER_KEY = [11, 24, 17, 28, 10, 11, 25, 19, 9, 22, 5, 11, 3, 20, 27, 9, 3, 21, 20, 5, 
              20, 22, 18, 18, 24, 16, 23, 2, 23, 24, 10, 5, 28, 19, 15, 19, 0, 25, 27, 
              17, 2, 14, 10, 15, 8, 22, 8, 8, 27, 14, 2, 2, 19, 0, 18, 14, 28, 2, 11, 14, 
              5, 3, 19, 8, 16, 11, 9, 5, 1, 21, 9, 9, 9, 5, 0, 19, 25, 28, 7, 14, 14, 7, 
              14, 3, 26, 18, 24, 23, 19, 8, 4, 9, 16, 7, 23]

Length: 95 characters
Sum: 1331 = 11³
```

## Tools Created

1. `batch_key_attack.py` - Basic batch testing
2. `intensive_batch_attack.py` - Comprehensive 5510-combination test
3. `deep_pattern_analysis.py` - Pattern investigation
4. `alternative_keys_test.py` - Alternative key sources
5. `page_formula_test.py` - Page-number formula testing
6. `results_summary.py` - Results compilation
7. `best_decryptions_analysis.py` - Detailed analysis

## Next Steps

1. **Investigate word spacing**: The cipher may not include spaces
2. **Try transposition**: Letters may need rearrangement
3. **Analyze letter frequency**: Compare to English distribution
4. **Multi-layer cipher**: May need to apply multiple operations
5. **Visual/structural clues**: Images in Liber Primus may contain hints

## Files Generated

- `batch_results.txt` - Basic batch results
- `intensive_batch_results.txt` - Full results
- `DECRYPTION_RESULTS.md` - Formatted decryptions
- `CURRENT_STATUS.md` - Updated status document
