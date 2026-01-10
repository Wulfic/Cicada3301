
import sys
import random
from attack_p20 import load_runes, score_text, text_from_indices, hill_climb

def scan_periods():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    print(f"Loaded {len(cipher)} runes.")
    print("Scanning periods 10-100...")
    
    results = []
    
    for p in range(10, 101):
        # Quick climb
        score_add, key_add, txt_add = hill_climb(cipher, p, 'ADD', iterations=200)
        # score_sub, key_sub, txt_sub = hill_climb(cipher, p, 'SUB', iterations=200)
        
        # print(f"Period {p}: Add={score_add}")
        
        results.append((score_add, p, 'ADD', txt_add))
        # results.append((score_sub, p, 'SUB', txt_sub))

    results.sort(key=lambda x: x[0], reverse=True)
    
    print("\n--- Top Periods ---")
    for res in results[:5]:
        print(f"Period {res[1]} ({res[2]}): Score={res[0]}")
        print(f"Preview: {res[3][:100]}...")

if __name__ == "__main__":
    scan_periods()
