from planner.parser.domain import Domain
from planner.parser.problem import Problem
from planner.http.response import SolverResult


def print_plan(result: SolverResult, verbose: bool) -> None:
    """Prints the plan from a solver result object"""
    print(repr(result) if verbose else result)
    for action in result.plan:
        print(repr(action) if verbose else action)


def game_actions(result: SolverResult) -> None:
    """Prints the actions from a solver result object"""
    for action in result.plan:
        print(action.pddl_action)
        print(action.pddl_params)


def write_as_json(out_dir: str, object: Domain | Problem) -> None:
    with open(f"{out_dir}/{object.name}.json", "w") as file:
        file.write(object.to_json(indent=4))
