

from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard, json_field
from os.path import join
from re import findall, match, search
from typing import Self
from pyre_extensions import override


@dataclass
class Type:
    name: str
    # parent: Self = field(init=False)

    @override
    def __str__(self) -> str:
        return self.name

@dataclass
class Parameter:
    name: str
    type_str: str = json_field("type_str", dump=False)
    type: Type | list[Type] = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.name.strip("?")
        types = match(r"^\(either ([ a-zA-Z0-9-]*)\)$", self.type_str)
        self.type = [
            Type(element) for element
            in types.group(1).split(" ")
        ] if types else Type(self.type_str)

    def __str__(self) -> str:
        return

    # def __post_init__(self, arg) -> None:
    #     self.name = self.name.strip("?")
    #     # self.type = [
    #     #     Type(obj) for obj in self.type
    #     # ] if match(r"$\(either [ a-zA-Z0-9-]*\)$", self.type) else self.type
    #
    #     types = match(r"^\(either ([ a-zA-Z0-9-]*)\)$", self.type)
    #     self.type = types.group(1).split(" ") if types else self.type
    #     # if types:
    #     #     print(types.group(1))
    #     # else:
    #     print(self.type)


@dataclass
class Predicate(JSONWizard):
    preposition: str
    parameters: list[Parameter]
    negation: bool = False
