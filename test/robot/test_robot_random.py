from mock import patch
from unittest import TestCase

from robotarena.robot import RobotRandom

class TestRobotRandom(TestCase):
    def __randint_side_effect(self, lower_bound, upper_bound):
        if lower_bound == 0 and upper_bound == 2:
            return 1 # always return "push"
        elif lower_bound == 0 and upper_bound == 3:
            return 2 # always return "S"
        else:
            return -1

    def test_reaction_should_return_empty_action(self):
        name = "any_name"
        robot = RobotRandom(name)
        field = None # any value should do
        robot_location = None # any value should do
        enemy_location = None # any value should do
        with patch('robotarena.robot.robot_random.randint', self.__randint_side_effect):
            reaction = robot.reaction(field, robot_location, enemy_location)
            self.assertEqual("push", reaction.action_type)
            self.assertEqual("S", reaction.direction)
