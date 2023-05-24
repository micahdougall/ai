from planner.response import SolverResponse

from dataclasses import dataclass, field
from requests import post


@dataclass
class SolverRequest():
    domain: str
    problem: str
    url: str = "http://solver.planning.domains/solve"
    domain_file: str = field(init=False)
    problem_file: str = field(init=False)
    request: dict = field(init=False)

    def __post_init__(self) -> None:
        self.domain_file = f"../pddl/{self.domain}.pddl"
        self.problem_file = f"../pddl/{self.problem}.pddl"

        with open(self.domain_file) as d, open(self.problem_file) as p:
            self.request = {
                "domain": d.read(),
                "problem": p.read()
            }

    def get_response(self) -> SolverResponse:
        return SolverResponse.from_dict(
            post(
                self.url,
                verify=False,
                json=self.request
            ).json()
        )
