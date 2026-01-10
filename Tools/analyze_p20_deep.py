"""
Page 20 - Deep Image Analysis
==============================
Focus on:
1. Red pixels (192,0,0) - only colored pixels in the image
2. APP2 ICC profile data
3. Position analysis of runes in the image
4. Check for OutGuess/F5 steganography patterns
"""

import os
import struct
from collections import Counter

IMG_PATH = r"c:\Users\tyler\Repos\Cicada3301\LiberPrimus\pages\page_20\images\20.jpg"

def analyze_red_pixels():
    """Analyze the positions and patterns of red (192,0,0) pixels."""
    print("="*60)
    print("RED PIXEL ANALYSIS")
    print("="*60)
    
    try:
        from PIL import Image
        import numpy as np
        
        img = Image.open(IMG_PATH)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = np.array(img)
        h, w, _ = pixels.shape
        
        # Find red pixels (192, 0, 0)
        red_mask = (pixels[:,:,0] == 192) & (pixels[:,:,1] == 0) & (pixels[:,:,2] == 0)
        red_positions = np.where(red_mask)
        
        print(f"Total red (192,0,0) pixels: {len(red_positions[0])}")
        
        if len(red_positions[0]) > 0:
            # Get bounding box
            min_y, max_y = red_positions[0].min(), red_positions[0].max()
            min_x, max_x = red_positions[1].min(), red_positions[1].max()
            
            print(f"Bounding box: ({min_x}, {min_y}) to ({max_x}, {max_y})")
            print(f"Box size: {max_x - min_x + 1} × {max_y - min_y + 1}")
            
            # Analyze red pixel rows
            rows_with_red = np.unique(red_positions[0])
            print(f"\nRows containing red pixels: {len(rows_with_red)}")
            
            # Check if row count relates to 28 (grid rows) or 29 (alphabet)
            if len(rows_with_red) in [28, 29, 812]:
                print(f"  ⚠️ Interesting: {len(rows_with_red)} rows matches grid structure!")
            
            # Analyze columns with red
            cols_with_red = np.unique(red_positions[1])
            print(f"Columns containing red pixels: {len(cols_with_red)}")
            
            if len(cols_with_red) in [28, 29, 812]:
                print(f"  ⚠️ Interesting: {len(cols_with_red)} columns matches grid structure!")
            
            # Look for patterns in red pixel positions
            print("\n--- Red Pixel Position Patterns ---")
            
            # Count red pixels per row
            red_per_row = Counter(red_positions[0])
            unique_counts = set(red_per_row.values())
            print(f"Unique red pixel counts per row: {sorted(unique_counts)}")
            
            # Look for prime-related patterns
            primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109]
            
            # Check if any prime appears in row positions
            prime_rows = [r for r in rows_with_red if r in primes or (r % 29) in range(29)]
            
            # Extract x-coordinates and check for message
            x_coords = sorted(set(red_positions[1]))
            print(f"\nFirst 50 red x-coordinates: {x_coords[:50]}")
            
            # Check if x-coords mod 29 give a message
            x_mod29 = [x % 29 for x in x_coords]
            print(f"X-coords mod 29: {x_mod29[:50]}")
            
        # Also check for near-red colors that might form patterns
        print("\n--- Near-Red Color Analysis ---")
        
        # Find all colors with R > 150 and G,B < 50
        red_ish_mask = (pixels[:,:,0] > 150) & (pixels[:,:,1] < 50) & (pixels[:,:,2] < 50)
        red_ish_pixels = pixels[red_ish_mask]
        
        if len(red_ish_pixels) > 0:
            unique_reds = Counter([tuple(c) for c in red_ish_pixels])
            print(f"Red-ish colors found:")
            for color, count in unique_reds.most_common(10):
                print(f"  {color}: {count}")
        
    except ImportError:
        print("PIL/numpy not available.")
    except Exception as e:
        print(f"Error: {e}")

def analyze_app2_profile():
    """Analyze the APP2 ICC profile segment for hidden data."""
    print("\n" + "="*60)
    print("APP2 ICC PROFILE ANALYSIS")
    print("="*60)
    
    with open(IMG_PATH, 'rb') as f:
        data = f.read()
    
    # Find APP2 marker
    i = 0
    while i < len(data) - 3:
        if data[i:i+2] == b'\xff\xe2':  # APP2
            length = struct.unpack('>H', data[i+2:i+4])[0]
            app2_data = data[i+4:i+2+length]
            
            print(f"APP2 segment at offset {i}, length {length}")
            print(f"First 50 bytes: {app2_data[:50]}")
            
            # Check for ICC_PROFILE header
            if app2_data[:12] == b'ICC_PROFILE\x00':
                print("ICC Profile detected")
                print(f"Profile chunk: {app2_data[12:14]}")  # Chunk number and total
                
                # Profile data starts after header
                profile_data = app2_data[14:]
                print(f"Profile data length: {len(profile_data)}")
                
                # Look for hidden text in profile
                printable = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in profile_data[:200])
                print(f"Profile data (printable): {printable}")
                
                # Check for interesting patterns
                if b'cicada' in profile_data.lower():
                    print("⚠️ 'cicada' found in ICC profile!")
                if b'3301' in profile_data:
                    print("⚠️ '3301' found in ICC profile!")
            
            break
        i += 1

def analyze_rune_positions():
    """Analyze positions of runes in the image to check for encoding in positions."""
    print("\n" + "="*60)
    print("RUNE POSITION ANALYSIS")
    print("="*60)
    
    try:
        from PIL import Image
        import numpy as np
        
        img = Image.open(IMG_PATH)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = np.array(img)
        h, w, _ = pixels.shape
        
        # Find black pixels (runes are black on white)
        # Black is (0,0,0) or close to it
        black_mask = (pixels[:,:,0] < 30) & (pixels[:,:,1] < 30) & (pixels[:,:,2] < 30)
        black_positions = np.where(black_mask)
        
        print(f"Total near-black pixels: {len(black_positions[0])}")
        
        # Find connected components (rough analysis)
        # Group by rows to find rune lines
        rows_with_black = Counter(black_positions[0])
        
        # Find row ranges with high black pixel density (rune rows)
        threshold = 100  # Minimum black pixels to consider a row part of text
        text_rows = [r for r, count in rows_with_black.items() if count > threshold]
        
        if text_rows:
            text_rows.sort()
            
            # Find row bands (groups of consecutive rows)
            bands = []
            current_band = [text_rows[0]]
            
            for r in text_rows[1:]:
                if r - current_band[-1] <= 10:  # Within same band
                    current_band.append(r)
                else:
                    bands.append(current_band)
                    current_band = [r]
            bands.append(current_band)
            
            print(f"\nFound {len(bands)} text bands (rows of runes)")
            
            if len(bands) == 28:
                print("⚠️ 28 bands matches the 28 rows of the Page 20 grid!")
            elif len(bands) == 29:
                print("⚠️ 29 bands matches the alphabet size!")
            
            # Analyze spacing between bands
            band_centers = [sum(b)/len(b) for b in bands]
            if len(band_centers) > 1:
                spacings = [band_centers[i+1] - band_centers[i] for i in range(len(band_centers)-1)]
                print(f"\nBand center spacings: {[int(s) for s in spacings[:10]]}...")
                print(f"Average spacing: {sum(spacings)/len(spacings):.1f} pixels")
                
                # Check if spacings encode a message
                spacings_mod29 = [int(s) % 29 for s in spacings]
                print(f"Spacings mod 29: {spacings_mod29}")
        
    except ImportError:
        print("PIL/numpy not available.")
    except Exception as e:
        print(f"Error: {e}")

def check_dct_patterns():
    """Check for patterns in DCT coefficients (F5/OutGuess detection)."""
    print("\n" + "="*60)
    print("DCT COEFFICIENT ANALYSIS")
    print("="*60)
    
    # This is a simplified check - real steganography detection
    # requires more sophisticated tools
    
    with open(IMG_PATH, 'rb') as f:
        data = f.read()
    
    # Count distribution of byte values in the image data
    # (after headers, this is mostly DCT-encoded data)
    
    # Find SOS marker (start of scan - compressed data begins)
    sos_pos = data.find(b'\xff\xda')
    if sos_pos != -1:
        # Skip SOS segment header
        sos_len = struct.unpack('>H', data[sos_pos+2:sos_pos+4])[0]
        scan_data = data[sos_pos + 2 + sos_len:]
        
        # Find EOI
        eoi_pos = scan_data.rfind(b'\xff\xd9')
        if eoi_pos != -1:
            scan_data = scan_data[:eoi_pos]
        
        print(f"Compressed scan data: {len(scan_data)} bytes")
        
        # Analyze byte distribution
        byte_counts = Counter(scan_data)
        
        # Check for characteristic F5 patterns
        # F5 tends to have more even distribution in LSBs
        
        # Count bytes by LSB
        lsb_0 = sum(c for b, c in byte_counts.items() if b % 2 == 0)
        lsb_1 = sum(c for b, c in byte_counts.items() if b % 2 == 1)
        
        ratio = lsb_0 / (lsb_0 + lsb_1) if (lsb_0 + lsb_1) > 0 else 0
        print(f"LSB=0 ratio: {ratio:.4f} (0.5 = uniform)")
        
        if abs(ratio - 0.5) < 0.02:
            print("⚠️ Very uniform LSB distribution - could indicate F5 steganography!")
        
        # Look for byte value 0xFF followed by 0x00 (byte stuffing)
        stuffing = scan_data.count(b'\xff\x00')
        print(f"Byte stuffing (FF 00) occurrences: {stuffing}")

def main():
    print("PAGE 20 - DEEP IMAGE ANALYSIS")
    print("="*60)
    
    analyze_red_pixels()
    analyze_app2_profile()
    analyze_rune_positions()
    check_dct_patterns()

if __name__ == "__main__":
    main()
