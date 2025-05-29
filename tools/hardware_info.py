# tools/hardware_info_viewer.py

import subprocess
import sys

def main():
    """
    Displays general hardware information about the system.
    Information varies by operating system.
    May require certain system commands to be present (e.g., lshw on Linux).
    """
    print("--- Hardware Info Viewer ---")
    print("Gathering system hardware information...")
    print("----------------------------")

    if sys.platform.startswith('win'):
        # Windows: Using systeminfo command
        print("\n--- Windows System Information ---")
        try:
            result = subprocess.run(
                ["systeminfo"],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW # Hide command prompt window
            )
            # Filter output to show relevant sections
            lines = result.stdout.splitlines()
            for line in lines:
                if any(keyword in line for keyword in ["OS Name", "OS Version", "System Manufacturer", "System Model", "System Type", "Processor(s)", "Total Physical Memory", "Available Physical Memory", "Virtual Memory"]):
                    print(line.strip())
        except FileNotFoundError:
            print("Error: 'systeminfo' command not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'systeminfo' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform.startswith('linux'):
        # Linux: Using lshw (if available) and /proc files
        print("\n--- Linux Hardware Information ---")
        try:
            print("\nProcessor Info (/proc/cpuinfo):")
            with open("/proc/cpuinfo", "r") as f:
                for _ in range(5): # Read first few lines for basic CPU info
                    line = f.readline()
                    if line.startswith("model name") or line.startswith("cpu cores"):
                        print(line.strip())

            print("\nMemory Info (/proc/meminfo):")
            with open("/proc/meminfo", "r") as f:
                print(f.readline().strip()) # MemTotal
                print(f.readline().strip()) # MemFree

            print("\nDetailed Hardware (sudo lshw -short -C cpu,memory,disk,display,network,audio):")
            print("  (May require 'sudo lshw' and 'lshw' package. Output might be long.)")
            result = subprocess.run(
                ["sudo", "lshw", "-short", "-C", "cpu,memory,disk,display,network,audio"],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
        except FileNotFoundError:
            print("Warning: 'lshw' command not found or /proc files inaccessible. Cannot get detailed info.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'lshw' (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform.startswith('darwin'):
        # macOS: Using system_profiler
        print("\n--- macOS Hardware Information ---")
        try:
            print("\nSystem Hardware Overview:")
            result = subprocess.run(
                ["system_profiler", "SPHardwareDataType"],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)

            print("\nProcessor Info:")
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout.strip())

            print("\nMemory Info (Total):")
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True,
                text=True,
                check=True
            )
            mem_bytes = int(result.stdout.strip())
            print(f"Total Memory: {mem_bytes / (1024**3):.2f} GB")

        except FileNotFoundError:
            print("Error: 'system_profiler' or 'sysctl' command not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Unsupported operating system for detailed hardware listing.")

    print("\n--- Hardware Info Complete ---")

# Do NOT call main() here. H7T does that automatically.
