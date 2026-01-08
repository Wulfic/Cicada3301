
import os
import re
import json

WORKSPACE_ROOT = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus"
PAGES_DIR = os.path.join(WORKSPACE_ROOT, "pages")
OUTPUT_FILE = os.path.join(WORKSPACE_ROOT, "verified_keys.json")

def scan_keys():
    verified_keys = {}
    
    # Iterate through page_00 to page_74 (limit 0 to 60 for now based on solved status)
    # Actually, iterate all directories in pages/
    
    if not os.path.exists(PAGES_DIR):
        print(f"Pages directory not found: {PAGES_DIR}")
        return

    page_dirs = sorted([d for d in os.listdir(PAGES_DIR) if d.startswith('page_') and os.path.isdir(os.path.join(PAGES_DIR, d))])
    
    for p_dir in page_dirs:
        try:
            page_num_str = p_dir.split('_')[1]
            page_num = int(page_num_str)
        except:
            continue
            
        readme_path = os.path.join(PAGES_DIR, p_dir, "README.md")
        if not os.path.exists(readme_path):
            continue
            
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Search for Key pattern
        # Pattern 1: **Key:** `[1, 2, 3...]`
        # Pattern 2: Key: [1, 2, 3...]
        
        # Regex to find list of integers
        match = re.search(r'(?:\*\*Key:\*\*|Key:)[\s`]*\[([\d,\s]+)\]', content)
        if match:
            key_str = match.group(1)
            try:
                key_list = [int(k.strip()) for k in key_str.split(',')]
                verified_keys[page_num] = key_list
                print(f"Found verified key for Page {page_num}: Length {len(key_list)}")
            except ValueError:
                print(f"Error parsing key for Page {page_num}")
        else:
            # Special case for Page 56 (Formula)
            if page_num == 56:
                print(f"Page {page_num}: Skipped (Uses formula/prime shift, not static key list in README)")
            else:
                # print(f"No key found for Page {page_num}")
                pass
                
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(verified_keys, f, indent=2)
        
    print(f"Saved {len(verified_keys)} verified keys to {OUTPUT_FILE}")

if __name__ == "__main__":
    scan_keys()
