# Liber Primus - Decryption Project

**Author:** Wulfic  
**Last Updated:** January 9, 2026  
**Repository:** [github.com/Wulfic/Cicada3301](https://github.com/Wulfic/Cicada3301)

---

## 📖 Overview

The Liber Primus ("First Book") is a 75-page cryptographic manuscript released by Cicada 3301 in 2014. It is written primarily in Anglo-Saxon runes using the **Gematria Primus** cipher alphabet.

### Document Structure

The Liber Primus was released in **two parts**:

| Part | Pages | Description |
|------|-------|-------------|
| **LP1** | 00-16 | Title page, Warning, Chapter 1 "Intus" (introduction) |
| **LP2** | 17-74 | Main body of the book (58 pages) |

**Total:** 75 pages (numbered 00-74)

---

## 📊 Current Decryption Status (Jan 2026)

| Category | Count | Pages |
|----------|-------|-------|
| ✅ **SOLVED (LP1)** | 15 | 00, 01, 03-16 |
| ✅ **SOLVED (LP2)** | 6 | 55, 56, 57, 73, 74, + partials |
| ❌ **UNSOLVED** | 54 | 02, 17-54, 58-72 |

> **Note:** See [MASTER_STATUS.md](MASTER_STATUS.md) for detailed page-by-page breakdown.

### LP1 (Pages 00-16) - Mostly Solved ✅

| Page | Status | Method | Credits |
|------|--------|--------|---------|
| 00 | ✅ | Cleartext | Cicada Community |
| 01 | ✅ | Reversed Gematria | Cicada Community |
| 02 | ❌ | Unknown (Title page) | - |
| 03-04 | ✅ | Vigenère (`DIVINITY`) | Cicada Community |
| 05 | ✅ | Substitution | Cicada Community |
| 06-09 | ✅ | Shift +3 Reversed | Cicada Community |
| 10-13 | ✅ | Substitution/Plaintext | Cicada Community |
| 14-15 | ✅ | Vigenère (`FIRFUMFERENFE`) | Cicada Community |
| 16 | ✅ | Substitution | Cicada Community |

### LP2 (Pages 17-74) - Mostly Unsolved ❌

| Range | Status | Notes |
|-------|--------|-------|
| 17 | ❓ | Partially solved (`YAHEOOPYJ`) |
| **18-54** | ❌ | **37 UNSOLVED PAGES** - The "Deep Web" segment |
| 55-57 | ✅ | φ(prime) cipher |
| **58-72** | ❌ | **15 UNSOLVED PAGES** |
| 73-74 | ✅ | φ(prime) + Substitution |

---

## 🛠️ GPU-Accelerated Solving Tools

### New Brute Force Suite (Jan 2026)

| Tool | Description |
|------|-------------|
| `master_dictionary.py` | 2,652 keys (primes, Self-Reliance, Cicada terms) |
| `brute_force_solver.py` | Parallel CPU + CuPy GPU solver |
| `gpu_solver.py` | Numba CUDA kernels for dual RTX 2080 Ti |
| `running_key_solver.py` | Self-Reliance + chained plaintext attacks |
| `batch_attack.py` | Process all unsolved pages in parallel |

**Quick Start:**
```bash
# Quick attack
python brute_force_solver.py --page 17 --quick --top 20

# Full batch attack on all unsolved pages
python batch_attack.py --output BATCH_RESULTS.md
```

### Legacy Tools
- `crack_vigenere_parallel.py` - Multi-process Vigenère
- `analyze_bulk_ic.py` - Index of Coincidence analysis

---

## 📂 Directory Structure

```
LiberPrimus/
├── README.md              # This file
├── MASTER_STATUS.md       # Page-by-page status
├── GEMATRIA_PRIMUS.md     # 29-character cipher
├── BATCH_RESULTS.md       # Attack results
├── pages/                 # Individual page data (00-74)
├── reference/             # Research materials
└── archive/               # Old attempts
```

---

## 🔑 Key Discoveries

1. **SUB mod 29** - Vigenère uses subtraction, not XOR
2. **Prime key lengths** - Keys often have prime length (43, 53, 83)
3. **φ(prime) cipher** - Pages 55, 73 use Euler's totient
4. **Literal F rule** - F runes sometimes pass through unencrypted
5. **Self-Reliance** - Emerson's essay may be a running key source

---

## 🏆 Credits

**Original Solutions (2014-2023):** The Cicada 3301 Community  
**GPU Tooling & Analysis (2026):** Wulfic
