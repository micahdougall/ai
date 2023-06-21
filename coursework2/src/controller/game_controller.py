from logger import Logger
from model.enums import Algorithm
from model.grid import Grid
from model.square import Percept, State
from view.run import CGame

import random


class GameController:
    """Class to manage the decision logic for a CWorld game"""

    def __init__(
            self,
            student_pos,
            filippos_pos,
            degree_pos,
            textbook_pos,
            grid_size
    ):
        self.student_pos = student_pos
        self.filippos_pos = filippos_pos
        self.degree_pos = degree_pos
        self.textbook_pos = textbook_pos
        self.grid = Grid(grid_size, 4)
        self.debug = False
        self.algorithm = Algorithm.STANDARD
        self.win = False
        self.states = []
        self.logger: Logger = Logger.logger()

    def choose_action(self, percepts: list[str]) -> str:
        """Selects an action based on the current Grid state and percepts

        Args:
            percepts: list of percepts as received from CWorld.

        Returns:
            a string representation of the move chosen.
        """

        self.logger.log("\nChoosing action...", warn=True, force=True)

        # Check route length in case impossible grid with blocked in F and D
        # leads to an endless search. Counts as a loss in the GameController state.
        if len(self.states) >= 50:
            return "C is dead!"

        # Update states prior to action decision
        self.grid.update_states(percepts)
        if self.algorithm == Algorithm.BAYES:
            self.logger.log("Updating probabilities", warn=True, force=True)
            self.grid.update_probabilities()

        # Print grid after update if in debug mode
        self.logger.log(self.grid)

        # Strategy for percepts
        current = self.grid.current
        if current.percepts:
            avoidance = self.avoid_hazard()
            if avoidance:
                self._add_states()
                return avoidance

        # First look for safe, unvisited options in adjacent squares
        safe_new = self.grid.safe.intersection(
            current.options
        )
        if safe_new:
            self.logger.log(f"Safe new option from current square.", warn=True)
            return self.move_to(
                self.set_choice(safe_new)
            )

        # Play safe from known visited/safe squares
        self.logger.log("Picking a random, safe square from available options.", warn=True)
        viable = current.options.intersection(
            self.grid.viable
        )
        if viable:
            return self.move_to(
                self.set_choice(viable)
            )

        # Must take a risk
        risks = self.grid.current.options.intersection(
            self.grid.risks
        )
        if risks:
            self.logger.log("No safe option, choosing a risky square.", warn=True)
            return self.move_to(
                self.set_choice(risks)
            )
        else:
            self.logger.log("No option possible, must be blocked in...about to self-combust!", warn=True)
            return self.move_to(
                self.set_choice(current.options)
            )

    def avoid_hazard(self) -> str | None:
        """Handles hazards presented by percepts from the agent.

        Returns:
            a string representation of the move chosen.
        """

        if Percept.DRONING in self.grid.current.percepts:
            self.convert_to_python()
            if self.win:
                return "C is dead!"
        else:
            self.logger.log("Yawn...C books detected in the vicinity.", warn=True)

        # Look for a guaranteed safe option
        safe_unexplored = self.grid.safe.intersection(
            self.grid.current.options
        )
        if safe_unexplored:
            self.logger.log(
                f"Safe unexplored options exist at: {safe_unexplored}.", 
                warn=True, force=True
            )
            return self.move_to(
                self.set_choice(safe_unexplored)
            )

        # If nothing is safe, consider going back a step
        elif len(self.grid.stack) > 1:
            if self.grid.safe_unexplored_path():
                self.logger.log("Stack has a viable route.", warn=True)
                self._add_states()
                return self.grid.back()
            else:
                self.logger.log("Going back presents no viable route.", warn=True)

            # Compare percepts with previous squares to guesstimate common risks
            self.logger.log(f"No safe options, cross-referencing percepts.", warn=True)
            possibly_safe = self.grid.safest_options(Percept.BORING)

            if possibly_safe:
                self.logger.log(
                    f"Common percepts found, selecting a possible safe option.", warn=True
                )
                return self.move_to(
                    self.set_choice(possibly_safe)
                )
            else:
                self.logger.log(f"No common percepts found.", warn=True)
        return None

    def convert_to_python(self) -> None:
        """Attempts to convert a C stalwart to Python"""

        print(f"\033[93mCompiler noise detected, attempting to convert Filippos...", end="")
        if self.grid.python_books:
            guess = self.set_choice(self.grid.filippos, hunt=True)
            print(f"aiming at {guess}...", end="")
            if guess == self.filippos_pos:
                print(f"\033[92mSuccessfully converted Filippos to a functional programming language!\033[0m\n")
                self.win = True
            else:
                print(f"\033[91mPointer error! Failed to convert Filippos.\033[0m\n")
                self.grid.filippos.remove(guess)

                # If no book percepts, update failed guess to a safe square
                if len(self.grid.current.percepts) == 1:
                    self.grid.get_square(*guess).state = State.SAFE
            self.grid.python_books -= 1
        else:
            self.logger.log("no Python book in armoury.", warn=True, force=True)

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

    def move_to(self, to_coords: tuple[int, int]) -> str:
        """Updates state before moving to a new square

        Args:
            to_coords: coordinates to move to.

        Returns:
            the string value for the move direction required.
        """

        self._add_states()
        return self.grid.move_to(to_coords)

    def _add_states(self) -> None:
        """Adds states to state history for game interface"""

        self.states.append({
            "coords": self.grid.current.coords,
            "visited": self.grid.visited.copy(),
            "safe": self.grid.safe.copy(),
            "risks": self.grid.risks.copy(),
            "books": self.grid.books.copy()
        })

    def pygame(self, resources: str) -> None:
        """Starts a PyGame representation of the game played

        Args:
            resources: full filepath for resources folder.
        """

        if len(self.states) >= 50:
            self.logger.log("Unsolvable game with long route detected, skipping PyGame output.")
        else:
            items_map = {
                self.student_pos: f"{resources}/pikachu.png",
                **{c: f"{resources}/c.png" for c in self.textbook_pos},
                self.filippos_pos: f"{resources}/duck.png",
                self.degree_pos: f"{resources}/degree.png"
            }
            CGame(items_map).play(self.states)
