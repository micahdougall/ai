from planner.parser.domain import Domain
from planner.parser.problem import Problem
from planner.http.response import SolverResult


def print_plan(result: SolverResult, verbose: bool) -> None:
    """Prints the plan from a solver result object"""
    print(repr(result) if verbose else result)
    for action in result.plan:
        print(
            repr(action) if verbose
            else f"\033[96m{action.pddl_action} \u27F9 \033[95m{action.pddl_params}\033[49m"
        )


def write_as_json(out_dir: str, object: Domain | Problem) -> None:
    with open(f"{out_dir}/{object.name}.json", "w") as file:
        file.write(object.to_json(indent=4))
