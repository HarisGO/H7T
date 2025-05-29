# tools/process_lister.py

import os
import sys

def main():
    """
    Lists currently running processes using platform-specific commands.
    """
    print("--- Process Lister ---")
    print("Listing active processes...")

    if sys.platform.startswith('win'):
        # Windows: Uses 'tasklist' command
        command = 'tasklist'
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # Linux/macOS: Uses 'ps aux' command
        command = 'ps aux'
    else:
        print("Unsupported operating system for this tool.")
        print("Cannot list processes automatically.")
        return

    try:
        # os.popen returns a file object connected to the pipe
        with os.popen(command) as process_output:
            for line in process_output:
                print(line.strip())
    except Exception as e:
        print(f"Error executing command '{command}': {e}")
        print("Could not list processes.")

    print("\n--- End of Process List ---")

# Do NOT call main() here. H7T does that automatically.
