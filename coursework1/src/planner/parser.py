# from planner.request import SolverRequest

from dataclasses import dataclass, field
from os.path import join
from re import findall
from typing import Self


@dataclass
class Parameter():
    name: str = field(init=False)
    type: str = field(init=False)

    def __init__(self, args) -> None:
        self.name = args[0].strip("?")
        self.type = args[1]


@dataclass
class Precondition():
    preposition: str = field(init=False)
    params: list[str] = field(init=False)

    def __init__(self, args) -> None:
        self.name = args[0]
        self.type = args[1]


@dataclass
class Effect():
    name: str = field(init=False)
    type: str = field(init=False)

    def __init__(self, args) -> None:
        self.name = args[0].strip("?")
        self.type = args[1]


@dataclass
class Action():
    name: str = field(init=False)
    parameters: list[Parameter] = field(init=False)

    def __init__(self, name, params: list[str]):
        self.name = name
        self.parameters = [
            Parameter(p.strip().split(" - ")) for p in params
        ]

    @classmethod
    def parse_actions(cls, pddl_dir: str) -> list[Self]:
        with open(
            join(pddl_dir, "domain.pddl")
            # SolverRequest.domain_file/
        ) as domain:
            domain_string = domain.read()

        word = " a-zA-Z0-9-"
        predicate = r"\(\)=?a-zA-Z0-9-\s"
        matches = findall(
            rf":action ([{word}]+)\s*"
            rf":parameters\s*\(\s*([{predicate}]*)\s*\)\s*"
            rf":precondition\s*\(and\s*([{predicate}]*)\s*\)\s*"
            rf":effect\s*\(and\s*([{predicate}]*)\s\)\s*\)",
            domain_string
        )
        for match in matches:
            print(match)
            # action = Action(match[0], (match[1].strip().split("\n")))
            # print(action)

