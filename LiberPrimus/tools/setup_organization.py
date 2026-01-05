"""
Liber Primus Organization Setup Script
Creates the complete folder structure with all page folders, copies images,
extracts rune text, and creates README templates for each page.
"""

import os
import shutil
import re
from pathlib import Path

# Configuration
BASE_PATH = Path(r"c:\Users\tyler\Repos\Cicada3301")
LP_PATH = BASE_PATH / "LiberPrimus"
PAGES_PATH = LP_PATH / "pages"

# Source locations
SOURCE_IMAGES = BASE_PATH / "2014" / "Liber Primus" / "liber primus images full"
SOURCE_ENHANCED = BASE_PATH / "2014" / "Liber Primus" / "Enhanced Rune Images"
SOURCE_RUNES = BASE_PATH / "2014" / "Liber Primus" / "runes in text format.txt"
SOURCE_ONION7 = BASE_PATH / "2014" / "Liber Primus" / "A drop box of all unmodified files" / "2014onion7"
SOURCE_LP_SACRED = BASE_PATH / "2014" / "Liber Primus" / "LP Sacred Book Edition"

# Analysis results from LIBER_PRIMUS_MASTER.md
PAGE_STATUS = {
    # Confirmed solved/work-in-progress pages with key lengths
    1: {"key_length": 71, "status": "wip", "reversibility": "100%", "score": 798},
    2: {"key_length": 83, "status": "wip", "reversibility": "100%", "score": 903},
    3: {"key_length": 83, "status": "wip", "reversibility": "100%", "score": 732},
    4: {"key_length": 103, "status": "wip", "reversibility": "100%", "score": 993},
    5: {"key_length": 71, "status": "wip", "reversibility": "100%", "score": 987},
    56: {"key_length": None, "status": "solved", "method": "Prime shift -(prime+57) mod 29"},
    57: {"key_length": None, "status": "solved", "method": "Plaintext (The Parable)"},
}

# Known page content descriptions
PAGE_DESCRIPTIONS = {
    0: "Cover/Title page",
    57: "The Parable - Confirmed plaintext containing the cicada emergence metaphor",
    56: "Philosophical text - Solved using prime shift cipher",
}

def create_page_readme(page_num, rune_content="", image_files=None):
    """Generate a README.md for a specific page."""
    
    status_info = PAGE_STATUS.get(page_num, {"status": "unsolved"})
    status = status_info.get("status", "unsolved")
    
    # Status emoji
    status_map = {
        "solved": "✅ SOLVED",
        "wip": "🔄 WORK IN PROGRESS",
        "unsolved": "❌ UNSOLVED"
    }
    status_display = status_map.get(status, "❌ UNSOLVED")
    
    # Rune count
    rune_count = sum(1 for c in rune_content if c not in '-./&$%\n\r\t ')
    
    # Build analysis section based on status
    analysis_section = ""
    if status == "solved":
        method = status_info.get("method", "Unknown")
        analysis_section = f"""
## Solution

**Method:** {method}

See [solution.md](analysis/solution.md) for full decryption details.
"""
    elif status == "wip":
        key_len = status_info.get("key_length", "Unknown")
        rev = status_info.get("reversibility", "Unknown")
        score = status_info.get("score", "Unknown")
        analysis_section = f"""
## Cryptanalysis Progress

| Property | Value |
|----------|-------|
| Best Key Length | {key_len} (prime) |
| Reversibility | {rev} |
| English Score | {score} |
| Operation | SUB mod 29 |

**Status:** Decryption achieves 100% reversibility but output appears fragmented.
Possible secondary cipher layer or interleaving.
"""
    else:
        analysis_section = """
## Cryptanalysis Status

This page has not yet been analyzed with the proven methodology.

### Recommended Next Steps
1. Run IoC analysis to find candidate key lengths
2. Test SUB mod 29 with top candidates
3. Verify 100% reversibility
4. Check for interleaving patterns
5. Document results
"""

    # Image list
    image_section = ""
    if image_files:
        image_section = "## Images\n\n| File | Description |\n|------|-------------|\n"
        for img in sorted(image_files):
            image_section += f"| [{img}](images/{img}) | Original scan |\n"
    
    description = PAGE_DESCRIPTIONS.get(page_num, "Standard content page")
    
    readme = f"""# Liber Primus - Page {page_num:02d}

**Status:** {status_display}

---

## Overview

**Description:** {description}  
**Rune Count:** {rune_count}  
**Image File:** {page_num:02d}.jpg

---

{image_section}

## Rune Text

```
{rune_content if rune_content else '[No rune text extracted yet]'}
```

---

{analysis_section}

---

## Notes

*Add research notes, hypotheses, and observations here.*

---

## References

- [Master Solving Document](../../MASTER_SOLVING_DOCUMENT.md)
- [Gematria Primus](../../GEMATRIA_PRIMUS.md)

---

**Last Updated:** January 5, 2026
"""
    return readme


def parse_runes_file(filepath):
    """Parse the runes text file and split into pages."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by page separator (%)
    raw_pages = content.split('%')
    
    pages = {}
    for i, page in enumerate(raw_pages):
        page = page.strip()
        if page:
            # Replace / with newlines for readability
            formatted = page.replace('/', '\n')
            pages[i] = formatted
    
    return pages


def setup_page_folders():
    """Create all page folders with proper structure."""
    
    print("=" * 60)
    print("LIBER PRIMUS ORGANIZATION SETUP")
    print("=" * 60)
    
    # Parse rune text
    print("\n[1/5] Parsing rune text file...")
    rune_pages = {}
    if SOURCE_RUNES.exists():
        rune_pages = parse_runes_file(SOURCE_RUNES)
        print(f"  Found {len(rune_pages)} page sections in runes file")
    else:
        print(f"  WARNING: Runes file not found at {SOURCE_RUNES}")
    
    # Determine total pages from images
    print("\n[2/5] Scanning image files...")
    image_files = {}
    if SOURCE_IMAGES.exists():
        for img in SOURCE_IMAGES.glob("*.jpg"):
            try:
                page_num = int(img.stem)
                if page_num not in image_files:
                    image_files[page_num] = []
                image_files[page_num].append(img.name)
            except ValueError:
                pass
        print(f"  Found images for {len(image_files)} pages (0-{max(image_files.keys())})")
    
    # Also check onion7 for original images
    if SOURCE_ONION7.exists():
        for img in SOURCE_ONION7.glob("*.jpg"):
            try:
                page_num = int(img.stem)
                if page_num not in image_files:
                    image_files[page_num] = []
                # Mark as onion7 variant
                if f"onion7_{img.name}" not in image_files[page_num]:
                    image_files[page_num].append(f"onion7_{img.name}")
            except ValueError:
                pass
    
    # Determine the maximum page number
    max_page = max(max(image_files.keys()) if image_files else 0,
                   max(rune_pages.keys()) if rune_pages else 0)
    
    print(f"\n[3/5] Creating {max_page + 1} page folders...")
    
    # Create directories
    PAGES_PATH.mkdir(parents=True, exist_ok=True)
    (LP_PATH / "tools").mkdir(exist_ok=True)
    (LP_PATH / "reference").mkdir(exist_ok=True)
    (LP_PATH / "reference" / "solved_pages").mkdir(exist_ok=True)
    (LP_PATH / "reference" / "transcripts").mkdir(exist_ok=True)
    (LP_PATH / "reference" / "research").mkdir(exist_ok=True)
    (LP_PATH / "archive").mkdir(exist_ok=True)
    
    # Create page folders
    for page_num in range(max_page + 1):
        page_dir = PAGES_PATH / f"page_{page_num:02d}"
        page_dir.mkdir(exist_ok=True)
        (page_dir / "images").mkdir(exist_ok=True)
        (page_dir / "analysis").mkdir(exist_ok=True)
        (page_dir / "notes").mkdir(exist_ok=True)
        
        # Get rune content for this page (mapping may not be 1:1)
        rune_content = rune_pages.get(page_num, "")
        
        # Create README
        page_images = image_files.get(page_num, [])
        readme_content = create_page_readme(page_num, rune_content, page_images)
        
        with open(page_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Save rune text
        if rune_content:
            with open(page_dir / "runes.txt", 'w', encoding='utf-8') as f:
                f.write(rune_content)
    
    print(f"  Created {max_page + 1} page folders")
    
    # Copy images
    print("\n[4/5] Copying images to page folders...")
    copied = 0
    for page_num, imgs in image_files.items():
        page_dir = PAGES_PATH / f"page_{page_num:02d}" / "images"
        for img_name in imgs:
            if img_name.startswith("onion7_"):
                # Source from onion7
                src = SOURCE_ONION7 / img_name.replace("onion7_", "")
                dst = page_dir / img_name
            else:
                src = SOURCE_IMAGES / img_name
                dst = page_dir / img_name
            
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)
                copied += 1
    
    print(f"  Copied {copied} images")
    
    # Copy enhanced images where available
    if SOURCE_ENHANCED.exists():
        print("\n[4b/5] Copying enhanced images...")
        enhanced_copied = 0
        for img in SOURCE_ENHANCED.glob("*.jpg"):
            # Try to determine page number from filename
            match = re.search(r'(\d+)', img.stem)
            if match:
                page_num = int(match.group(1)) - 1  # Enhanced images seem to be 1-indexed
                if 0 <= page_num <= max_page:
                    page_dir = PAGES_PATH / f"page_{page_num:02d}" / "images"
                    dst = page_dir / f"enhanced_{img.name}"
                    if not dst.exists():
                        shutil.copy2(img, dst)
                        enhanced_copied += 1
        print(f"  Copied {enhanced_copied} enhanced images")
    
    print("\n[5/5] Creating reference files...")
    
    # Copy full transcript
    if SOURCE_RUNES.exists():
        shutil.copy2(SOURCE_RUNES, LP_PATH / "reference" / "transcripts" / "runes_full.txt")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print(f"\nCreated structure at: {LP_PATH}")
    print(f"Total pages: {max_page + 1}")
    print("\nNext steps:")
    print("1. Review page READMEs and add analysis notes")
    print("2. Run cryptanalysis on unsolved pages")
    print("3. Update status as pages are solved")


if __name__ == "__main__":
    setup_page_folders()
