from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from os.path import join
from re import search
from typing import ClassVar, Self

from typing_extensions import override

# from typing_extensions import override


@dataclass
class SolverAction:
    action: str
    name: str
    pddl_action: str = field(init=False)
    pddl_params: list[str] = field(init=False)

    def __post_init__(self) -> None:
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
        return f"    {matches.group(1)} -> {matches.group(2)}"
    
    @override
    def __repr__(self) -> str:
        return self.action


@dataclass
class SolverResult:
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
    status: str
    result: SolverResult
    valid: bool = field(init=False)
    resources: ClassVar[str]
    file_suffix: ClassVar[str] = "-response.json"

    def __post_init__(self):
        self.valid = True if self.status == "ok" else False

    def write(self, problem) -> Self:
        with open(join(self.resources, f"{problem}{__class__.file_suffix}"), "w") as f:
            f.write(self.to_json())
        return self

    @classmethod
    def read(cls, problem) -> Self:
        with open(
            join(__class__.resources, f"{problem}{__class__.file_suffix}")
        ) as file:
            return cls.from_json(file.read())
