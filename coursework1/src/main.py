from argparse import ArgumentParser
import requests
import json
import re
from pddlpy import pddl


def get_definitions(domain_file: str, problem_file: str) -> dict:
    with open(domain_file) as d, open(problem_file) as p:
        return {
            "domain": d.read(),
            "problem": p.read()
        }


def pddl_plan(request: dict) -> dict:
    return requests.post(
        "http://solver.planning.domains/solve",
        verify=False,
        json=request
    ).json()


def save_plan(plan_dict: dict, full_response: str) -> None:
    with open(full_response, "w") as f:
        f.write(json.dumps(plan_dict))


def print_actions_lite(actions: list[dict]) -> None:
    for each in actions:
        matches = re.search(
            r":action ([-a-zA-Z]+)[\s]+:parameters ([(][ a-zA-Z-]+[)])",
            each.get("action")
        )
        print(f"{matches.group(1)} -> {matches.group(2)}")


def print_verbose(plan: dict) -> None:
    print(f"""{plan.get("result", {}).get("output")}""")
    for each in plan.get("result", {}).get("plan"):
        print(f"""{each.get("action")}\n""")



def args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = args()
    plan = pddl_plan(
        get_definitions("../pddl/domain.pddl", "../pddl/swords.pddl")
    )
    save_plan(plan, "response.json")
    
    (
        print_verbose(plan) 
        if args.verbose 
        else print_actions_lite(plan.get("result", {}).get("plan"))
    )
    