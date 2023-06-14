from controller.grid_controller import GameController
from model.util import printc


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
        self.controller = GameController(
            self.student_pos, self.filippos_pos, self.degree_pos, self.textbook_pos, size
        )

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
            print("Percept:", percept)
            action = self.choose_action(percept)
            self.move_student(action)

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def choose_action(self, percept):
        self.controller.choose_action(percept)

        # from args import GlobalArgs
        # import actions.standard as standard
        #
        # options = GlobalArgs.args(None)
        # if options.args.algorithm == "standard":
        #     return standard.choose_action(self, percept)
        # else:
        #     print("Awaiting Bayesian implementation.")
