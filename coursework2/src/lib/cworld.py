from src.model.grid import Grid
from src.model.square import Percept
from src.model.util import printc

import random


class CWorld:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.student_pos = (0, 0)
        self.textbook_pos = [self.generate_random_position() for _ in range(size)]
        self.filippos_pos = self.generate_random_position(self.textbook_pos)
        self.degree_pos = self.generate_random_position(self.textbook_pos + [self.filippos_pos])
        self.is_game_over = False
        self.student_map = [['?' for _ in range(size)] for _ in range(size)]
        self.textbook_available = True
        self.percept_history = []

    def generate_random_position(self, exclude_positions=[]):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if (x, y) not in exclude_positions and (x, y) != (0, 0):
                return x, y

    def get_percept(self):
        percept = []
        x, y = self.student_pos

        adjacent_squares = [
            (x-1, y), (x+1, y), (x, y-1), (x, y+1)
        ]

        for square in adjacent_squares:
            if square == self.filippos_pos:
                percept.append("Droning")
            if square in self.textbook_pos:
                percept.append("Boring")

        if self.degree_pos == (x, y):
            percept.append("Success")

        return percept

    def move_student(self, action):
        x, y = self.student_pos
        if action == "up" and x > 0:
            self.student_pos = (x - 1, y)
            printc("Student moves up.")
        elif action == "down" and x < self.size - 1:
            self.student_pos = (x + 1, y)
            printc("Student moves down.")
        elif action == "left" and y > 0:
            self.student_pos = (x, y - 1)
            printc("Student moves left.")
        elif action == "right" and y < self.size - 1:
            self.student_pos = (x, y + 1)
            printc("Student moves right.")

        if self.student_pos == self.filippos_pos or self.student_pos in self.textbook_pos:
            self.is_game_over = True
            printc("Student is either affected by Filippos's Droning or has succumb to the Boring C textbooks!")

        if self.student_pos == self.degree_pos:
            self.is_game_over = True
            printc("Student found the first-class degree and wins!")

        self.update_student_map(action)

        self.percept_history.append(self.get_percept())

    def update_student_map(self, action):
        x, y = self.student_pos
        self.student_map[x][y] = '-'

        if action == "up" and x > 0:
            self.student_map[x - 1][y] = '?'
        elif action == "down" and x < self.size - 1:
            self.student_map[x + 1][y] = '?'
        elif action == "left" and y > 0:
            self.student_map[x][y - 1] = '?'
        elif action == "right" and y < self.size - 1:
            self.student_map[x][y + 1] = '?'

    def print_state(self):
        for i in range(self.size):
            print(self.grid[i], "\t", self.student_map[i])

    def show_initial_grid(self):
        self.grid[self.student_pos[0]][self.student_pos[1]] = 'S'
        self.grid[self.filippos_pos[0]][self.filippos_pos[1]] = 'F'
        self.grid[self.degree_pos[0]][self.degree_pos[1]] = 'D'
        for textbook in self.textbook_pos:
            self.grid[textbook[0]][textbook[1]] = 'C'

    def play(self):
        self.show_initial_grid()
        initial_map_printed = True
        while not self.is_game_over:
            if initial_map_printed:
                self.print_state()
            else:
                initial_map_printed = True
            percept = self.get_percept()
            # print("Percept:", percept)
            action = self.choose_action(percept)
            self.move_student(action)

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def choose_action(self, percept):
        """Selects an action based on the current Grid state and percepts"""

        grid = Grid.grid(self.size)

        # Update states
        if not percept:
            for s in grid.current.options:
                grid.safe.add(s)
        else:
            grid.update_percepts(percept)
        grid.risks.difference_update(grid.safe)
        print(grid)

        # Handle percepts
        if grid.current.percepts:
            avoidance = self.avoid_hazard()
            if avoidance:
                return avoidance
        else:
            printc("Nothing to see here.")

        # Check for unexplored squares in valid adjacent coordinates
        if grid.current.unexplored:
            printc(f"Unexplored new option from current square.")
            take_a_punt = random.choice(list(grid.current.unexplored))
            return grid.move_to(grid.get_square(*take_a_punt))
        else:
            # Else pick a random safe adjacent square
            printc("Picking a random, safe square from available options.")
            if not grid.current.options:
                printc(
                    "No option possible"
                    f"Route taken: {grid.route}"
                    f"Stack: {grid.stack}"
                    f"Endpoint: {grid.current.coords}"
                )
                exit(-1)
            else:
                move = random.choice(list(grid.current.options))
                square = grid.get_square(*move)
                return grid.move_to(square)

    def avoid_hazard(self) -> str | None:
        """Handles hazards presented by percepts"""

        grid = Grid.grid(self.size)

        if Percept.DRONING in grid.current.percepts:
            self.convert_to_python()
        else:
            printc("Yawn...C books detected in the vicinity.")

        # Look for a guaranteed safe option
        safe_options = grid.safe & set(grid.current.unexplored)
        if safe_options:
            printc(f"Safe unexplored options exist at: {safe_options}.")
            random_safe = random.choice(list(safe_options))
            return grid.move_to(grid.get_square(*random_safe))
        # Consider going back a step
        elif len(grid.stack) > 1:
            if not grid.is_path_explored():
                # More to discover from last position
                printc("Stack not fully explored, moving back.")
                return grid.back()
            elif grid.safe_path():
                printc("Stack has a viable route.")
                return grid.back()
            else:
                print(
                    f"Options: {grid.current.options}"
                    f"Unknowns: {grid.current.unexplored}"
                )
                printc("Going back presents no viable route.")
        else:
            # Compare percepts with previous squares to guesstimate common risks
            printc(f"No safe options, cross-referencing percepts.")
            possibly_safe = grid.safe_options(Percept.BORING)

            if possibly_safe:
                printc(f"Common percepts found, selecting a possible safe option.")
                random_chance = random.choice(list(possibly_safe))
                return grid.move_to(grid.get_square(*random_chance))
            else:
                printc(f"No common percepts found.")
                return None

    def convert_to_python(self) -> tuple[int, int]:
        """Attempts to convert a C stalwart to Python"""

        from src.model.grid import Grid
        grid = Grid.grid(self.size)

        print(f"\033[93mCompiler noise detected, attempting to convert Filippos...", end="")
        if grid.python_books:
            # Guesstimate based on set of possible locations (could be singular!)
            guess = random.choice(list(grid.filippos))
            print(f"aiming at {guess}...", end="")
            if guess == self.filippos_pos:
                print(f"\033[92mSuccessfully converted Filippos to a functional programming language!\033[0m\n")
                self.is_game_over = True
                # Force exit as this isn't otherwise effected
                exit()
            else:
                print(f"\033[91mPointer error! Failed to convert Filippos.\033[0m\n")
                grid.filippos.remove(guess)
                # If no book percepts, update failed guess to a safe square
                if len(grid.current.percepts) == 1:
                    grid.safe.add(guess)
            grid.python_books -= 1
        else:
            print(f"\033[91mNo Python book in armoury.\033[0m\n")
