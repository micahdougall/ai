from config import Config
from planner.http.request import SolverRequest
from planner.http.response import SolverResponse, SolverResult
from planner.parser.domain import parse_domain
from planner.parser.problem import parse_problem

from argparse import ArgumentParser
import json
from os.path import abspath, dirname, join


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


def args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-s", "--solve", action="store_true")
    parser.add_argument("-d", "--domain", action="store", default="domain")
    parser.add_argument("-p", "--problem", action="store")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = args()

    root = abspath(join(dirname(__file__), "../"))
    with open(join(root, "config.json")) as options:
        config = Config(json.load(options))
    
    SolverRequest.url = config.solver_url
    SolverRequest.pddl_dir = join(root, config.pddl_dir)
    SolverRequest.resources = join(root, config.resources)
    SolverResponse.resources = join(root, config.resources)

    pddl_dir = join(root, config.pddl_dir)

    domain = parse_domain(
        join(root, "pddl/domain-parsable.pddl")
    )
    problem = parse_problem(
        join(root, "pddl/sword-parsable.pddl"),
        domain
    )
    print(problem.goal)
    exit()

    response = (
        SolverRequest(args.domain, args.problem).get_response()
        if args.solve
        else SolverResponse.read(args.problem)
    )

    if not response.valid:
        print(
            f"Output: \n\t{response.result.output}\n"
            f"Parse Status: \n\t{response.result.parse_status}\n"
            f"Error: \n\t{response.result.error}"
        )
    else:
        print_plan(response.result, args.verbose)
        # game_actions(response.result)
