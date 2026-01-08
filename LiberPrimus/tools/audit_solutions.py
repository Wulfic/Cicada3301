
import os
import re

OUTPUT_DIR = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\runeglish_output"

COMMON_ENGLISH = {"THE", "AND", "IS", "OF", "TO", "IN", "THAT", "IT", "YOU", "WE", "ARE", "NOT", "DEATH", "LIFE", "END", "BELONG", "PRESERVING"}
OLD_ENGLISH = {"FLETH", "HATHEN", "THEON", "EORNG", "AETH", "EATHTH"}

def score_text(text):
    # Remove punctuation
    cleaned = re.sub(r'[^A-Z\s]', '', text.upper())
    words = cleaned.split()
    if not words:
        return 0, 0, 0
    
    eng_count = 0
    oe_count = 0
    
    for w in words:
        if w in COMMON_ENGLISH:
            eng_count += 1
        elif w in OLD_ENGLISH:
            oe_count += 1
            
    # Check for "THE-Heavy" artifact
    the_count = words.count('THE')
    the_ratio = the_count / len(words)
    
    return eng_count, oe_count, the_ratio

def main():
    print("Page | Status | Eng | OE | THE% | Preview")
    print("-----|--------|-----|----|------|--------")
    
    for filename in sorted(os.listdir(OUTPUT_DIR)):
        if not filename.endswith("_runeglish.txt"):
            continue
            
        page_num = filename.split('_')[1]
        path = os.path.join(OUTPUT_DIR, filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        eng, oe, the_ratio = score_text(text)
        
        preview = text.replace('\n', ' ')[:40]
        
        status = "❓ UNKNOWN"
        if eng > 5 and the_ratio < 0.2:
            status = "✅ ENGLISH"
        elif oe > 2:
            status = "📜 RUNEGLISH"
        elif the_ratio > 0.25:
            status = "⚠️ THE-HEAVY"
        elif eng == 0 and oe == 0:
            status = "❌ GARBAGE"
            
        print(f"{page_num} | {status} | {eng} | {oe} | {the_ratio:.2f} | {preview}")

if __name__ == "__main__":
    main()
