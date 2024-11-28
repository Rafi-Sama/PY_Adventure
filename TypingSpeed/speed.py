from time import time, sleep
import random as r
from itertools import zip_longest
from threading import Thread
import os

# Function to calculate the number of mistakes
def calculate_mistakes(expected, user_input):
    errors = 0
    mismatches = []
    for idx, (i, j) in enumerate(zip_longest(expected, user_input, fillvalue=None)):
        if i != j:
            errors += 1
            mismatches.append((idx, i, j))
    return errors, mismatches

# Function to calculate typing speed (characters per second)
def calculate_speed(start_time, end_time, user_input):
    elapsed_time = round(end_time - start_time, 2)  # Total time taken
    if elapsed_time == 0:  # Avoid division by zero
        return 0
    return round(len(user_input) / elapsed_time)

# Function to calculate WPM (Words Per Minute)
def calculate_wpm(start_time, end_time, user_input):
    elapsed_time = round(end_time - start_time, 2)  # Total time taken
    word_count = len(user_input.split())  # Count of words
    if elapsed_time == 0:  # Avoid division by zero
        return 0
    return round((word_count / elapsed_time) * 60)  # Words per minute

# Function to calculate accuracy
def calculate_accuracy(expected, user_input):
    total_chars = len(expected)
    correct_chars = sum(1 for i, j in zip_longest(expected, user_input, fillvalue=None) if i == j)
    return round((correct_chars / total_chars) * 100, 2)

# Function to display a real-time timer
def real_time_timer(start_time, stop_flag, total_sentences, progress_tracker):
    while not stop_flag[0]:
        elapsed_time = round(time() - start_time, 2)
        progress = f"{progress_tracker[0]}/{total_sentences} sentences"
        print(f"\rTime Elapsed: {elapsed_time:.2f} seconds | Progress: {progress}", end="")
        sleep(0.1)

# Function to clear console (cross-platform)
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Save results to a file
def save_results(results):
    with open("results.txt", "a") as file:
        file.write(results + "\n")

# Display leaderboard from the saved file
def display_leaderboard():
    try:
        with open("results.txt", "r") as file:
            scores = [line.strip() for line in file.readlines()]
        if not scores:
            print("No leaderboard data available yet.")
            return
        print("\n====== Leaderboard ======")
        for idx, score in enumerate(sorted(scores, key=lambda x: int(x.split(" ")[-2]), reverse=True)[:5], 1):
            print(f"{idx}. {score}")
    except FileNotFoundError:
        print("No leaderboard data available yet.")

# Main typing test function
def typing_speed_test():
    sentences = {
        "Easy": [
            "The quick brown fox jumps over the lazy dog.",
            "My name is Abdullah.",
            "Nice to be here!",
        ],
        "Medium": [
            "Typing tests are fun and help improve your speed.",
            "Consistency is the key to success.",
            "The early bird catches the worm.",
        ],
        "Hard": [
            "Artificial intelligence is revolutionizing the modern world.",
            "She sells sea shells by the seashore.",
            "The purpose of life is not to be happy. It is to be useful.",
        ],
    }
    
    print("\n!!!!!!!!!!!!!------ Typing Speed Test -----!!!!!!!!!!!!!!")
    print("Select Difficulty Level:")
    print("1. Easy\n2. Medium\n3. Hard")
    
    while True:
        try:
            choice = int(input("Enter your choice (1/2/3): "))
            if choice == 1:
                level = "Easy"
            elif choice == 2:
                level = "Medium"
            elif choice == 3:
                level = "Hard"
            else:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")
    
    num_sentences = int(input("Enter the number of sentences you want to type: "))
    selected_sentences = r.sample(sentences[level], min(num_sentences, len(sentences[level])))

    clear_console()
    progress_tracker = [0]
    stop_flag = [False]
    results = []

    for idx, test_sentence in enumerate(selected_sentences, 1):
        print(f"\nSentence {idx}/{len(selected_sentences)}:")
        print(f"'{test_sentence}'\n")
        print("Start typing below. Timer starts when you begin typing.")

        start_time = None
        user_input = ""

        def capture_input():
            nonlocal start_time, user_input
            start_time = time()  # Start time when typing begins
            user_input = input("\nYour Input: ").strip()
            progress_tracker[0] += 1
            stop_flag[0] = True  # Stop the timer

        # Start real-time timer feedback
        timer_thread = Thread(target=real_time_timer, args=(time(), stop_flag, len(selected_sentences), progress_tracker))
        timer_thread.start()

        # Capture user input
        capture_input()
        timer_thread.join()  # Wait for the timer thread to finish

        end_time = time()
        errors, mismatches = calculate_mistakes(test_sentence, user_input)
        speed_cps = calculate_speed(start_time, end_time, user_input)
        speed_wpm = calculate_wpm(start_time, end_time, user_input)
        accuracy = calculate_accuracy(test_sentence, user_input)
        elapsed_time = round(end_time - start_time, 2)

        result = f"Sentence {idx}: {speed_wpm} WPM | Accuracy: {accuracy}% | Time: {elapsed_time}s"
        results.append(result)
        clear_console()
        print(result)

    print("\nFinal Results:")
    for result in results:
        print(result)

    print("\nWould you like to save your results?")
    save_option = input("Enter 'y' to save or any other key to skip: ").lower()
    if save_option == "y":
        name = input("Enter your name: ").strip()
        save_results(f"{name} - {' | '.join(results)}")
        print("Results saved successfully!")

    print("\nDisplaying Leaderboard:")
    display_leaderboard()

    # Replay option
    print("\nWould you like to try again?")
    retry = input("Enter 'y' to try again or any other key to exit: ").lower()
    if retry == "y":
        clear_console()
        typing_speed_test()
    else:
        print("Thank you for using the Typing Speed Test! Goodbye.")

# Run the typing speed test
typing_speed_test()
