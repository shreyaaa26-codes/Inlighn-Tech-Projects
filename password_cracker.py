import hashlib
import itertools
import string
import argparse
from tqdm import tqdm

def generate_passwords(min_length, max_length, characters):
    for length in range(min_length, max_length + 1):
        for pwd in itertools.product(characters, repeat=length):
            yield ''.join(pwd)

def crack_hash(target_hash, hash_type='md5', min_length=1, max_length=4, characters=string.ascii_lowercase + string.digits):
    try:
        hash_fn = getattr(hashlib, hash_type)
    except AttributeError:
        print(f"[!] Unsupported hash type: {hash_type}")
        return None

    total = sum(len(characters) ** i for i in range(min_length, max_length + 1))
    print(f"[*] Attempting to crack {target_hash} using {hash_type}...")
    
    for password in tqdm(generate_passwords(min_length, max_length, characters), total=total, desc="Cracking"):
        if hash_fn(password.encode()).hexdigest() == target_hash:
            return password
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Hash Cracker")
    parser.add_argument("hash", help="Hash to crack")
    parser.add_argument("--hash_type", default="md5", help="Hashing algorithm (e.g., md5, sha256, sha3_512)")
    parser.add_argument("--min_length", type=int, default=1, help="Minimum password length")
    parser.add_argument("--max_length", type=int, default=4, help="Maximum password length")
    parser.add_argument("-c", "--characters", default=string.ascii_lowercase + string.digits, help="Characters to use (default: a-z, 0-9)")

    args = parser.parse_args()

    result = crack_hash(args.hash, args.hash_type, args.min_length, args.max_length, args.characters)
    if result:
        print(f"[+] Password found: {result}")
    else:
        print("[!] Password not found.")
