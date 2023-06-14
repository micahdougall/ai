# from controller.cworld import CWorld
from view.run import CGame


import sys

from args import GlobalArgs
# import view.run as game
# from lib.cworld import CWorld
from model.grid import Grid
from model.square import Percept
from model.util import printc

from argparse import Namespace
import random


class GameController:

    def __init__(self, student_pos, filippos_pos, degree_pos, textbook_pos, grid_size):
        self.student_pos = student_pos
        self.filippos_pos = filippos_pos
        self.degree_pos = degree_pos
        self.textbook_pos = textbook_pos
        self.grid_size = grid_size

        items_map = {
            self.student_pos: "pikachu_win.png",
            **{c: "C.jpeg" for c in self.textbook_pos},
            self.filippos_pos: "steve.png",
            self.degree_pos: "degree.jpeg"
        }
        self.game = CGame(items_map).play()
        self.grid = Grid(self.grid_size)
        self.options = GlobalArgs.args(None).args

    def choose_action(self, percept):
        """Selects an action based on the current Grid state and percepts"""

        # options = GlobalArgs.args(None)

        for i in range(5):
            self.game.move()
        exit()

        # Update status if on new square
        if self.grid.route.count(self.grid.current.coords):
            if not percept:
                for s in self.grid.current.options:
                    self.grid.safe.add(s)
            else:
                self.grid.update_percepts(percept)
            self.grid.risks.difference_update(self.grid.safe)
        if self.options.debug:
            print(self.grid)

        # Handle percepts
        if self.grid.current.percepts:
            avoidance = self.avoid_hazard()
            if avoidance:
                return avoidance
        else:
            if self.options.debug:
                print("Nothing to see here.")

        # Check for unexplored squares in valid adjacent coordinates
        if self.grid.current.unexplored:
            if self.options.debug:
                printc(f"Unexplored new option from current square.")
            take_a_punt = random.choice(list(self.grid.current.unexplored))
            return self.grid.move_to(self.grid.get_square(*take_a_punt))
        else:
            # Else pick a random safe adjacent square
            if self.options.debug:
                printc("Picking a random, safe square from available options.")
            if not self.grid.current.options:
                printc(
                    "No option possible"
                    f"Route taken: {self.grid.route}"
                    f"Stack: {self.grid.stack}"
                    f"Endpoint: {self.grid.current.coords}"
                )
                exit(-1)
            else:
                move = random.choice(list(self.grid.current.options))
                square = self.grid.get_square(*move)
                return self.grid.move_to(square)


    def avoid_hazard(self) -> str | None:
        """Handles hazards presented by percepts"""

        if Percept.DRONING in self.grid.current.percepts:
            self.convert_to_python()
        else:
            if self.options.debug:
                printc("Yawn...C books detected in the vicinity.")

        # TODO: Handle when 2 boring percepts exist

        # Look for a guaranteed safe option
        safe_options = self.grid.safe & set(self.grid.current.unexplored)
        if safe_options:
            if self.options.debug:
                printc(f"Safe unexplored options exist at: {safe_options}.")
            random_safe = random.choice(list(safe_options))
            return self.grid.move_to(self.grid.get_square(*random_safe))
        # Consider going back a step
        elif len(self.grid.stack) > 1:
            # if not grid.is_path_explored():
            #     # More to discover from last position
            #     printc("Stack not fully explored, moving back.")
            #     return grid.back()
            # elif grid.safe_path():
            # Prefer to look for useful safe and available routes
            if self.grid.safe_path():
                if self.options.debug:
                    printc("Stack has a viable route.")
                return self.grid.back()
            else:
                if self.options.debug:
                    printc("Going back presents no viable route.")
        # else:
        # Compare percepts with previous squares to guesstimate common risks
        if self.options.debug:
            printc(f"No safe options, cross-referencing percepts.")
        possibly_safe = self.grid.safe_options(Percept.BORING)

        if possibly_safe:
            if self.options.debug:
                printc(f"Common percepts found, selecting a possible safe option.")
            random_chance = random.choice(list(possibly_safe))
            return self.grid.move_to(self.grid.get_square(*random_chance))
        else:
            if self.options.debug:
                printc(f"No common percepts found.")
            return None


    def convert_to_python(self) -> tuple[int, int]:
        """Attempts to convert a C stalwart to Python"""

        print(f"\033[93mCompiler noise detected, attempting to convert Filippos...", end="")
        if self.grid.python_books:
            # Guesstimate based on set of possible locations (could be singular!)
            guess = random.choice(list(self.grid.filippos))
            print(f"aiming at {guess}...", end="")
            if guess == self.filippos_pos:
                print(f"\033[92mSuccessfully converted Filippos to a functional programming language!\033[0m\n")
                # world.is_game_over = True
                # Force exit as this isn't otherwise effected
                exit()
            else:
                print(f"\033[91mPointer error! Failed to convert Filippos.\033[0m\n")
                self.grid.filippos.remove(guess)
                # If no book percepts, update failed guess to a safe square
                if len(self.grid.current.percepts) == 1:
                    self.grid.safe.add(guess)
            self.grid.python_books -= 1
        else:
            print(f"\033[91mNo Python book in armoury.\033[0m\n")