# from http.request import SolverRequest
from planner.parser.predicate import Parameter

from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from os.path import join
from re import findall
from typing import Self




# @dataclass
# class Predicate:
#     preposition: str
#     parameters: list[Parameter]
#     negation: bool = False


@dataclass
class Precondition:
    preposition: str
    # preposition: str = field(init=False)
    params: list[str]
    # params: list[str] = field(init=False)

    # def __init__(self, args) -> None:
    #     self.name = args[0]
    #     self.type = args[1]


@dataclass
class Effect:
    name: str = field(init=False)
    type: str = field(init=False)

    def __init__(self, args) -> None:
        self.name = args[0].strip("?")
        self.type = args[1]


@dataclass
class Action(JSONWizard):
    # name: str = field(init=False)
    name: str
    # parameters: list[Parameter] = field(init=False)
    parameters: list[Parameter]

    # def __init__(self, name, params: list[str]):
    #     self.name = name
    #     self.parameters = [
    #         Parameter(p.strip().split(" - ")) for p in params
    #     ]

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
        for match in matches[:1]:
            action = {
                "name": match[0],
                "parameters": [
                    {
                        k: v for k, v
                        in zip(
                            ("name", "type"),
                            args.strip().split(" - ")
                        )
                    }
                    for args in match[1].strip().split("\n")
                ],
                # "precondition": [
                #     {
                #
                #     }
                # ]
            }
            print(action)
            a = Action.from_dict(action)
            print(a)