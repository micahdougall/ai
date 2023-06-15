# import game.run as game
from controller.cworld import CWorld
from controller.grid_controller import GameController

from args import args, GlobalArgs
from contextlib import redirect_stdout
import io


if __name__ == "__main__":
    options = GlobalArgs.args(args())

    if options.args.test_runs:
        with io.StringIO() as buf, redirect_stdout(buf):
            print('redirected')
            for _ in range(int(options.args.test_runs)):
                game = CWorld()
                game.play()
                # TODO: Capture result
                output = buf.getvalue()
                print("Out")
                print(output)
                # TODO: Still buggy empty sequence and recursive run
    else:
        # Declare new instance but postpone instantiation
        controller = object.__new__(GameController)

        world = CWorld(controller)
        # game = game.CGame.get(world)


        # This all works fine from here! - moved to standard
        # items_map = {
        #     world.student_pos: "pikachu_win.png",
        #     **{c: "C.jpeg" for c in world.textbook_pos},
        #     world.filippos_pos: "steve.png",
        #     world.degree_pos: "degree.jpeg"
        # }
        # game = game.GridGame.get(world)
        # game.play()

        world.play()
        controller.pygame()
