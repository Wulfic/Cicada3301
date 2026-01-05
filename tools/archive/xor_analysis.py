#!/usr/bin/env python3
"""
XOR analysis on the high-entropy Cicada hex blocks.
Since all three blocks are the same length, they might XOR together to reveal something.
"""

from pathlib import Path
from collections import Counter
import itertools

# The three outguess hex blocks all have same length (991 bytes)
BLOCKS = {
    "liber_primus": """775d0481115f6e4f3ba8873ac66da1df6bbe3ff19389878f2ddb9423881b
5a95bb5dff35ebab119090c5c19678e58bf9cfe2a93694e23da86465cd11
64d7de4744d7a4fea07f75c7db7676f8fc9b52621881b02f2296fe5922b2
6759ee322200e7d8c8a92c0e1ea401cb384a466f3f237ee220b95d151210
c03cd464ba34077eab3529503d6395f84fedbc0245b2f8425ac4b774bf91
16f5dcc1b3af3fa15ee85bc63dcb40b6eec5c2c05d34295f25eb7b788abc
f5674f5a6344a2768e768407a06a48fb9c7d4b6c75b243043d562d0db556
3650e412fc04b538c3900dea56da01591a00f87b6f42831e3a9730ec76a2
e3c7262cf7a6ba39c70b50c35a9b9226b1404bd4b00e79b508a4a3410eaf
057bb314a41c9e381820cea07b323f038749548c042f6203a30a5fa12f18
08109faf49c18a2d55eca3610b8206b143d487cd195c58080fe84e26f6f7
57b6a7cbdaeab019be4482644a02effce5e7e0920b3173412c7245ad832e
ea3e00e49c7a88d52f136aed5b4b1973541de38b8093901522e26491c2ea
ede8464e3e77a2cc1bb78c2274aaff68120a4751337c1f92892dc80dc51a
ad3df760f5a022e835e902aa389df29a8be04f067f0735622125e7fd0eda
de4fcf6ff48ad4954e8ab6b130e4d5fb2540c178c7fcc243cc7701aa3cf8
21546dfe0558854b202745a87c98d2ea3236d850c25bf0cb93d4c0bc78ec
c0841a9b341b9a2c8449c5825600139d3b9710822e4f5dcd8f8ae6395868
265221a7eade3f93441b33bbd45145fd08a8816247f55b6e1a2fdc2d9b44
451c828194abbe59730fe07894a5536138ce1cd21b0306211c4c9ddd8be6
3c69f6470bcb878f544825a789aaf9adff2b2e4408469de7f6c2fc6d1823
8d5efa614aec168f4f33f49c2eac1ed9a6606b39c6213b5a5c0ca5fb6cf2
0e0f19e8a7faffe11edad29472acf65d6535b0832c5b589623a3b5a3c337
f7b0aae38ec1cd7815f334447d2e9d0ccd75d06e9d533f7623bfe22611d5
661c65d7c4bad3074ba437b9d9006eb638eb2d744716b0fda8a6f2a09b8c
f7b7a9bae4a7b96054bdeb220e99c32eb2fdead676becde5938ee32abb4c
126e8420e6259029d1bcd9a51486fb0e619a7654c67954787c696df49b57
ef42b503da982fd5b02acb142ce2d1fe64db441c895240c6a07c1f5baabd
ace7525482dd263f348c6e0ae5a0693346ed966f726e2d7261e7e50f1e48
0c0b14d1e1acf72d29e678b322ebaa3828b5b1d2ca17671e8687a15ddf89
c1a8f5a35b2e4d9e958452676ad69a66e2944b5843768d1deb6b9bdb12fe
38d34769da0bbd00ac22724b8df8dd412ef0c114762f4f1f5b00c796ebf8
733c11d9f435ae76a72dc66c162f1f4b25fc3473b157c1b044d72ecfa059
fe""",
        
    "intus": """4dd1c8afafceed237cca8a334b24fe09069e3771e416a749687af002b4de
844566fdef57ba9f76a17c2ca1472f08cbb7b595524310614d8f9044f7f5
49c422a0f10599ace22d443907db0d54d6bf726f1c42c27fe93b7d8a5980
0661353b73fd868adc2ab687a0fdc7cd6560f917a1392e6594b62554b8cc
b844f766583cada19fff1e233867020d49c5b4669b64c1bfe2cb7127b2ca
76d117be8994665dde9a1b49f16494eed2cbd31d4faa8f66b3afd1dc8fd0
96c344c89f2a23ed0d493524ab9f61ef020cbd8a4cd8fb0f21ecdfc461b0
e5aae8037a9ffc7667bee4a11479000c1c93f64dd2e38173f9e8aa380a3a
5387612fbe0787389a91633033be608eb9c0b799869704413a6bdf74961c
d81ac702815f0d4503a212828ad9b25efae12b9bafb4debb3f38f6825fbc
81053014e17d79e82c2548d23e9c32228feccf3a53ca80def3a96a75d83e
5f21b4c35d2641e9ac3a0124dd6dfb2f5187b16c4858158afc0bd285b0a0
ff43bc3452c52e59ffcdc6d5837daabf6800ed0354780625215b2eaa3e4b
1f7323d5ef64419c6ce0b84efe4f5b4c2656d47da20820c91780001d6759
84ee9984864f6679e35fdf255f6478d49c1843277364ecd66da6d0d2d133
fbbd94a63d6f1edb6b8f692c87aa1c99078f8a9e855ee80e27cac12c3033
082355388893e86bff30b33820f71254ee6e920e0ee27b1ca97b1ed69147
a4ee2cca257b9e728ff835b162289f112a90d2de9feaff313beaa624ce7e
a4a3f875bcad3e42aa5bd19c3e3c9a3641c692bc2b987fb2ab551d9503f0
91cf1ca69a88354153c8308b759010bd415f85776cdc1c0f5b965ab00ab4
52ef5f513daad68fd1c94d3547f46aa9baf2e5323a933ec4b2334dea55eb
37a4ec7453d40790d27a082264586e0e3ee1e499e1e0544e2f578bd25d22
06774a80f0d56d4d5f6de6cb95e557b392071497fda207d1f82abc6d71bf
deca78cd55bf7c89be389d8840d5f57f8109ae2cc4879b22191b10297c0c
10965320ae295521074743a119fed32a078031cd35dd1e108e41b0f0f591
e4941f1be81d8ff793e3ec2ad1a3ca718220d8f402eac82da7e51668b90d
0dde5db35f5f933c0d13397afa4377ada56ed49c7ca3fa0b6a190261561b
eba51e102fff455a1bec3424f5e9800c6345460c4fdf23b8c8ce0baaf73c
55712d8a71cd2aa3143f337cb322adea56ee79ce4b239ce352f4b863298f
2c1f5c4ec348f1569c1d125be9c3419ffc5b533b4fb5154c3c5c51a7c4e8
0f3aebf392cc81f2b29f773a44b4a2d7bc3c690f8f58e1aa4ba9d716961a
31003f22306b8c9271b5fa0dc588be92ece2c79043c841592d69fbfbeac4
60c4259e4339a3c8e3e100c3dceab0acb351f026189e1335cd0701f97667
a3""",
        
    "runes": """17a1e10393d3c62b0e2c2d59ca197f85246746c533bf6d8316f2256679e8
f3fdf08d1a2a30470f0bccba289066e74a44703ebf32d0c85072b96d75ab
0d52aeb0fa971d00161a78adfcf82fe97e68004551973b11ebf9d09f377d
41328e401cb3287240c6d6c7f479f1521b73e958d15305c6e12f2b0fe59f
37581648ab3ce7ff718573295f249dff41476700feba4c9ed321cc593e68
5015c175301674d1ad5f02ca8be69a786c4941fd41d7e177d710fff64041
4e8926bff638e4e9f056de4d31d56e7aeb21b1c64f5b963f328bc3e9fca1
9daf235deff53c368d24e32213ea621747d64c77dae0452f9235c9ad4eab
e001066c03e47f663bdb56a55f6ba3c358e5b63a66b64dbd5dae1a7fa9e0
bf0c1c520e08dd1f57b79510b48fc55717cf2f45c5c1f2cad771d06e00f3
cf46e6cc99cd80f30ca39ec403485ac4e34a2e9905d2f3b29a754f2354a6
49e0564ee196b5934010c116e4195da9fb2a62cf493d1ea1e913cf6c01bc
7e14939380edffb4e890d571a2618aaa56567da3bda4ef5c70d87d6f848a
c4cb27f9e27d873f2e19711be4b4d3687d2da067a5270c30cfa7bc77ef39
6ce0228d259e76e187c1acc9299dc4656dbf7d427d5489fb09f00768b287
69c33a87b9949f657277bdfc83299a044d983cb700f57f099d8e93a97ff3
230161f6e58e1c48885992a76a18b0d6b53f7c36848fc4ae73ce86459d9a
0133503262335d3671f0b5065b63c7ed7940b06df492c1a48527026dde55
cb83e8851b795ba6a021a571ab1f8e8a221756a438460fa8dc3cf189d78d
bce1af1f4d4adf4d66a892bece6f3ba50bf0aed30f96287b08839442f11e
01e8dc401d040941d7d862cba80edb651f83b31059e6c17613a9d2ff24a7
e88f7d534a612334e50798ee2c81329eccb9fdc36db00e25180b64664bb5
522e10471e4ce5e400855932a07dcde4c45ed07d879a1b298afb53a9c8be
6017e101ae19f79693a9d89b0cc91902164a262b2386f4677ffc9f3b28b7
0fe2469121c9e87e07b3385d8f88edd77c012ad378fac5b465950e3d2969
4777e6e7748d0ff19d38757198625816759c5f4b040667a26238c0315423
4af3bff4d40b5674bbc2848ad8b3b5f58dc191a68cf1dc435c7a0da7ac21
7cb5ee52de5527e9c7adba5f8f4104934bcf4821b4c639322ef45ec817b0
ceec2abfab5b41f04cc0193401da8e8a244e8d940d2283ba0b713629548a
2a272bcf09d53023e3c21a8ef95fb1e5bfa4a7d9c4d51d0af3efbcc25124
b7f8500a93818b3f6b621d1f410854f02bd87a648a4955fcebb67bfcdcbc
7bbe410dae6a45e79fffc51f1f1f4c8786682db0609d42045d203650340b
67923e6a9a2120930182828f9a82ffc7c5e4831be89d87d7ccfd021bfb13
57"""
}

def clean_hex(hex_str):
    """Remove whitespace from hex string."""
    return ''.join(hex_str.split())

def hex_to_bytes(hex_str):
    """Convert hex string to bytes."""
    return bytes.fromhex(clean_hex(hex_str))

def xor_bytes(a, b):
    """XOR two byte arrays."""
    return bytes(x ^ y for x, y in zip(a, b))

def analyze_xor_result(data, name):
    """Analyze XOR result for patterns."""
    printable = sum(1 for b in data if 32 <= b <= 126)
    zero_bytes = sum(1 for b in data if b == 0)
    
    print(f"\n{name}:")
    print(f"  Length: {len(data)} bytes")
    print(f"  Zero bytes: {zero_bytes} ({100*zero_bytes/len(data):.1f}%)")
    print(f"  Printable: {printable} ({100*printable/len(data):.1f}%)")
    
    # Check for repeating patterns
    for pattern_len in [1, 2, 4, 8, 16, 29, 32]:
        if len(data) >= pattern_len * 3:
            chunks = [data[i:i+pattern_len] for i in range(0, len(data), pattern_len)]
            unique_chunks = len(set(chunks))
            if unique_chunks < len(chunks) * 0.5:
                print(f"  Repeating pattern detected at length {pattern_len}!")
    
    # Show first bytes
    print(f"  First 50 bytes hex: {data[:50].hex()}")
    
    # Try as ASCII
    try:
        text = data.decode('ascii', errors='replace')
        if printable > len(data) * 0.3:
            print(f"  As ASCII: {text[:100]}")
    except:
        pass
    
    return data

def check_single_byte_xor(data, name):
    """Try single-byte XOR keys."""
    print(f"\n--- Single Byte XOR Analysis: {name} ---")
    
    best_score = 0
    best_key = 0
    best_text = ""
    
    for key in range(256):
        decrypted = bytes(b ^ key for b in data)
        score = sum(1 for b in decrypted if b in b'etaoinshrdlcumwfgypbvkjxqz ETAOINSHRDLCUMWFGYPBVKJXQZ')
        if score > best_score:
            best_score = score
            best_key = key
            best_text = decrypted
    
    print(f"  Best key: 0x{best_key:02x} ('{chr(best_key) if 32<=best_key<=126 else '?'}')")
    print(f"  Score: {best_score}")
    print(f"  First 100 bytes: {best_text[:100].decode('ascii', errors='replace')}")
    
    return best_key, best_text

def main():
    print("="*70)
    print("XOR ANALYSIS OF CICADA HEX BLOCKS")
    print("="*70)
    
    # Convert all blocks to bytes
    blocks = {name: hex_to_bytes(data) for name, data in BLOCKS.items()}
    
    print("\nBlock sizes:")
    for name, data in blocks.items():
        print(f"  {name}: {len(data)} bytes")
    
    # All should be same size
    sizes = set(len(d) for d in blocks.values())
    if len(sizes) == 1:
        print(f"\nAll blocks are {sizes.pop()} bytes - good for XOR analysis!")
    
    # XOR pairs together
    print("\n" + "="*70)
    print("XOR COMBINATIONS")
    print("="*70)
    
    lp = blocks["liber_primus"]
    intus = blocks["intus"]
    runes = blocks["runes"]
    
    # XOR each pair
    lp_xor_intus = xor_bytes(lp, intus)
    lp_xor_runes = xor_bytes(lp, runes)
    intus_xor_runes = xor_bytes(intus, runes)
    
    analyze_xor_result(lp_xor_intus, "liber_primus XOR intus")
    analyze_xor_result(lp_xor_runes, "liber_primus XOR runes")
    analyze_xor_result(intus_xor_runes, "intus XOR runes")
    
    # XOR all three together
    all_xor = xor_bytes(xor_bytes(lp, intus), runes)
    analyze_xor_result(all_xor, "ALL THREE XORed")
    
    # Try single-byte XOR on each
    print("\n" + "="*70)
    print("SINGLE BYTE XOR ANALYSIS")
    print("="*70)
    
    for name, data in blocks.items():
        check_single_byte_xor(data, name)
    
    # Check if any XOR result has more structure
    check_single_byte_xor(lp_xor_intus, "LP XOR INTUS")
    check_single_byte_xor(lp_xor_runes, "LP XOR RUNES")
    check_single_byte_xor(intus_xor_runes, "INTUS XOR RUNES")
    
    # Save results
    output_dir = Path("c:/Users/tyler/Repos/Cicada3301/tools/extracted")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "xor_lp_intus.bin", 'wb') as f:
        f.write(lp_xor_intus)
    with open(output_dir / "xor_lp_runes.bin", 'wb') as f:
        f.write(lp_xor_runes)
    with open(output_dir / "xor_intus_runes.bin", 'wb') as f:
        f.write(intus_xor_runes)
    with open(output_dir / "xor_all_three.bin", 'wb') as f:
        f.write(all_xor)
    
    print(f"\nXOR results saved to {output_dir}")
    
    print("\n" + "="*70)
    print("SPECIAL CHECK: mod 29 RELATIONSHIP")
    print("="*70)
    
    # Check if there's a relationship via mod 29 (alphabet size)
    for name, hex_data in BLOCKS.items():
        hex_clean = clean_hex(hex_data)
        n = int(hex_clean, 16)
        print(f"{name}: int mod 29 = {n % 29}")
        
        # Check if consecutive byte differences follow prime pattern
        data = hex_to_bytes(hex_data)
        diffs = [(data[i+1] - data[i]) % 29 for i in range(len(data)-1)]
        diff_counts = Counter(diffs)
        print(f"  Byte diff mod 29 distribution (top 5): {diff_counts.most_common(5)}")

if __name__ == "__main__":
    main()
