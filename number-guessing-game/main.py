import random

highscore = {"Easy": 0, "Medium": 0, "Hard": 0}


def handle_highscore(difficulty, tries):
    highscore[difficulty] = tries

    print("\nYour High Score is: ")
    for diff, score in highscore.items():
        print(f"{diff}: in {score} tries")


def generate_number(min_range=1, max_range=100):
    correct_number = random.randint(min_range, max_range)
    return correct_number


def get_guess(difficulty):
    correct_number = generate_number()
    print(correct_number)

    tries = difficulty["chances"]

    while tries > 0:
        print(f"Tries remaining: {tries}")
        guess = int(input(f"Enter your guess: "))

        if guess > correct_number:
            print(f"Incorrect! The number is less than {guess}.")
        elif guess < correct_number:
            print(f"Incorrect! The number is greater than {guess}.")
        else:
            handle_highscore(difficulty["type"], tries)
            print(
                f"Congratulations! You guessed the correct number in {tries} attempts."
            )
            return

        tries -= 1

    print(
        f"Unfortunately, it wasn't this time. The correct number was {correct_number}. Try again!"
    )


def get_safe_input(prompt):
    while True:
        try:
            diff_level = int(input(prompt))

            if diff_level not in (1, 2, 3):
                raise Exception

            return diff_level
        except:
            print("\nInvalid value, choose between 1 and 3.\n")


def menu():
    keep_playing = "y"

    while keep_playing == "y":
        print(
            """Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
You have some chances to guess the correct number.

Please select the difficulty level:
1. Easy (10 chances)
2. Medium (5 chances)
3. Hard (3 chances)

4. Exit the game."""
        )

        choice = get_safe_input("\nEnter your choice: ")

        difficulties = [
            {"type": "Easy", "chances": 10},
            {"type": "Medium", "chances": 5},
            {"type": "Hard", "chances": 3},
        ]

        selected_diff = difficulties[choice - 1]

        print(
            f"Great! You have selected the {selected_diff['type']} difficulty level. \nLet's start the game!"
        )

        get_guess(selected_diff)

        keep_playing = input("Do you want to keep trying? [Y/N] ").strip().lower()

    print("Ending the Guessing Game, see you soon!")


if __name__ == "__main__":
    menu()
