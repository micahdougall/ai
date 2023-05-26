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

        matches = findall(
            r":action ([ a-zA-Z0-9-]+)[\s]*"
            r":parameters[\s]*[(][\s]*([ ?a-zA-Z0-9-[\s]+)[\s]*[)][\s]*"
            r":precondition[\s]*[(]and[\s]*([()][ ?a-zA-Z0-9-[)][\s]+)[\s]*[)][\s]*",
            # r":effect[\s]*[(]and[\s]*([()][ ?a-zA-Z0-9-[)][\s]+)[\s][)]",
            domain_string
        )
        for match in matches:
            action = Action(match[0], (match[1].strip().split("\n")))
            print(action)

