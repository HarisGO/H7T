# tools/guess_the_number.py

import random

def main():
    """
    A 'Guess the Number' game.
    The user tries to guess a randomly generated number within a specified range.
    """
    print("--- Guess the Number! ---")
    print("I'm thinking of a number. Can you guess it?")

    while True:
        try:
            min_num = int(input("Enter the minimum number for the range: "))
            max_num = int(input("Enter the maximum number for the range: "))
            if min_num >= max_num:
                print("Error: Minimum number must be less than the maximum number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter whole numbers.")

    secret_number = random.randint(min_num, max_num)
    attempts = 0

    while True:
        try:
            guess = int(input(f"Guess a number between {min_num} and {max_num}: "))
            attempts += 1

            if guess < min_num or guess > max_num:
                print("Your guess is outside the specified range. Try again.")
            elif guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts!")
                break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    print("Thanks for playing!")

# Do NOT call main() here. H7T does that automatically.
