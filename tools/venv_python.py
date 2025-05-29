# tools/create_venv.py

import os
import subprocess

def main():
    """
    Creates a new Python virtual environment.
    """
    print("--- Python Virtual Environment Creator ---")

    venv_name = input("Enter a name for your new virtual environment (e.g., 'myenv'): ").strip()

    if not venv_name:
        print("Virtual environment name cannot be empty. Aborting.")
        return

    print(f"Creating virtual environment '{venv_name}'...")
    try:
        # Use subprocess.run for better control and error handling
        # It's more robust than os.system for this task.
        result = subprocess.run(
            ["python", "-m", "venv", venv_name],
            capture_output=True,
            text=True,
            check=True # Raise an exception if the command returns a non-zero exit code
        )
        print(f"Successfully created virtual environment '{venv_name}'.")
        print("\nTo activate it, run the following command in your terminal:")
        if os.name == 'nt':  # For Windows
            print(f"  {venv_name}\\Scripts\\activate")
        else:  # For Linux/macOS
            print(f"  source {venv_name}/bin/activate")
        print("\nTo deactivate it, simply type 'deactivate' in your terminal.")

    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment:")
        print(f"  Command: {' '.join(e.cmd)}")
        print(f"  Return Code: {e.returncode}")
        if e.stdout:
            print(f"  Output: {e.stdout}")
        if e.stderr:
            print(f"  Error: {e.stderr}")
        print("Please ensure Python is correctly installed and accessible in your PATH.")
    except FileNotFoundError:
        print("Error: 'python' command not found. Please ensure Python is installed and added to your system's PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Do NOT call main() here. H7T does that automatically.
