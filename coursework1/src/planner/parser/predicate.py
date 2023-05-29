from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from pyre_extensions import override
from re import match
from typing import Self, ClassVar


@dataclass
class Type:
    """Class to represent an object type in a domain"""

    type: str
    children: list[Self] = field(default_factory=list)
    _root_: ClassVar[Self] = None

    def get(self, search: str) -> Self | None:
        """Returns a specific Type node from descendents

        Equivalent to:
            if self.children:
                for c in self.children:
                    if c.type == search:
                        return c
                else:
                    for c in self.children:
                        optional = c.get_node(search)
                        if optional:
                            return optional
            else:
                return None
        """
        return (
            next(filter(lambda c: c.type == search, self.children), None)
            or next(iter([c.get(search) for c in self.children]))
            if self.children
            else None
        )

    @classmethod
    def get_root(cls):
        """Pseudo-singleton class method for root Type"""
        if not cls._root_:
            cls._root_ = cls("object")
        return cls._root_


@dataclass
class Parameter(JSONWizard):
    """Class to represent a parameter for a predicate"""

    name: str
    types: Type | list[Type]

    @override
    def __str__(self) -> str:
        return (
            f"{self.name} -> type(s): ("
            f"{([t.type for t in self.types] if isinstance(self.types, list) else self.types.type)})"
        )

    @classmethod
    def from_string(cls, param: str) -> Self:
        """Builds a parameter object from a string"""
        objs = param.strip().split(" - ")
        types = match(r"^\(either ([ a-zA-Z0-9-]*)\)$", objs[1])
        root = Type.get_root()
        return cls(
            name=objs[0].strip("?"),
            types=[root.get(element) for element in types.group(1).split(" ")]
            if types
            else root.get(objs[1])
        )

    @staticmethod
    def get(name, parameters: list[Self]) -> Self:
        """Looks for a parameter by name"""
        return next(filter(lambda p: p.name == name, parameters), None)


@dataclass
class Predicate(JSONWizard):
    """Class to represent a predicate in a planning domain"""

    preposition: str
    parameters: list[Parameter]

    @staticmethod
    def get(preposition: str, predicates: list[Self]) -> Self:
        """Looks for a predicate by preposition"""
        return next(filter(lambda p: p.preposition == preposition, predicates))


@dataclass
class Condition:
    """Class to represent a condition for a state"""

    predicate: Predicate
    parameters: list[Parameter]
    negation: bool

    @classmethod
    def build(
        cls, args: list[str], predicates: list[Predicate], parameters: list[Parameter]
    ):
        """Builder constructor using lookups on parameters/predicates"""
        return cls(
            predicate=Predicate.get(args[0].removeprefix("not ("), predicates),
            parameters=[Parameter.get(p, parameters) for p in args[1:]],
            negation=args[0].startswith("(not ("),
        )
