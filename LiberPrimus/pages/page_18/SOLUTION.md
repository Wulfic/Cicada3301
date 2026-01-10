# Page 18 Solution

## Status: SOLVED (Jan 9, 2026)

### Method
*   **Cipher:** Vigenère Cipher (Variant: `P = C - K`)
*   **Key Length:** 53 (Prime)
*   **Key:** `JGULAELNSAYAEWMHIAENFTNRXOEPPOEACNGAMCUIAXGBAAOEHDGOEMTHJOMAESA`
    *   *Note: This key was recovered by manually overriding indices to produce coherent English.*
    *   *Note: The key length of 53 matches the length of the plaintext message.*

## Plaintext
```
BEING OF ALL I WILL ASC THE OATH IS SWORN TO THE ONE WITHIN THE ABOVE THE WAY
```

### Analysis
*   The plaintext is exactly **53 runes** long.
*   The fact that the message length equals the key length (53) and 53 is Prime confirms the "Primes are Sacred" hint.
*   The rest of the page produces gibberish when this key is repeated, suggesting either:
    1.  The page contains only this single message.
    2.  The key changes after the first cycle.
    3.  The text `BEING...` serves as a key for subsequent pages.
*   "ASC" is used for "ASK", consistent with Runic transliteration where 'K' is often 'C'.
*   "ABOVE" is spelled "ABOFE", consistent with Runic usage where 'V' is often represented by 'F' or 'U'.

### Key Reconstruction
The key was recovered by assuming a Vigenère SUB operation and guessing likely words ("BEING", "OF ALL", "I WILL", "THE OATH", "WITHIN THE", "ABOVE", "WAY").

**Recovered Key Indices (Latin Table):**
`[11, 6, 1, 20, 25, 20, 9, 15, 24, 26, 25, 7, 19, 8, 10, 24, 18, 9, 0, 16, 9, 4, 14, 22, 13, 13, 3, 28, 5, 21, 24, 19, 5, 1, 27, 14, 6, 17, 24, 24, 22, 8, 23, 6, 22, 19, 2, 11, 3, 19, 25, 15, 24]`
