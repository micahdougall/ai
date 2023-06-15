from controller.cworld import CWorld
from controller.grid_controller import GameController

from args import args, GlobalArgs
from contextlib import redirect_stdout
import io


def cworld_with_states() -> GameController:
    # Declare new instance but postpone instantiation
    controller = object.__new__(GameController)

    # Save states of CWorld in controller
    world = CWorld(controller)
    world.play()

    return controller


if __name__ == "__main__":
    options = GlobalArgs.args(args())

    # TODO: Refactor
    if options.args.test_runs:
        with io.StringIO() as buf, redirect_stdout(buf):
            print('redirected')
            for _ in range(int(options.args.test_runs)):
                controller = cworld_with_states()
                pass

    else:
        controller = cworld_with_states()

        # Output game results to pygame
        controller.pygame()
