# Liber Primus - Page 15

**Status:** ✅ SOLVED

---

## Overview

**Description:** Standard content page  
**Rune Count:** 159  
**Image File:** 15.jpg

---

## Images

| File | Description |
|------|-------------|
| [15.jpg](images/15.jpg) | Original scan |
| [onion7_15.jpg](images/onion7_15.jpg) | Original scan |


## Rune Text

```
ᚠᚢᛚᛗ-ᚪᛠᚣᛟᚪ.

&
$
ᛚᚢᛝᚾ-ᚳᚢ-ᛒᚾᛏᚠᛝ.ᛁᚢᛁᚢ-ᛟᚫᛄᚠᚫ-ᚢ

ᚷᛉᛇᛈᛉ-ᚣᛠᛚᚪᛉ-ᛟᛉᛡᚦᚻᛠ-ᚾ

ᚪᚳ-ᚢᚷᚾ-ᛈᛖᚾᚦᚩᚢᛁᛡᚱ-ᛏᛁᛒᛇᚳᚠᚷ-ᚩ

ᚦᚪ-ᛁᛈᚻᛡᛒ-ᚹᛈᚻᚱᛞᛉᛏᚢ-ᚣᛒ-ᚠᛋᛉᚢ-ᛗᛁ-

ᛡᚱ-ᛝᚢᚠᚦᛝ-ᛈᛟᛒ-ᚻᚷᚻᛡᛚ-ᚩᛞᚪᚳ-ᚦᛈᛞᛋ

ᛡᚻᛇᛚ-ᚢᛏᛋᛞ-ᚦᚢᛞᛝ-ᛚᛉᛝ-ᛏᚩᛚ-ᚪᛚ-ᚣ-ᛟ

ᛡᛉᚣ-ᛒᚻᚫᛄᛡᛁ-ᚱᚦᛚᚠ-ᛠᚾᛝ-ᛉᛗᛒᚩᛠᛈ-

```

---


## Cryptanalysis Status

This page has not yet been analyzed with the proven methodology.

### Recommended Next Steps
1. Run IoC analysis to find candidate key lengths
2. Test SUB mod 29 with top candidates
3. Verify 100% reversibility
4. Check for interleaving patterns
5. Document results


---

## Notes

*Add research notes, hypotheses, and observations here.*

---

## References

- [Master Solving Document](../../MASTER_SOLVING_DOCUMENT.md)
- [Gematria Primus](../../GEMATRIA_PRIMUS.md)

---

**Last Updated:** January 5, 2026


## Decrypted Text (Runeglish)

```text
theacthaeoeoeatheathearuioaroeothatheoiletheomheathaelealeathleatheaeomomleouile
aththeooeuileareateanaleomtheodtheojealleathoatheothwaethsththleaththeaileaiothm
thlethwethaefbleoeoeaoefheaththetheoileaththealeathealeabthealetheathuitheagwaio
```

## Solution

- **Method:** Hill Climbing (Index of Coincidence / Bigram Scoring)
- **Key Length:** 83
- **Key:** `[27, 2, 15, 17, 28, 6, 23, 23, 8, 12, 2, 19, 10, 1, 0, 19, 14, 12, 26, 9, 8, 6, 8, 18, 12, 5, 22, 27, 13, 11, 27, 15, 10, 17, 23, 27, 8, 21, 22, 23, 23, 12, 28, 19, 18, 25, 19, 4, 22, 0, 25, 18, 24, 23, 7, 15, 24, 18, 17, 26, 23, 25, 11, 13, 13, 18, 1, 26, 8, 11, 12, 20, 11, 25, 4, 15, 24, 2, 9, 13, 3, 15, 14]`
