# tools/coin_flipper.py

import random

def main():
    """
    Simulates flipping a coin multiple times.
    """
    print("--- Coin Flipper ---")

    while True:
        try:
            num_flips = int(input("How many times do you want to flip the coin? "))
            if num_flips <= 0:
                print("Please enter a positive number of flips.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    heads_count = 0
    tails_count = 0

    print("\n--- Flipping! ---")
    for i in range(num_flips):
        result = random.choice(["Heads", "Tails"])
        print(f"Flip {i+1}: {result}")
        if result == "Heads":
            heads_count += 1
        else:
            tails_count += 1

    print("\n--- Results ---")
    print(f"Total flips: {num_flips}")
    print(f"Heads: {heads_count}")
    print(f"Tails: {tails_count}")
    print("-----------------")

# Do NOT call main() here. H7T does that automatically.
