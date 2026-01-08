import re

def extract_solutions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'(^## .*)', content, flags=re.MULTILINE)
    
    pages_of_interest = [
        "00.jpg", "01.jpg", "02.jpg", "03.jpg", "04.jpg", "05.jpg", "06.jpg", "08.jpg", "09.jpg",
        "10.jpg", "11.jpg", "12.jpg", "13.jpg", "14.jpg", "15.jpg", "16.jpg", "73.jpg", "74.jpg"
    ]

    current_header = ""
    for section in sections:
        if section.startswith("## "):
            current_header = section.strip()
            continue
        
        # Check if this section belongs to a page of interest
        found = False
        for p in pages_of_interest:
            if p in current_header:
                found = True
                print(f"--- {current_header} ---")
                
                # Try to find key
                key_match = re.search(r'\*\*Key:\*\*(.*?)(?=\n)', section)
                if key_match:
                    print(f"Method: {key_match.group(1).strip()}")
                
                # Print lines that look like English or are marked as such
                lines = section.split('\n')
                print_mode = False
                for line in lines:
                    strip_line = line.strip()
                    if "Outguess:" in line:
                         print_mode = True 
                         print("Found Outguess section:")
                    elif "English:" in line or "Decrypted" in line or "The runes were not encrypted" in line or "The runes on it translate to" in line or "Decoding the runes on the page using a Vigenere cipher" in line:
                        print_mode = True
                        print(line)
                    elif "Runes:" in line or "Runes -" in line:
                         print_mode = False
                    
                    if print_mode:
                        # Clean up some markdown artifacts if needed, but keeping it raw is safer
                        if not strip_line.startswith("Runes:") and strip_line != "":
                             print(line)
                
                print("\n")
                break

extract_solutions('people_liber_primus.md')
