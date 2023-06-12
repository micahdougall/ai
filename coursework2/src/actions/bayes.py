from src.lib.cworld import CWorld
from src.model.grid import Grid
from src.model.square import Percept
from src.model.util import printc

import random


def choose_action(world: CWorld, percept):
    """Selects an action based on the current Grid state and percepts"""
#
#     grid = Grid.grid(world.size)
#
#     # Update status if on new square
#     if grid.route.count(grid.current.coords):
#         if not percept:
#             for s in grid.current.options:
#                 grid.safe.add(s)
#         else:
#             grid.update_percepts(percept)
#         grid.risks.difference_update(grid.safe)
#     print(grid)
#
#     # Handle percepts
#     if grid.current.percepts:
#         avoidance = avoid_hazard(world, grid)
#         if avoidance:
#             return avoidance
#     else:
#         printc("Nothing to see here.")
#
#     # Check for unexplored squares in valid adjacent coordinates
#     if grid.current.unexplored:
#         printc(f"Unexplored new option from current square.")
#         take_a_punt = random.choice(list(grid.current.unexplored))
#         return grid.move_to(grid.get_square(*take_a_punt))
#     else:
#         # Else pick a random safe adjacent square
#         printc("Picking a random, safe square from available options.")
#         if not grid.current.options:
#             printc(
#                 "No option possible"
#                 f"Route taken: {grid.route}"
#                 f"Stack: {grid.stack}"
#                 f"Endpoint: {grid.current.coords}"
#             )
#             exit(-1)
#         else:
#             move = random.choice(list(grid.current.options))
#             square = grid.get_square(*move)
#             return grid.move_to(square)
#
#
# def avoid_hazard(world: CWorld, grid: Grid) -> str | None:
#     """Handles hazards presented by percepts"""
#
#     if Percept.DRONING in grid.current.percepts:
#         convert_to_python(world, grid)
#     else:
#         printc("Yawn...C books detected in the vicinity.")
#
#     # Look for a guaranteed safe option
#     safe_options = grid.safe & set(grid.current.unexplored)
#     if safe_options:
#         printc(f"Safe unexplored options exist at: {safe_options}.")
#         random_safe = random.choice(list(safe_options))
#         return grid.move_to(grid.get_square(*random_safe))
#     # Consider going back a step
#     elif len(grid.stack) > 1:
#         # if not grid.is_path_explored():
#         #     # More to discover from last position
#         #     printc("Stack not fully explored, moving back.")
#         #     return grid.back()
#         # elif grid.safe_path():
#         # Prefer to look for useful safe and available routes
#         if grid.safe_path():
#             printc("Stack has a viable route.")
#             return grid.back()
#         else:
#             printc("Going back presents no viable route.")
#     # else:
#     # Compare percepts with previous squares to guesstimate common risks
#     printc(f"No safe options, cross-referencing percepts.")
#     possibly_safe = grid.safe_options(Percept.BORING)
#
#     if possibly_safe:
#         printc(f"Common percepts found, selecting a possible safe option.")
#         random_chance = random.choice(list(possibly_safe))
#         return grid.move_to(grid.get_square(*random_chance))
#     else:
#         printc(f"No common percepts found.")
#         return None
#
#
# def convert_to_python(world: CWorld, grid: Grid) -> tuple[int, int]:
#     """Attempts to convert a C stalwart to Python"""
#
#     print(f"\033[93mCompiler noise detected, attempting to convert Filippos...", end="")
#     if grid.python_books:
#         # Guesstimate based on set of possible locations (could be singular!)
#         guess = random.choice(list(grid.filippos))
#         print(f"aiming at {guess}...", end="")
#         if guess == world.filippos_pos:
#             print(f"\033[92mSuccessfully converted Filippos to a functional programming language!\033[0m\n")
#             world.is_game_over = True
#             # Force exit as this isn't otherwise effected
#             exit()
#         else:
#             print(f"\033[91mPointer error! Failed to convert Filippos.\033[0m\n")
#             grid.filippos.remove(guess)
#             # If no book percepts, update failed guess to a safe square
#             if len(grid.current.percepts) == 1:
#                 grid.safe.add(guess)
#         grid.python_books -= 1
#     else:
#         print(f"\033[91mNo Python book in armoury.\033[0m\n")