from .action import Action, parse_actions
from .predicate import Predicate, Parameter, Type
from .util import predicate_args, split_string

from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from re import search


@dataclass
class Domain(JSONWizard):
    """Class to represent a planning Domain"""
    types: Type
    predicates: list[Predicate]
    actions: list[Action]


def parse_domain(domain_file: str) -> Domain:
    """Parses a planning domain from a file"""
    with open(domain_file) as domain:
        domain_string = domain.read()

    word = "a-zA-Z0-9 -"
    types = r"a-zA-Z0-9-\s"
    pred_pattern = r"\(\)=?a-zA-Z0-9-\s"

    type_regx_matches = search(
        rf":types\s*([{types}]*)\s*\)",
        domain_string
    )
    lines = split_string(type_regx_matches.group(1))

    root = Type("object")
    for line in lines:
        (children, parent) = line.strip().split(" - ")
        objs = children.split(" ")

        if parent == "object":
            parent_node = root
        else:
            if root.get_node(parent) is None:
                root.children.append(Type(parent))
            parent_node = root.get_node(parent)

        for obj in objs:
            parent_node.children.append(Type(obj))

    pred_regx_matches = search(
        rf":predicates\s*([{pred_pattern}]*)\s*\)",
        domain_string
    )
    lines = split_string(pred_regx_matches.group(1))

    predicates = [
        Predicate(
            preposition=predicate_args(predicate)[0],
            parameters=[
                Parameter.from_string(p)
                for p in predicate_args(predicate)[1:]
            ]
        )
        for predicate in lines
    ]

    actions = parse_actions(domain_string, predicates)

    return Domain(root, predicates, actions)
