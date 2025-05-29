# tools/dependency_scanner.py

import os
import re
import subprocess
import sys

def get_installed_packages():
    """
    Returns a set of top-level package names that are currently installed.
    """
    try:
        # Use pip list --format=freeze for basic package names
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=freeze"],
            capture_output=True, text=True, check=True
        )
        installed = set()
        for line in result.stdout.splitlines():
            if '==' in line: # Only consider lines with version specifiers
                package_name = line.split('==')[0].strip()
                # Basic normalization for common cases (e.g., beautifulsoup4 -> bs4)
                # This is a simple heuristic and might not cover all cases.
                if package_name.lower() == 'beautifulsoup4':
                    installed.add('bs4')
                else:
                    installed.add(package_name.lower())
        return installed
    except Exception as e:
        print(f"Warning: Could not get list of installed packages ({e}).")
        return set()

def main():
    """
    Scans Python files in the 'tools/' directory for import statements
    and suggests potential missing modules to install.
    """
    print("--- H7T Dependency Scanner (Basic) ---")
    print("This tool attempts to find imported modules in other tools and suggest installations.")
    print("It might not be perfectly accurate due to parsing complexity.")

    tools_dir = os.path.join(os.path.dirname(__file__)) # Assumes this tool is in 'tools/'
    potential_modules = set()

    print(f"\nScanning Python files in '{tools_dir}'...")

    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and filename != os.path.basename(__file__):
            filepath = os.path.join(tools_dir, filename)
            print(f"  Processing: {filename}")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Regex to find 'import <module>' or 'from <module> import ...'
                    # It tries to be simple to avoid complex parsing.
                    # It will capture anything after 'import ' or 'from ' up to the first space/newline
                    imports = re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_.]+)', content, re.MULTILINE)
                    for imp in imports:
                        # Take the top-level module name (e.g., 'requests.exceptions' -> 'requests')
                        top_level_module = imp.split('.')[0]
                        potential_modules.add(top_level_module.lower())
            except Exception as e:
                print(f"    Warning: Could not read/parse {filename}: {e}")

    if not potential_modules:
        print("\nNo potential external module imports found in other tools.")
        print("This could mean all dependencies are built-in or detection failed.")
        return

    print("\n--- Detected Potential External Module Imports ---")
    print("Note: This list includes *all* detected imports, including standard library modules.")
    print("You will need to manually identify which ones are external packages.")

    installed_packages = get_installed_packages()
    missing_suggestions = []

    for module in sorted(list(potential_modules)):
        if module not in installed_packages:
            missing_suggestions.append(module)
        print(f"- {module} {'(Installed)' if module in installed_packages else '(Potentially Missing/External)'}")

    print("\n-------------------------------------------------")

    if missing_suggestions:
        print("\nBased on initial scan, these modules *might* be missing/external:")
        for suggestion in missing_suggestions:
            print(f"- {suggestion}")
        print("\nConsider installing them if your tools are not working as expected.")
    else:
        print("\nAll detected potential external modules seem to be installed.")

    # Now, offer to install
    while True:
        install_choice = input("\nEnter module name to install, 'list' to see suggestions, or 'exit': ").strip()
        if install_choice.lower() == 'exit':
            print("Exiting Dependency Scanner.")
            break
        elif install_choice.lower() == 'list':
            if missing_suggestions:
                print("\nSuggested modules to install:")
                for suggestion in missing_suggestions:
                    print(f"- {suggestion}")
            else:
                print("No clear missing module suggestions at this time.")
            continue
        elif not install_choice:
            print("Please enter a module name, 'list', or 'exit'.")
            continue

        print(f"Attempting to install '{install_choice}'...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", install_choice],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"\nSuccessfully installed '{install_choice}'.")
            if result.stdout:
                print("\n--- Pip Output ---")
                print(result.stdout)
                print("------------------")
            # After installation, update the installed packages list for future checks
            installed_packages = get_installed_packages()

        except subprocess.CalledProcessError as e:
            print(f"\nError installing '{install_choice}':")
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
            print("Error: 'pip' command not found. Ensure Python and pip are correctly installed.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Do NOT call main() here. H7T does that automatically.
