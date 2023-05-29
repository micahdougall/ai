import requests
import json
import re
from pddlpy import pddl


def get_definitions(domain_file: str, problem_file: str) -> dict:
    with open(domain_file) as d, open(problem_file) as p:
        return {"domain": d.read(), "problem": p.read()}


def pddl_plan(request: dict) -> dict:
    return requests.post(
        "http://solver.planning.domains/solve", verify=False, json=request
    ).json()


def save_plan(plan_dict: dict, full_response: str) -> None:
    with open(full_response, "w") as f:
        f.write(json.dumps(plan_dict))


if __name__ == "__main__":
    plan = pddl_plan(get_definitions("domain.pddl", "problem.pddl"))
    save_plan(plan, "response.json")

    print(f"""{plan.get("result", {}).get("output")}""")
    for each in plan.get("result", {}).get("plan"):
        print(f"""{each.get("action")}\n""")
