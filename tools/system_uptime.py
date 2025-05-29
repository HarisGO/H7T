# tools/system_uptime_checker.py

import subprocess
import sys
import datetime
import os # Added for os.path.exists to check /proc/uptime

def main():
    """
    Checks and displays the system's uptime.
    Supports Linux, macOS, Windows, and includes specific handling for Android.
    """
    print("--- System Uptime Checker ---")

    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        # For Linux and macOS, try the 'uptime' command first
        try:
            print("Fetching uptime for Linux/macOS...")
            result = subprocess.run(
                ["uptime"],
                capture_output=True,
                text=True,
                check=True
            )
            print("\n" + result.stdout.strip())

        except FileNotFoundError:
            # Fallback for Linux/macOS if 'uptime' command isn't present
            print("Warning: 'uptime' command not found. Trying /proc/uptime...")
            try_proc_uptime()
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'uptime' command (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform.startswith('win'):
        # For Windows, use 'wmic' to get the last boot up time
        try:
            print("Fetching uptime for Windows...")
            result = subprocess.run(
                ["wmic", "os", "get", "LastBootUpTime"],
                capture_output=True,
                text=True,
                check=True
            )
            output_lines = result.stdout.splitlines()
            boot_time_str = ""
            # Parse the output to find the actual timestamp string
            for line in output_lines:
                line = line.strip()
                if line and not line.startswith("LastBootUpTime"): # Skip header line
                    boot_time_str = line
                    break

            if boot_time_str:
                # Extract the YYYYMMDDHHMMSS part before the decimal point
                boot_time_str_cleaned = boot_time_str.split('.')[0]
                
                # Parse the time string into a datetime object
                boot_time = datetime.datetime.strptime(boot_time_str_cleaned, "%Y%m%d%H%M%S")
                current_time = datetime.datetime.now()
                
                # Calculate the duration
                uptime_duration = current_time - boot_time

                # Format the duration for display
                days = uptime_duration.days
                # The .seconds attribute gives seconds within the last day
                seconds_total = int(uptime_duration.total_seconds()) # Get total seconds for calculation
                hours = (seconds_total % (3600 * 24)) // 3600
                minutes = (seconds_total % 3600) // 60
                seconds_remainder = seconds_total % 60

                print(f"\nSystem Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds_remainder} seconds")
            else:
                print("Could not parse system boot time from 'wmic' output.")

        except FileNotFoundError:
            print("Error: 'wmic' command not found. Cannot determine uptime on this system.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'wmic' command (Exit Code: {e.returncode}):")
            print(f"Stderr: {e.stderr.strip()}")
        except ValueError:
            print("Error: Could not parse boot time string from 'wmic' output. Format unexpected.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif sys.platform == 'android':
        # For Android (often running via Termux or similar Linux-like environment)
        # Try /proc/uptime as it's typically reliable on Linux-based systems
        print("Fetching uptime for Android (via /proc/uptime or 'uptime' command)...")
        try_proc_uptime()
        
    else:
        print("Unsupported operating system. Uptime cannot be determined automatically for this platform.")

    print("\n-------------------------")

def try_proc_uptime():
    """Helper function to read uptime from /proc/uptime."""
    try:
        if os.path.exists("/proc/uptime"):
            with open("/proc/uptime", "r") as f:
                uptime_seconds_str = f.readline().split()[0]
                uptime_seconds = float(uptime_seconds_str)
                
                uptime_duration = datetime.timedelta(seconds=uptime_seconds)
                days = uptime_duration.days
                seconds_total = int(uptime_duration.total_seconds())
                hours = (seconds_total % (3600 * 24)) // 3600
                minutes = (seconds_total % 3600) // 60
                seconds_remainder = seconds_total % 60
                
                print(f"\nSystem Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds_remainder} seconds (from /proc/uptime)")
        else:
            print("Error: /proc/uptime not found. Trying 'uptime' command as fallback...")
            # Fallback to uptime command if /proc/uptime failed, though less likely on stock Android term
            subprocess.run(
                ["uptime"],
                capture_output=True,
                text=True,
                check=True
            )
            print("\n" + result.stdout.strip())
            
    except FileNotFoundError:
        print("Error: 'uptime' command not found and /proc/uptime failed. Cannot determine uptime.")
    except Exception as e:
        print(f"An error occurred while trying to get uptime: {e}")

# Do NOT call main() here. H7T does that automatically.
