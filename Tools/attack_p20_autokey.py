
import sys
import random
from attack_p20 import load_runes, score_text, text_from_indices, LATIN_TABLE

def autokey_decrypt(cipher, primer, mode='SUB'):
    # P[i] = (C[i] - K[i]) % 29
    # K[i] = Primer[i] for i < len(Primer)
    # K[i] = P[i - len(Primer)] for i >= len(Primer)
    
    primer_len = len(primer)
    plain = []
    
    # First segment
    for i in range(min(len(cipher), primer_len)):
        k = primer[i]
        c = cipher[i]
        if mode == 'SUB':
            p = (c - k) % 29
        else: # ADD Decryption: P = (C + K) % 29
            # Wait, if Encryption was C = (P + K), then P = C - K.
            # If Encryption was C = (P - K)? P = C + K?
            # We call it "ADD" mode usually referring to Encryption.
            # Page 19 was ADD mode: P = (C + K). Wait.
            # Let's check Page 19 logic.
            # P19: P = (C + K) % 29.
            # This means Encryption was C = (P - K).
            # So Decryption is ADD.
            # Standard Vigenere is C = P + K. -> P = C - K (SUB).
            p = (c + k) % 29
            
        plain.append(p)
        
    # Subsequent segments
    for i in range(primer_len, len(cipher)):
        k = plain[i - primer_len] # Autokey from Plaintext
        c = cipher[i]
        
        if mode == 'SUB':
            p = (c - k) % 29
        else:
            p = (c + k) % 29
            
        plain.append(p)
        
    return plain

def hill_climb_autokey(cipher, primer_len, mode='SUB', iterations=1000):
    # Initialize random primer
    primer = [random.randint(0, 28) for _ in range(primer_len)]
    
    current_plain = autokey_decrypt(cipher, primer, mode)
    current_text = text_from_indices(current_plain)
    current_score = score_text(current_text)
    
    print(f"L={primer_len} Mode={mode} Init Score: {current_score}")
    
    for _ in range(iterations):
        for i in range(primer_len):
            original_val = primer[i]
            best_val = original_val
            best_s = current_score
            
            for v in range(29):
                primer[i] = v
                # Full decrypt needed because change propagates
                res = autokey_decrypt(cipher, primer, mode)
                s = score_text(text_from_indices(res))
                
                if s > best_s:
                    best_s = s
                    best_val = v
            
            primer[i] = best_val
            current_score = best_s
            
    return current_score, primer, text_from_indices(autokey_decrypt(cipher, primer, mode))

def main():
    path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\runes.txt"
    cipher = load_runes(path)
    
    print("Testing Autokey Primers...")
    
    best_overall = (0, None, None, None)
    
    for length in range(3, 15): # Short primers suitable for Hill Climbing
        # Try SUB
        s, p, t = hill_climb_autokey(cipher, length, 'SUB', iterations=10)
        if s > best_overall[0]:
            best_overall = (s, length, 'SUB', t)
            
        # Try ADD
        s, p, t = hill_climb_autokey(cipher, length, 'ADD', iterations=10)
        if s > best_overall[0]:
            best_overall = (s, length, 'ADD', t)
            
    print("\n--- Best Autokey Result ---")
    print(f"Length: {best_overall[1]}")
    print(f"Mode: {best_overall[2]}")
    print(f"Score: {best_overall[0]}")
    print(f"Text: {best_overall[3][:200]}")

if __name__ == "__main__":
    main()
