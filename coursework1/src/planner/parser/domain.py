# from http.request import SolverRequest

from .action import Action
from .predicate import Parameter, Predicate

from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from os.path import join
from re import findall, search
from typing import Self


@dataclass
class Domain:
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
    # print(predicate_matches)
    # for match in predicate_matches:
    #     print(f"match -> {matches.group(1)}")
    # exit()

    lines = matches.group(1).strip().split("\n")
    # parts = pred_match.split(" ?")
    for line in lines:
        # print(f"""p -> {line.strip(" ()")}""")
        parts = line.strip(" ()").split(" ?")

        # exit()
        predicate = {
            "preposition": parts[0],
            "parameters": [
                {
                    k: v for k, v
                    in zip(("name", "type_str"), param.strip().split(" - "))
                }
                for param in parts[1:]
            ]
        }
        # print(predicate)
        p = Predicate.from_dict(predicate)
        # print(p)
    # exit()

    # parts = line.strip(" ()").split(" ?")
    def split_types(text: str): return text.strip(" ()").split(" ?")
    predicates = [
        Predicate.from_dict({
            "preposition": split_types(line)[0],
            "parameters": [
                {
                    k: v for k, v
                    in zip(("name", "type_str"), param.strip().split(" - "))
                }
                for param in split_types(line)[1:]
            ]
        })
        for line in lines
    ]
    print(predicates)

    exit()

    matches = findall(
        rf":action ([{word}]+)\s*"
        rf":parameters\s*\(\s*([{predicate}]*)\s*\)\s*"
        rf":precondition\s*\(and\s*([{predicate}]*)\s*\)\s*"
        rf":effect\s*\(and\s*([{predicate}]*)\s\)\s*\)",
        domain_string
    )
    for match in matches[:1]:
        action = {
            "name": match[0],
            "parameters": [
                {
                    k: v for k, v
                    in zip(("name", "type_str"), args.strip().split(" - "))
                }
                for args in match[1].strip().split("\n")
            ],
            # "precondition": [
            #     {
            #
            #     }
            # ]
        }
        print(action)
        a = Action.from_dict(action)
        print(a)

    return Domain()
