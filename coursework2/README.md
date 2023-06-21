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

**NB: The PyGame implementation is in Alpha release, please excuse bugs, lack of commenting etc. Only for interest to show the state of each square.**

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
# `deactivate` to exit env

# install requirements
python3 -m pip install -r requirements.txt
```

## Usage

The program can either be run as a game output (using pygame) or as several iterations to test the performance (pygme output excluded). In either case, an `algorithm` *must* be selected:

- `-a | --algorithm [standard | bayes]` &rArr; **algorithm**: *Selects which algorithm to use for solving the puzzle. Following argument must either be `standard` or `bayes`, **required***.
- `-t [n]` &rArr; **test**: *Used for testing; the program will execute the game `n` times and print the overall win percentage to the console.*
- `-d` &rArr; **debug**: *This will print the results in debug mode, which includes details for the state of the grid at each move along with the reason for the action taken.*
- `-g` &rArr; **game**: *This is a **False** arg which will **prevent** the pygame display from running after the game.* 

**NB: PyGame only runs in normal mode (including debug) but not during testing.**

For example, to enjoy the game in its full glory:

```bash
# Standard algorithm
python3 src/main.py -a standard

# Bayes algorithm
python3 src/main.py -a bayes
```

To test the performance of the algorithms by running the game 1000 times:

```bash
# Standard algorithm
python3 src/main.py -a standard -t 1000

# Bayes algorithm
python3 src/main.py -a bayes -t 1000
```

To skip the PyGame but print all debug statements for each step:

```bash
# Standard algorithm
python3 src/main.py -a standard -d -g
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
      """Finds potentially safe squares by comparing previous percepts.

      Args:
          percept: the percept to be cross-referenced.

      Returns:
          a set of options which are more likely to be safe.

      """
      options = self.current.options.difference(
          self.visited, self.hazards
      )
      for xy in self.visited.difference({self.current.coords}):
          shared = self.current.shared_percepts(
              self.get_square(*xy), 
              percept
          )
          if shared:
              likely = shared.difference(self.all_safe)
              self.logger.log(f"Book might be at one of {likely}. ")
              options.difference_update(likely)
      self.logger.log(f"Potentially safe options are: {options}")
      return options
```

### Bayes

The Bayes implementation uses the same controller to determine the state of the grid along with the same order of precedence for selecting an action. However, rather than choosing a random square from the required set (eg. adjacents, or *unvisited* squares) the program orders each of the candidate squares by ascending order of their combined likelihood of containing a C book or a Filippos, then chooses the least likely.

This is determined in the `set_choice` function in [game_controller.py](src/controller/game_controller.py):

```python
  def set_choice(
          self, options: set[tuple[int, int]], hunt: bool = False
  ) -> tuple[int, int]:
      """
      Selects an option from a list of coordinates based on the algorithm.

      Args:
          options: set of coordinates to choose from
          hunt: whether to choose the highest probability (Bayes only)

      Returns:
          a random coordinate from the set, if algorithm is Standard
          the lowest probability square if algorithm is Bayes (or highest if hunt=True)

      """
      if self.algorithm == Algorithm.STANDARD:
          return random.choice(list(options))
      else:
          ordered = sorted(
              [self.grid.get_square(*s) for s in options],
              key=lambda x: (x.filippos_prob if hunt else x.risk),
              reverse=hunt
          )
          print(f"ordered: {ordered}")
          return ordered[0].coords
```

The Bayes implementation can then be found in [bayes.py](src/model/bayes.py) and the reader will be delighted to hear that the variable names are intuitive:

```python
def bayes_probability(
        prior: float, 
        specificity: float,
        sensitivity: float = 1  # Percept always occurs for positives
) -> float:
    """Calculates the Bayesian probability for a required posterior.

    Args:
        prior: the prior probability.
        specificity: the specificity - true negative rate.
        sensitivity: the sensitivity - true positive rate.

    Returns:
        the new probability (posterior).
    """
    if prior == 0:
        return 0
    else:
        marginalised = (
            sensitivity * prior
            + ((1 - specificity) * (1 - prior))
        )
        return sensitivity * prior / marginalised

```

## Directory Overview


## Directory Wiki

For reference, the following tree outlines the purpose of each folder or file in the project directory:

```python
.
├── README.md
├── requirements.txt
├── resources                   # Images for PyGame
│   ├── c.png
│   ├── degree.png
│   ├── duck.png
│   └── pikachu.png
└── src                         # Application code
    ├── __init__.py
    ├── controller              # Program logic
    │   ├── __init__.py
    │   ├── cworld.py           # Provided CWorld game 
    │   └── game_controller.py  # Controller class
    ├── logger.py               # Handles printing in debug
    ├── main.py                 # Entry point
    ├── model                   # Classes to manage state
    │   ├── __init__.py
    │   ├── bayes.py            # Bayes implementation
    │   ├── enums.py
    │   ├── grid.py
    │   └── square.py
    └── view                    # PyGame program
        ├── __init__.py
        ├── player.py
        ├── pygrid.py
        └── run.py
```
