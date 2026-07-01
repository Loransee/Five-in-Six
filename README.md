# Five in Six 🟩🟨⬜

A Wordle-inspired word-guessing game built in Python — created as a final project for [Code in Place](https://codeinplace.stanford.edu/cip6/share/f7FfTN3VtZObv2IDdN6I).

## 🎮 How to Play

Guess the hidden **5-letter word** in **6 tries**.

After each guess, you get feedback on every letter:

| Symbol | Meaning |
|--------|---------|
| `[A]`  | ✅ Right letter, right spot |
| `(A)`  | 🟡 Right letter, wrong spot |
| ` A `  | ❌ Letter is not in the word |

The game also shows a running summary of all the letters you've tried, so you can plan your next guess strategically.

## ▶️ How to Run

Make sure you have **Python 3** installed, then run:

```bash
python five_in_six.py
```

No extra libraries needed — it only uses Python's built-in `random` module!

## 🧠 Concepts Used

- Functions
- Loops & conditionals
- Lists & strings
- Dictionaries
- The `random` module

## 📸 Example Output

```
========================================
            Five in Six
========================================
Feedback after each guess:
   [A]   right letter, right spot
   (A)   right letter, wrong spot
    A    letter is not in the word
========================================

I'm thinking of a 5-letter word.
You have 6 guesses. Good luck!

Guess 1: crane
    [C]  (R)   A   (N)   E  
   In word:    N, R
   Not in word: A, E

Guess 2: river
    R   [I]  [V]  [E]  [R] 
   ...
```

## 👤 Author

Built with ❤️ as a final project for Stanford's Code in Place program.
