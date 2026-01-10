
import os

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    p6 = load('LiberPrimus/pages/page_06/runes.txt')
    p64 = load('LiberPrimus/pages/page_64/runes.txt')
    
    if p6 == p64:
        print("Page 06 and Page 64 are IDENTICAL.")
    else:
        print("Page 06 and Page 64 are DIFFERENT.")
        # Find differences
        min_len = min(len(p6), len(p64))
        diff_count = 0
        for i in range(min_len):
            if p6[i] != p64[i]:
                diff_count += 1
                if diff_count < 10:
                    print(f"Diff at {i}: P6={ord(p6[i])} vs P64={ord(p64[i])}")
        print(f"Total Diffs: {diff_count}")
        print(f"P6 Len: {len(p6)}, P64 Len: {len(p64)}")

if __name__ == "__main__":
    main()
