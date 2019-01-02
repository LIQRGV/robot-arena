from .Coordinate import Coordinate
from .Action import Action

from random import randint

class Robot:
    def __init__(self, name):
        self.name = name

    # this should return object `Action`
    def reaction(self, field, enemy_location):
        random_action = randint(0,2)
        random_direction = randint(0,3)
        actions = ["move", "push", "defend"]
        directions = ["N","E","S","W"]
        return Action(actions[random_action], directions[random_direction])


