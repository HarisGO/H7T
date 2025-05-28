# tools/stego_tool.py
from PIL import Image
from core.utils import ENCRYPTION_KEY

def xor(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def encode_text_in_image(image_path, output_path, text):
    img = Image.open(image_path)
    binary_text = ''.join([format(ord(char), '08b') for char in xor(text, ENCRYPTION_KEY)]) + '1111111111111110'
    data = iter(img.getdata())
    new_data = []

    for byte in binary_text:
        pixel = list(next(data))
        pixel[0] = pixel[0] & ~1 | int(byte)
        new_data.append(tuple(pixel))
    new_data += list(data)
    img.putdata(new_data)
    img.save(output_path)
    print("Text encoded and saved to", output_path)

def decode_text_from_image(image_path):
    img = Image.open(image_path)
    binary = ''
    for pixel in img.getdata():
        binary += str(pixel[0] & 1)
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    msg = ''.join(chars).split('\x0f')[0]
    print("Hidden message:", xor(msg, ENCRYPTION_KEY))

def main():
    print("\n[1] Encode text into image\n[2] Decode text from image")
    choice = input("Choose: ")
    if choice == "1":
        path = input("Path to image: ")
        output = input("Output image name: ")
        text = input("Text to hide: ")
        encode_text_in_image(path, output, text)
    elif choice == "2":
        path = input("Path to image: ")
        decode_text_from_image(path)
    else:
        print("Invalid choice.")