from dataclasses import dataclass
from typing import Any, ClassVar, Self


@dataclass
class Logger:
    """Singleton logger class used for debugging"""

    debug: bool = False
    _logger_: ClassVar[Self] = None  # Used for 'singleton'

    def log(self, text: Any, warn: bool = False, force: bool = False) -> None:
        if self.debug or force:
            print(text) if not warn else print(f"\033[93m{text}\033[0m")

    @classmethod
    def logger(cls, debug: bool = False) -> Self:
        """Lightweight singleton class method"""
        if not cls._logger_:
            cls._logger_ = cls(debug)
        return cls._logger_
