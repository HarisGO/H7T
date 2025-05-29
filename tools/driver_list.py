# tools/driver_lister.py

import subprocess
import sys

def main():
    """
    Attempts to list basic driver information using OS-specific commands.
    Note: Requires relevant OS commands to be available in PATH and
          may require elevated privileges for full details.
    """
    print("--- Driver Lister ---")

    if sys.platform.startswith('win'):
        # Windows: Using 'driverquery' command
        print("Listing drivers for Windows (may take a moment)...")
        try:
            result = subprocess.run(
                ["driverquery"],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW # Hide command prompt window
            )
            print("\n" + result.stdout)
        except FileNotFoundError:
            print("Error: 'driverquery' command not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'driverquery' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform.startswith('linux'):
        # Linux: Using 'lsmod' for kernel modules, and 'lspci -k' for device drivers
        print("Listing drivers/kernel modules for Linux (may require 'sudo' or 'kmod' package)...")
        print("\n--- Kernel Modules (lsmod) ---")
        try:
            result = subprocess.run(
                ["lsmod"],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
        except FileNotFoundError:
            print("Warning: 'lsmod' command not found. Kernel modules cannot be listed.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'lsmod' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        print("\n--- PCI Device Kernel Drivers (lspci -k) ---")
        try:
            result = subprocess.run(
                ["lspci", "-k"], # -k shows kernel driver in use
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
        except FileNotFoundError:
            print("Warning: 'lspci' command not found. PCI device drivers cannot be listed.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'lspci' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform.startswith('darwin'):
        # macOS: Using 'kextstat' for kernel extensions
        print("Listing kernel extensions for macOS...")
        try:
            result = subprocess.run(
                ["kextstat"],
                capture_output=True,
                text=True,
                check=True
            )
            print("\n" + result.stdout)
        except FileNotFoundError:
            print("Error: 'kextstat' command not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'kextstat' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    else:
        print("Unsupported operating system for automatic driver listing.")
        print("Please check your OS documentation for commands like 'driverquery' (Windows), 'lsmod'/'lspci' (Linux), or 'kextstat' (macOS).")

    print("\n--- Driver Listing Complete ---")

# Do NOT call main() here. H7T does that automatically.
