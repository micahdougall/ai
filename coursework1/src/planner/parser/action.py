from .predicate import Parameter

from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from typing import Self

from coursework1.src.planner.parser.predicate import Predicate


# @dataclass
# class Precondition:
#     preposition: str
#     # preposition: str = field(init=False)
#     params: list[str]
#     # params: list[str] = field(init=False)
#
#     # def __init__(self, args) -> None:
#     #     self.name = args[0]
#     #     self.type = args[1]


# @dataclass
# class Effect:
#     name: str = field(init=False)
#     type: str = field(init=False)
#
#     def __init__(self, args) -> None:
#         self.name = args[0].strip("?")
#         self.type = args[1]


@dataclass
class Action(JSONWizard):
    name: str
    parameters: list[Parameter]
    precondition: list[Predicate]
    effect: list[Predicate]
