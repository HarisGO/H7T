# tools/world_capital_guesser.py

import random

def main():
    """
    A simple game to guess the capital of a given country.
    """
    print("--- World Capital Guesser ---")
    print("Guess the capital city for the given country.")
    print("Type 'exit' to quit the game at any time.")

    # A small, curated list of countries and their capitals
    # (Expand this dictionary for more variety!)
    capitals_data = {
        "France": "Paris",
        "Germany": "Berlin",
        "Japan": "Tokyo",
        "United Kingdom": "London",
        "United States": "Washington D.C.",
        "Canada": "Ottawa",
        "Australia": "Canberra",
        "Brazil": "Brasilia",
        "India": "New Delhi",
        "China": "Beijing",
        "Egypt": "Cairo",
        "South Africa": "Pretoria", # Administrative capital
        "Italy": "Rome",
        "Spain": "Madrid",
        "Mexico": "Mexico City",
        "Russia": "Moscow",
        "Argentina": "Buenos Aires",
        "Nigeria": "Abuja",
        "Turkey": "Ankara",
        "Greece": "Athens"
    }

    countries = list(capitals_data.keys())
    score = 0
    rounds_played = 0

    while True:
        if not countries:
            print("\nNo more countries in the list! Game over.")
            break

        country = random.choice(countries)
        correct_capital = capitals_data[country].lower()

        guess = input(f"\nWhat is the capital of {country}? ").strip().lower()

        if guess == 'exit':
            print("Exiting game. Thanks for playing!")
            break

        if guess == correct_capital:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The capital of {country} is {capitals_data[country]}.")

        rounds_played += 1
        print(f"Current Score: {score}/{rounds_played}")

        # Remove the country to avoid repeating too soon (or just let it repeat)
        countries.remove(country)

    print(f"\nGame Over! You scored {score} out of {rounds_played} rounds.")

# Do NOT call main() here. H7T does that automatically.
