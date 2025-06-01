# tools/code_studio_lite.py

import os
import subprocess
import sys
import time

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_file(filepath):
    """Loads content from a file into a list of lines."""
    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist. Creating a new one.")
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print(f"Error loading file '{filepath}': {e}")
        return None

def save_file(filepath, lines):
    """Saves a list of lines back to a file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"File saved successfully to '{filepath}'.")
        return True
    except Exception as e:
        print(f"Error saving file '{filepath}': {e}")
        return False

def display_code(lines, highlight_line=None):
    """Prints the code with line numbers."""
    print("\n--- Current Code ---")
    if not lines:
        print("(File is empty)")
        return

    for i, line in enumerate(lines):
        line_num = f"{i+1:4d} "
        if i+1 == highlight_line:
            # Highlight the line if requested (basic highlighting)
            print(f"> {line_num}| {line.rstrip()}")
        else:
            print(f"  {line_num}| {line.rstrip()}")
    print("--------------------")

def lint_code(filepath):
    """Runs flake8 linter on the specified Python file."""
    print("\n--- Running Linter (flake8) ---")
    if not os.path.exists(filepath):
        print("File does not exist. Cannot lint.")
        return

    try:
        # Check if flake8 is installed by trying to run it
        subprocess.run(["flake8", "--version"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform.startswith('win') else 0)
    except FileNotFoundError:
        print("Error: 'flake8' not found. Please install it: 'pip install flake8'")
        print("Cannot perform linting without flake8.")
        return
    except Exception as e:
        print(f"Error checking flake8 installation: {e}")
        return

    try:
        result = subprocess.run(
            ["flake8", filepath],
            capture_output=True,
            text=True,
            check=False # Do not raise exception on non-zero exit code (flake8 uses non-zero for found errors)
        )
        if result.stdout.strip():
            print("Linter Warnings/Errors Found:")
            print(result.stdout)
        else:
            print("No linting warnings or errors found. Code looks clean!")
    except Exception as e:
        print(f"An error occurred during linting: {e}")
    print("-----------------------------")

def run_code(filepath):
    """Executes the specified Python file."""
    print("\n--- Running Code ---")
    if not os.path.exists(filepath):
        print("File does not exist. Cannot run.")
        return

    try:
        process = subprocess.Popen(
            [sys.executable, filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Print output in real-time
        for line in iter(process.stdout.readline, ''):
            print(f"OUT: {line.strip()}")
        for line in iter(process.stderr.readline, ''):
            print(f"ERR: {line.strip()}")

        return_code = process.wait()
        print(f"\nCode finished with exit code {return_code}.")
    except FileNotFoundError:
        print(f"Error: Python executable or file '{filepath}' not found.")
    except Exception as e:
        print(f"An error occurred while running code: {e}")
    print("--------------------")

def main():
    """
    Code Studio Lite: A simple command-driven terminal editor, linter, and runner.
    """
    print("--- Code Studio Lite ---")
    print("This is a command-driven editor, not a full-screen editor like Nano.")
    print("It works with Python files.")
    print("------------------------")

    filepath = input("Enter the path to your Python file (e.g., 'my_script.py'): ").strip()
    if not filepath.lower().endswith(".py"):
        filepath += ".py" # Auto-add .py extension

    current_lines = load_file(filepath)
    if current_lines is None: # Error loading
        input("Press Enter to return to menu...")
        return

    while True:
        clear_screen()
        display_code(current_lines)

        print("\n--- Actions ---")
        print(" view             : Redisplay code")
        print(" append           : Add new lines to end")
        print(" edit <line_num>  : Edit a specific line")
        print(" delete <line_num>: Delete a specific line")
        print(" insert <line_num>: Insert line before specified line")
        print(" save             : Save changes to file")
        print(" lint             : Check code for errors/style (requires 'flake8')")
        print(" run              : Execute the code")
        print(" exit             : Exit the studio")
        print("-----------------")

        command = input("Enter command: ").strip().lower()
        parts = command.split(' ', 1) # Split into command and argument

        if parts[0] == 'view':
            # display_code is already called at top of loop
            pass
        elif parts[0] == 'append':
            print("\n--- Append Mode ---")
            print("Enter lines of code. Type 'EOF' on a new line to finish.")
            new_lines = []
            while True:
                line = input(f"[{len(current_lines) + len(new_lines) + 1}] > ")
                if line.strip().lower() == 'eof':
                    break
                new_lines.append(line + '\n') # Add newline for consistency
            current_lines.extend(new_lines)
        elif parts[0] == 'edit' and len(parts) > 1:
            try:
                line_num = int(parts[1])
                if 1 <= line_num <= len(current_lines):
                    print(f"Editing line {line_num}: {current_lines[line_num - 1].rstrip()}")
                    new_content = input(f"Enter new content for line {line_num}: ")
                    current_lines[line_num - 1] = new_content + '\n'
                else:
                    print("Invalid line number.")
            except ValueError:
                print("Invalid line number. Use 'edit <number>'.")
        elif parts[0] == 'delete' and len(parts) > 1:
            try:
                line_num = int(parts[1])
                if 1 <= line_num <= len(current_lines):
                    deleted_line = current_lines.pop(line_num - 1)
                    print(f"Deleted line {line_num}: {deleted_line.rstrip()}")
                else:
                    print("Invalid line number.")
            except ValueError:
                print("Invalid line number. Use 'delete <number>'.")
        elif parts[0] == 'insert' and len(parts) > 1:
            try:
                line_num = int(parts[1])
                if 1 <= line_num <= len(current_lines) + 1: # Can insert at end
                    new_content = input(f"Enter content to insert before line {line_num}: ")
                    current_lines.insert(line_num - 1, new_content + '\n')
                else:
                    print("Invalid line number. Cannot insert beyond current end.")
            except ValueError:
                print("Invalid line number. Use 'insert <number>'.")
        elif parts[0] == 'save':
            save_file(filepath, current_lines)
        elif parts[0] == 'lint':
            # Save before linting to ensure latest changes are checked
            if save_file(filepath, current_lines):
                lint_code(filepath)
            input("Press Enter to continue...")
        elif parts[0] == 'run':
            # Save before running to ensure latest changes are executed
            if save_file(filepath, current_lines):
                run_code(filepath)
            input("Press Enter to continue...")
        elif parts[0] == 'exit':
            print("Exiting Code Studio Lite.")
            break
        else:
            print("Unknown command. Please try again.")
            input("Press Enter to continue...")

# Do NOT call main() here. H7T does that automatically.