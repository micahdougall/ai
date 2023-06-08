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
            print("Student moves up.")
        elif action == "down" and x < self.size - 1:
            self.student_pos = (x + 1, y)
            print("Student moves down.")
        elif action == "left" and y > 0:
            self.student_pos = (x, y - 1)
            print("Student moves left.")
        elif action == "right" and y < self.size - 1:
            self.student_pos = (x, y + 1)
            print("Student moves right.")

        if self.student_pos == self.filippos_pos or self.student_pos in self.textbook_pos:
            self.is_game_over = True
            print("Student is either affected by Filippos's Droning or has succumb to the Boring C textbooks!")

        if self.student_pos == self.degree_pos:
            self.is_game_over = True
            print("Student found the first-class degree and wins!")

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
            print("Percept:", percept)
            action = self.choose_action(percept)
            self.move_student(action)

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def choose_action(self, percept):
        # TODO: This function needs to take in the precept, and decide what action to do
        print(f"Percept -> {percept}")
        # print(f"Percept History -> {self.percept_history}")
        # GridModel.map[self.student_pos] = percept
        # print(f"GridModel Map -> {GridModel.map}")

        # all_moves = moves_coords_map(*self.student_pos, self.size)
        # print(f"All Moves: {all_moves}")

        # options = {k: v for (k, v) in all_moves.items() if v}
        # print(f"Options: {options}")

        # Think about things in terms of a tree with A* search

        # TODO: If percept is Filippos, add Python step
        from coursework2.src.model.grid import Grid
        grid = Grid.grid(self.size)

        if percept and len(grid.stack):
        # if percept and GridModel.last_move and not GridModel.returned:
            print("There is a percept")
            # back = opposite(GridModel.last_move)
            # last_square = moves_coords_map(*self.student_pos, self.size).get(back)

            # if not is_explored(*last_square, self.size):
            if not grid.stack[-1].is_explored():
                # More to discover from last position
                print("Last square not fully discovered")
                # GridModel.last_move = back
                # GridModel.returned = True
                return grid.back()
                # return back

        # TODO: Add step to compare percepts

        # for move, square in options.items():
        for square in grid.current.options:
            # if square not in GridModel.map.keys():
            if square not in grid.route:

                # New square to discover
                print("New square found")
                # GridModel.last_move = move
                # GridModel.returned = False
                # return move
                return grid.move_to(square)
        # else:

        # If it sees filippos, it should try to attack with Python, else avoid him
        # If it sees a C book, it should try and avoid it
        # If it pecieves nothing, it should move, ideally rationally
        # You generally want to be returning the other relevant functions here, either avoid_hazard & convert_to_python

        # move = random.choice(["up", "down", "left", "right"])
        # GridModel.last_move = move
        # GridModel.returned = False
        move = random.choice(grid.current.options)
        return grid.move_to(move)
        # return move.di
        # return action.choose_action(self, percept)



    def avoid_hazard(self):
        # TODO: This function is for dealing with avoiding either Filippos or C books
        # It is up to you to decide how you want to deal with the current precept sequence, but the result should be some level of movement
        return random.choice(["up", "down", "left", "right"])

    def convert_to_python(self):
        # TODO: This function is for attempting to convert filippos to C
        # Here you should be using the python book to convert Filippos, by checking where he is and using the relevant action
        return random.choice(["up", "down", "left", "right"])

#
# def is_explored(x: int, y: int, grid_size) -> bool:
#     moves = moves_coords_map(x, y, grid_size)
#     possible = {k: v for (k, v) in moves.items() if v}
#
#     unexplored = {k: v for (k, v) in possible.items() if v not in GridModel.map.keys()}
#     print(f"Unexplored coords: {unexplored}")
#     return False if len(unexplored) else True
#
#
# def moves_coords_map(x: int, y: int, grid_size) -> dict:
#     return {
#         "up": (x - 1, y) if x > 0 else None,
#         "down": (x + 1, y) if x < grid_size - 1 else None,
#         "left": (x, y - 1) if y > 0 else None,
#         "right": (x, y + 1) if y < grid_size - 1 else None,
#     }
#
#
# def opposite(move: str) -> str:
#     return {
#         "up": "down",
#         "down": "up",
#         "left": "right",
#         "right": "left",
#     }.get(move)
#
#
# class GridModel:
#     returned: bool = False
#     last_move: str = None
#     map: dict[tuple, str] = {}

if __name__ == "__main__":
    game = CWorld()
    # game.print_state()
    game.play()
    # game.print_state()
