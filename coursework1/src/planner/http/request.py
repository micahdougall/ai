from .response import SolverResponse

from dataclasses import dataclass, field
from os.path import join
from requests import post
from typing import ClassVar


@dataclass
class SolverRequest:
    """Class to represent a request to the Solver"""
    domain: str
    problem: str
    domain_file: str = field(init=False)
    problem_file: str = field(init=False)
    request: dict = field(init=False)
    url: ClassVar[str]
    pddl_dir: ClassVar[str]

    def __post_init__(self) -> None:
        """Uses class constants for file directory"""
        self.domain_file = join(
            __class__.pddl_dir, f"{self.domain}.pddl"
        )
        self.problem_file = join(
            __class__.pddl_dir, f"{self.problem}.pddl"
        )

        with (
            open(self.domain_file) as domain,
            open(self.problem_file) as problem
        ):
            self.request = {
                "domain": domain.read(),
                "problem": problem.read()
            }

    def get_response(self) -> SolverResponse:
        """Gets the response from a solver as a SolverResponse instance"""
        return SolverResponse.from_dict(
            post(
                __class__.url,
                verify=False,
                json=self.request
            ).json()
        ).write(self.problem)
