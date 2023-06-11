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
            # else:
            initial_map_printed = False
            percept = self.get_percept()
            print("Percept:", percept)
            action = self.choose_action(percept)
            self.move_student(action)

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def choose_action(self, percept):
        # If it sees filippos, it should try to attack with Python, else avoid him
        # If it sees a C book, it should try and avoid it
        # If it pecieves nothing, it should move, ideally rationally
        # You generally want to be returning the other relevant functions here, either avoid_hazard & convert_to_python
        from coursework2.src.model.grid import Grid
        from coursework2.src.model.square import Percept
        grid = Grid.grid(self.size)

        # Update states
        if not percept:
            for s in grid.current.options:
                grid.safe.add(s)
        else:
            grid.update_percepts(percept)
            print(f"Risks: {grid.risks}")
            print(f"Filippos: {grid.filippos}")
        grid.risks.difference_update(grid.safe)


        # if percept:
        if grid.current.percepts:
            # self.avoid_hazard(percepts)
            # grid.current.percepts = percept
            # print(f"Current: {grid.current}")
            # grid.risks.update([r for r in grid.current.options if r not in grid.safe])
            if Percept.DRONING in grid.current.percepts:
                # attempted = self.convert_to_python()
                self.convert_to_python()

                # Safe options may have been made

            # if "Boring" not in percept:
            #     printc(f"Safe option at {attempted}.")
            #     square = grid.get_square(*attempted)
            #     return grid.move_to(square)

            # if Percept.BORING in grid.current.percepts:
            # if "Boring" in percept:
            #     printc("Yawn...C books detected in the vicinity.")

            safe_options = grid.safe & set(grid.current.unknowns)

            if safe_options:
                printc(f"Safe unexplored options exist at: {safe_options}.")
                random_safe = random.choice(list(safe_options))
                return grid.move_to(grid.get_square(*random_safe))

            # Compare percepts with previous squares to guesstimate common risks
            printc(f"No safe options, cross-referencing percepts.")
            possibly_safe = grid.safe_options(Percept.BORING)

            if possibly_safe:
                printc(f"Common percepts found, selecting a possible safe option.")
                random_chance = random.choice(list(possibly_safe))
                return grid.move_to(grid.get_square(*random_chance))
            else:
                printc(f"No common percepts found.")

                # for s in possibly_safe:
                #     print(f"Attempting safe move to: {s}")
                #     square = grid.get_square(*s)
                #     return grid.move_to(square)


                    #
                    #
                    # for s in grid.current.unknowns:
                    #     if s in grid.safe:
                    #         printc(f"Safe unexplored option exists as {s}.")
                    #         square = grid.get_square(*s)
                    #         return grid.move_to(square)

                    # if not grid.safe_option("Boring"):
                    # possibly_safe = grid.safe_options("Boring")

                    # if possibly_safe:
                    #     square = grid.get_square(*probably_safe)
                    #     return grid.move_to(square)

                    # for s in possibly_safe:
                    #     print(f"Attempting safe move to: {s}")
                    #     square = grid.get_square(*s)
                    #     return grid.move_to(square)

                    # for xy in grid.route:
                    #     # if grid.current.is_diagonal(*xy):
                    #     risks = grid.current.shared_percepts(grid.get_square(*xy), "Boring")
                    #     # shared = grid.current.shared_adjacents(grid.get_square(*xy))
                    #     print(f"Shared risk squares with {xy} = {risks}")
                    #     if risks:
                    #         potential = [s for s in risks if s not in grid.route]
                    #         print(f"Potential = {potential}")
                    #         if potential:
                    #             print("potential exists")
                    #         if len(potential):
                    #             print("potential has length")
                    #             printc(f"Detected a book at one of: {potential}.")
                    #         for s in potential:
                    #             print(f"s: {s}")
                    #             print(f"type s: {type(s)}")
                    #             square = grid.get_square(*s)
                    #             # print(f"square: {square}")
                    #             # if "Boring" in grid.get_square(*s).percepts:
                    #             printc(f"Book might be at {s}.")
                    #             # TODO: Convert this to safe list
                    #             grid.current.unknowns.remove(s)

                    # else:
                        # TODO: Where does this go now?
            if len(grid.stack) > 1:
                previous = grid.get_square(*grid.stack[-2])
                # print(f"Previous: {previous}")

                # TODO: This isn't right
                if not grid.is_path_explored():
                    # More to discover from last position
                    printc("Stack not fully explored, moving back.")
                    return grid.back()
                # elif:
                #     if not previous.is_explored() and not previous.percepts:
                #     printc("Last square not fully discovered, moving back.")
                else:
                    printc("Going back leads to a risky square.")

            # No options except in stack
            if not grid.current.unknowns:
                printc("No other options from here, moving back.")
                return grid.back()

        # Check for unexplored squares in valid adjacent coordinates
        # TODO: Make this random
        else:
            printc("Nothing to see here, marching on.")
        for coords in grid.current.unknowns:
            if coords not in grid.route:
                # New square to discover
                square = grid.get_square(*coords)
                return grid.move_to(square)

        # TODO: Could be potentially safe options back at previous route

        # Else pick a random valid adjacent square
        printc("Picking a random option from available options.")
        move = random.choice(grid.current.options)
        square = grid.get_square(*move)
        return grid.move_to(square)

    # TODO: This will go in solution file
    # from coursework2.src.model.square import Percept
    # def avoid_hazard(self, percepts: list[Percept]):
    #     from coursework2.src.model.grid import Grid
    #     from coursework2.src.model.square import Percept
    #
    #     grid = Grid.grid(self.size)
    #
    #     if Percept.DRONING in percepts:
    #         attempted = self.convert_to_python()
    #         # If st
    #
    #
    #         if "Boring" not in percept:
    #             printc(f"Safe option at {attempted}.")
    #             square = grid.get_square(*attempted)
    #             return grid.move_to(square)
    #
    #     if "Boring" in percept:
    #         printc("Yawn...C books detected in the vicinity.")
    #
    #         for s in grid.current.unknowns:
    #             if s in grid.safe:
    #                 printc(f"Safe unexplored option exists as {s}.")
    #                 square = grid.get_square(*s)
    #                 return grid.move_to(square)
    #
    #         # if not grid.safe_option("Boring"):
    #         possibly_safe = grid.safe_options("Boring")
    #
    #         # if possibly_safe:
    #         #     square = grid.get_square(*probably_safe)
    #         #     return grid.move_to(square)
    #
    #         for s in possibly_safe:
    #             print(f"Attempting safe move to: {s}")
    #             square = grid.get_square(*s)
    #             return grid.move_to(square)

    def convert_to_python(self) -> tuple[int, int]:
        from coursework2.src.model.grid import Grid
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
                # elif:
                #     len(grid.current.percepts) ==
                # return guess
            grid.python_books -= 1
        else:
            print(f"\033[91mNo Python book in armoury.\033[0m\n")


def printc(text: str):
    print(f"\033[93m{text}\033[0m\n")


if __name__ == "__main__":
    game = CWorld()
    game.play()
