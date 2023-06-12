from args import args, GlobalArgs
from contextlib import redirect_stdout
import io
from lib.cworld import CWorld


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
                # TODO: Still buggy empty sequence and recursuve run
    else:
        game = CWorld()
        game.play()
