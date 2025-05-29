# tools/website_status_checker.py

import requests

def main():
    """
    Checks the HTTP status code for a list of provided URLs.
    Requires the 'requests' library (pip install requests).
    """
    print("--- Website Status Checker ---")
    print("Enter URLs one by one. Type 'done' or press Enter on an empty line to finish.")
    print("----------------------------")

    urls = []
    while True:
        url_input = input("Enter URL (or 'done' to finish): ").strip()
        if url_input.lower() == 'done' or not url_input:
            break
        # Basic validation to ensure it looks like a URL
        if not url_input.startswith("http://") and not url_input.startswith("https://"):
            print("  (Warning: URL does not start with http:// or https://. Adding https://)")
            url_input = "https://" + url_input
        urls.append(url_input)

    if not urls:
        print("\nNo URLs entered. Aborting.")
        return

    print("\n--- Checking URLs ---")
    for url in urls:
        try:
            # Use a timeout to prevent hanging on unresponsive servers
            response = requests.get(url, timeout=10)
            print(f"  {url}: Status Code {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"  {url}: Timeout Error (Server took too long to respond)")
        except requests.exceptions.ConnectionError:
            print(f"  {url}: Connection Error (Could not connect to server)")
        except requests.exceptions.RequestException as e:
            print(f"  {url}: An error occurred - {e}")
        except Exception as e:
            print(f"  {url}: An unexpected error occurred - {e}")

    print("\n--- Check Complete ---")

# Do NOT call main() here. H7T does that automatically.
