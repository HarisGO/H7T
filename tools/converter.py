# tools/all_in_one_converter.py

import requests # Required for currency conversion
import json # To parse API response

# --- API Configuration for Currency Converter ---
# IMPORTANT: You need a FREE API Key from https://www.exchangerate-api.com/
# Sign up, get your key, and paste it below.
# The free tier offers 1500 requests/month and updates once every 24 hours.
API_KEY = "1ef7f77d64327c51633428fb" # <<<--- Your provided API Key
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

def get_exchange_rates(base_currency):
    """Fetches exchange rates from the API for a given base currency."""
    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY: # Check if key is still default or empty
        print("\nERROR: API Key not set for currency converter.")
        print("Please get a FREE API Key from https://www.exchangerate-api.com/ and update 'API_KEY' in the tool's code.")
        return None

    url = f"{BASE_URL}/latest/{base_currency.upper()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
        else:
            print(f"API Error: {data.get('error-type', 'Unknown error')}")
            # Provide specific guidance for common API errors
            if data.get('error-type') == 'invalid-key':
                print("Guidance: Your API key is invalid. Double-check it or generate a new one.")
            elif data.get('error-type') == 'inactive-account':
                print("Guidance: Your account might be inactive. Check your email for confirmation or log in to ExchangeRate-API.com.")
            elif data.get('error-type') == 'quota-reached':
                print("Guidance: You have exceeded your API request quota. Wait for your quota to reset or upgrade your plan.")
            return None
    except requests.exceptions.Timeout:
        print("Network Error: Request to currency API timed out.")
        return None
    except requests.exceptions.ConnectionError:
        print("Network Error: Could not connect to the currency API. Check your internet connection.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None
    except json.JSONDecodeError:
        print("API Response Error: Could not parse JSON from API response. API might be down or returned unexpected data.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during API call: {e}")
        return None

def get_supported_currencies():
    """Fetches list of supported currency codes from the API."""
    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY: # Check if key is still default or empty
        print("\nERROR: API Key not set for currency converter.")
        print("Please get a FREE API Key from https://www.exchangerate-api.com/ and update 'API_KEY' in the tool's code.")
        return None

    url = f"{BASE_URL}/codes"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['result'] == 'success':
            return {code_info[0]: code_info[1] for code_info in data['supported_codes']}
        else:
            print(f"API Error fetching currency codes: {data.get('error-type', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"An error occurred fetching currency codes: {e}")
        return None

# --- Main Converter Logic ---
def main():
    """
    An all-in-one unit converter for various categories:
    Currency, Weight, Energy, Fuel Efficiency, Speed, Area, Time, Temperature.
    Currency rates are fetched real-time using ExchangeRate-API.com (requires API key).
    """
    print("--- All-in-One Converter ---")
    print("NOTE: Currency conversion requires internet and an API Key from ExchangeRate-API.com.")
    print("      (Free tier: 1500 req/month, updated every 24h)")
    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY:
        print("\n!!! WARNING: API_KEY is not set. Currency conversion will NOT work. !!!")
        print("             Please edit 'all_in_one_converter.py' and set your API_KEY.")


    conversion_factors = {
        "weight": {
            "kg_to_lbs": 2.20462,
            "lbs_to_kg": 0.453592,
            "g_to_oz": 0.035274,
            "oz_to_g": 28.3495
        },
        "energy": {
            "joules_to_calories": 0.239006,
            "calories_to_joules": 4.184,
            "kWh_to_joules": 3.6e6,
            "joules_to_kWh": 2.7778e-7
        },
        "fuel_efficiency": {
            "mpg_to_lp100km": 235.214583, # miles per gallon to liters per 100km
            "lp100km_to_mpg": 100 / 4.25143707 # liters per 100km to miles per gallon
        },
        "speed": {
            "mph_to_kmh": 1.60934,
            "kmh_to_mph": 0.621371,
            "mps_to_kmh": 3.6, # meters per second to km/h
            "kmh_to_mps": 0.277778
        },
        "area": {
            "sqm_to_sqft": 10.7639,
            "sqft_to_sqm": 0.092903,
            "acres_to_sqm": 4046.86,
            "sqm_to_acres": 0.000247105
        },
        "time": {
            "hours_to_minutes": 60,
            "minutes_to_seconds": 60,
            "days_to_hours": 24,
            "weeks_to_days": 7
        }
    }

    # Temperature conversion is handled by formulas, not simple factors
    # so we add it as a category with None factors
    conversion_factors["temperature"] = {
        "celsius_to_fahrenheit": None,
        "fahrenheit_to_celsius": None,
        "celsius_to_kelvin": None,
        "kelvin_to_celsius": None,
        "fahrenheit_to_kelvin": None,
        "kelvin_to_fahrenheit": None
    }


    print("\n--- Select a Conversion Category ---")
    categories = list(conversion_factors.keys())
    # Add 'currency' as the first option
    categories.insert(0, "currency") 

    for i, cat in enumerate(categories):
        print(f"{i + 1}. {cat.replace('_', ' ').title()}")
    print("0. Exit")

    while True:
        try:
            choice = input("\nEnter category number: ").strip()
            if choice == '0':
                print("Exiting converter.")
                break
            
            category_index = int(choice) - 1
            if not (0 <= category_index < len(categories)):
                print("Invalid category number. Please try again.")
                continue
            
            selected_category = categories[category_index]
            print(f"\n--- {selected_category.replace('_', ' ').title()} Conversions ---")
            
            if selected_category == "currency":
                handle_currency_conversion()
            else:
                category_conversions = conversion_factors[selected_category]
                conversion_options = list(category_conversions.keys())

                for i, opt in enumerate(conversion_options):
                    from_unit, to_unit = opt.split('_to_')
                    print(f"{i + 1}. {from_unit.upper()} to {to_unit.upper()}")
                print("0. Back to categories")

                while True:
                    conv_choice = input("Enter conversion number: ").strip()
                    if conv_choice == '0':
                        break # Go back to main category menu
                    
                    conversion_index = int(conv_choice) - 1
                    if not (0 <= conversion_index < len(conversion_options)):
                        print("Invalid conversion number. Please try again.")
                        continue
                    
                    selected_conversion_key = conversion_options[conversion_index]
                    from_unit, to_unit = selected_conversion_key.split('_to_')

                    while True:
                        try:
                            value = float(input(f"Enter value in {from_unit.upper()}: "))
                            result = None
                            
                            if selected_category == "temperature":
                                if from_unit == "celsius" and to_unit == "fahrenheit":
                                    result = (value * 9/5) + 32
                                elif from_unit == "fahrenheit" and to_unit == "celsius":
                                    result = (value - 32) * 5/9
                                elif from_unit == "celsius" and to_unit == "kelvin":
                                    result = value + 273.15
                                elif from_unit == "kelvin" and to_unit == "celsius":
                                    result = value - 273.15
                                elif from_unit == "fahrenheit" and to_unit == "kelvin":
                                    result = (value - 32) * 5/9 + 273.15
                                elif from_unit == "kelvin" and to_unit == "fahrenheit":
                                    result = (value - 273.15) * 9/5 + 32
                                else:
                                    print("Error: Invalid temperature conversion units.")
                            else:
                                factor = category_conversions[selected_conversion_key]
                                result = value * factor

                            if result is not None:
                                print(f"{value} {from_unit.upper()} is {result:.4f} {to_unit.upper()}")
                            break # Exit value input loop
                        except ValueError:
                            print("Invalid value. Please enter a number.")
                        except Exception as e:
                            print(f"An error occurred: {e}")
                    print("\n---") # Separator after each conversion result
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def handle_currency_conversion():
    """Handles the currency conversion logic using the API."""
    print("\n--- Live Currency Conversion (via ExchangeRate-API.com) ---")
    print("Ensure your API_KEY is set in the tool's code (currently: 1ef7f77d64327c51633428fb).")
    print("Type 'list' to see supported currency codes.")
    print("Type 'back' to return to category menu.")

    supported_currencies_map = None # Cache this after first fetch

    while True:
        base_code = input("Enter FROM currency code (e.g., USD, EUR, or 'list'/'back'): ").strip().upper()
        if base_code == 'BACK':
            return
        if base_code == 'LIST':
            if supported_currencies_map is None:
                print("Fetching supported currency codes...")
                supported_currencies_map = get_supported_currencies()
            
            if supported_currencies_map:
                print("\n--- Supported Currency Codes (ISO 4217) ---")
                # Print in columns for readability
                codes = sorted(supported_currencies_map.keys())
                num_cols = 4
                # Calculate max width for code and name for formatting
                max_code_len = max(len(c) for c in codes) if codes else 0
                max_name_len = max(len(supported_currencies_map[c]) for c in codes) if codes else 0

                for i in range(0, len(codes), num_cols):
                    row_codes = codes[i:i+num_cols]
                    row_display = []
                    for code in row_codes:
                        name = supported_currencies_map[code]
                        row_display.append(f"{code.ljust(max_code_len)} - {name.ljust(max_name_len)}")
                    print("  ".join(row_display))
                print("------------------------------------------")
            else:
                print("Could not retrieve supported currency codes. Check API key and internet.")
            continue

        target_code = input("Enter TO currency code (e.g., GBP, JPY, or 'back'): ").strip().upper()
        if target_code == 'BACK':
            return

        if not base_code or not target_code:
            print("Currency codes cannot be empty.")
            continue

        if supported_currencies_map is None: # Fetch if not already fetched
            supported_currencies_map = get_supported_currencies()
        
        # Basic validation of currency codes
        if supported_currencies_map and (base_code not in supported_currencies_map or target_code not in supported_currencies_map):
            print(f"One or both currency codes ('{base_code}', '{target_code}') not recognized.")
            print("Type 'list' to see supported codes.")
            continue

        while True:
            try:
                amount_str = input(f"Enter amount in {base_code} (or 'back' to choose codes again): ").strip()
                if amount_str.lower() == 'back':
                    break # Go back to currency code input
                amount = float(amount_str)
                if amount < 0:
                    print("Amount cannot be negative.")
                    continue

                rates = get_exchange_rates(base_code)
                if rates:
                    if target_code in rates:
                        converted_amount = amount * rates[target_code]
                        print(f"\n{amount} {base_code} = {converted_amount:.4f} {target_code}")
                        print(f"(Rate: 1 {base_code} = {rates[target_code]:.4f} {target_code})")
                    else:
                        print(f"Could not find exchange rate for {target_code} from {base_code}.")
                        print("Check if both currencies are supported or if base currency has rates for target.")
                else:
                    print("Could not retrieve rates. Please check API key, internet, and currency codes.")
                break # Exit amount input loop
            except ValueError:
                print("Invalid amount. Please enter a number.")
            except Exception as e:
                print(f"An error occurred: {e}")

# Do NOT call main() here. H7T does that automatically.
