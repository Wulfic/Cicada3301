# KEY HINTS FOR UNSOLVED PAGES (18-54)
## Extracted from Solved Liber Primus Pages

**Date:** January 9, 2026  
**Analysis By:** Copilot AI Assistant

---

## 📋 EXECUTIVE SUMMARY

After analyzing all solved pages (01-17, 55-74) and reference materials, the following potential key hints for unsolved pages 18-54 have been identified:

| Priority | Hint Type | Source | Key Finding |
|----------|-----------|--------|-------------|
| 🔴 **HIGH** | Number "18" | Page 63 | Appears twice in mysterious grid - direct page reference? |
| 🔴 **HIGH** | SUOID | Page 63 | Unknown term - possible anagram or key |
| 🔴 **HIGH** | φ(prime) cipher | Pages 55, 73 | Proven method using Euler's totient |
| 🟡 **MEDIUM** | DIVINITY key | Pages 03-04, 61 | Reused key - may chain to later pages |
| 🟡 **MEDIUM** | YAHEOOPYJ | Page 17 | Epilogue key - already linked to Page 18 title |
| 🟡 **MEDIUM** | Self-Reliance | Pages 56-57 | Literary reference may be running key source |
| 🟢 **LOW** | Symmetric numbers | Page 63 | 272138↔138272, 131151↔151131 pattern |

---

## 🔴 CRITICAL DISCOVERIES

### 1. Page 63 Contains Direct "18" Reference

**Source:** [Page 63 README](../LiberPrimus/pages/page_63/README.md)  
**Original Decoded Text (CAESAR_0 / Direct Gematria):**
```
SOME WISDOM
THE PRIMES ARE SACRED
THE TOTIENT FUNCTION IS SACRED
ALL THINGS SHOULD BE ENCRYPTED

KNOW THIS

272    138    SHADOWS    131    151
AETHEREAL    BUFFERS    VOID    CARNAL    18
226    OBSCURA    FORM    245    MOBIUS
18    ANALOG    VOID    MOURNFUL    AETHEREAL
151    131    CABAL    138    272
```

**Analysis:**
- **The number 18 appears TWICE** in this grid, at positions that seem significant
- Row 2: `AETHEREAL BUFFERS VOID CARNAL 18`
- Row 4: `18 ANALOG VOID MOURNFUL AETHEREAL`
- This could be a **direct hint to decrypt Page 18** using terms from this grid
- The grid has palindromic structure: numbers 272-138-131-151 mirror to 151-131-138-272

**Potential Keys for Page 18:**
- `VOID` (appears twice in grid)
- `AETHEREAL` (appears twice)
- `CARNAL`
- `ANALOG`
- `MOURNFUL`
- The number sequence itself

---

### 2. Mysterious Terms (Possible Keys)

**Source:** Page 63  
**Terms Requiring Investigation:**

| Term | Context | Possible Meaning | As Key (Gematria Indices) |
|------|---------|-----------------|---------------------------|
| **SUOID** | "BUFFERS SUOID CARNAL" | Unknown - anagram? Reversed DIOUS? | [15, 1, 3, 10, 23] |
| **MOBIUS** | "245 MOBIUS" | Möbius strip/function | [19, 3, 17, 10, 1, 15] |
| **ANALOGUOID** | "ANALOGUOID MOURNFUL" | Analog + void? Entity type? | Needs mapping |
| **AETHEREAL CABAL** | Final line | Ethereal group/organization | Combined key? |
| **OBSCURA** | "226 OBSCURA FORM" | Camera obscura? Dark/hidden | [3, 17, 15, 5, 1, 4, 24] |

**SUOID Analysis:**
- Anagrams: DIOUS, OUIDIS, SUDOI
- Reverse: DIUOS
- Could be Latin-derived (sui = of oneself)
- Note: Page 63 says "VOID" separately - SUOID may be related

---

### 3. The φ(prime) Cipher Method

**Source:** Pages 55, 73 (Verified Solutions)  
**Method:** `plaintext[i] = (cipher[i] - φ(prime[key_idx])) mod 29`

**Algorithm:**
```python
prime_sequence = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73...]
for i in range(len(cipher)):
    if is_literal_F(cipher[i], position):
        output 'F'  # Don't increment key
    else:
        key = φ(prime[key_idx]) % 29  # φ(p) = p-1 for primes
        plaintext[i] = (cipher[i] - key) % 29
        key_idx += 1
```

**Special Rule (Literal F):**
- When cipher = ᚠ AND expected plaintext = F, output F directly
- Do NOT increment the prime counter
- This shifts all subsequent decryptions

**Status:** Works for Pages 55, 73 - **TRY ON PAGES 18-54**

---

### 4. Confirmed Key Words from Solved Pages

| Key | Used On | Notes |
|-----|---------|-------|
| `DIVINITY` | Pages 03, 04, 61 | 8 characters, frequently reused |
| `FIRFUMFERENFE` | Pages 14, 15, 72 | 13 characters, variant of CIRCUMFERENCE |
| `YAHEOOPYJ` | Page 17 | 9 characters, links to Page 18 |
| `CONSUMPTION` | Page 62? | Theme from Page 68 |
| `CICADA` | Page 67? | 6 characters |
| `KOAN`/`KAON` | Page 64? | 4 characters |

---

## 🟡 THEMATIC HINTS

### 5. The Epilogue Connection (Page 17 → Page 18)

**Source:** [Page 17 README](../LiberPrimus/pages/page_17/README.md)  
**Page 17 Key:** `YAHEOOPYJ`  
**Page 17 Content:**
```
EPILOGUE
WITHIN THE DEEP WEB THERE EXISTS A PAGE THAT HASHES TO
36367763AB73783C7AF284446C59466B4CD653239A311CB7116D4618DEE09A84
25893DC7500B464FDAF1672D7BEF5E891C6E2274568926A49FB4F45132C2A8B4
IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE AND TO FIND IT
```

**Connection to Page 18:**
- Page 18 title partially decrypts with YAHEOOPYJ shifted by 7 positions
- Key alignment: `J, Y, A, H, EO, O, P, Y` (starting at index 7)
- Partial title: `INGGLJD-BOY-RIOAEOE-THE-WCH-PIOT-N` (needs work)
- **Body requires different key** - possibly autokey or chained

---

### 6. Self-Reliance Literary Reference

**Source:** Pages 56-57, 74  
**Text:** "Like the instar, tunneling to the surface, we must shed our own circumferences. Find the divinity within and emerge."

**Reference:** Ralph Waldo Emerson's "Self-Reliance" (1841)
- Contains phrase about "circumferences"
- May be used as **running key source** for pages 18-54

**Emerson Quote:** "...we shall be forced to take with shame our own opinion..."

---

### 7. Mathematical Hints

**Source:** Page 05, Page 63  
**Explicit Statements:**
```
THE PRIMES ARE SACRED
THE TOTIENT FUNCTION IS SACRED
ALL THINGS SHOULD BE ENCRYPTED
```

**Gematria Value Sums (from Page 63):**
- "SOME WISDOM" = 468
- "THE PRIMES ARE SACRED" = 853
- "THE TOTIENT FUNCTION IS SACRED" = 1039
- "ALL THINGS SHOULD BE ENCRYPTED" = 1237 (EMIRP - prime spelled backward!)
- "KNOW THIS" = 157 (EMIRP!)

**Number Relationships:**
- 272138 ÷ 29 = 9384.07...
- 138272 ÷ 29 = 4768 (exact!)
- 4768 × 29 = 138272
- 3301 is the 464th prime
- 464 × 29 = 13456

---

## 🟢 CROSS-PAGE PATTERNS

### 8. Symmetric Structure in Page 63 Grid

```
272    138    SHADOWS    131    151
AETHEREAL    BUFFERS    VOID    CARNAL    18
226    OBSCURA    FORM    245    MOBIUS
18    ANALOG    VOID    MOURNFUL    AETHEREAL
151    131    CABAL    138    272
```

**Observations:**
- Row 1 numbers: 272, 138, 131, 151
- Row 5 numbers: 151, 131, 138, 272 (REVERSED!)
- Words AETHEREAL, VOID appear twice in mirrored positions
- Central column: SHADOWS → VOID → FORM → VOID → CABAL
- This is a **palindromic/chiastic structure**

**Gematria Sum Matrix:**
```
272     138     341     131     151
366     199     130     320     18
226     245     91      245     226
18      320     130     199     366
151     131     341     138     272
```
- Row sums may indicate page numbers or key positions

---

### 9. Key Chaining Theory

**Pattern Observed:**
- Page 03-04: Key = DIVINITY
- Page 14-15: Key = FIRFUMFERENFE  
- Page 17: Key = YAHEOOPYJ
- Page 18: Uses YAHEOOPYJ shifted?

**Hypothesis:** Keys chain forward:
- Page N's plaintext/key → derived key for Page N+1
- Or: Epilogue (Page 17) contains hints for Chapter 2 (Pages 18+)

---

## 📊 RECOMMENDED ATTACK PRIORITIES

### For Page 18 Specifically:

1. **Try φ(prime) cipher** (works on 55, 73)
2. **Try Page 63 terms as keys:**
   - VOID
   - AETHEREAL
   - CARNAL
   - ANALOG
   - SUOID
   - MOURNFUL
   - Combined: VOIDCARNAL, AETHEREALVOID, etc.
3. **Try YAHEOOPYJ with autokey extension**
4. **Try running key from solved pages' plaintext**

### For Pages 18-54 Generally:

1. **Batch test φ(prime) with literal F rule**
2. **Test all Page 63 mysterious terms as Vigenère keys**
3. **Use solved page plaintexts as running keys**
4. **Look for pages that decrypt with CAESAR_0 (plaintext in disguise)**
5. **Test symmetric number sequences from Page 63**

---

## 🔍 EXTRACTED POTENTIAL KEYS (Ready to Test)

```python
POTENTIAL_KEYS = {
    # From Page 63 grid
    'SUOID': [15, 1, 3, 10, 23],  # S=15, U=1, O=3, I=10, D=23
    'VOID': [1, 3, 10, 23],       # Actually appears in grid as separate word
    'MOBIUS': [19, 3, 17, 10, 1, 15],
    'AETHEREAL': [24, 18, 2, 18, 4, 18, 24, 20],  # AE-TH-E-R-E-A-L
    'CARNAL': [5, 24, 4, 9, 24, 20],
    'OBSCURA': [3, 17, 15, 5, 1, 4, 24],
    'ANALOG': [24, 9, 24, 20, 3, 6],
    'MOURNFUL': [19, 3, 1, 4, 9, 0, 1, 20],
    'CABAL': [5, 24, 17, 24, 20],
    'SHADOWS': [15, 8, 24, 23, 3, 7, 15],
    'BUFFERS': [17, 1, 0, 0, 18, 4, 15],
    
    # Verified working keys
    'DIVINITY': [23, 10, 1, 10, 9, 10, 16, 26],
    'FIRFUMFERENFE': [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18],
    'YAHEOOPYJ': [26, 24, 8, 18, 3, 3, 13, 26, 11],
    
    # Number sequences from grid
    'NUMBERS_ROW1': [272 % 29, 138 % 29, 131 % 29, 151 % 29],  # [11, 22, 15, 6]
    'NUMBERS_COL1': [272 % 29, 366 % 29, 226 % 29, 18, 151 % 29],  # [11, 18, 23, 18, 6]
}
```

---

## 📚 SOURCE REFERENCES

| Source Page | Key Content | Link |
|-------------|-------------|------|
| Page 63 | Grid with "18", mysterious terms | [README](../LiberPrimus/pages/page_63/README.md) |
| Page 55/73 | φ(prime) cipher method | [Page 55](../LiberPrimus/pages/page_55/README.md), [Page 73](../LiberPrimus/pages/page_73/README.md) |
| Page 17 | YAHEOOPYJ key, Epilogue | [README](../LiberPrimus/pages/page_17/README.md) |
| Page 05 | "PRIMES ARE SACRED" statement | [README](../LiberPrimus/pages/page_05/README.md) |
| Page 56-57 | Self-Reliance reference, Parable | [README](../LiberPrimus/pages/page_56/README.md) |
| Page 68 | CIRCUMFERENCE, CONSUMPTION theme | [README](../LiberPrimus/pages/page_68/README.md) |

---

## ⚠️ NOTES

1. **Page 63's "18" is likely NOT coincidental** - it appears twice in a carefully structured grid
2. **SUOID remains the biggest mystery** - no known word matches, may be code or anagram
3. **The φ(prime) method WORKS** - proven on Pages 55, 73 - must try on 18-54
4. **Self-Reliance may be key source** - the literary reference is deliberate
5. **Keys may need combining** - e.g., VOIDCARNAL or AETHEREALCABAL as single keys

---

*Document generated from comprehensive analysis of solved Liber Primus pages.*
