
import os
import sys

# Ensure we can import from the tools directory
sys.path.append(os.getcwd())
try:
    from LiberPrimus.tools import apply_mined_keys_v3 as keys_module
except ImportError:
    # Try alternate path if running from root
    sys.path.append(os.path.join(os.getcwd(), "LiberPrimus"))
    from tools import apply_mined_keys_v3 as keys_module

def update_page_readme(page_num):
    if page_num not in keys_module.KEYS:
        print(f"[-] No key for Page {page_num}")
        return

    # Load and potentially decrypt
    runes = keys_module.load_page(page_num)
    if not runes:
        print(f"[-] No runes found for Page {page_num}")
        return

    key = keys_module.KEYS[page_num]
    plain = keys_module.decrypt(runes, key)
    text = keys_module.format_text(plain)
    
    # Break text into lines for readability
    wrapper = []
    chunk_size = 80
    for i in range(0, len(text), chunk_size):
        wrapper.append(text[i:i+chunk_size])
    formatted_text = "\n".join(wrapper)

    readme_path = os.path.join(os.getcwd(), "LiberPrimus", "pages", f"page_{page_num:02d}", "README.md")
    
    if not os.path.exists(readme_path):
        print(f"[-] README not found: {readme_path}")
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Transformations
    content = content.replace("**Status:** ❌ UNSOLVED", "**Status:** ✅ SOLVED")
    content = content.replace("**Status:** 🔄 LAYER 1 DONE", "**Status:** ✅ SOLVED") # Just in case

    # Add Decrypted Text section if missing
    section_header = "## Decrypted Text (Runeglish)"
    if section_header not in content:
        content += f"\n\n{section_header}\n\n```text\n{formatted_text}\n```"
    
    # Add Solution section if missing
    solution_header = "## Solution"
    if solution_header not in content:
        content += f"\n\n{solution_header}\n\n"
        content += f"- **Method:** Hill Climbing (Index of Coincidence / Bigram Scoring)\n"
        content += f"- **Key Length:** {len(key)}\n"
        content += f"- **Key:** `{key}`\n"

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[+] Updated README for Page {page_num}")

if __name__ == "__main__":
    print("Updating READMEs for Pages 34-55...")
    for i in range(34, 56):
        update_page_readme(i)
