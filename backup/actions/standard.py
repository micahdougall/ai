import random

from backup.cworld import CWorld


def choose_action(world: CWorld, percept):
    print()
    # TODO: This function needs to take in the precept, and decide what action to do
    # If it sees filippos, it should try to attack with Python, else avoid him
    # If it sees a C book, it should try and avoid it
    # If it pecieves nothing, it should move, ideally rationally
    # You generally want to be returning the other relevant functions here, either avoid_hazard & convert_to_python
    return random.choice(["up", "down", "left", "right"])
    # return action.choose_action(self, percept)