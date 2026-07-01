"""
Five in Six
A final project for Code in Place.

Guess the hidden 5-letter word in 6 tries. After each guess you get
feedback on every letter:

    [A]   right letter, right spot      (green)
    (A)   right letter, wrong spot      (yellow)
     A    letter is not in the word     (gray)

Concepts used: functions, loops, conditionals, lists, strings,
dictionaries, and the random module.
"""

import random


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

WORD_LENGTH = 5
MAX_GUESSES = 6

# Set this to True only if your console supports color (most terminals do).
# If you ever see odd symbols like "[42m" in the output, set it back to False.
USE_COLOR = False

# A pool of common 5-letter words. These are used both as the hidden word
# and as the set of "real" words the game knows about.
WORDS = [
    "apple", "brave", "crane", "dream", "eagle", "frost", "grape", "house",
    "igloo", "juice", "knife", "lemon", "money", "night", "ocean", "piano",
    "queen", "river", "snake", "tiger", "unity", "voice", "wagon", "yacht",
    "zebra", "bread", "chess", "dance", "earth", "flame", "glove", "honey",
    "input", "jolly", "koala", "light", "magic", "noble", "olive", "pearl",
    "quilt", "robot", "sugar", "train", "vivid", "whale", "youth", "beach",
    "cloud", "daisy", "faith", "ghost",
]


# ---------------------------------------------------------------------------
# Color helpers (only used when USE_COLOR is True)
# ---------------------------------------------------------------------------

GREEN = "\033[42m\033[30m"   # green background, black text
YELLOW = "\033[43m\033[30m"  # yellow background, black text
GRAY = "\033[47m\033[30m"    # light gray background, black text
RESET = "\033[0m"


def paint(text, status):
    """Wrap text in color codes for the given status, if color is turned on."""
    if not USE_COLOR:
        return text
    if status == "correct":
        return GREEN + text + RESET
    if status == "present":
        return YELLOW + text + RESET
    return GRAY + text + RESET


# ---------------------------------------------------------------------------
# Game logic
# ---------------------------------------------------------------------------

def score_guess(guess, secret):
    """
    Compare a guess to the secret word.

    Returns a list of 5 status strings, one per letter:
        "correct"  -> right letter in the right spot
        "present"  -> letter is in the word but in a different spot
        "absent"   -> letter is not in the word

    Repeated letters are handled the same way the real game does: a letter
    only shows as "present" if the secret still has an unmatched copy of it.
    """
    result = ["absent"] * WORD_LENGTH

    # Count how many of each letter the secret has available to match.
    remaining = {}
    for letter in secret:
        if letter in remaining:
            remaining[letter] = remaining[letter] + 1
        else:
            remaining[letter] = 1

    # First pass: mark letters that are in the correct position (green).
    for i in range(WORD_LENGTH):
        if guess[i] == secret[i]:
            result[i] = "correct"
            remaining[guess[i]] = remaining[guess[i]] - 1

    # Second pass: mark letters that are present but misplaced (yellow).
    for i in range(WORD_LENGTH):
        if result[i] == "correct":
            continue
        letter = guess[i]
        if letter in remaining and remaining[letter] > 0:
            result[i] = "present"
            remaining[letter] = remaining[letter] - 1

    return result


def win_message(guess_number):
    """Return a little praise based on how few guesses were used."""
    messages = {
        1: "Genius!",
        2: "Magnificent!",
        3: "Impressive!",
        4: "Splendid!",
        5: "Great!",
        6: "Phew!",
    }
    return messages.get(guess_number, "Nice!")


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def format_cell(letter, status):
    """Turn one letter and its status into a 3-character display cell."""
    upper = letter.upper()
    if status == "correct":
        cell = "[" + upper + "]"
    elif status == "present":
        cell = "(" + upper + ")"
    else:
        cell = " " + upper + " "
    return paint(cell, status)


def show_guess(guess, statuses):
    """Print one guessed word with feedback for each letter."""
    cells = []
    for i in range(WORD_LENGTH):
        cells.append(format_cell(guess[i], statuses[i]))
    print("   " + " ".join(cells))


def update_letter_status(letter_status, guess, statuses):
    """Remember the best-known status for each letter the player has tried."""
    rank = {"absent": 0, "present": 1, "correct": 2}
    for i in range(WORD_LENGTH):
        letter = guess[i]
        new_status = statuses[i]
        if letter not in letter_status:
            letter_status[letter] = new_status
        elif rank[new_status] > rank[letter_status[letter]]:
            # Only upgrade (absent -> present -> correct), never downgrade.
            letter_status[letter] = new_status


def show_letter_status(letter_status):
    """Print what we have learned about letters so far."""
    correct = []
    present = []
    absent = []
    for letter in sorted(letter_status):
        status = letter_status[letter]
        if status == "correct":
            correct.append(letter.upper())
        elif status == "present":
            present.append(letter.upper())
        else:
            absent.append(letter.upper())

    if correct:
        print("   Right spot:  " + ", ".join(correct))
    if present:
        print("   In word:     " + ", ".join(present))
    if absent:
        print("   Not in word: " + ", ".join(absent))


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

def get_guess(guess_number):
    """Ask the player for a valid guess and return it in lowercase."""
    while True:
        guess = input("Guess " + str(guess_number) + ": ").strip().lower()
        if len(guess) != WORD_LENGTH:
            print("   Please enter a word that is exactly "
                  + str(WORD_LENGTH) + " letters.")
        elif not guess.isalpha():
            print("   Please use letters only (no numbers or symbols).")
        else:
            return guess


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------

def play_one_game():
    """Play a single game of Wordle. Returns True if the player won."""
    secret = random.choice(WORDS)
    letter_status = {}

    print()
    print("I'm thinking of a " + str(WORD_LENGTH) + "-letter word.")
    print("You have " + str(MAX_GUESSES) + " guesses. Good luck!")
    print()

    for guess_number in range(1, MAX_GUESSES + 1):
        guess = get_guess(guess_number)
        statuses = score_guess(guess, secret)

        show_guess(guess, statuses)
        update_letter_status(letter_status, guess, statuses)

        if guess == secret:
            print()
            print(win_message(guess_number)
                  + " You got it in " + str(guess_number) + " guess(es).")
            return True

        show_letter_status(letter_status)
        print()

    # The player ran out of guesses.
    print("Out of guesses! The word was: " + secret.upper())
    return False


def print_intro():
    """Print the title and the rules of the game."""
    print("=" * 40)
    print("            Five in Six")
    print("=" * 40)
    print("Feedback after each guess:")
    print("   [A]   right letter, right spot")
    print("   (A)   right letter, wrong spot")
    print("    A    letter is not in the word")
    print("=" * 40)


def main():
    """Run the game and let the player play as many rounds as they like."""
    print_intro()

    wins = 0
    games = 0

    keep_playing = True
    while keep_playing:
        won = play_one_game()
        games = games + 1
        if won:
            wins = wins + 1

        print()
        print("You've won " + str(wins) + " of " + str(games) + " game(s).")
        answer = input("Play again? (yes/no): ").strip().lower()
        print()
        if answer != "yes" and answer != "y":
            keep_playing = False

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
