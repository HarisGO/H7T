# tools/typing_speed_tester.py

import time

def main():
    """
    Measures a user's typing speed (WPM) and accuracy.
    """
    print("--- Typing Speed Tester ---")
    print("Type the following paragraph as fast and accurately as you can.")
    print("Press Enter when you are done.")
    print("---------------------------")

    paragraph = "The quick brown fox jumps over the lazy dog. Programming is a valuable skill that opens up many opportunities. Practice makes perfect when it comes to typing speed. Terminal tools can be very efficient for quick tasks."
    
    print("\n" + paragraph)
    print("\nStart typing now:")

    input("Press Enter when you are ready to start...") # Wait for user to be ready

    start_time = time.time()
    user_input = input("") # Capture the entire line of input
    end_time = time.time()

    time_taken = end_time - start_time
    
    # Calculate WPM (Words Per Minute)
    # A "word" is typically considered 5 characters (including space)
    num_chars = len(user_input)
    words_typed = num_chars / 5
    wpm = (words_typed / time_taken) * 60 if time_taken > 0 else 0

    # Calculate accuracy
    correct_chars = 0
    min_len = min(len(paragraph), len(user_input))
    for i in range(min_len):
        if paragraph[i] == user_input[i]:
            correct_chars += 1
    
    accuracy = (correct_chars / len(paragraph)) * 100 if len(paragraph) > 0 else 0

    print("\n--- Results ---")
    print(f"Time Taken: {time_taken:.2f} seconds")
    print(f"Characters Typed: {num_chars}")
    print(f"Words Per Minute (WPM): {wpm:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")
    print("---------------")

# Do NOT call main() here. H7T does that automatically.
