from .action import Action
from .predicate import Predicate, Parameter
from .util import is_negated, parameter_items, predicate_args

from dataclasses import dataclass
from re import findall, search


@dataclass
class Domain:
    predicates: list[Predicate]
    actions: list[Action]


def parse_domain(domain_file: str) -> Domain:
    with open(domain_file) as domain:
        domain_string = domain.read()

    word = " a-zA-Z0-9-"
    predicate = r"\(\)=?a-zA-Z0-9-\s"

    matches = search(
        rf":predicates\s*([{predicate}]*)\s*\)",
        domain_string
    )
    lines = matches.group(1).strip().split("\n")

    predicates = [
        Predicate(
            preposition=predicate_args(line)[0],
            parameters=[
                Parameter.from_string(p)
                for p in predicate_args(line)[1:]
            ]
        )
        for line in lines
    ]

    matches = findall(
        rf":action ([{word}]+)\s*"
        rf":parameters\s*\(\s*([{predicate}]*)\s*\)\s*"
        rf":precondition\s*\(and\s*([{predicate}]*)\s*\)\s*"
        rf":effect\s*\(and\s*([{predicate}]*)\s\)\s*\)",
        domain_string
    )

    actions: list[Action] = []
    for match in matches:
        parameters = [
            Parameter.from_string(params)
            for params in match[1].strip().split("\n")
        ]
        preconditions = [
            Predicate.from_precondition(
                predicate_args(line),
                Parameter.types_dict(parameters)
            )
            for line in match[2].strip().split("\n")
        ]
        effects = [
            Predicate.from_precondition(
                predicate_args(line),
                Parameter.types_dict(parameters)
            )
            for line in match[3].strip().split("\n")
        ]
        action = Action(
            name=match[0],
            parameters=parameters,
            precondition=preconditions,
            effect=effects
        )
        actions.append(action)

    return Domain(predicates, actions)
