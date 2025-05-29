# tools/higher_lower_card_game.py

import random
import time

def main():
    """
    A 'Higher/Lower' card guessing game.
    """
    print("--- Higher/Lower Card Game ---")
    print("Guess if the next card drawn will be higher or lower than the current card.")
    print("Card values: Ace (1) to King (13).")
    print("Type 'exit' to quit at any time.")
    print("------------------------------")

    deck = list(range(1, 14)) * 4 # Create a deck of 4 suits (values 1-13)
    random.shuffle(deck) # Shuffle the deck

    score = 0
    games_played = 0

    def get_card_name(value):
        if value == 1: return "Ace"
        if value == 11: return "Jack"
        if value == 12: return "Queen"
        if value == 13: return "King"
        return str(value)

    while len(deck) >= 2: # Need at least two cards to play a round
        games_played += 1
        current_card_value = deck.pop()
        current_card_name = get_card_name(current_card_value)

        print(f"\n--- Round {games_played} ---")
        print(f"Current card is: {current_card_name}")

        while True:
            guess = input("Will the next card be [H]igher or [L]ower? (H/L, or 'exit'): ").strip().lower()
            if guess == 'exit':
                print("Exiting game. Thanks for playing!")
                return
            if guess in ['h', 'l']:
                break
            print("Invalid input. Please enter 'H' for Higher, 'L' for Lower, or 'exit'.")

        next_card_value = deck.pop()
        next_card_name = get_card_name(next_card_value)
        time.sleep(0.5) # A little suspense
        print(f"The next card is: {next_card_name}")

        correct = False
        if next_card_value > current_card_value:
            if guess == 'h':
                correct = True
        elif next_card_value < current_card_value:
            if guess == 'l':
                correct = True
        else: # next_card_value == current_card_value
            # For ties, it's generally considered a loss or push, let's make it a loss for simplicity
            print("It's a tie! (You lose this round).")
            
        if correct:
            print("You guessed correctly! Well done!")
            score += 1
        elif next_card_value != current_card_value: # If it's a tie, it's already handled
            print("Incorrect guess. Better luck next time!")

        print(f"Score: {score} out of {games_played} rounds.")

    print("\n--- Game Over ---")
    print("Not enough cards left to play another round.")
    print(f"Final Score: {score} out of {games_played} rounds played.")
    print("Thanks for playing!")

# Do NOT call main() here. H7T does that automatically.
