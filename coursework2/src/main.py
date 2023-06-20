# from args import GlobalArgs, args
from argparse import ArgumentParser, Namespace
from os.path import abspath, join, dirname

from controller.cworld import CWorld
from controller.game_controller import GameController
from logger import Logger
from model.enums import Algorithm


def args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-a", "--algorithm", 
        action="store", 
        default="standard", 
        choices=["standard", "bayes"]
    )
    parser.add_argument("-t", "--test-runs", action="store")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-g", "--game", action="store_false", default=True)
    return parser.parse_args()


def cworld_with_states(algorithm: Algorithm) -> GameController:
    """Executes a CWorld game as a wrapper to a state controller.

    Args:
        algorithm: which solving algorithm to use, one of Standard, Bayes.

    Returns:
        the controller for the game execution.
    """

    # Declare new instance but postpone instantiation
    controller = object.__new__(GameController)

    # Save states of CWorld in controller
    world = CWorld(controller)
    controller.algorithm = algorithm

    if algorithm == Algorithm.BAYES:
        controller.grid.python_books = 0

    world.play()

    return controller


if __name__ == "__main__":

    root = abspath(join(dirname(__file__), "../"))
    resources = join(root, "resources")

    args = args()
    Logger.logger(debug=args.debug)
    algorithm = Algorithm[args.algorithm.upper()]

    if args.test_runs:
        wins = 0
        n = int(args.test_runs)
        for _ in range(n):
            controller = cworld_with_states(algorithm)
            if controller.win:
                wins += 1
        print(
            f"Win rate from {n} runs => {round(wins / n * 100, 2)}%"
        )
    else:
        # Output game results to pygame
        controller = cworld_with_states(algorithm)
        if args.game:
            controller.pygame(resources)
