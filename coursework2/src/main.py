from args import args, GlobalArgs
from controller.cworld import CWorld
from controller.grid_controller import GameController



def cworld_with_states() -> GameController:
    # Declare new instance but postpone instantiation
    controller = object.__new__(GameController)

    # Save states of CWorld in controller
    world = CWorld(controller)
    world.play()

    return controller


if __name__ == "__main__":
    options = GlobalArgs.args(args())

    if options.args.test_runs:
        wins = 0
        n = int(options.args.test_runs)
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
        cworld_with_states().pygame()
