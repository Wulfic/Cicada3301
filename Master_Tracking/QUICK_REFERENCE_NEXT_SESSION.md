# NEXT SESSION QUICK REFERENCE
## Attack Strategy for Pages 31-54

### 🎯 IMMEDIATE ACTION PLAN

#### Phase 1: Plaintext Extraction (1-2 hours)
**Goal:** Convert high-IoC results into readable English

**For Page 20 Non-Primes:**
```python
# Input: Shift 16 result (671 chars, IoC 2.0135)
# Try: zigzag(2), diagonal, column-read, spiral
# Expected: Readable Old English/Middle English
# Check against: Keywords like DEATH, PATH, SEEKER
```

**For Pages 21-30:**
```python
# Input: 10 pages with identified keys and high IoCs
# Page 21: CABAL/Beaufort (IoC 1.9728)
# Try: Same transposition methods
# Expected: Modern English philosophical content
```

**Transposition Testing Script Template:**
```python
def zigzag(text, rows=2):
    # Read: left→right, right←left, left→right, etc.
    result = []
    for r in range(rows):
        if r % 2 == 0:  # forward
            result.extend(text[r::rows*2])
        else:  # backward
            result.extend(reversed(text[r::rows*2]))
    return ''.join(result)

def diagonal(text, size=None):
    # Read diagonally from matrix
    if size is None:
        size = int(len(text)**0.5)
    grid = [text[i*size:(i+1)*size] for i in range(size)]
    result = []
    for i in range(size):
        for j in range(size):
            if i+j < size:
                result.append(grid[i][j])
    return ''.join(result)
```

---

#### Phase 2: Pages 31-54 Scout (2-3 hours)
**Goal:** Find which pages are reference/wisdom pages

**Scan for:**
1. Low entropy pages (readable runs of common words)
2. Pages with grid structures or patterns
3. Pages with repeated sequences

**Quick Test:**
```python
for page_num in range(31, 55):
    runes = load_runes(f"page_{page_num:02d}/runes.txt")
    # Try 10 top keywords from Page 63
    for keyword in ['DIVINITY', 'VOID', 'PRIMES', 'TOTIENT', 'SACRED']:
        # Try SUB mode only
        result_ioc = test_vigenere(runes, keyword, 'SUB')
        if result_ioc > 1.65:
            print(f"Page {page_num}: {keyword} → IoC {result_ioc}")
```

**Expected Result:** 5-10 pages show high IoC with known keywords → these are content pages

---

#### Phase 3: Reference Page Discovery (1-2 hours)
**If Phase 2 finds content pages but no reference:**
1. Look for pages with suspicious patterns
2. Try ALL keywords as keys on those suspicious pages
3. Look for readable wisdom/instructional text

**If Phase 2 finds reference page:**
1. Extract all keywords from it
2. Attack all of Pages 31-54 with those keywords
3. Repeat the Pages 21-30 success pattern

---

### 📋 KEYWORD MASTER LIST
From Page 63 + Page 68 + Solved Pages:
```
PRIMARY: VOID, AETHEREAL, CARNAL, ANALOG, MOURNFUL, SHADOWS, BUFFERS, MOBIUS, OBSCURA, CABAL
SECONDARY: DIVINITY, DEOR, PRIMES, TOTIENT, SACRED, ENCRYPTION, CONSUMPTION, WISDOM
MYSTICAL: FAITH, TRUTH, DEATH, PATH, SEEK, FIND, KNOW, SPIRIT, SOUL, LIGHT
CIPHER: ENCRYPT, KEY, CIPHER, RUNE, GEMATRIA, HASH
```

---

### 🔍 IF YOU GET STUCK

1. **High IoC but gibberish text?**
   - Try 20 different transposition methods
   - Check if it's Old English vs Modern English
   - Try reading every Nth character
   - Try reversing the entire text

2. **No keywords working on Pages 31-54?**
   - Look for images on those pages
   - Check if pages 65-74 have patterns
   - Try mathematical keys (primes, Fibonacci, powers of 2)
   - Look for hidden keys in solved page plaintext

3. **Pages 31-54 seem random?**
   - They might be RNG stream cipher
   - They might use a page-number dependent key
   - They might use running key from previous page
   - Check if Page 30's plaintext becomes Page 31's key

---

### ✅ SUCCESS CHECKLIST
When you mark a page as SOLVED:
- [ ] Full plaintext extracted and readable
- [ ] Common English words appear naturally
- [ ] Sentence structure makes sense
- [ ] Content aligns with Cicada themes
- [ ] Document in `pages/page_XX/SOLUTION.md`
- [ ] Update MASTER_STATUS.md with method

---

### 💡 CICADA'S PATTERNS (Verified)
✅ Self-referential page links (Page 19→20, Page 63→21-30)
✅ Keyword reuse across pages (DIVINITY, DEOR, CABAL)
✅ Wisdom pages contain keys
✅ Multiple cipher modes used
✅ Transposition often needed alongside substitution
❓ Running key from previous page?
❓ Page-number dependent keys?
❓ Mixed Old English + Modern English?

---

### 📊 CURRENT STATE
- Verified Solved: ~25 pages
- High-IoC Candidates: ~20 pages (need plaintext extraction)
- Unsolved: ~22 pages (mostly Pages 31-54)
- **Goal:** Convert all candidates to solved by plaintext extraction
- **Stretch Goal:** Identify reference pages for Pages 31-54 and solve entire book

---

**Key Insight:** If you can extract plaintext from Pages 20-30, you'll have ~40 pages of content that teaches you about Pages 31-54. Use them as hints!
