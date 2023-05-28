# from collections.abc import dict_items
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard, json_field
from itertools import chain
from pyre_extensions import override
from re import match
from typing import Self


@dataclass
class Type:
    type: str
    children: list[Self] = field(default_factory=list)

    def nodes(self) -> list[Self]:
        return list(
            chain.from_iterable(
                [t.nodes for t in self.children]
            )
        )

    def get_node(self, search: str) -> Self | None:
        # print(f"Getting node: {search} from {self.type}")
        if self.children:
            # optional = next(
            #     filter(
            #         lambda t: t.type == search,
            #         self.children
            #     )
            # ) or next([
            #     c.get_node(search) for c in self.children
            # ])
            for c in self.children:
                # print(c.type)
                if c.type == search:
                    # print("found")
                    return c
            return None
        # else:
        #     print(f"{self.type} has no children")
        # else:
        #     optional = None
        # print(optional)
        # return optional

# @dataclass
# class Type:
#     name: str
#     parent: Self = None
#
#     def __post_init__(self):
#         self.parent = (
#             "object"
#             if self.parent is None
#                and self.name != "object"
#             else self.parent
#         )
#
#     @override
#     def __str__(self) -> str:
#         return self.name
#
#     # @override
#     # def __repr__(self) -> str:
#     #     return f"{self.name}: {self.parent}"
#
#     @classmethod
#     def type_names(cls, types: list[Self]) -> list[str]:
#         return [
#             type.name for type in types
#         ]




@dataclass
class Parameter(JSONWizard):
    name: str
    # type_str: str = json_field("type_str", dump=False)
    # type Type | list[Type] = field(init=False)
    types: Type | list[Type]

    # def __post_init__(self) -> None:
    #     self.name = self.name.strip("?")
    #     types = match(r"^\(either ([ a-zA-Z0-9-]*)\)$", self.type_str)
    #     self.type = [
    #         Type(element) for element
    #         in types.group(1).split(" ")
    #     ] if types else Type(self.type_str)

    @classmethod
    def from_string(cls, param: str) -> Self:
        objs = param.strip().split(" - ")
        types = match(r"^\(either ([ a-zA-Z0-9-]*)\)$", objs[1])
        return cls(
            name=objs[0].strip("?"),
            types=[
                Type(element) for element
                in types.group(1).split(" ")
            ] if types else Type(objs[1])
        )

    @classmethod
    def types_dict(cls, parameters: list[Self]) -> dict[str ,Type]:
        return {
            list(p.__dict__.values())[0]: list(p.__dict__.values())[1]
            for p in parameters
        }


@dataclass
class Predicate(JSONWizard):
    preposition: str
    parameters: list[Parameter]
    negation: bool = False

    @classmethod
    def from_precondition(cls, args: list[str], lookup: dict):
        params = [
            Parameter(p, lookup.get(p))
            for p in args[1:]
        ]
        return cls(
            args[0].removeprefix("not ("),
            params,
            args[0].startswith("not (")
        )

    # def predicate_args(text: str) -> list[str]:
    #     # args = text.strip(" ()").split(" ?")
    #     # args[0] = args[0].removeprefix("not (")
    #     # return args
    #     return text.strip(" ()").split(" ?")
    #
    # def is_negated(text: str) -> bool:
    #     return text.strip(" ()").startswith("not (")

    # def types(self) -> Self:
    #     return next(
    #         filter(
    #             lambda p: p.preposition == preposition,
    #             predicates
    #         )
    #     )

    # @classmethod
    # def get(cls, predicates: list[Self], preposition: str) -> Self:
    #     return next(
    #         filter(
    #             lambda p: p.preposition == preposition,
    #             predicates
    #         )
    #     )
