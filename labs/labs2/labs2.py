import random


def guessing_game(actual_num: int) -> None:
    print(actual_num)
    guessed: bool = False

    while not guessed:
        guessed = True if guess_number(actual_num) else False
    print("Congrats!")


def guess_number(actual: int) -> bool:
    return int(input("Feeling lucky, punk?\n")) == actual


guessing_game(random.randint(1, 10))
