from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import ClassVar, Self


def args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-a", "--algorithm", action="store", default="standard")
    parser.add_argument("-t", "--test-runs", action="store")
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args()


@dataclass
class GlobalArgs:
    """Hacky way to share global args without changing entry point"""

    args: Namespace
    _args_: ClassVar[Self] = None  # Used for 'singleton'

    @classmethod
    def args(cls, arguments: Namespace | None) -> Namespace:
        """Pseudo-singleton class method for Args"""

        if not cls._args_:
            cls._args_ = cls(arguments)
        return cls._args_
