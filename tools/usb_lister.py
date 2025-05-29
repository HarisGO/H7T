# tools/usb_device_lister.py

import subprocess
import sys

def main():
    """
    Lists connected USB devices using OS-specific commands.
    Note: Requires relevant OS commands to be present (e.g., lsusb on Linux).
    """
    print("--- USB Device Lister ---")
    print("Attempting to list connected USB devices...")
    print("-------------------------")

    if sys.platform.startswith('win'):
        # Windows: Using 'wmic' command for USB controllers and devices
        print("\n--- Windows USB Devices ---")
        try:
            # List USB controllers
            result_controllers = subprocess.run(
                ["wmic", "path", "Win32_USBController", "get", "Caption,DeviceID"],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            print("USB Controllers:")
            print(result_controllers.stdout)

            # List USB hubs/devices (can be verbose)
            print("USB Hubs/Devices (potentially verbose):")
            result_devices = subprocess.run(
                ["wmic", "path", "Win32_USBHub", "get", "Caption,DeviceID,Name"], # Or Win32_PnPEntity for more
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            print(result_devices.stdout)

        except FileNotFoundError:
            print("Error: 'wmic' command not found. Cannot list USB devices.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing wmic command (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform.startswith('linux') or sys.platform == 'android':
        # Linux/Android: Using 'lsusb' command
        print("\n--- Linux/Android USB Devices (lsusb) ---")
        try:
            result = subprocess.run(
                ["lsusb"],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
        except FileNotFoundError:
            print("Error: 'lsusb' command not found. Please install it (e.g., 'sudo apt install usbutils' or 'pkg install usbutils' on Termux).")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'lsusb' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform.startswith('darwin'):
        # macOS: Using 'system_profiler SPUSBDataType'
        print("\n--- macOS USB Devices ---")
        try:
            result = subprocess.run(
                ["system_profiler", "SPUSBDataType"],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
        except FileNotFoundError:
            print("Error: 'system_profiler' command not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'system_profiler' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    else:
        print("Unsupported operating system for automatic USB device listing.")

    print("\n--- USB Device Listing Complete ---")

# Do NOT call main() here. H7T does that automatically.
