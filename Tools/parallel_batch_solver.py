
import os
import random
import time
import concurrent.futures
from collections import Counter
import sys

# --- CONFIGURATION ---
ITERATIONS = 50000 
TRIES_PER_PAGE = 3
MAX_WORKERS = 8 

# Output file
RESULTS_FILE = r"LiberPrimus/BATCH_RESULTS.md"

# Rune Mapping
RUNE_TO_IDX = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28,
}
IDX_TO_LETTER = ['F','U','TH','O','R','C','G','W','H','N','I','J','EO','P','X','S','T','B','E','M','L','NG','OE','D','A','AE','Y','IO','EA']
IDX_TO_RUNE = list(RUNE_TO_IDX.keys())

# Bigram scores (English/Runeglish optimized)
# Base scores
BIGRAM_SCORES = {
    'TH': 30, 'HE': 28, 'IN': 25, 'ER': 25, 'AN': 20, 'RE': 20, 
    'ON': 20, 'AT': 18, 'EN': 18, 'ND': 18, 'TI': 15, 'ES': 15, 
    'OR': 15, 'TE': 15, 'OF': 15, 'ED': 15, 'IS': 15, 'IT': 15, 
    'AL': 15, 'AR': 15, 'ST': 12, 'TO': 12, 'NT': 12, 'NG': 12, 
    'SE': 12, 'HA': 12, 'AS': 12, 'OU': 12, 'IO': 12, 'LE': 12, 
    'VE': 10, 'CO': 10, 'ME': 10, 'DE': 10, 'HI': 10, 'RI': 10, 
    'RO': 10, 'IC': 10, 'NE': 10, 'EA': 10, 'RA': 10, 'CE': 10,
    # Penalties
    'QW': -50, 'QZ': -50, 'QX': -50, 'J': -10 
}

# Known/Predicted Key Lengths
PREDICTIONS = {
    71: [1, 5, 8, 9, 13, 15, 17, 18, 21, 23, 27, 29, 31, 32, 33, 36, 48, 54, 55],
    56: [16, 19, 21, 23, 51, 63, 67, 72, 82, 88, 102], # Added based on primes for Page 56
}

def get_possible_key_lengths(page_num, ciphertext_len):
    lengths = []
    if page_num in PREDICTIONS:
        lengths.extend(PREDICTIONS[page_num])
    
    # Common primes
    primes = [29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]
    for p in primes:
        if p not in lengths and p < ciphertext_len:
            lengths.append(p)
            
    return lengths[:5]

def load_page_runes(page_num):
    # Try multiple base paths
    base_dirs = [
        "LiberPrimus/pages",
        r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages"
    ]
    
    for base in base_dirs:
        path = os.path.join(base, f"page_{page_num:02d}", "runes.txt")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            indices = [RUNE_TO_IDX[r] for r in content if r in RUNE_TO_IDX]
            if indices:
                return indices
    return []

def decrypt_indices(cipher, key):
    key_repeated = (key * (len(cipher) // len(key) + 1))[:len(cipher)]
    return [(c - k) % 29 for c, k in zip(cipher, key_repeated)]

def indices_to_text(indices):
    return "".join(IDX_TO_LETTER[i] for i in indices)

def score_text(indices):
    text = indices_to_text(indices)
    score = 0
    l = len(text)
    if l < 2: return 0
    
    for i in range(l - 1):
        bi = text[i:i+2]
        score += BIGRAM_SCORES.get(bi, 0)
    
    common_words = ["THE", "AND", "THAT", "HAVE", "FOR", "NOT", "WITH", "THIS", "FROM", "WILL", "WHO", "ALL", "ARE", "OUR", "OUT", "MAN", "GOD", "LIFE"]
    for w in common_words:
        score += text.count(w) * 15
        
    return score

def solve_page(args):
    page_num, key_len, run_id = args
    
    cipher = load_page_runes(page_num)
    if not cipher or len(cipher) < key_len:
        return None

    # Hill Climbing
    current_key = [random.randint(0, 28) for _ in range(key_len)]
    current_plain = decrypt_indices(cipher, current_key)
    current_score = score_text(current_plain)
    
    best_key = list(current_key)
    best_score = current_score
    
    for i in range(ITERATIONS):
        candidate_key = list(best_key)
        idx = random.randint(0, key_len - 1)
        if random.random() < 0.8:
            change = random.choice([-1, 1, -2, 2])
            candidate_key[idx] = (candidate_key[idx] + change) % 29
        else:
            candidate_key[idx] = random.randint(0, 28)
            
        plain = decrypt_indices(cipher, candidate_key)
        score = score_text(plain)
        
        if score > best_score:
            best_score = score
            best_key = candidate_key
    
    plaintext = indices_to_text(decrypt_indices(cipher, best_key))
    return {
        "page": page_num,
        "key_len": key_len,
        "score": best_score,
        "key": best_key,
        "plaintext_preview": plaintext[:100],
        "plaintext": plaintext
    }

def main():
    print(f"Starting Threaded Solver with {MAX_WORKERS} workers.")
    
    tasks = []
    # Identify pages
    for page_num in range(75):
        cipher = load_page_runes(page_num)
        if cipher and len(cipher) > 10:
            key_lens = get_possible_key_lengths(page_num, len(cipher))
            print(f"Page {page_num}: Found {len(cipher)} runes. Checking Lengths: {key_lens}")
            for kl in key_lens:
                for i in range(TRIES_PER_PAGE):
                    tasks.append((page_num, kl, i))
        # else:
        #     # print(f"Page {page_num}: Skipped (Empty or short)")
        #     pass

    print(f"Total tasks: {len(tasks)}")
    if not tasks:
        print("No tasks generated. Check extracted runes locations.")
        return

    results_by_page = {}
    
    # Use ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_task = {executor.submit(solve_page, task): task for task in tasks}
        
        count = 0
        for future in concurrent.futures.as_completed(future_to_task):
            count += 1
            if count % 10 == 0:
                print(f"Progress: {count}/{len(tasks)}")
                
            try:
                res = future.result()
                if res:
                    p = res['page']
                    if p not in results_by_page or res['score'] > results_by_page[p]['score']:
                        results_by_page[p] = res
                        print(f"New Best for Page {p}: Score {res['score']} (Len {res['key_len']})")
            except Exception as exc:
                print(f"Task generated exception: {exc}")

    # Write Results
    try:
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            f.write("# BATCH ANALYSIS RESULTS\n\n")
            f.write(f"Date: {time.ctime()}\n")
            f.write(f"Iterations: {ITERATIONS}\n\n")
            
            for p in sorted(results_by_page.keys()):
                r = results_by_page[p]
                f.write(f"## Page {p:02d}\n")
                f.write(f"- **Key Length:** {r['key_len']}\n")
                f.write(f"- **Score:** {r['score']}\n")
                f.write(f"- **Preview:** {r['plaintext_preview']}...\n")
                f.write(f"- **Key:** {r['key']}\n")
                f.write("\n")
        print(f"Analysis complete. Results saved to {RESULTS_FILE}")
    except Exception as e:
        print(f"Error writing results: {e}")

if __name__ == "__main__":
    main()
