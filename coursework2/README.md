# CSF307 Artificial Intelligence - Coursework 2
<p align="center">
  <img src="../large/pikachu_win.png" alt="drawing" width="100"/><br><br>
  <img src="https://img.shields.io/github/followers/micahdougall?style=social" alt="drawing" width="100"/>
</p>


This README is a brief overview of the program structure with the aim of simplifying its execution. As usual, this document is best viewed in an IDE or on [GitHub](https://github.com/micahdougall/ai/tree/main/coursework2).

There are essentially three components to the code:
- [model](src/model) &rArr; manages the state of the grid as the game progresses.
- [view](src/view) &rArr; provides a way to visualise the game results using the [pygame](https://www.pygame.org/news) library.
- [controller](src/controller) &rArr; controls the program flow by integrating with `CWorld`.


## Contents
- [Requirements](#requirements)
- [Directory Overview](#directory-overview)
    - [Model](#model)
    - [View](#view)
    - [Controller](#controller)
- [AI Implementation](#ai-implementation)
  - [Standard](#standard)
  - [Bayes](#bayes)
- [Directory Tree Wiki](#directory-tree-wiki)
- [References](#references)


# TODO!
- Readme
- Requirements
- Probabilities for standard


## Requirements

- Python (version 3.11.3).
- Packages in [requirements.txt](requirements.txt).


To install the necessary `requirements`, simply run (in the root directory):
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

The program can either be run as a game output (using pygame) or as several iterations to test the performance (pygme output excluded). In either case, an `algorithm` *must* be selected:

- `-a | --algorithm [standard | bayes]` &rArr; **algorithm**: *Selects which algorithm to use for solving the puzzle. Following argument must either be `standard` or `bayes`, **required***.
- `-t [n]` &rArr; **test**: *Used for testing; the program will execute the game `n` times and print the overall win percentage to the console.*
- `-d` &rArr; **debug**: *This will print the results in debug mode, which includes details for the state of the grid at each move.*

For example, to enjoy the game in its full glory:

```bash
# Standard algorithm
python3 src/main.py -a standard

# Bayes algorithm
python3 src/main.py -a bayes
```

To test the performance of the algorithms by running the game 10 times:

```bash
# Standard algorithm
python3 src/main.py -a standard -t 10

# Bayes algorithm
python3 src/main.py -a bayes -t 10
```

## AI Implementation

### Standard

The standard implemetation uses a combination of saved states, process by elimination, and an element of randomness to navigate around the grid.

The implementation can be seen in [game_controller.py](src/controller/game_controller.py) where each of the main functions mirror the suggested functions originally provided in `CWorld` (`choose_action`, `avoid_hazard`, `convert_to_python`).

From a high level, the order of precendence is:
- If **DRONING** is perceived, attempt to convert Filippos by randomly selecting an adjacent square *which has not already been eliminated as a possible Filipppos square*.
- If **BORING** is detected:
    - look first for a guarenteed *safe* adjacent square.
    - else search the history of states for an unexplored safe route.
    - else cross-reference the percept with previous percepts to see if there is a shared coordinate which *could* be a risk, then just avoid it.
- If **no percepts**, select an adjacent square which hasn't yet been explored.
- If none of the above, pick a random adjacent square.

For example, the third sub-option when BORING is perceived uses the state in [grid.py](src/model/grid.py) to determine the possible safe options:

```python
  def safest_options(self, percept: Percept) -> set[tuple[int, int]]:
      """Finds potentially safe squares by comparing previous percepts"""

      options = set()
      for xy in [s for s in self.route if s != self.current.coords]:
          risks = self.current.shared_percepts(self.get_square(*xy), percept)
          if risks:
              potential = [s for s in risks if s not in self.route]
              for s in potential:
                  print(f"Book might be at {s}. ", end="")
                  options.update([o for o in self.current.unexplored if not o == s])
              print(f"Potentially safe options are: {options}")
      return options
```

### Bayes





## Directory Overview

### Model



### View


### Controller

## Directory Wiki

For reference, the following tree outlines the purpose of each folder or file in the project directory:


## References

- https://planning.wiki/ref/pddl
- http://solver.planning.domains
- https://realpython.com/python-virtual-environments-a-primer/


## Repository links
- https://github.com/micahdougall/ai/tree/main/coursework1
