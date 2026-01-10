
import os
import sys
import random
import multiprocessing
import time
import argparse

# --- Constants ---

RUNE_MAP = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7,
    'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11, 'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15,
    'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22, 'ᛞ': 23,
    'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}

LATIN_TABLE = [
    'F', 'U', 'TH', 'O', 'R', 'C', 'G', 'W', 'H', 'N', 'I', 'J', 'EO', 'P', 'X', 
    'S', 'T', 'B', 'E', 'M', 'L', 'NG', 'OE', 'D', 'A', 'AE', 'Y', 'IA', 'EA'
]

# Standard English Trigram Scores (Log Probabilities or Frequencies)
TRIGRAMS = {
    'THE': 100, 'AND': 90, 'THA': 85, 'ENT': 80, 'ION': 80, 'TIO': 75,
    'FOR': 75, 'nde': 70, 'HAS': 70, 'NCE': 65, 'EDT': 65, 'TIS': 65,
    'OFT': 65, 'STH': 65, 'MEN': 65, 'ING': 100, 'HER': 70, 'ARE': 70,
    'ERE': 70, 'ALL': 65, 'WIS': 60, 'DOM': 50, 'MEA': 50, 'INT': 60,
    'OME': 50, 'BUT': 60, 'NOT': 60, 'YOU': 60, 'HIS': 50, 'PLA': 50,
    'DTH': 50, 'ETH': 50, 'HAT': 50
}

BIGRAMS = {
    'TH': 50, 'HE': 45, 'IN': 40, 'ER': 40, 'AN': 40, 'RE': 35, 
    'ON': 35, 'AT': 35, 'EN': 35, 'ND': 35, 'TI': 30, 'ES': 30, 
    'OR': 30, 'TE': 30, 'OF': 30, 'ED': 30, 'IS': 30, 'IT': 30,
    'AL': 25, 'AR': 25, 'ST': 25, 'TO': 25, 'NT': 25, 'NG': 25, 
    'SE': 25, 'HA': 25, 'AS': 25, 'OU': 25, 'IO': 25, 'LE': 25
}

# --- Functions ---

def load_runes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return [RUNE_MAP[c] for c in content if c in RUNE_MAP]

def decrypt(cipher, key, mode='SUB'):
    key_len = len(key)
    res = []
    for i, c in enumerate(cipher):
        k = key[i % key_len]
        if mode == 'SUB':
            res.append((c - k) % 29)
        elif mode == 'ADD':
            res.append((c + k) % 29)
        elif mode == 'SUB_REV':
            res.append((k - c) % 29)
    return res

def text_from_indices(indices):
    return "".join([LATIN_TABLE[i] for i in indices])

def score_indices_fast(indices):
    text = text_from_indices(indices)
    score = 0
    # Bigrams
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        if bg in BIGRAMS:
            score += BIGRAMS[bg]
    # Trigrams
    for i in range(len(text) - 2):
        tg = text[i:i+3]
        if tg in TRIGRAMS:
            score += TRIGRAMS[tg] * 2
    return score

def worker(args):
    cipher, key_len, iterations, worker_id, mode = args
    if worker_id == 0:
        print(f"Worker {worker_id} started. KeyLen: {key_len} Mode: {mode}")
        
    random.seed(os.urandom(4))
    
    # Init random key
    best_key = [random.randint(0, 28) for _ in range(key_len)]
    best_plain = decrypt(cipher, best_key, mode)
    best_score = score_indices_fast(best_plain)
    
    for i in range(iterations):
        # Mutate
        candidate_key = list(best_key)
        idx = random.randint(0, key_len - 1)
        
        # Mutation types
        r = random.random()
        if r < 0.5:
            # Small shift
            candidate_key[idx] = (candidate_key[idx] + random.choice([-1, 1])) % 29
        elif r < 0.8:
            # Random byte
            candidate_key[idx] = random.randint(0, 28)
        else:
            if key_len > 1:
                idx2 = random.randint(0, key_len - 1)
                candidate_key[idx], candidate_key[idx2] = candidate_key[idx2], candidate_key[idx]
        
        candidate_plain = decrypt(cipher, candidate_key, mode)
        score = score_indices_fast(candidate_plain)
        
        if score > best_score:
            best_score = score
            best_key = candidate_key
            
    return (best_score, best_key, mode)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", type=int, required=True)
    parser.add_argument("--key_len", type=int, required=True)
    parser.add_argument("--iter", type=int, default=10000)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    
    repo = r"c:\Users\tyler\Repos\Cicada3301"
    path = os.path.join(repo, "LiberPrimus", "pages", f"page_{args.page:02d}", "runes.txt")
    
    if not os.path.exists(path):
        print("Runes not found")
        return
        
    cipher = load_runes(path)
    
    # Try all modes
    modes = ['SUB', 'ADD', 'SUB_REV']
    all_results = []
    
    print(f"Starting Hill Climb on Page {args.page} (Len {len(cipher)}) with KeyLen {args.key_len}")
    
    for mode in modes:
        worker_args = [(cipher, args.key_len, args.iter, i, mode) for i in range(args.workers)]
        with multiprocessing.Pool(args.workers) as pool:
            results = pool.map(worker, worker_args)
        all_results.extend(results)

    best_s, best_k, best_m = max(all_results, key=lambda x: x[0])
    
    print("\n--- Best Result ---")
    print(f"Score: {best_s} Mode: {best_m}")
    plain_indices = decrypt(cipher, best_k, best_m)
    text = text_from_indices(plain_indices)
    print(f"Key Indices: {best_k}")
    print(f"Key Text: {text_from_indices(best_k)}")
    print(f"Plaintext: {text[:200]}...")

if __name__ == "__main__":
    main()
