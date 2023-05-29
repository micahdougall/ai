from .predicate import Condition, Predicate, Parameter
from .util import list_params, split_string

from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from re import findall


@dataclass
class Action(JSONWizard):
    """Class to represent an action in a domain"""

    name: str
    parameters: list[Parameter]
    precondition: list[Condition]
    effect: list[Condition]


def parse_actions(domain_string: str, predicates: list[Predicate]) -> list[Action]:
    """Parses actions from a domain file string"""

    word = "a-zA-Z0-9 -"
    types = r"a-zA-Z0-9-\s"
    pred_pattern = r"\(\)=?a-zA-Z0-9-\s"

    action_regx_matches = findall(
        rf":action ([{word}]+)\s*"
        rf":parameters\s*\(\s*([{pred_pattern}]*)\s*\)\s*"
        rf":precondition\s*\(and\s*([{pred_pattern}]*)\s*\)\s*"
        rf":effect\s*\(and\s*([{pred_pattern}]*)\s\)\s*\)",
        domain_string,
    )

    actions: list[Action] = []
    for match in action_regx_matches[:1]:
        action_regx = match[0]
        (param_regx, cond_regx, effect_regx) = [
            split_string(each) for each in match[1:]
        ]

        parameters = [Parameter.from_string(parameter) for parameter in param_regx]

        preconditions = [
            Condition.build(list_params(condition), predicates, parameters)
            for condition in cond_regx
        ]

        effects = [
            Condition.build(list_params(effect), predicates, parameters)
            for effect in effect_regx
        ]

        actions.append(
            Action(
                name=action_regx,
                parameters=parameters,
                precondition=preconditions,
                effect=effects,
            )
        )
