
def load_words():
    with open(r"c:\Users\tyler\Repos\Cicada3301\extract_solutions.py", 'r') as f:
        # Just use a small built-in list or load a dictionary if available
        # I'll use the standard english dictionary if I can find one, 
        # but for now let's just use a hardcoded list of likely candidates 
        # or search the solved text.
        pass
    
    # Let's use a standard word list from NLTK or similar if available, 
    # but since I can't access internet, I will use a simple heuristic.
    pass

def get_pattern(word):
    seen = {}
    res = []
    idx = 0
    for char in word:
        if char not in seen:
            seen[char] = idx
            idx += 1
        res.append(seen[char])
    return res

def main():
    target_pattern = [0, 1, 2, 3, 4, 5, 6, 0] # M ... M
    
    # I'll read the "words_alpha.txt" or similar if present in the workspace.
    # I don't see one.
    # I will scan the transcripts for words of length 8 matching this pattern.
    
    transcript_path = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\reference\transcripts\github_liber_primus.md"
    with open(transcript_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    words = re.findall(r'\b[a-zA-Z]{8}\b', content)
    
    matches = set()
    for w in words:
        w_upper = w.upper()
        if get_pattern(w_upper) == target_pattern:
            matches.add(w_upper)
            
    # Also check common English words matching this
    # 8 letters, ends with same letter as start.
    # E.g. "MAXIMUM", "MOMENTUM".
    # "MAGNETISM".
    
    print("Matches in transcript:", matches)

if __name__ == "__main__":
    main()
