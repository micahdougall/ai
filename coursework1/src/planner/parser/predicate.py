from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from itertools import chain
from re import match
from typing import Self


@dataclass
class Type:
    """Class to represent an object type in a domain"""
    type: str
    children: list[Self] = field(default_factory=list)

    def nodes(self) -> list[Self]:
        """Returns all sub-nodes from this parent"""
        return list(
            chain.from_iterable(
                [t.nodes for t in self.children]
            )
        )

    def get_node(self, search: str) -> Self | None:
        """Returns a specific Type node from descendents"""
        if self.children:
            # return next(
            #     filter(
            #         lambda c: c.type == search,
            #         self.children
            #     ), None
            # ) or next(
            #     iter(
            #         [c.get_node(search) for c in self.children]
            #     )
            # )
            for c in self.children:
                if c.type == search:
                    return c
            else:
                for c in self.children:
                    opt = c.get_node(search)
                    if opt:
                        return opt
        else:
            return None


@dataclass
class Parameter(JSONWizard):
    """Class to represent a parameter for a predicate"""
    name: str
    types: Type | list[Type]

    @classmethod
    def from_string(cls, param: str) -> Self:
        """Builds a parameter object from a string"""
        objs = param.strip().split(" - ")
        types = match(r"^\(either ([ a-zA-Z0-9-]*)\)$", objs[1])
        return cls(
            name=objs[0].strip("?"),
            # TODO: Change to lookup on class variable
            types=[
                Type(element) for element
                in types.group(1).split(" ")
            ] if types else Type(objs[1])
        )

    @staticmethod
    def get(name, parameters: list[Self]) -> Self:
        """Looks for a parameter by name"""
        return next(
            filter(
                lambda p: p.name == name,
                parameters
            ), None
        )


@dataclass
class Predicate(JSONWizard):
    """Class to represent a predicate in a planning domain"""
    preposition: str
    parameters: list[Parameter]

    @staticmethod
    def get(preposition: str, predicates: list[Self]) -> Self:
        """Looks for a predicate by preposition"""
        return next(
            filter(
                lambda p: p.preposition == preposition,
                predicates
            )
        )


@dataclass
class Condition:
    """Class to represent a condition for a state"""
    predicate: Predicate
    parameters: list[Parameter]
    negation: bool

    @classmethod
    def build(
            cls,
            args: list[str],
            predicates: list[Predicate],
            parameters: list[Parameter]
    ):
        """Builder constructor using lookups on parameters/predicates"""
        return cls(
            predicate=Predicate.get(
                args[0].removeprefix("not ("),
                predicates
            ),
            parameters=[
                Parameter.get(p, parameters)
                for p in args[1:]
            ],
            negation=args[0].startswith("(not (")
        )