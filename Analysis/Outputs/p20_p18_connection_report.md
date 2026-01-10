# Page 20 & Page 18 Connection Report

## Summary
The hint from Page 19 "REARRANGING THE PRIMES ... PATH TO THE DEOR K" has led to a statistical breakthrough on Page 20, but not a full decryption of Page 18 yet.

## The Breakthrough (Page 20)
By extracting Runes from **Page 20** at **Prime Indices** and decrypting them using Runes from the **Deor Poem** at the same **Prime Indices**:

-   **Cipher:** `Index_P20[p] - Index_Deor[p]`
-   **Shift:** +5
-   **Result:** A High-Entropy Stream (IoC 1.1459).
-   **Stream Content:**
    `YEOTJEOBJSGOXAEOUIWEEOHSHCHELTFFXENGMHETHEAAEWTHFJIAHEAJYFCN...`

### Key Findings in Stream:
1.  **"THE"** appears clearly.
2.  **"WE"** appears.
3.  **"HE"** appears multiple times.
4.  **"ENG"** (English?) appears.

## Connection to Page 18
Hypothesis: This stream is the "Deor Key" needed to solve Page 18.

### Tests Performed:
1.  **Direct Vigenère**: Used `YEOT...` as a repeating key on Page 18 Runes.
    -   **Result**: IoC 0.98 (Random Noise).
    -   **Conclusion**: Not a direct Vigenère key on the raw text.

2.  **Atbash of Key**: Converted `YEOT...` via Atbash.
    -   **Result**: `ENGIT...`.
    -   **Conclusion**: "ENG" suggests "ENGLISH". The key might need to be translated to English or Atbashed before use.

## Next Steps
1.  **Decode the Stream**: The 141-character stream is likely a message or instruction itself.
    -   Try Transposition Ciphers on the stream.
    -   Try Anagramming the stream.
2.  **Apply to Composites**: The "Path" might be to use this extracted key to decrypt the **Composite** numbers on Page 20 or Page 18.
