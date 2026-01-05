"""
Comprehensive interleaving analysis of the XOR-71 Page 1 output.

The previous analysis showed every-3rd-character (offset=1) had the best score.
This script exhaustively tests all reasonable N and offset combinations,
looking for hidden readable streams.
"""

import os
from collections import Counter
import re

RUNES = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
RUNE_TO_INDEX = {r: i for i, r in enumerate(RUNES)}

LETTERS = [
    "F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X",
    "S", "T", "B", "E", "M", "L", "NG", "OE", "D", "A", "AE", "Y", "IA", "EA"
]

OPTIMIZED_KEY_71 = [16, 4, 13, 27, 4, 15, 25, 27, 16, 8, 5, 10, 22, 0, 1, 6, 24, 9, 15, 10, 0, 0, 6, 3, 10, 22, 14, 5, 16, 3, 15, 20, 27, 1, 4, 24, 0, 20, 19, 21, 4, 21, 14, 14, 6, 0, 10, 17, 24, 17, 3, 8, 17, 16, 6, 2, 12, 25, 24, 13, 7, 18, 21, 15, 19, 10, 6, 10, 27, 3, 5]

def load_page1():
    """Load Page 1."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    trans_path = os.path.join(repo_root, "2014", "Liber Primus", "runes in text format.txt")
    
    with open(trans_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    segments = content.split('%')
    page1_indices = [RUNE_TO_INDEX[c] for c in segments[0] if c in RUNE_TO_INDEX]
    return page1_indices

def decrypt_xor(cipher_indices, key_indices):
    """XOR decrypt."""
    plaintext = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % len(key_indices)]
        plaintext.append((c ^ k) % 29)
    return plaintext

def indices_to_text(indices):
    """Convert to text."""
    return "".join(LETTERS[i] for i in indices)

def score_text_advanced(text):
    """Advanced English scoring with word detection."""
    text_upper = text.upper()
    
    # High-value complete words
    high_value_words = {
        "THE": 10, "AND": 8, "THAT": 8, "WITH": 8, "FROM": 7,
        "THIS": 7, "HAVE": 7, "WHICH": 8, "THEIR": 7, "WOULD": 7,
        "THERE": 8, "COULD": 7, "OTHER": 7, "ABOUT": 7, "THESE": 7,
        "WITHIN": 9, "DIVINE": 10, "EMERGE": 10, "INSTAR": 12,
        "CIRCUMFERENCE": 15, "TRUTH": 8, "WISDOM": 9, "KNOWLEDGE": 10,
        "SEEK": 6, "FIND": 6, "SHALL": 7, "MUST": 6, "BEING": 7
    }
    
    # Medium-value common words
    common_words = {
        "OF": 5, "TO": 5, "IN": 5, "IS": 5, "IT": 5, "FOR": 5,
        "AS": 5, "WAS": 5, "ON": 5, "BE": 5, "AT": 5, "BY": 5,
        "OR": 4, "AN": 4, "ARE": 4, "ONE": 5, "ALL": 5, "BUT": 4,
        "NOT": 4, "YOU": 4, "CAN": 4, "OUT": 4, "WHO": 4, "HAS": 5,
        "HAD": 5, "HER": 4, "HIS": 4, "HOW": 4, "ITS": 4, "MAY": 4,
        "NEW": 4, "NOW": 4, "OLD": 4, "OUR": 4, "OWN": 4, "SAY": 4,
        "SHE": 4, "TWO": 4, "USE": 4, "WAY": 4, "WILL": 5, "WORD": 5
    }
    
    score = 0.0
    
    # Score high-value words (whole word matches)
    for word, weight in high_value_words.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = len(re.findall(pattern, text_upper))
        if matches > 0:
            score += matches * weight * 2  # Double weight for important words
    
    # Score common words
    for word, weight in common_words.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        matches = len(re.findall(pattern, text_upper))
        score += matches * weight
    
    # Common bigrams
    bigrams = {
        "TH": 3, "HE": 2.5, "IN": 2, "ER": 2, "AN": 2,
        "RE": 1.8, "ON": 1.5, "AT": 1.5, "EN": 1.5, "ND": 1.5,
        "TI": 1.3, "ES": 1.3, "OR": 1.3, "TE": 1.3, "OF": 2,
        "ED": 1.2, "IS": 1.2, "IT": 1.2, "AL": 1.2, "AR": 1.2
    }
    
    for bg, weight in bigrams.items():
        score += text_upper.count(bg) * weight
    
    # Common trigrams
    trigrams = {"THE": 3, "AND": 2.5, "ING": 2, "ION": 1.5, "ENT": 1.5}
    for tg, weight in trigrams.items():
        score += text_upper.count(tg) * weight
    
    # Penalize excessive repetition
    if len(text) > 10:
        for letter in "ETAOINSHRDLU":
            freq = text_upper.count(letter) / len(text)
            if freq > 0.20:  # More than 20%
                score *= 0.6
    
    # Bonus for reasonable length
    if 50 <= len(text) <= 300:
        score *= 1.1
    
    return score

def extract_interleaved(indices, n, offset):
    """Extract every Nth element starting at offset."""
    return indices[offset::n]

def deinterleave_streams(indices, n):
    """Split indices into N interleaved streams and try to reconstruct."""
    streams = [[] for _ in range(n)]
    for i, val in enumerate(indices):
        streams[i % n].append(val)
    return streams

def test_all_interleavings(indices, max_n=20):
    """Test all reasonable interleaving patterns."""
    results = []
    
    total_tests = 0
    for n in range(2, max_n + 1):
        for offset in range(n):
            total_tests += 1
    
    print(f"Testing {total_tests} interleaving patterns...")
    
    for n in range(2, max_n + 1):
        for offset in range(n):
            extracted = extract_interleaved(indices, n, offset)
            
            if len(extracted) < 10:  # Too short
                continue
            
            text = indices_to_text(extracted)
            score = score_text_advanced(text)
            
            results.append({
                'n': n,
                'offset': offset,
                'length': len(extracted),
                'score': score,
                'text': text
            })
    
    return results

def try_multiple_stream_reconstruction(indices):
    """Try to reconstruct text from multiple interleaved streams."""
    print("\n" + "="*80)
    print("Multiple Stream Reconstruction")
    print("="*80)
    
    results = []
    
    # Test decomposing into 2-5 streams
    for n in range(2, 6):
        streams = deinterleave_streams(indices, n)
        
        # Convert each stream to text
        stream_texts = [indices_to_text(stream) for stream in streams]
        
        # Score each stream
        stream_scores = [score_text_advanced(text) for text in stream_texts]
        
        # Also try concatenating streams in different orders
        total_score = sum(stream_scores)
        avg_score = total_score / n
        
        # Check if any single stream is particularly good
        best_stream_idx = stream_scores.index(max(stream_scores))
        best_stream_score = stream_scores[best_stream_idx]
        
        results.append({
            'n_streams': n,
            'total_score': total_score,
            'avg_score': avg_score,
            'best_single_score': best_stream_score,
            'best_stream': best_stream_idx,
            'best_text': stream_texts[best_stream_idx][:150]
        })
    
    return results

def main():
    print("="*80)
    print("Comprehensive Interleaving Analysis - Page 1 XOR-71 Output")
    print("="*80)
    
    # Get XOR-71 decrypted indices
    cipher_indices = load_page1()
    xor_output = decrypt_xor(cipher_indices, OPTIMIZED_KEY_71)
    
    print(f"\nTotal symbols: {len(xor_output)}")
    print(f"Base text: {indices_to_text(xor_output)[:100]}...")
    
    # Test all single-stream interleavings
    print("\n" + "="*80)
    print("Testing Single-Stream Interleavings (every Nth character)")
    print("="*80)
    
    results = test_all_interleavings(xor_output, max_n=20)
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\nTop 20 results:")
    print(f"\n{'Rank':<6} {'N':<6} {'Offset':<8} {'Length':<8} {'Score':<10} {'Preview'}")
    print("-"*100)
    
    for i, r in enumerate(results[:20], 1):
        preview = r['text'][:60]
        print(f"{i:<6} {r['n']:<6} {r['offset']:<8} {r['length']:<8} {r['score']:<10.2f} {preview}")
    
    # Show full text for top 5
    print("\n" + "="*80)
    print("Full Text for Top 5 Results")
    print("="*80)
    
    for i, r in enumerate(results[:5], 1):
        print(f"\n--- Rank {i}: N={r['n']}, Offset={r['offset']}, Score={r['score']:.2f} ---")
        print(r['text'])
        print()
    
    # Try multiple stream reconstruction
    multi_stream_results = try_multiple_stream_reconstruction(xor_output)
    
    print("\n" + "="*80)
    print("Multiple Stream Reconstruction Results")
    print("="*80)
    
    for r in multi_stream_results:
        print(f"\n{r['n_streams']} streams:")
        print(f"  Total score: {r['total_score']:.2f}")
        print(f"  Average per stream: {r['avg_score']:.2f}")
        print(f"  Best single stream (#{r['best_stream']}): {r['best_single_score']:.2f}")
        print(f"  Preview: {r['best_text']}")
    
    # Save results
    output_path = "tools/PAGE1_INTERLEAVING_ANALYSIS.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("Page 1 - Comprehensive Interleaving Analysis\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Base: XOR-71 decryption ({len(xor_output)} symbols)\n\n")
        
        f.write("TOP 20 SINGLE-STREAM INTERLEAVINGS\n")
        f.write("="*80 + "\n\n")
        
        for i, r in enumerate(results[:20], 1):
            f.write(f"Rank {i}: N={r['n']}, Offset={r['offset']}, Length={r['length']}, Score={r['score']:.2f}\n")
            f.write(f"{r['text']}\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("MULTIPLE STREAM DECOMPOSITION\n")
        f.write("="*80 + "\n\n")
        
        for r in multi_stream_results:
            f.write(f"{r['n_streams']} streams (total score={r['total_score']:.2f}, avg={r['avg_score']:.2f})\n")
            f.write(f"Best single stream: {r['best_stream']} (score={r['best_single_score']:.2f})\n")
            f.write(f"{r['best_text']}\n\n")
    
    print(f"\n\nResults saved to: {output_path}")

if __name__ == "__main__":
    main()
