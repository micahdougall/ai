from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from os.path import join
from re import search
from typing import ClassVar, Self
from typing_extensions import override



@dataclass
class SolverAction:
    """Class to represent an action in a SolverResponse"""
    action: str
    name: str
    pddl_action: str = field(init=False)
    pddl_params: list[str] = field(init=False)

    def __post_init__(self) -> None:
        """Splits action text into actions and params"""
        args = self.name.strip("()").split(" ")
        self.pddl_action = args[0]
        self.pddl_params = [
            param for param in args[1:]
        ]

    @override
    def __str__(self) -> str:
        matches = search(
            r":action ([ a-zA-Z0-9-]+)[\s]+:parameters ([(][ a-zA-Z0-9-]+[)])",
            self.action
        )
        return f"""
            \033[96m{matches.group(1)} -> \033[95m{matches.group(2)}\033[49m
        """.strip()
    
    @override
    def __repr__(self) -> str:
        return self.action


@dataclass
class SolverResult:
    """Class to represent the result of a plan from the solver"""
    output: str
    parse_status: str
    error: str = None
    type: str = None
    length: int = None
    plan: list[SolverAction] = None
    cost: str = None
    val_stdout: str = None
    val_stderr: str = None
    val_status: str = None
    planPath: str = None
    logPath: str = None

    @override
    def __str__(self) -> str:
        return f"{self.length} actions needed:"
    
    @override
    def __repr__(self) -> str:
        return self.output


@dataclass
class SolverResponse(JSONWizard):
    """Class to represent a response from the solver"""
    status: str
    result: SolverResult
    valid: bool = field(init=False)
    responses: ClassVar[str]
    file_suffix: ClassVar[str] = "-response.json"

    def __post_init__(self):
        self.valid = True if self.status == "ok" else False

    def write(self, problem) -> Self:
        """Writes to a file"""
        with open(join(self.responses, f"{problem}{__class__.file_suffix}"), "w") as f:
            f.write(self.to_json(indent=4))
        return self

    @classmethod
    def read(cls, problem) -> Self:
        """Reads from a file"""
        with open(
            join(__class__.responses, f"{problem}{__class__.file_suffix}")
        ) as file:
            return cls.from_json(file.read())
