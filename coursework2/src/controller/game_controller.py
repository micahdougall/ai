import random
# from enum import Enum
from typing import Any

# from args import GlobalArgs
from model.enums import Algorithm
from model.grid import Grid
from model.square import Percept, State
from view.run import CGame



class GameController:

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
        # self.is_game_over = False
        self.grid = Grid(grid_size, 4)
        self.debug = False
        self.algorithm = Algorithm.STANDARD
        self.win = False
        self.states = []

    def choose_action(self, percept: str) -> str:
        """Selects an action based on the current Grid state and percepts"""

        self.log("\nChoose action...", warn=True, force=True)

        self.grid.update_states(percept)
        # Update status if on new square
        # if self.grid.route.count(self.grid.current.coords):
        # current = self.grid.current

        # if not current.state == State.VISITED:
        #     current.state = State.VISITED
        #     if not percept:
        #         print(f"No percept, updating adjacents as safe")
        #         for s in current.options:
        #             # self.grid.safe.add(s)
        #             self.grid.get_square(*s).state = State.SAFE
        #     else:
        #         self.grid.update_percepts(percept)
        #         # TODO: Move this down
        if self.algorithm == Algorithm.BAYES:
            self.log("Updating probabilities", warn=True, force=True)
            self.grid.update_probabilities()
            # self.grid.risks.difference_update(self.grid.safe)

        # Print grid after update if in debug mode
        self.log(self.grid)
        for s in self.grid.squares:
            self.log(s)

        # Strategy for percepts
        current = self.grid.current

        if current.percepts:
            avoidance = self.avoid_hazard()
            if avoidance:
                return avoidance
        else:
            self.log("Nothing to see here.")

        # Check for unexplored squares in valid adjacent coordinates
        unexplored = self.grid.unknown.intersection(
            current.options
        )
        if unexplored:
            self.log(f"Unexplored new option from current square.", warn=True)
            # take_a_punt = random.choice(
            #     list(current.unexplored)
            # )
            return self.move_to(
                random.choice(list(unexplored))
            )
        else:
            # Else pick a random safe adjacent square
            self.log("Picking a random, safe square from available options.", warn=True)
            safe = self.grid.safe.intersection(
                current.options
            )
            if safe:
                # move = random.choice(
                #     list(current.options)
                # )
                # return self.move_to(move)
                return self.move_to(
                    random.choice(list(safe))
                )
            else:
                self.log(
                    "No option possible"
                    # f"Route taken: {self.grid.route}"
                    f"Stack: {self.grid.stack}"
                    f"Endpoint: {current.coords}",
                    warn=True
                )
                exit(-1)

    def avoid_hazard(self) -> str | None:
        """Handles hazards presented by percepts"""

        if Percept.DRONING in self.grid.current.percepts:
            self.convert_to_python()
            if self.win:
                # self.win = True
                return "C is dead!"
        else:
            self.log("Yawn...C books detected in the vicinity.", warn=True)

        # TODO: Handle when 2 boring percepts exist

        # Look for a guaranteed safe option
        # safe_unexplored = self.grid.safe & set(self.grid.current.unexplored)
        safe_unexplored = self.grid.safe.intersection(
            self.grid.current.options
        )
        # print(f"From {self.grid.current.coords}, safe are {self.grid.safe}")
        # print(f"From {self.grid.current.coords}, unexplored are {self.grid.current.unexplored}")
        if safe_unexplored:
            self.log(
                f"Safe unexplored options exist at: {safe_unexplored}.", 
                warn=True, force=True
            )
            # random_safe = random.choice(list(safe_unexplored))
            return self.move_to(
                random.choice(list(safe_unexplored))
            )

        # If nothing is safe, consider going back a step
        elif len(self.grid.stack) > 1:
            if self.grid.safe_unexplored_path():
                self.log("Stack has a viable route.", warn=True)
                self.add_states()
                return self.grid.back()
            else:
                self.log("Going back presents no viable route.", warn=True)
            # if not grid.is_path_explored():
            #     # More to discover from last position
            #     self.log("Stack not fully explored, moving back.", warn=True)
            #     return grid.back()
            # elif grid.safe_path():
            # Prefer to look for useful safe and available routes
            # if self.grid.safe_path():
            #     self.log("Stack has a viable route.", warn=True)
            #     return self.grid.back()
            # else:
            #     self.log("Going back presents no viable route.", warn=True)

            # Compare percepts with previous squares to guesstimate common risks
            self.log(f"No safe options, cross-referencing percepts.", warn=True)
            possibly_safe = self.grid.safest_options(Percept.BORING)

            if possibly_safe:
                self.log(
                    f"Common percepts found, selecting a possible safe option.", warn=True
                )
                # chance_it = random.choice(list(possibly_safe))
                return self.move_to(
                    random.choice(list(possibly_safe))
                )
            else:
                self.log(f"No common percepts found.", warn=True)
        return None

    def convert_to_python(self) -> tuple[int, int]:
        """Attempts to convert a C stalwart to Python"""

        print(f"\033[93mCompiler noise detected, attempting to convert Filippos...", end="")
        if self.grid.python_books:
            # Guesstimate based on set of possible locations (could be singular!)
            guess = random.choice(
                list(self.grid.filippos)
            )
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
                    # self.grid.safe.add(guess)
            self.grid.python_books -= 1
        else:
            print(f"\033[91mNo Python book in armoury.\033[0m\n")

    def move_to(self, to_coords: tuple[int, int]) -> str:
        """Updates state before moving to a new square"""

        # self.log(f"Updated controller state: {self.states}")
        self.add_states()
        return self.grid.move_to(to_coords)

    def add_states(self) -> None:
        self.states.append({
            "coords": self.grid.current.coords,
            # "risks": self.grid.risks.copy(),
            "safe": self.grid.safe.copy()
        })

    def pygame(self) -> None:
        items_map = {
            self.student_pos: "pikachu_win.png",
            **{c: "C.jpeg" for c in self.textbook_pos},
            self.filippos_pos: "steve.png",
            self.degree_pos: "degree.jpeg"
        }
        CGame(items_map).play(self.grid.route, self.states)

    def log(self, text: Any, warn: bool = False, force: bool = False) -> None:
        if self.debug or force:
            print(text) if not warn else print(f"\033[93m{text}\033[0m")
