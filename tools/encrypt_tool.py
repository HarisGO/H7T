# tools/encrypt_tool.py
from core.utils import ENCRYPTION_KEY

def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def main():
    print("\n[1] Encrypt\n[2] Decrypt")
    mode = input("Select mode: ")

    if mode not in ['1', '2']:
        print("Invalid choice.")
        return

    data = input("Enter text: ")
    result = xor_encrypt_decrypt(data, ENCRYPTION_KEY)
    print("Result:", result)