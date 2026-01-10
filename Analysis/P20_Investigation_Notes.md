# Page 20 Investigation Notes

## Statistical Analysis
- **IoC**: ~1.18 (Very low, close to Random ~1.03).
- **Entropy**: 
    - Prime-Valued Runes (N=237, Alphabet=9): IoC 3.21. Expected for Random: ~3.22. -> **Random**.
    - Non-Prime Runes (N=575, Alphabet=20): IoC 1.44. Expected for Random: ~1.45. -> **Random**.
- **Conclusion**: The cipher produces output indistinguishable from random noise. Likely a Polyalphabetic Cipher with a Key Length >= Message Length, or a specific algorithmic generator (Stream Cipher).

## Hypotheses Tested
1. **Key = Primes Sequence (2, 3, 5...)**
   - Method: Vigenere Subtract (`C - Key`), Vigenere Add.
   - Result: Random IoC.
   - Script: `Tools/solve_p20_primes_key.py`

2. **Key = Deor Poem**
   - Method: Running Key (`C - Deor`).
   - Result: Random IoC.
   - Checked all offsets (0-950). Best IoC 1.27 (insufficient).
   - Script: `Tools/check_p20_deor_ioc.py`, `Tools/scan_deor_offsets.py`

3. **Key = Deor [Prime Indices]**
   - Method: Extracted runes from Deor at prime positions.
   - Result: Random IoC.
   - Script: `Tools/attack_p20_deor_primes.py`

4. **Key = Deor Strophes**
   - Method: Concatenated strophes 2, 3, 5, 7.
   - Result: Random IoC.
   - Script: `Tools/attack_p20_deor_strophes.py`

5. **Autokey with P19 Hint**
   - Method: Autokey using "REARRANGING..." as primer.
   - Result: Random IoC.
   - Script: `Tools/test_p20_autokey_primer.py`

6. **Affine Cipher with Prime Slopes**
   - Method: `P = (A*C + B) % 29` for A in Primes.
   - Result: All IoC < 1.3.
   - Script: `Tools/brute_affine_primes.py`

## Next Steps
- Investigate "REARRANGING THE PRIMES NUMBERS" more abstractly.
- Consider if P19 Plaintext has a typo or should be interpreted differently.
- Analyze if Page 20 *Plaintext* is the "Path" (requiring a different Key).
