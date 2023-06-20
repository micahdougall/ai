# from args import GlobalArgs, args
from argparse import ArgumentParser, Namespace
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
    return parser.parse_args()


def cworld_with_states(args) -> GameController:
    # Declare new instance but postpone instantiation
    controller = object.__new__(GameController)

    # Save states of CWorld in controller
    world = CWorld(controller)
    controller.algorithm = Algorithm[args.algorithm.upper()]
    world.play()

    return controller


if __name__ == "__main__":
    args = args()
    Logger.logger(debug=args.debug)

    if args.test_runs:
        wins = 0
        n = int(args.test_runs)
        for _ in range(n):
            controller = cworld_with_states()
            print(controller.win)
            if controller.win:
                wins += 1
        print(
            f"Win rate from {n} runs => {round(wins / n * 100, 2)}%"
        )
    else:
        # Output game results to pygame
        cworld_with_states(args)
        # cworld_with_states().pygame()
