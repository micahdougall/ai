import itertools


def coors():
    # coords = itertools.product(range(4), repeat=2)
    print("Hello")
    coords = ((x, y) for x in range(4) for y in range(4))
    for c in coords:
        print(c)
    test = [
        # Square(*xy, self.grid_size) for xy in coords
        (x, y)
        for x in range(4)
        for y in range(4)
    ]
    print(test)
    for t in test:
        print(t)

# def map_moves(self, grid_size: int) -> dict:
#     return {
#         "up": (self.x - 1, self.y) if self.x > 0 else None,
#         "down": (self.x + 1, self.y) if self.x < grid_size - 1 else None,
#         "left": (self.x, self.y - 1) if self.y > 0 else None,
#         "right": (self.x, self.y + 1) if self.y < grid_size - 1 else None,
#     }

if __name__ == '__main__':
    coors()
