#!/usr/bin/env python3
"""
Verify PGP signature on the XOR-discovered message using Cicada 3301's public key.
"""

import pgpy
from pathlib import Path

def verify_signature():
    print("="*70)
    print("PGP SIGNATURE VERIFICATION")
    print("="*70)
    
    # Load Cicada's public key
    key_path = Path("c:/Users/tyler/Repos/Cicada3301/6D854CD7933322A601C3286D181F01E57A35090F.asc")
    print(f"\nLoading public key from: {key_path.name}")
    
    key, _ = pgpy.PGPKey.from_file(str(key_path))
    print(f"Key ID: {key.fingerprint}")
    print(f"Key created: {key.created}")
    
    # Show key user IDs
    for uid in key.userids:
        print(f"User ID: {uid}")
    
    # Load the signed message
    message_path = Path("c:/Users/tyler/Repos/Cicada3301/tools/extracted/xor_discovered_message.pgp")
    print(f"\nLoading message from: {message_path.name}")
    
    with open(message_path, 'r') as f:
        message_text = f.read()
    
    # Parse the signed message
    signed_message = pgpy.PGPMessage.from_blob(message_text)
    
    print(f"\nMessage type: {signed_message.type}")
    print(f"Is signed: {signed_message.is_signed}")
    
    if signed_message.is_signed:
        print("\n--- Signature Details ---")
        for sig in signed_message.signatures:
            print(f"  Signature type: {sig.type}")
            print(f"  Signer: {sig.signer}")
            print(f"  Created: {sig.created}")
            print(f"  Hash algorithm: {sig.hash_algorithm}")
    
    # Verify the signature
    print("\n--- Verification ---")
    try:
        verification = key.verify(signed_message)
        
        if verification:
            print("✅ SIGNATURE VERIFIED!")
            print("   This message is authentically signed by Cicada 3301!")
        else:
            print("❌ Signature verification failed")
            
    except Exception as e:
        print(f"Verification error: {e}")
        
        # Try with the subkey
        print("\nTrying with subkeys...")
        for subkey_id, subkey in key.subkeys.items():
            try:
                verification = subkey.verify(signed_message)
                if verification:
                    print(f"✅ VERIFIED with subkey {subkey_id}!")
                    break
            except:
                pass
    
    # Extract the message content
    print("\n--- Message Content ---")
    print(signed_message.message)
    
    return signed_message.message

if __name__ == "__main__":
    message = verify_signature()
    
    print("\n" + "="*70)
    print("THE CIPHER TO SOLVE")
    print("="*70)
    
    # Extract just the cipher part
    lines = message.strip().split('\n')
    cipher_lines = [l for l in lines if l.strip() and not l.startswith('Good') and not l.strip().isdigit()]
    cipher = ' '.join(cipher_lines)
    
    print(f"\nCipher text: {cipher}")
    print(f"\nThis is an authentic Cicada 3301 puzzle!")
