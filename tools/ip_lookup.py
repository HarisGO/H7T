# tools/whois_ip_lookup.py

import whois # This is the 'python-whois' library

def main():
    """
    Performs a WHOIS lookup for a given IP address.
    Requires the 'python-whois' library (pip install python-whois).
    """
    print("--- WHOIS IP Lookup ---")
    print("Enter an IP address to perform a WHOIS lookup.")
    print("Type 'exit' to quit.")
    print("-----------------------")

    while True:
        ip_address = input("Enter IP address: ").strip()

        if ip_address.lower() == 'exit':
            print("Exiting WHOIS IP Lookup.")
            break

        if not ip_address:
            print("IP address cannot be empty. Please enter an IP or 'exit'.")
            continue

        print(f"\nLooking up WHOIS information for {ip_address}...")
        try:
            # Perform the WHOIS lookup
            w = whois.whois(ip_address)

            if isinstance(w, whois.parser.WhoisEntry):
                print("\n--- WHOIS Information ---")
                for key, value in w.items():
                    if value: # Only print if value exists
                        # Handle list values for better readability
                        if isinstance(value, list):
                            print(f"{key.replace('_', ' ').title()}:")
                            for item in value:
                                print(f"  - {item}")
                        else:
                            print(f"{key.replace('_', ' ').title()}: {value}")
                print("-------------------------")
            else:
                print(f"No WHOIS information found for {ip_address} or it could not be parsed.")

        except whois.exceptions.WhoisCommandFailed:
            print(f"Error: WHOIS lookup failed for {ip_address}. It might be a private IP, invalid, or no WHOIS server responded.")
        except Exception as e:
            print(f"An unexpected error occurred during WHOIS lookup: {e}")
            print("Please ensure you have the 'python-whois' library installed (pip install python-whois).")

# Do NOT call main() here. H7T does that automatically.
