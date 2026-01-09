
import os
import sys
import random
import multiprocessing
import argparse
import time
from collections import Counter

# --- Configuration & Constants ---

RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}

IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']

# Page 0 Bigrams (Runeglish Profile)
BIGRAM_SCORES = {
    'LE': 52, 'UI': 46, 'IL': 46, 'HE': 33, 'TH': 33, 'IC': 26, 'ET': 19,
    'HA': 19, 'EO': 19, 'WA': 19, 'AR': 19, 'EF': 19, 'AL': 19, 'LC': 13,
    'AN': 13, 'CA': 13, 'NH': 13, 'EA': 13, 'LU': 13, 'RN': 13, 'NF': 13,
    'FS': 13, 'SU': 13, 'FI': 13, 'IS': 13, 'SO': 13, 'OD': 13, 'DI': 13,
    'CE': 13, 'OM': 13, 'MU': 13, 'EU': 13, 'UY': 13, 'YD': 13, 'DN': 13,
    'NU': 13, 'UH': 13, 'AT': 13, 'EN': 13, 'NA': 13, 'AI': 13, 'WE': 6,
    'EL': 6, 'CU': 6, 'UM': 6, 'MA': 6, 'NW': 6, 'WY': 6, 'YL': 6,
}

# --- Helper Functions ---

def load_page(page_num):
    paths = [
        f"LiberPrimus/pages/page_{page_num:02d}/runes.txt",
        f"LiberPrimus/pages/page_{page_num:02d}/runes.txt",
        f"../LiberPrimus/pages/page_{page_num:02d}/runes.txt",
        f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{page_num:02d}\\runes.txt"
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            runes = [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]
            return runes, path
    return None, None

def decrypt(cipher, key):
    return [(c - k) % 29 for c, k in zip(cipher, key * (len(cipher) // len(key) + 1))]

def score_text(plain_indices):
    letters = [IDX_TO_LETTER[i] for i in plain_indices]
    text = "".join(letters)
    score = 0
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        score += BIGRAM_SCORES.get(bigram, -5)
    
    # Bonus for known Page 0 words
    words = ["UILE", "EALL", "IAEO", "TH", "EO", "JEALL", "WAETH"]
    for w in words:
        if w in text:
            score += 20 * len(w)
    return score

def format_text(indices):
    return "".join([IDX_TO_LETTER[i] for i in indices]).lower()

# --- Worker Function ---

def worker_task(worker_id, cipher, key_len, iterations, result_queue):
    """
    Runs a hill climbing session in a separate process.
    """
    try:
        # Initialize random key
        key = [random.randint(0, 28) for _ in range(key_len)]
        best_key = list(key)
        best_score = score_text(decrypt(cipher, key))
        no_improve = 0
        
        # Local loop
        for i in range(iterations):
            candidate_key = list(best_key)
            idx = random.randint(0, key_len - 1)
            
            # Mutation strategy
            if random.random() < 0.7:
                 change = random.choice([-1, 1, -2, 2])
                 candidate_key[idx] = (candidate_key[idx] + change) % 29
            else:
                 candidate_key[idx] = random.randint(0, 28)
                
            plain = decrypt(cipher, candidate_key)
            score = score_text(plain)
            
            if score > best_score:
                best_score = score
                best_key = list(candidate_key)
                no_improve = 0
            else:
                no_improve += 1
                
            # Restart if stuck
            if no_improve > 3000:
                 key = [random.randint(0, 28) for _ in range(key_len)]
                 plain = decrypt(cipher, key)
                 score = score_text(plain)
                 if score > best_score:
                     best_score = score
                     best_key = key
                 no_improve = 0
        
        result_queue.put((best_score, best_key))
    except Exception as e:
        print(f"Worker {worker_id} failed: {e}")

# --- Main Controller ---

def main():
    parser = argparse.ArgumentParser(description="Parallel Hill Climbing for Cicero 3301")
    parser.add_argument('page', type=int)
    parser.add_argument('key_len', type=int)
    parser.add_argument('--iter', type=int, default=50000, help="Iterations per worker")
    parser.add_argument('--workers', type=int, default=None, help="Number of worker processes (default: CPU count)")
    args = parser.parse_args()
    
    cipher, path = load_page(args.page)
    if not cipher:
        print(f"[-] Could not find runes for Page {args.page}")
        return

    num_workers = args.workers if args.workers else multiprocessing.cpu_count()
    print(f"[+] Analyzing Page {args.page} (Len: {len(cipher)})")
    print(f"[+] Key Length: {args.key_len}")
    print(f"[+] Launching {num_workers} workers with {args.iter} iterations each...")
    
    result_queue = multiprocessing.Queue()
    processes = []
    
    start_time = time.time()
    
    for i in range(num_workers):
        p = multiprocessing.Process(target=worker_task, args=(i, cipher, args.key_len, args.iter, result_queue))
        processes.append(p)
        p.start()
        
    # Collect results
    results = []
    for _ in range(num_workers):
        results.append(result_queue.get())
        
    for p in processes:
        p.join()
        
    elapsed = time.time() - start_time
    
    # Find best result
    best_score, best_key = max(results, key=lambda x: x[0])
    
    print(f"\n[=] Completed in {elapsed:.2f}s")
    print(f"[=] Best Score: {best_score}")
    print(f"[=] Key: {best_key}")
    
    plain = decrypt(cipher, best_key)
    text = format_text(plain)
    print("\nDecrypted Text Preview:")
    print("-" * 60)
    print(text[:300])
    print("-" * 60)
    
    # Save to file automatically if score is good (heuristic > 3000 for standard pages)
    # Different pages have different lengths so raw score varies, but typically > 3000 is good for >200 chars
    
if __name__ == "__main__":
    main()
