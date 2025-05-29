# tools/file_encryptor.py

import os

def main():
    """
    Encrypts/decrypts a file using a simple XOR cipher with a fixed key.
    NOT SECURE FOR SENSITIVE DATA. FOR DEMONSTRATION ONLY.
    """
    print("--- Simple File Encryptor/Decryptor ---")
    print("WARNING: This tool uses a very basic XOR cipher with a fixed key.")
    print("         It is NOT secure for sensitive or confidential data.")
    print("         Use for demonstration or non-critical files only.")

    fixed_key = "98706547"
    key_bytes = fixed_key.encode('utf-8') # Convert key string to bytes
    key_len = len(key_bytes)

    input_filepath = input("\nEnter the path to the input file (e.g., 'my_document.txt'): ").strip()
    output_filepath = input("Enter the path for the output file (e.g., 'encrypted_document.txt'): ").strip()

    if not input_filepath or not output_filepath:
        print("Input or output file path cannot be empty. Aborting.")
        return

    if not os.path.exists(input_filepath):
        print(f"Error: Input file '{input_filepath}' not found.")
        return

    print(f"Processing '{input_filepath}' with XOR cipher...")

    try:
        with open(input_filepath, 'rb') as infile, open(output_filepath, 'wb') as outfile:
            i = 0
            while True:
                byte_data = infile.read(1) # Read one byte at a time
                if not byte_data:
                    break # End of file

                # Apply XOR operation
                encrypted_byte = bytes([byte_data[0] ^ key_bytes[i % key_len]])
                outfile.write(encrypted_byte)
                i += 1
        print(f"Successfully processed file. Output saved to '{output_filepath}'.")
        print("The same tool can be used to decrypt by running it on the output file.")

    except Exception as e:
        print(f"An error occurred during file processing: {e}")

# Do NOT call main() here. H7T does that automatically.
