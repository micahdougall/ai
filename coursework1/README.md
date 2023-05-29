# CSF307 Artificial Intelligence - Coursework 1
<p align="center">
  <img src="resources/character.png" alt="drawing" width="100"/><br><br>
  <img src="https://img.shields.io/github/followers/micahdougall?style=social" alt="drawing" width="100"/>
</p>


This README outlines the required setup to run the program, and outlines the chosen implementation for the Python integration task (see [Integration](#integration)). It is recommended to view this document in preview mode in an IDE.

## Contents
- [PDDL files](#pddl)
- [Requirements](#requirements)
- [Usage](#usage)
- [Integration](#integration)
  - [HTTP](#http)
  - [Parser](#parser)
- [Directory Tree Wiki](#directory-tree-wiki)
- [References](#references)


## PDDL

Various PDDL problem and domain files can be found in the [pddl/](pddl/) directory with each subdirectory corresponding to a different use case:

- *[api/](pddl/api/)* &rArr; *These are the files used to send to the solver at runtime as they conform to the [PDDL 1.2 specification](https://planning.wiki/ref/pddl).*
- *[enhanced/](pddl/enhanced/)* &rArr; *A slightly more complex set of files (including `function` declarations) are included for interest. These canot be effected by the solver at [planning.domains](https://solver.planning.domains) as alater version of PDDL is required.*
- *[parsed/](pddl/parsed/)* &rArr; *Owing to the ***Pre-Alpha*** nature of the custom parser (see [Parser](#parser)), some adjustments have been made to the original files in [api/](pddl/api/). Namely, the removal of `exists` and `forall` loops.*

**NB: For DRY reasons, comments have only been included in the [enhanced/](pddl/enhanced/) versions of the files.**


## Requirements

- Python (version 3.11.3).
- Packages in [requirements file](requirements.txt).


To install the necessary requirements, simply run (in the root directory):
```bash
# python/python3 for systems with multiple versions

python3 -m pip install -r requirements.txt
```

Or to avoid conflicts with existing package versions, use the [venv](https://realpython.com/python-virtual-environments-a-primer/) module:

```bash
# create virtual env
python3 -m venv <new-venv-name>

# activate (on Linux/macOS)
source <new-venv-name>/bin/activate

# install requirements
python3 -m pip install -r requirements.txt
```
## Usage

There are several possible CLI arguments which can be provided to [main.py](src/main.py) depending on the required execution:

- `-s` &rArr; **solve**: *Will send the domain and problem file (in [pddl/api/](pddl/api/)) to the solver at [planning.domains](https://solver.planning.domains) and handle the response. Omit this argument to use locally saved results in [resources/responses/](resources/responses/).*
- `-d` &rArr; **domain**: *Denotes the domain file (exclude pddl extension) to use for solver requests, default=[runescape](pddl/api/runescape.pddl).*
- `-p` &rArr; **solve**: *Denotes the problem file to use for solver requests. This is a required argument when using `-s`. Must be a valid filename in [pddl/api/](pddl/api/) (exclude pddl extension)*
- `-v` &rArr; **verbose**: *Will print response results in verbose mode. This is only recommended for debugging failed requests to the solver.*

For example, to send a request to the solver for the [makesword](pddl/api/makesword.pddl) problem, run (from the root folder):

```bash
python3 src/main.py -s -p makesword
```

Or to print the locally stored response for the [makearrow](pddl/api/makearrow.pddl) problem:

```bash
python3 src/main.py -p makearrow
```

## Integration

### HTTP

The integration with the solver API can be seen in [src/planner/http](src/planner/http). The [SolverRequest](src/planner/http/request.py) builds a simple HTTP request from the specified domain and problem files, and generates a [SolverResponse](src/planner/http/response.py) with the action details parsed from the solver response. The `__str__` method shows how each action is returned as a string to the console.

Eg:

<!-- ```bash -->

<p>14 actions needed:</p>
<span style="color:cyan">equip -> </span><span style="color:magenta">(player pickaxe shed)</span></br>
<span style="color:cyan">move-to -> </span><span style="color:magenta">(player shed anvil)</span></br>
<span style="color:cyan">move-to -> </span><span style="color:magenta">(player anvil mine)</span></br>
<span style="color:cyan">mine-rocks -> </span><span style="color:magenta">(player mine pickaxe rock ore)</span></br>
<span style="color:cyan">move-to -> </span><span style="color:magenta">(player mine furnace)</span></br>
<span style="color:cyan">smelt-ore -> </span><span style="color:magenta">(player furnace ore bars)</span></br>
<span style="color:cyan">move-to -> </span><span style="color:magenta">(player furnace shed)</span></br>
<span style="color:cyan">store -> </span><span style="color:magenta">(player pickaxe shed)</span></br>
<span style="color:cyan">equip -> </span><span style="color:magenta">(player hammer shed)</span></br>
<span style="color:cyan">move-to -> </span><span style="color:magenta">(player shed anvil)</span></br>
<span style="color:cyan">smithe-bars -> </span><span style="color:magenta">(player anvil hammer bars sword)</span></br>
<span style="color:cyan">move-to -> </span><span style="color:magenta">(player anvil shed)</span></br>
<span style="color:cyan">store -> </span><span style="color:magenta">(player sword shed)</span></br>
<span style="color:cyan">store -> </span><span style="color:magenta">(player hammer shed)</span></br></br>

Solver responses from program executions are saved to [resources/responses/](resources/responses/). In case of failed requests, a cached version or each response is saved to [resources/local/](resources/local).

*In the case of the `-s` arg not being passed, SolverResponse reads from the local file and generates the action output.*

### Parser

The author has made the (questionable) decision to attempt to create a manual parser for PDDL domain and problem files which can be seen in [src/planner/parser/](src/planner/parser/).

The parser maps the actions, types and predicates contained in the specified domain-problem into useable complex object types, and implicitly allows for a simple validation by virtue of requiring certain types.

- **Domain** &rArr; maps to a [Domain](src/planner/parser/domain.py) object containing the following sub-objects as attributes:
    * **type** &rArr; a root object [Type](src/planner/parser/predicate.py) containing a hierarchy of subtypes.
    * **predicate** &rArr; a list of [Predicate](src/planner/parser/predicate.py) objects for the domain.
    * **action** &rArr; a list of [Action](src/planner/parser/action.py) objects for the domain.


- **Problem** &rArr; maps to a [Domain](src/planner/parser/domain.py) object containing the following sub-objects as attributes:
    * **objects** &rArr; a list of [Condition](src/planner/parser/predicate.py) types .
    * **init** &rArr; a list of [Condition](src/planner/parser/predicate.py) objects for the problem.
    * **goal** &rArr; a list of [Action](src/planner/parser/action.py) objects for the problem.

Each of the child objects contains all the necessary sub-instances to know the state of a problem at any given stage (as may be useful, for example, in a custom solver implementation). So a `Condition` type includes as its children a `Predicate`, a list of `Parameters` and a `Negation` (true/false).

With this compositional nature, the domain and problem attributes can then be access at runtime by, for example, calling the nested attributes on the domain. Eg:

```python
problem = Problem(...parse problem file...)

# Format print selected child attributes
for condition in problem.init:
    print(
        f"Preposition: {condition.predicate.preposition}"
        f"  -> takes Parameters:\n\t"
        f"{(chr(10) + chr(9)).join([str(p) for p in condition.predicate.parameters])}\n"
    )

# Serialize to JSON
print(problem.to_json(indent=4))
```

The serialized outputs for the domain and problem files are saved to [resources/objects/](resources/objects/) directory, with the filename determined be the parse step from the original PDDL file.

Snippet of a serialized predicate:

```Json
"init": [
    {
        "predicate": {
            "preposition": "at",
            "parameters": [
                {
                    "name": "p",
                    "types": {
                        "type": "player",
                        "children": []
                    }
                },
                {
                    "name": "l",
                    "types": {
                        "type": "location",
                        "children": [
                            {
                                "type": "anvil",
                                "children": []
                            },
                            {
                                "type": "farm",
                                "children": []
                            },
                            {
                                "type": "forest",
                                "children": []
                            },
                            {
                                "type": "furnace",
                                "children": []
                            },
                            {
                                "type": "mine",
                                "children": []
                            },
                            {
                                "type": "storage",
                                "children": []
                            }
                        ]
                    }
                }
            ]
        }
    }, 
  
    ...
    
]
```

## Directory Tree Wiki
```
.
├── README.md
├── config.json                       # config variables
├── pddl                              # root for pddl files
│   ├── api                           # pddl files for solver 
│   │   ├── makearrow.pddl
│   │   ├── makesword.pddl
│   │   └── runescape.pddl
│   ├── enhanced                      # enhanced files with comments 
│   │   ├── makearrow.pddl
│   │   ├── makesword.pddl
│   │   └── runescape.pddl
│   └── parsed                        # simplified pddl files for parser
│       ├── makearrow.pddl
│       ├── makesword.pddl
│       └── runescape.pddl
├── requirements.txt
├── resources
│   ├── character.png
│   ├── local                         # backup solver repsonses
│   │   ├── makearrow-response.json
│   │   └── makesword-response.json
│   ├── objects                       # serialized parsed domain/problems
│   │   ├── makearrow.json
│   │   ├── makesword.json
│   │   └── runescape.json
│   └── responses                     # runtime responses from solver
│       ├── makearrow-response.json
│       └── makesword-response.json
└── src                               # application root
    ├── __init__.py                   
    ├── config.py                     # config variables
    ├── main.py                       # entry point
    ├── output.py                     # print helper
    └── planner
        ├── __init__.py
        ├── http
        │   ├── __init__.py
        │   ├── request.py            # solver request handler
        │   └── response.py           # solver response handler
        └── parser
            ├── __init__.py
            ├── action.py             # parses actions
            ├── domain.py             # parses domain
            ├── predicate.py          # subclasses for object structure
            ├── problem.py            # parses actions
            └── util.py               # parse helper
```

## References

- https://planning.wiki/ref/pddl
- http://solver.planning.domains
- https://realpython.com/python-virtual-environments-a-primer/


## Repository links
- https://github.com/micahdougall/ai
- https://gitfront.io/r/user-8542067/SE98YnTAwUMt/advanced-object-oriented/
