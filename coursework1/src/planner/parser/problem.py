import re

from .action import Action
from .predicate import Predicate, Parameter
# from .predicate import Predicate, Parameter, Type
from .util import predicate_args, split_string

from dataclasses import dataclass, field
from itertools import chain
from re import findall, search
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
        print(f"Getting node: {search} from {self.type}")
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
                print(c.type)
                if c.type == search:
                    print("found")
                    return c
            return None
        else:
            print(f"{self.type} has no children")
        # else:
        #     optional = None
        # print(optional)
        # return optional




        # if child in [
        #     child.type for child in self.children
        # ]:







@dataclass
class Problem:
    types: list[Parameter]
    state: list[Predicate]
    goal: list[Action]


def parse_problem(problem_file: str) -> Problem:
    with open(problem_file) as problem:
        problem_string = problem.read()

    word = "a-zA-Z0-9 -"
    types = r"a-zA-Z0-9-\s"
    pred_pattern = r"\(\)=?a-zA-Z0-9-\s"

    type_regx_matches = search(
        rf":types\s*([{types}]*)\s*\)",
        problem_string
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
    # print(root)
    # print(root.children)
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


    # print(root)
    exit()
#
#     pred_regx_matches = search(
#         rf":predicates\s*([{pred_pattern}]*)\s*\)",
#         domain_string
#     )
#     lines = split_string(pred_regx_matches.group(1))
#
#     predicates = [
#         Predicate(
#             preposition=predicate_args(predicate)[0],
#             parameters=[
#                 Parameter.from_string(p)
#                 for p in predicate_args(pred_pattern)[1:]
#             ]
#         )
#         for predicate in lines
#     ]
#
#     action_regx_matches = findall(
#         rf":action ([{word}]+)\s*"
#         rf":parameters\s*\(\s*([{pred_pattern}]*)\s*\)\s*"
#         rf":precondition\s*\(and\s*([{pred_pattern}]*)\s*\)\s*"
#         rf":effect\s*\(and\s*([{pred_pattern}]*)\s\)\s*\)",
#         domain_string
#     )
#
#     actions: list[Action] = []
#     for match in action_regx_matches[:1]:
#         action_regx = match[0]
#         (param_regx, cond_regx, effect_regx) = [
#             split_string(each) for each in match[1:]
#         ]
#         parameters = [
#             Parameter.from_string(parameter)
#             for parameter in param_regx
#         ]
#         param_types = Parameter.types_dict(parameters)
#         preconditions = [
#             Predicate.from_precondition(
#                 predicate_args(condition), param_types
#             )
#             for condition in cond_regx
#         ]
#         effects = [
#             Predicate.from_precondition(
#                 predicate_args(effect), param_types
#             )
#             for effect in effect_regx
#         ]
#         action = Action(
#             name=action_regx,
#             parameters=parameters,
#             precondition=preconditions,
#             effect=effects
#         )
#         actions.append(action)
#
#     return Domain(types, predicates, actions)
