# tools/download_modules.py

import subprocess
import sys

def main():
    """
    A tool to download Python modules (packages) using pip.
    """
    print("--- Module Downloader ---")
    print("This tool uses 'pip' to install Python packages.")
    print("Type 'exit' to quit.")

    while True:
        module_name = input("\nEnter the name of the module to install (e.g., 'requests', 'beautifulsoup4'): ").strip()

        if module_name.lower() == 'exit':
            print("Exiting Module Downloader.")
            break

        if not module_name:
            print("Module name cannot be empty. Please enter a module name or 'exit'.")
            continue

        print(f"Attempting to install '{module_name}'...")
        try:
            # Using sys.executable -m pip ensures that the pip associated
            # with the currently running Python interpreter (H7T's interpreter) is used.
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", module_name],
                capture_output=True,  # Capture stdout and stderr
                text=True,            # Decode stdout/stderr as text
                check=True            # Raise CalledProcessError if the command returns a non-zero exit code
            )

            print(f"\nSuccessfully installed '{module_name}'.")
            if result.stdout:
                print("\n--- Pip Output ---")
                print(result.stdout)
                print("------------------")

        except subprocess.CalledProcessError as e:
            print(f"\nError installing '{module_name}':")
            print(f"  Command: {' '.join(e.cmd)}")
            print(f"  Return Code: {e.returncode}")
            if e.stdout:
                print("\n--- Pip Stdout ---")
                print(e.stdout)
            if e.stderr:
                print("\n--- Pip Stderr (Error) ---")
                print(e.stderr)
            print("Please check the module name and your internet connection.")
        except FileNotFoundError:
            print("Error: 'pip' command not found. Ensure Python and pip are correctly installed and added to your system's PATH.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Do NOT call main() here. H7T does that automatically.
