from config import Config
from planner.parser.domain import parse_domain
from planner.parser.problem import parse_problem
from planner.parser.action import Action
from planner.http.request import SolverRequest
from planner.http.response import SolverResponse, SolverResult

from argparse import ArgumentParser
import json
from os.path import abspath, dirname, join
# from pddlpy import http


def print_plan(result: SolverResult, verbose: bool) -> None:
    print(repr(result) if verbose else result)
    for action in result.plan:
        print(repr(action) if verbose else action)


def game_actions(result: SolverResult) -> None:
    for action in result.plan:
        # args = line.trim("()").split(" ")
        # l = list(args)
        # for l in list:
        #     print(l)
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

    # prob = pddlpy.DomainProblem("../http/domain.http", "../http/sword.http")
    # state = list(prob.initialstate())

    
    # for each in state:
        # print(f"State: {each}")
    #     # print(each.ground(0))

    #     (a, b, c) = each
    #     print(a)
        # for param in each:
            # print(f"    param: {param}")
    # for each in prob.goals():
    #     print("Goals:")
    #     for param in each:
    #         print(f"    param: {param}")
    #         print(param)
    # print(prob.goals())
    # for item, name in prob.worldobjects().items():
    #     print(f"{item} -> {name}")
    # print(list(prob.operators()))
    # for each in prob.operators():
        # print(f"this is an op: {each}")
    # print(prob.ground_operator('move-to'))


    # exit()

    root = abspath(join(dirname(__file__), "../"))
    with open(join(root, "config.json")) as options:
        config = Config(json.load(options))
    
    SolverRequest.url = config.solver_url
    SolverRequest.pddl_dir = join(root, config.pddl_dir)
    SolverRequest.resources = join(root, config.resources)
    SolverResponse.resources = join(root, config.resources)

    pddl_dir = join(root, config.pddl_dir)

    # Action.parse_actions(pddl_dir)
    # problem = parse_problem(join(root, "pddl/sword.pddl"))
    # problem = parse_problem(join(root, "pddl/domain.pddl"))
    # print(problem.types)
    # print("exit")

    domain = parse_domain(join(root, "pddl/domain.pddl"))
    print(domain.types)
    print("exit")
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
