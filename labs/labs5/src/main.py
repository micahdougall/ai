from planner.request import SolverRequest
from planner.response import SolverResponse, SolverResult

from argparse import ArgumentParser
# from pddlpy import pddl


def get_solver_response(domain_file: str, problem_file: str) -> None:
    solver_response = SolverRequest(domain_file, problem_file).get_response()
    solver_response.write(problem_file)
    return solver_response


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

    response = (
        get_solver_response(args.domain, args.problem)
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
