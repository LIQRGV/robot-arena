from .robot_base import RobotBase

from ..coordinate import Coordinate
from ..action import Action

from random import randint

class RobotRandom(RobotBase):
    # this should return object `Action`
    def reaction(self, field, self_location, enemy_location):
        random_action = randint(0,2)
        random_direction = randint(0,3)
        actions = ["move", "push", "defend"]
        directions = ["N","E","S","W"]
        return Action(actions[random_action], directions[random_direction])

