from config import Config
from output import print_plan, write_as_json
from planner.http.request import SolverRequest
from planner.http.response import SolverResponse
from planner.parser.domain import parse_domain
from planner.parser.problem import parse_problem

from argparse import ArgumentParser
import json
from os.path import abspath, dirname, join


def args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-s", "--solve", action="store_true")
    parser.add_argument("-d", "--domain", action="store", default="runescape")
    parser.add_argument("-p", "--problem", action="store")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = args()
    root = abspath(join(dirname(__file__), "../"))
    with open(join(root, "config.json")) as options:
        config = Config(json.load(options))

    # Parse domain and problem file into meaningful objects
    pddl_parsed_dir = join(root, config.pddl_parsed_dir)
    domain = parse_domain(join(pddl_parsed_dir, f"{args.domain}.pddl"))
    write_as_json(join(root, config.objects), domain)
    problem = parse_problem(join(pddl_parsed_dir, f"{args.problem}.pddl"), domain)
    write_as_json(join(root, config.objects), problem)

    # Print example for init state
    if args.verbose:
        print("Print-out example for init state for problem file...\n\n")
        for condition in problem.init:
            print(
                f"Preposition: {condition.predicate.preposition}"
                f"  -> takes Parameters:\n\t"
                f"{(chr(10) + chr(9)).join([str(p) for p in condition.predicate.parameters])}\n"
            )
        print("Serializing problem object...\n\n")
        print(problem.to_json(indent=4))

    # Config for solver requests
    response_dir = config.responses if args.solve else config.local
    SolverRequest.url = config.solver_url
    SolverRequest.pddl_dir = join(root, config.pddl_api_dir)
    SolverRequest.responses = join(root, response_dir)
    SolverResponse.responses = join(root, response_dir)

    # Get response from Solver API
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
