from .action import Action
from .predicate import Predicate, Parameter, Type
from .util import predicate_args, split_string

from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from re import findall, search


# @dataclass
# class TypeMap:
#

@dataclass
class Domain(JSONWizard):
    # types: list[Type]
    # types: dict[str, str]
    types: Type
    predicates: list[Predicate]
    actions: list[Action]


def parse_domain(domain_file: str) -> Domain:
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

    # types: list[Type] = []
    # for line in lines:
    #     (children, parent) = line.strip().split(" - ")
    #     objs = children.split(" ")
    #
    #     if parent not in Type.type_names(types):
    #         types.append(Type(parent))
    #
    #     types += [
    #         Type(obj, parent) for obj in objs
    #     ]

    root = Type("object")
    for line in lines:
        (children, parent) = line.strip().split(" - ")
        objs = children.split(" ")

        if parent == "object":
            parent_node = root
        else:
            if root.get_node(parent) is None:
                # print(
                #     f"""adding {parent} becuase get_node = {root.get_node(parent)}"""
                # )
                root.children.append(Type(parent))
            # else:
            # print(f"{parent} already exists in root")
            parent_node = root.get_node(parent)
        # print(f"Parent is now {parent_node}")

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
                for p in predicate_args(pred_pattern)[1:]
            ]
        )
        for predicate in lines
    ]

    action_regx_matches = findall(
        rf":action ([{word}]+)\s*"
        rf":parameters\s*\(\s*([{pred_pattern}]*)\s*\)\s*"
        rf":precondition\s*\(and\s*([{pred_pattern}]*)\s*\)\s*"
        rf":effect\s*\(and\s*([{pred_pattern}]*)\s\)\s*\)",
        domain_string
    )

    actions: list[Action] = []
    for match in action_regx_matches[:1]:
        action_regx = match[0]
        (param_regx, cond_regx, effect_regx) = [
            split_string(each) for each in match[1:]
        ]
        parameters = [
            Parameter.from_string(parameter)
            for parameter in param_regx
        ]
        param_types = Parameter.types_dict(parameters)
        preconditions = [
            Predicate.from_precondition(
                predicate_args(condition), param_types
            )
            for condition in cond_regx
        ]
        effects = [
            Predicate.from_precondition(
                predicate_args(effect), param_types
            )
            for effect in effect_regx
        ]
        action = Action(
            name=action_regx,
            parameters=parameters,
            precondition=preconditions,
            effect=effects
        )
        actions.append(action)

    return Domain(root, predicates, actions)
