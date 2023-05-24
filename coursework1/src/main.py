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
    print(f"{len(actions)} actions needed:")
    for each in actions:
        matches = re.search(
            r":action ([-a-zA-Z]+)[\s]+:parameters ([(][ a-zA-Z-]+[)])",
            each.get("action")
        )
        print(f"    {matches.group(1)} -> {matches.group(2)}")


def print_verbose(plan: dict) -> None:
    print(f"""{plan.get("result", {}).get("output")}""")
    for each in plan.get("result", {}).get("plan"):
        print(f"""{each.get("action")}\n""")


def make_plan(domain_file: str, problem_file: str) -> None:
    plan = pddl_plan(
        get_definitions(f"../pddl/{domain_file}.pddl", f"../pddl/{problem_file}.pddl")
    )
    save_plan(plan, f"../resources/{problem_file}-response.json")
    return plan


def get_plan(problem_file: str) -> dict:
    with open(f"../resources/{problem_file}-response.json") as file:
        return json.load(file)


def render_plan(plan: dict, verbose: bool) -> None:
    (
        print_verbose(plan) 
        if verbose
        else print_actions_lite(plan.get("result", {}).get("plan"))
    )



def args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-s", "--solve", action="store_true")
    parser.add_argument("-d", "--domain", action="store", default="domain")
    parser.add_argument("-p", "--problem", action="store")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = args()

    plan = (
        make_plan(args.domain, args.problem)
        if args.solve
        else get_plan(args.problem)
    )
    render_plan(plan, args.verbose)

    

    aig-upf/universal-pddl-parser .. temporal-planning