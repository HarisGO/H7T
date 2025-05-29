# tools/simple_terminal.py

import os

def main():
    """
    A simple terminal-like tool for H7T.
    Allows users to execute basic shell commands.
    """
    print("Welcome to the H7T Simple Terminal!")
    print("Type 'exit' to quit.")

    while True:
        try:
            command = input("H7T_term $ ")
            if command.lower() == 'exit':
                print("Exiting Simple Terminal.")
                break
            elif not command.strip():
                continue # Skip empty commands

            # Execute the command and print its output
            # For security and simplicity, this example uses os.system()
            # For more robust applications, subprocess module is recommended
            os.system(command)

        except Exception as e:
            print(f"Error: {e}")

# Do NOT call main() here. H7T does that automatically.
