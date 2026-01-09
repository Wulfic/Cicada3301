
import os
import sys
import random
import multiprocessing
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
        f"c:\\Users\\tyler\\Repos\\Cicada3301\\LiberPrimus\\pages\\page_{page_num:02d}\\runes.txt"
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            runes = [RUNE_TO_IDX[c] for c in content if c in RUNE_TO_IDX]
            return runes
    return None

def decrypt(cipher, key):
    return [(c - k) % 29 for c, k in zip(cipher, key * (len(cipher) // len(key) + 1))]

def score_text(indices):
    text = "".join([IDX_TO_LETTER[i] for i in indices])
    score = 0
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        score += BIGRAM_SCORES.get(bigram, 0)
    return score

def worker_task(args):
    cipher, key_len, iterations, seed = args
    random.seed(seed)
    
    # Initialize random key
    current_key = [random.randint(0, 28) for _ in range(key_len)]
    current_plain = decrypt(cipher, current_key)
    current_score = score_text(current_plain)
    
    best_key = list(current_key)
    best_score = current_score
    
    for _ in range(iterations):
        # Mutate one position
        idx = random.randint(0, key_len - 1)
        original_val = current_key[idx]
        current_key[idx] = random.randint(0, 28)
        
        # Eval
        # Optimization: Only re-score affected parts? For now, full re-score is fast enough.
        new_plain = decrypt(cipher, current_key)
        new_score = score_text(new_plain)
        
        if new_score >= current_score:
            current_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_key = list(current_key)
        else:
            # Revert
            current_key[idx] = original_val
            
    return best_score, best_key

def solve_page(page_num, key_len, iterations=50000):
    print(f"\n[+] Analyzing Page {page_num} (Key Length: {key_len})")
    runes = load_page(page_num)
    if not runes:
        print(f"[-] Could not load runes for Page {page_num}")
        return None

    # Parallel Execution
    num_workers = min(multiprocessing.cpu_count(), 16)
    pool = multiprocessing.Pool(processes=num_workers)
    
    tasks = [(runes, key_len, iterations, random.random()) for _ in range(num_workers)]
    
    results = pool.map(worker_task, tasks)
    pool.close()
    pool.join()
    
    # Find best
    best_score = -1
    best_key = None
    
    for score, key in results:
        if score > best_score:
            best_score = score
            best_key = key
            
    print(f"[=] Best Score: {best_score}")
    return best_key

def append_to_key_file(page_num, key):
    file_path = "LiberPrimus/tools/apply_mined_keys_v3.py"
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the end of the KEYS dict
    insert_idx = -1
    for i in range(len(lines) - 1, 0, -1):
        if lines[i].strip() == '}':
            insert_idx = i
            break
            
    if insert_idx != -1:
        new_entry = f"    {page_num}: {key},\n"
        lines.insert(insert_idx, new_entry)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"[+] Saved key for Page {page_num} to database.")
    else:
        print("[-] Could not find insertion point in key database.")

def update_readme(page_num, key):
    # This invokes the separate update script logic (simulated/inline here would be duplication)
    # We'll just run the update script at the end of the batch
    pass

def main():
    # Pages to attempt
    # 59 (Encrypted)
    # 61-62 (Encrypted)
    # 64 (Encrypted)
    # 67 (Encrypted)
    
    target_pages = [59, 61, 62, 64, 67]
    iterations = 50000 
    
    print(f"STARTING BATCH SOLVE: Pages {target_pages}")
    print(f"Iterations per Worker: {iterations}")
    print("="*60)
    
    for page in target_pages:
        # Determine Key Length Pattern
        # 1 + 4n -> 71. Others 83.
        # Check: (Page - 1) % 4 == 0  ?
        if (page - 1) % 4 == 0:
            key_len = 71
        else:
            key_len = 83
            
        key = solve_page(page, key_len, iterations)
        
        if key:
            append_to_key_file(page, key)
            
            # Decrypt Preview
            runes = load_page(page)
            plain = decrypt(runes, key)
            text = "".join([IDX_TO_LETTER[i] for i in plain]).lower()
            print(f"PREVIEW P{page}: {text[:60]}...")
        
    print("\n[+] Batch Complete.")

if __name__ == "__main__":
    multiprocessing.freeze_support() # For Windows
    main()
