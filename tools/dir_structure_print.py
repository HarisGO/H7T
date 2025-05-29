# tools/directory_structure_printer.py

import os

def main():
    """
    Prints the directory structure in a tree-like format.
    """
    print("--- Directory Structure Printer ---")

    target_dir = input("Enter the path to the directory you want to list (e.g., '.' for current): ").strip()

    if not target_dir:
        print("Directory path cannot be empty. Aborting.")
        return

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    print(f"\n--- Directory Structure for '{target_dir}' ---")

    def print_tree(startpath, indent=''):
        """Recursive function to print directory tree."""
        # Get list of entries, sorting directories before files
        entries = sorted(os.listdir(startpath), key=lambda s: (not os.path.isdir(os.path.join(startpath, s)), s.lower()))

        for i, entry in enumerate(entries):
            full_path = os.path.join(startpath, entry)
            is_last = (i == len(entries) - 1)
            
            # Determine prefix for current entry
            prefix = "└── " if is_last else "├── "
            print(f"{indent}{prefix}{entry}")

            # If it's a directory, recurse
            if os.path.isdir(full_path):
                next_indent = indent + ("    " if is_last else "│   ")
                print_tree(full_path, next_indent)

    try:
        print_tree(target_dir)
    except Exception as e:
        print(f"An error occurred while printing the directory structure: {e}")

    print("\n-------------------------------------------")

# Do NOT call main() here. H7T does that automatically.
