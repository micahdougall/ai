from .action import Action, parse_actions
from .predicate import Predicate, Parameter, Type
from .util import list_params, split_string

from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from re import search


@dataclass
class Domain(JSONWizard):
    """Class to represent a planning Domain"""

    name: str
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

    # Domain name as per file header
    domain_name = search(
        rf"\(define\s*\(domain\s*([{word}]*)\)",
        domain_string
    ).group(1)

    # Extract all Type entries for domain
    type_regx_matches = search(rf":types\s*([{types}]*)\s*\)", domain_string)
    type_lines = split_string(type_regx_matches.group(1))

    # Build tree of Types with object as root node
    root = Type.get_root()
    for line in type_lines:
        (children, parent) = line.strip().split(" - ")
        objs = children.split(" ")

        if parent == "object":
            parent_node = root
        else:
            if root.get(parent) is None:
                root.children.append(Type(parent))
            parent_node = root.get(parent)

        for obj in objs:
            parent_node.children.append(Type(obj))

    # Predicates from domain
    pred_regx_matches = search(
        rf":predicates\s*([{pred_pattern}]*)\s*\)", domain_string
    )
    predicate_lines = split_string(pred_regx_matches.group(1))

    predicates = [
        Predicate(
            preposition=list_params(predicate)[0],
            parameters=[
                Parameter.from_string(p) for p in list_params(predicate)[1:]
            ],
        )
        for predicate in predicate_lines
    ]

    # Delegate actions parsing to Actions class
    actions = parse_actions(domain_string, predicates)

    return Domain(domain_name, root, predicates, actions)
