from .action import Action
from .domain import Domain
from .predicate import Condition, Predicate, Parameter
from .util import split_string, split_negated

from dataclasses import dataclass
from re import search


@dataclass
class Problem:
    """Class to represent a planning Problem"""
    objects: list[Parameter]
    state: list[Predicate]
    goal: list[Action]


def parse_problem(problem_file: str, domain: Domain) -> Problem:
    """Parses a planning problem from a file"""
    with open(problem_file) as problem:
        problem_string = problem.read()

    word = "a-zA-Z0-9 -"
    types = r"a-zA-Z0-9-\s"
    pred_pattern = r"\(\)=?a-zA-Z0-9-\s"

    obj_regx_matches = search(
        rf":objects\s*([{types}]*)\s*\)",
        problem_string
    )
    obj_lines = split_string(obj_regx_matches.group(1))

    objects = [
        Parameter.from_string(obj)
        for obj in obj_lines
    ]

    init_regx_matches = search(
        rf":init\s*([{pred_pattern}]*)\s*\)",
        problem_string
    )
    init_lines = split_string(init_regx_matches.group(1))
    init = [
        Condition.build(
            state.strip(" ()").split(" "),
            domain.predicates,
            objects
        )
        for state in init_lines
    ]

    goal_regx_matches = search(
        rf":goal\s*\(and\s*([{pred_pattern}]*)\s*\)\s*\)\s*\)",
        problem_string
    )
    goal_lines = split_string(goal_regx_matches.group(1))
    goal = [
        Condition.build(
            split_negated(aim),
            domain.predicates,
            objects
        )
        for aim in goal_lines
    ]

    return Problem(objects, init, goal)
