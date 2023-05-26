from properties import Config
from planner.request import SolverRequest
from planner.response import SolverResponse, SolverResult

from argparse import ArgumentParser
import json
from os.path import abspath, dirname, join
# from pddlpy import pddl


def print_plan(result: SolverResult, verbose: bool) -> None:
    print(repr(result) if verbose else result)
    for action in result.plan:
        print(repr(action) if verbose else action)


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
