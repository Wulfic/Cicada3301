"""
Page 20 - Image Analysis
========================
Analyze the original Page 20 images for:
1. EXIF metadata
2. Hidden comments/data
3. Steganography (LSB, etc.)
4. Pixel patterns related to primes
"""

import os
import struct
from pathlib import Path

# Image paths
IMG_DIR = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\images"
IMAGES = ["20.jpg", "onion7_20.jpg"]

def analyze_file_structure(filepath):
    """Analyze raw file bytes for hidden data."""
    print(f"\n{'='*60}")
    print(f"FILE: {os.path.basename(filepath)}")
    print(f"{'='*60}")
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Check JPEG markers
    if data[:2] == b'\xff\xd8':
        print("Format: JPEG")
        analyze_jpeg(data, filepath)
    elif data[:8] == b'\x89PNG\r\n\x1a\n':
        print("Format: PNG")
        analyze_png(data)
    else:
        print(f"Format: Unknown (magic: {data[:4].hex()})")
    
    # Check for appended data after image
    check_appended_data(data, filepath)

def analyze_jpeg(data, filepath):
    """Analyze JPEG structure for hidden data."""
    print("\n--- JPEG Marker Analysis ---")
    
    i = 0
    markers = []
    comments = []
    
    while i < len(data) - 1:
        if data[i] == 0xFF:
            marker = data[i+1]
            
            # Skip padding
            if marker == 0xFF:
                i += 1
                continue
            
            # SOI (Start of Image)
            if marker == 0xD8:
                markers.append(("SOI", i))
                i += 2
                continue
            
            # EOI (End of Image)
            if marker == 0xD9:
                markers.append(("EOI", i))
                i += 2
                continue
            
            # RST markers (no length)
            if 0xD0 <= marker <= 0xD7:
                markers.append((f"RST{marker-0xD0}", i))
                i += 2
                continue
            
            # Markers with length
            if i + 4 <= len(data):
                length = struct.unpack('>H', data[i+2:i+4])[0]
                
                marker_name = {
                    0xE0: "APP0 (JFIF)",
                    0xE1: "APP1 (EXIF)",
                    0xE2: "APP2",
                    0xEC: "APP12",
                    0xED: "APP13 (IPTC)",
                    0xEE: "APP14",
                    0xFE: "COM (Comment)",
                    0xDB: "DQT",
                    0xC0: "SOF0",
                    0xC2: "SOF2",
                    0xC4: "DHT",
                    0xDA: "SOS",
                    0xDD: "DRI",
                }.get(marker, f"0x{marker:02X}")
                
                markers.append((marker_name, i, length))
                
                # Extract comments
                if marker == 0xFE:  # COM
                    comment_data = data[i+4:i+2+length]
                    try:
                        comment = comment_data.decode('utf-8', errors='replace')
                        comments.append(comment)
                    except:
                        comments.append(comment_data.hex())
                
                # Extract EXIF/APP1
                if marker == 0xE1:
                    exif_data = data[i+4:i+2+length]
                    if exif_data[:4] == b'Exif':
                        print(f"  EXIF found at offset {i}, length {length}")
                        analyze_exif(exif_data)
                
                i += 2 + length
            else:
                i += 1
        else:
            i += 1
    
    print(f"\nMarkers found: {len(markers)}")
    for m in markers[:20]:  # First 20 markers
        if len(m) == 3:
            print(f"  {m[0]}: offset={m[1]}, length={m[2]}")
        else:
            print(f"  {m[0]}: offset={m[1]}")
    
    if len(markers) > 20:
        print(f"  ... and {len(markers)-20} more")
    
    if comments:
        print(f"\n--- JPEG Comments ({len(comments)}) ---")
        for i, c in enumerate(comments):
            print(f"  Comment {i+1}: {c[:200]}{'...' if len(c) > 200 else ''}")
    else:
        print("\nNo JPEG comments found.")

def analyze_exif(exif_data):
    """Basic EXIF analysis."""
    print("  EXIF Data Preview:")
    # Look for interesting strings
    try:
        text = exif_data.decode('latin-1', errors='replace')
        # Find printable sequences
        import re
        strings = re.findall(r'[\x20-\x7e]{4,}', text)
        for s in strings[:10]:
            print(f"    String: {s}")
    except:
        pass

def analyze_png(data):
    """Analyze PNG structure for hidden data."""
    print("\n--- PNG Chunk Analysis ---")
    
    i = 8  # Skip PNG signature
    chunks = []
    
    while i < len(data) - 8:
        length = struct.unpack('>I', data[i:i+4])[0]
        chunk_type = data[i+4:i+8].decode('ascii', errors='replace')
        chunks.append((chunk_type, i, length))
        
        # Check for text chunks
        if chunk_type in ['tEXt', 'iTXt', 'zTXt']:
            chunk_data = data[i+8:i+8+length]
            print(f"  Text chunk '{chunk_type}': {chunk_data[:100]}")
        
        i += 12 + length  # 4 (length) + 4 (type) + length + 4 (CRC)
    
    print(f"\nChunks found: {len(chunks)}")
    for c in chunks:
        print(f"  {c[0]}: offset={c[1]}, length={c[2]}")

def check_appended_data(data, filepath):
    """Check for data appended after the image end marker."""
    print("\n--- Appended Data Check ---")
    
    # For JPEG, find EOI marker
    if data[:2] == b'\xff\xd8':
        # Find last EOI (0xFFD9)
        eoi_pos = data.rfind(b'\xff\xd9')
        if eoi_pos != -1:
            remaining = len(data) - eoi_pos - 2
            if remaining > 0:
                print(f"⚠️  DATA AFTER EOI: {remaining} bytes!")
                appended = data[eoi_pos+2:]
                print(f"  First 100 bytes: {appended[:100]}")
                
                # Try to decode as text
                try:
                    text = appended.decode('utf-8', errors='replace')
                    if any(c.isalpha() for c in text[:50]):
                        print(f"  As text: {text[:200]}")
                except:
                    pass
                
                # Check for known signatures
                if appended[:3] == b'PK\x03':
                    print("  Signature: ZIP archive!")
                elif appended[:4] == b'Rar!':
                    print("  Signature: RAR archive!")
                elif appended[:2] == b'\xff\xd8':
                    print("  Signature: Another JPEG!")
                elif appended[:8] == b'\x89PNG\r\n\x1a\n':
                    print("  Signature: PNG image!")
            else:
                print("No data after EOI marker.")
        else:
            print("No EOI marker found (unusual for JPEG)")

def analyze_lsb(filepath):
    """Analyze Least Significant Bits for hidden data."""
    print("\n--- LSB Analysis ---")
    
    try:
        from PIL import Image
        import numpy as np
        
        img = Image.open(filepath)
        print(f"Image size: {img.size}")
        print(f"Mode: {img.mode}")
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = np.array(img)
        
        # Extract LSBs from each channel
        lsb_r = pixels[:,:,0] & 1
        lsb_g = pixels[:,:,1] & 1
        lsb_b = pixels[:,:,2] & 1
        
        # Flatten and combine
        lsb_bits = np.stack([lsb_r, lsb_g, lsb_b], axis=-1).flatten()
        
        # Convert bits to bytes (first 1000 bytes)
        bytes_to_extract = min(1000, len(lsb_bits) // 8)
        extracted = []
        for i in range(bytes_to_extract):
            byte_bits = lsb_bits[i*8:(i+1)*8]
            byte_val = sum(b << (7-j) for j, b in enumerate(byte_bits))
            extracted.append(byte_val)
        
        extracted_bytes = bytes(extracted)
        
        # Check for patterns
        print(f"LSB extracted (first 100 bytes): {extracted_bytes[:100]}")
        
        # Check for ASCII text
        printable = sum(1 for b in extracted_bytes if 32 <= b <= 126)
        print(f"Printable ASCII ratio: {printable}/{len(extracted_bytes)} = {printable/len(extracted_bytes)*100:.1f}%")
        
        # Try to decode as text
        try:
            text = extracted_bytes.decode('utf-8', errors='replace')
            # Look for words
            import re
            words = re.findall(r'[a-zA-Z]{3,}', text)
            if words:
                print(f"Potential words found: {words[:20]}")
        except:
            pass
        
        # Check for specific patterns
        if extracted_bytes[:4] == b'PK\x03\x04':
            print("⚠️  LSB contains ZIP signature!")
        if b'-----BEGIN' in extracted_bytes:
            print("⚠️  LSB contains PGP/certificate header!")
        
    except ImportError:
        print("PIL/numpy not available. Skipping LSB analysis.")
    except Exception as e:
        print(f"Error in LSB analysis: {e}")

def analyze_color_patterns(filepath):
    """Look for patterns in color values related to primes."""
    print("\n--- Color Pattern Analysis ---")
    
    try:
        from PIL import Image
        import numpy as np
        from collections import Counter
        
        img = Image.open(filepath)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = np.array(img)
        h, w, _ = pixels.shape
        
        print(f"Dimensions: {w} × {h} = {w*h} pixels")
        
        # Check if dimensions relate to primes
        primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
        
        for p in primes:
            if w % p == 0:
                print(f"  Width {w} divisible by prime {p}: {w//p}")
            if h % p == 0:
                print(f"  Height {h} divisible by prime {p}: {h//p}")
        
        # Analyze most common colors
        flat = pixels.reshape(-1, 3)
        colors = [tuple(c) for c in flat]
        color_counts = Counter(colors)
        
        print(f"\nUnique colors: {len(color_counts)}")
        print("Top 10 colors (RGB):")
        for color, count in color_counts.most_common(10):
            # Check if any component is a Gematria prime
            gematria_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109]
            prime_match = [c for c in color if c in gematria_primes]
            print(f"  {color}: {count} occurrences" + (f" (primes: {prime_match})" if prime_match else ""))
        
        # Check pixel values mod 29 distribution
        all_values = flat.flatten()
        mod29 = all_values % 29
        mod29_counts = Counter(mod29)
        
        print("\nPixel values mod 29 distribution:")
        for i in range(29):
            count = mod29_counts.get(i, 0)
            bar = '█' * (count // 10000)
            print(f"  {i:2d}: {bar} {count}")
        
    except ImportError:
        print("PIL/numpy not available. Skipping color analysis.")
    except Exception as e:
        print(f"Error in color analysis: {e}")

def check_outguess_signature(data):
    """Check for OutGuess steganography tool signature."""
    print("\n--- OutGuess Signature Check ---")
    
    # OutGuess typically modifies DCT coefficients
    # Look for characteristic patterns
    
    # Check for "JFIF" vs "Exif" - OutGuess sometimes modifies these
    if b'JFIF' in data[:50]:
        print("  JFIF header present")
    if b'Exif' in data[:50]:
        print("  Exif header present")
    
    # Check quantization tables for modifications
    # (This would require deeper JPEG parsing)
    
    print("  Note: Full OutGuess detection requires specialized tools (outguess -r)")

def main():
    print("="*60)
    print("PAGE 20 - IMAGE ANALYSIS")
    print("="*60)
    
    for img_name in IMAGES:
        img_path = os.path.join(IMG_DIR, img_name)
        if os.path.exists(img_path):
            analyze_file_structure(img_path)
            analyze_lsb(img_path)
            analyze_color_patterns(img_path)
            check_outguess_signature(open(img_path, 'rb').read())
        else:
            print(f"Image not found: {img_path}")

if __name__ == "__main__":
    main()
