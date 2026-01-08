#!/usr/bin/env python3
"""
LIBER PRIMUS UNIFIED SOLVER
===========================

A comprehensive tool for attacking Liber Primus pages using the proven methodology:
1. IoC analysis to find key length candidates
2. SUB operation (not XOR) with mod 29 arithmetic
3. Frequency-based key initialization
4. Hill-climbing optimization
5. Reversibility verification
6. Interleaving detection

Usage:
    python liber_primus_solver.py --page 3
    python liber_primus_solver.py --page 3 --key-length 69
    python liber_primus_solver.py --ioc-only --page 3
    python liber_primus_solver.py --all-pages

Based on breakthroughs from Pages 1 (key 71) and 2 (key 83).
"""

import argparse
import os
from collections import Counter
from pathlib import Path

# ============================================================================
# CONSTANTS
# ============================================================================

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}
INDEX_TO_RUNE = {i: r for i, r in enumerate(RUNES)}

# Some transcriptions use the Unicode rune ᛄ for J instead of ᛂ.
RUNE_TO_INDEX.setdefault("ᛄ", 11)

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
          67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
          139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]

# ============================================================================
# DATA LOADING
# ============================================================================

def get_liber_primus_root() -> Path:
    """Get LiberPrimus directory (parent of tools/)."""
    return Path(__file__).resolve().parent.parent


def get_pages_root() -> Path:
    """Get LiberPrimus/pages directory."""
    return get_liber_primus_root() / "pages"

def load_all_pages():
    """Load all pages from LiberPrimus/pages/page_XX/runes.txt."""
    pages_root = get_pages_root()
    pages: list[dict] = []

    if not pages_root.exists():
        raise FileNotFoundError(f"Pages directory not found: {pages_root}")

    for child in pages_root.iterdir():
        if not child.is_dir():
            continue
        if not child.name.startswith("page_"):
            continue
        try:
            page_num = int(child.name.split("page_")[-1])
        except ValueError:
            continue

        rune_path = child / "runes.txt"
        if not rune_path.exists():
            continue

        raw_text = rune_path.read_text(encoding="utf-8")
        indices = [RUNE_TO_INDEX[c] for c in raw_text if c in RUNE_TO_INDEX]
        if not indices:
            continue

        pages.append({
            "page_num": page_num,
            "indices": indices,
            "raw_text": raw_text,
            "path": rune_path,
        })

    pages.sort(key=lambda p: p["page_num"])
    return pages

def load_page(page_num: int):
    """Load a specific page by number (0-74)."""
    pages_root = get_pages_root()
    rune_path = pages_root / f"page_{page_num:02d}" / "runes.txt"
    if not rune_path.exists():
        raise ValueError(f"Page {page_num} not found at {rune_path}")

    raw_text = rune_path.read_text(encoding="utf-8")
    indices = [RUNE_TO_INDEX[c] for c in raw_text if c in RUNE_TO_INDEX]
    if not indices:
        raise ValueError(f"Page {page_num} has no runes in {rune_path}")

    return {
        "page_num": page_num,
        "indices": indices,
        "raw_text": raw_text,
        "path": rune_path,
    }

# ============================================================================
# INDEX OF COINCIDENCE
# ============================================================================

def compute_ioc(indices, key_length):
    """
    Compute Index of Coincidence for a given key length.
    
    IoC measures how likely two random letters from the text are the same.
    For polyalphabetic ciphers, IoC spikes at the true key length.
    """
    if key_length < 1 or key_length >= len(indices):
        return 0.0
    
    # Split into cosets (every key_length-th character)
    cosets = [[] for _ in range(key_length)]
    for i, idx in enumerate(indices):
        cosets[i % key_length].append(idx)
    
    # Calculate IoC for each coset and average
    ioc_sum = 0.0
    valid_cosets = 0
    
    for coset in cosets:
        n = len(coset)
        if n < 2:
            continue
        
        freqs = Counter(coset)
        ioc = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
        ioc_sum += ioc
        valid_cosets += 1
    
    return ioc_sum / valid_cosets if valid_cosets > 0 else 0.0

def find_key_length_candidates(indices, max_length=150, top_n=10):
    """
    Find the best key length candidates via IoC analysis.
    Returns list of (key_length, ioc_score) tuples, sorted by score descending.
    """
    results = []
    
    for klen in range(1, min(max_length + 1, len(indices))):
        ioc = compute_ioc(indices, klen)
        is_prime = klen in PRIMES
        results.append({
            'key_length': klen,
            'ioc': ioc,
            'is_prime': is_prime
        })
    
    # Sort by IoC descending
    results.sort(key=lambda x: x['ioc'], reverse=True)
    return results[:top_n]


def find_best_prime_key_length(indices, max_length=150):
    """Return the best (highest IoC) prime key length candidate within max_length."""
    best = None
    upper = min(max_length, len(indices) - 1)
    for klen in PRIMES:
        if klen < 1 or klen > upper:
            continue
        ioc = compute_ioc(indices, klen)
        candidate = {"key_length": klen, "ioc": ioc, "is_prime": True}
        if best is None or candidate["ioc"] > best["ioc"]:
            best = candidate
    return best

# ============================================================================
# SUB CIPHER OPERATIONS
# ============================================================================

def decrypt_sub(cipher_indices, key):
    """
    Decrypt using SUB operation: plaintext = (cipher - key) mod 29
    This is the CORRECT operation (not XOR).
    """
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key[i % len(key)]
        plaintext.append((c - k) % 29)
    return plaintext

def encrypt_sub(plaintext_indices, key):
    """
    Encrypt using ADD operation: cipher = (plaintext + key) mod 29
    """
    cipher = []
    for i, p in enumerate(plaintext_indices):
        k = key[i % len(key)]
        cipher.append((p + k) % 29)
    return cipher

def verify_reversibility(cipher_indices, key):
    """
    Verify that decrypt→encrypt produces original cipher.
    MUST be 100% for a correct solution.
    """
    plaintext = decrypt_sub(cipher_indices, key)
    re_encrypted = encrypt_sub(plaintext, key)
    matches = sum(1 for c1, c2 in zip(cipher_indices, re_encrypted) if c1 == c2)
    return matches, len(cipher_indices)

# ============================================================================
# KEY GENERATION
# ============================================================================

def generate_frequency_key(cipher_indices, key_length, target_letter='E'):
    """
    Generate initial key assuming most common cipher symbol in each coset
    decrypts to the target letter (default 'E', index 18).
    
    For SUB: plaintext = (cipher - key) mod 29
    So: key = (cipher - plaintext) mod 29
    """
    target_idx = LETTERS.index(target_letter) if target_letter in LETTERS else 18
    key = []
    
    for i in range(key_length):
        # Get all cipher symbols at this position mod key_length
        coset = [cipher_indices[j] for j in range(i, len(cipher_indices), key_length)]
        
        if not coset:
            key.append(0)
            continue
        
        # Find most common symbol in coset
        most_common = Counter(coset).most_common(1)[0][0]
        
        # Calculate key value
        key_val = (most_common - target_idx) % 29
        key.append(key_val)
    
    return key

# ============================================================================
# ENGLISH SCORING
# ============================================================================

def indices_to_text(indices):
    """Convert indices to readable text using Gematria Primus letters"""
    return "".join(LETTERS[i] for i in indices)

def score_english(text):
    """
    Score English-likeness using trigrams, bigrams, and keywords.
    Higher score = more English-like.
    """
    text = text.upper()
    score = 0.0
    
    # Common trigrams (heavily weighted)
    trigrams = {
        'THE': 30, 'AND': 20, 'ING': 18, 'ION': 15, 'ENT': 12,
        'FOR': 10, 'TIO': 10, 'ERE': 10, 'HER': 10, 'ATE': 10,
        'VER': 8, 'TER': 8, 'THA': 8, 'ATI': 8, 'HAT': 8,
        'ERS': 7, 'HIS': 7, 'RES': 7, 'ILL': 7, 'ARE': 7,
        'WIT': 6, 'ITH': 6, 'OUT': 6, 'ALL': 6, 'OUR': 6
    }
    
    # Common bigrams
    bigrams = {
        'TH': 15, 'HE': 14, 'IN': 12, 'ER': 11, 'AN': 10,
        'RE': 9, 'ON': 8, 'AT': 8, 'EN': 7, 'ND': 7,
        'TI': 6, 'ES': 6, 'OR': 6, 'TE': 6, 'OF': 6,
        'ED': 5, 'IS': 5, 'IT': 5, 'AL': 5, 'AR': 5
    }
    
    # Cicada-specific keywords (bonus)
    keywords = {
        'WISDOM': 50, 'TRUTH': 50, 'DIVINE': 50, 'EMERGE': 50,
        'INSTAR': 60, 'CIRCUMFERENCE': 70, 'KNOWLEDGE': 50,
        'SEEK': 40, 'FIND': 40, 'PATH': 40, 'WITHIN': 45,
        'PARABLE': 50, 'CICADA': 60, 'ENLIGHTEN': 50
    }
    
    # Score trigrams
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in trigrams:
            score += trigrams[trigram]
    
    # Score bigrams
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in bigrams:
            score += bigrams[bigram]
    
    # Keyword bonuses
    for keyword, bonus in keywords.items():
        score += text.count(keyword) * bonus
    
    return score

# ============================================================================
# OPTIMIZATION
# ============================================================================

def hill_climb_optimize(cipher_indices, initial_key, max_iterations=500, verbose=False):
    """
    Hill-climbing optimization: try ±1 adjustments to each key position.
    Keep changes that improve the English-likeness score.
    """
    current_key = initial_key[:]
    current_plaintext = decrypt_sub(cipher_indices, current_key)
    current_score = score_english(indices_to_text(current_plaintext))
    
    if verbose:
        print(f"  Starting score: {current_score:.2f}")
    
    improvements = 0
    
    for iteration in range(max_iterations):
        improved = False
        
        for i in range(len(current_key)):
            for delta in [-1, 1]:
                test_key = current_key[:]
                test_key[i] = (current_key[i] + delta) % 29
                
                test_plaintext = decrypt_sub(cipher_indices, test_key)
                test_score = score_english(indices_to_text(test_plaintext))
                
                if test_score > current_score:
                    current_key = test_key
                    current_score = test_score
                    improvements += 1
                    improved = True
                    
                    if verbose and improvements % 10 == 0:
                        print(f"  Iteration {iteration}: score {current_score:.2f} ({improvements} improvements)")
                    break
            
            if improved:
                break
        
        if not improved:
            if verbose:
                print(f"  Converged at iteration {iteration}")
            break
    
    if verbose:
        print(f"  Final score: {current_score:.2f} ({improvements} total improvements)")
    
    return current_key, current_score

# ============================================================================
# INTERLEAVING DETECTION
# ============================================================================

def detect_interleaving(plaintext_indices, max_n=20):
    """
    Test if the plaintext is interleaved (multiple streams merged).
    
    Extract every-Nth-character from different offsets and score them.
    If any extraction scores HIGHER than the full text, it's interleaved.
    """
    full_text = indices_to_text(plaintext_indices)
    full_score = score_english(full_text)
    
    results = []
    
    for n in range(2, min(max_n + 1, len(plaintext_indices) // 2)):
        for offset in range(n):
            stream_indices = plaintext_indices[offset::n]
            if len(stream_indices) < 10:
                continue
            
            stream_text = indices_to_text(stream_indices)
            stream_score = score_english(stream_text)
            
            results.append({
                'n': n,
                'offset': offset,
                'score': stream_score,
                'text': stream_text,
                'length': len(stream_indices)
            })
    
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return {
        'full_score': full_score,
        'full_text': full_text,
        'best_extraction': results[0] if results else None,
        'is_interleaved': results[0]['score'] > full_score if results else False,
        'top_5': results[:5]
    }

# ============================================================================
# MAIN ATTACK FUNCTION
# ============================================================================

def attack_page(page_num, key_length=None, verbose=True):
    """
    Full attack on a Liber Primus page.
    
    1. Load page data
    2. If no key_length specified, run IoC analysis
    3. Generate frequency-based initial key
    4. Optimize with hill-climbing
    5. Verify reversibility
    6. Check for interleaving
    """
    if verbose:
        print("=" * 80)
        print(f"ATTACKING PAGE {page_num}")
        print("=" * 80)
    
    # Load page
    try:
        page = load_page(page_num)
    except ValueError as e:
        print(f"Error: {e}")
        return None
    
    cipher = page['indices']
    
    if verbose:
        print(f"\nPage {page_num}: {len(cipher)} runes")
    
    # IoC analysis if no key length specified
    if key_length is None:
        if verbose:
            print("\n--- IoC Analysis ---")
        
        candidates = find_key_length_candidates(cipher, top_n=10)
        
        if verbose:
            print(f"{'Rank':<6} {'KeyLen':<8} {'IoC':<12} {'Prime?'}")
            print("-" * 40)
            for i, c in enumerate(candidates, 1):
                prime_str = "✓" if c['is_prime'] else ""
                print(f"{i:<6} {c['key_length']:<8} {c['ioc']:<12.6f} {prime_str}")
        
        # Prefer a prime candidate when available
        prime_candidates = [c for c in candidates if c['is_prime']]
        chosen = prime_candidates[0] if prime_candidates else candidates[0]
        key_length = chosen['key_length']
        if verbose:
            print(f"\nUsing key length: {key_length}")
    
    # Generate initial key
    if verbose:
        print("\n--- Key Generation ---")
    
    initial_key = generate_frequency_key(cipher, key_length)
    initial_plaintext = decrypt_sub(cipher, initial_key)
    initial_score = score_english(indices_to_text(initial_plaintext))
    
    if verbose:
        print(f"Initial key generated (frequency-based)")
        print(f"Initial score: {initial_score:.2f}")
    
    # Optimize
    if verbose:
        print("\n--- Optimization ---")
    
    optimized_key, optimized_score = hill_climb_optimize(
        cipher, initial_key, max_iterations=500, verbose=verbose
    )
    
    # Verify reversibility
    if verbose:
        print("\n--- Reversibility Check ---")
    
    matches, total = verify_reversibility(cipher, optimized_key)
    reversibility_pct = (matches / total) * 100
    
    if verbose:
        print(f"Reversibility: {matches}/{total} ({reversibility_pct:.1f}%)")
        if matches == total:
            print("✓ PERFECT REVERSIBILITY - Solution is mathematically correct!")
        else:
            print("⚠ WARNING: Imperfect reversibility indicates potential issues")
    
    # Decrypt
    final_plaintext = decrypt_sub(cipher, optimized_key)
    final_text = indices_to_text(final_plaintext)
    
    # Check interleaving
    if verbose:
        print("\n--- Interleaving Analysis ---")
    
    interleaving = detect_interleaving(final_plaintext)
    
    if verbose:
        print(f"Full text score: {interleaving['full_score']:.2f}")
        if interleaving['best_extraction']:
            best = interleaving['best_extraction']
            print(f"Best extraction: every {best['n']}th from offset {best['offset']}, score {best['score']:.2f}")
        
        if interleaving['is_interleaved']:
            print("✓ INTERLEAVED MESSAGE DETECTED")
        else:
            print("No interleaving detected - full text is primary")
    
    # Results
    result = {
        'page_num': page_num,
        'cipher_length': len(cipher),
        'key_length': key_length,
        'key': optimized_key,
        'score': optimized_score,
        'reversibility': (matches, total),
        'plaintext_indices': final_plaintext,
        'plaintext_text': final_text,
        'interleaving': interleaving
    }
    
    if verbose:
        print("\n" + "=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"\nKey length: {key_length}")
        print(f"Score: {optimized_score:.2f}")
        print(f"Reversibility: {matches}/{total}")
        print(f"\nDecrypted text:")
        print(final_text[:500] + "..." if len(final_text) > 500 else final_text)
        
        if interleaving['is_interleaved']:
            print(f"\nPrimary message (interleaved):")
            print(interleaving['best_extraction']['text'][:300])
    
    return result

def run_ioc_analysis(page_num, top_n=20):
    """Run IoC analysis only (no attack)"""
    print("=" * 80)
    print(f"IOC ANALYSIS - PAGE {page_num}")
    print("=" * 80)
    
    page = load_page(page_num)
    cipher = page['indices']
    
    print(f"\nPage {page_num}: {len(cipher)} runes")
    print("\nTop 20 key length candidates:")
    print(f"{'Rank':<6} {'KeyLen':<8} {'IoC':<12} {'Prime?'}")
    print("-" * 40)
    
    candidates = find_key_length_candidates(cipher, top_n=top_n)
    for i, c in enumerate(candidates, 1):
        prime_str = "✓" if c['is_prime'] else ""
        print(f"{i:<6} {c['key_length']:<8} {c['ioc']:<12.6f} {prime_str}")
    
    return candidates


def run_ioc_analysis_range(start_page: int, end_page: int, top_n: int = 10, quiet: bool = False):
    """Run IoC analysis for a range of pages. Returns per-page summaries."""
    summaries: list[dict] = []

    for page_num in range(start_page, end_page + 1):
        try:
            page = load_page(page_num)
        except ValueError as e:
            if not quiet:
                print(f"Skipping page {page_num}: {e}")
            continue

        cipher = page["indices"]
        candidates = find_key_length_candidates(cipher, top_n=top_n)
        best = candidates[0] if candidates else None
        best_prime = find_best_prime_key_length(cipher)
        summaries.append({
            "page_num": page_num,
            "runes": len(cipher),
            "best_key_length": best["key_length"] if best else None,
            "best_ioc": best["ioc"] if best else None,
            "best_is_prime": best["is_prime"] if best else None,
            "best_prime_key_length": best_prime["key_length"] if best_prime else None,
            "best_prime_ioc": best_prime["ioc"] if best_prime else None,
            "top_candidates": candidates,
        })

    if not quiet:
        print("=" * 80)
        print(f"IOC SUMMARY ({start_page}-{end_page})")
        print("=" * 80)
        print(f"{'Page':<6} {'Runes':<8} {'BestLen':<8} {'IoC':<12} {'Prime?'} {'BestPrime':<10} {'PrimeIoC'}")
        print("-" * 50)
        for s in summaries:
            prime = "✓" if s["best_is_prime"] else ""
            ioc_str = f"{s['best_ioc']:.6f}" if s["best_ioc"] is not None else ""
            prime_len = "" if s["best_prime_key_length"] is None else str(s["best_prime_key_length"])
            prime_ioc = "" if s["best_prime_ioc"] is None else f"{s['best_prime_ioc']:.6f}"
            print(f"{s['page_num']:<6} {s['runes']:<8} {str(s['best_key_length']):<8} {ioc_str:<12} {prime:<6} {prime_len:<10} {prime_ioc}")

    return summaries

def save_result(result, output_dir=None):
    """Save attack result to file"""
    if output_dir is None:
        output_dir = Path(__file__).parent / "results"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    key_len = result.get('key_length')
    key_suffix = f"_k{key_len}" if isinstance(key_len, int) else ""
    filename = output_dir / f"page{result['page_num']}{key_suffix}_result.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"LIBER PRIMUS - PAGE {result['page_num']} DECRYPTION\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Cipher length: {result['cipher_length']} runes\n")
        f.write(f"Key length: {result['key_length']}\n")
        f.write(f"Score: {result['score']:.2f}\n")
        f.write(f"Reversibility: {result['reversibility'][0]}/{result['reversibility'][1]}\n")
        f.write(f"\nKey (indices):\n{result['key']}\n")
        f.write(f"\nDecrypted text:\n{result['plaintext_text']}\n")
        
        if result['interleaving']['is_interleaved']:
            f.write(f"\n--- INTERLEAVED MESSAGE ---\n")
            best = result['interleaving']['best_extraction']
            f.write(f"Extraction: every {best['n']}th from offset {best['offset']}\n")
            f.write(f"Score: {best['score']:.2f}\n")
            f.write(f"Text:\n{best['text']}\n")
    
    print(f"\nResult saved to: {filename}")


def save_ioc_summary(summaries, output_dir=None, filename="ioc_summary.csv"):
    """Save IoC batch summaries to a CSV file."""
    if output_dir is None:
        output_dir = Path(__file__).parent / "results"

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    out_path = output_dir / filename

    lines = ["page,runes,best_key_length,best_ioc,best_is_prime,best_prime_key_length,best_prime_ioc\n"]
    for s in summaries:
        best_ioc = "" if s["best_ioc"] is None else f"{s['best_ioc']:.8f}"
        best_is_prime = "" if s["best_is_prime"] is None else ("1" if s["best_is_prime"] else "0")
        best_prime_len = "" if s.get("best_prime_key_length") is None else str(s.get("best_prime_key_length"))
        best_prime_ioc = "" if s.get("best_prime_ioc") is None else f"{s.get('best_prime_ioc'):.8f}"
        lines.append(
            f"{s['page_num']},{s['runes']},{s['best_key_length']},{best_ioc},{best_is_prime},{best_prime_len},{best_prime_ioc}\n"
        )

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\nIoC summary saved to: {out_path}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Liber Primus Unified Solver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python liber_primus_solver.py --page 3
  python liber_primus_solver.py --page 3 --key-length 69
  python liber_primus_solver.py --ioc-only --page 3
  python liber_primus_solver.py --all-pages --start 3 --end 10
        """
    )
    
    parser.add_argument('--page', type=int, help='Page number to attack (0-74)')
    parser.add_argument('--key-length', type=int, help='Specific key length to use')
    parser.add_argument('--ioc-only', action='store_true', help='Only run IoC analysis')
    parser.add_argument('--all-pages', action='store_true', help='Attack multiple pages')
    parser.add_argument('--start', type=int, default=1, help='Starting page for --all-pages')
    parser.add_argument('--end', type=int, default=10, help='Ending page for --all-pages')
    parser.add_argument('--save', action='store_true', help='Save results to files')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')
    
    args = parser.parse_args()
    
    if args.ioc_only and args.all_pages:
        summaries = run_ioc_analysis_range(args.start, args.end, top_n=10, quiet=args.quiet)
        if args.save:
            save_ioc_summary(summaries)
    elif args.ioc_only and args.page is not None:
        run_ioc_analysis(args.page)
    elif args.all_pages:
        for page_num in range(args.start, args.end + 1):
            try:
                result = attack_page(page_num, verbose=not args.quiet)
                if result and args.save:
                    save_result(result)
            except Exception as e:
                print(f"Error on page {page_num}: {e}")
    elif args.page:
        result = attack_page(args.page, args.key_length, verbose=not args.quiet)
        if result and args.save:
            save_result(result)
    else:
        # Default: show help and attack Page 3 as demo
        parser.print_help()
        print("\n" + "=" * 80)
        print("DEMO: Attacking Page 3")
        print("=" * 80)
        result = attack_page(3)
        if result:
            save_result(result)

if __name__ == "__main__":
    main()
