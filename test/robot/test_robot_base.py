from unittest import TestCase

from robotarena.robot import RobotBase

class TestRobotBase(TestCase):
    def test_init_should_assign_name(self):
        name = "any_name"
        robot = RobotBase(name)
        self.assertEqual(name, robot.name)

    def test_reaction_should_return_empty_action(self):
        name = "any_name"
        robot = RobotBase(name)
        field = None # any value should do
        robot_location = None # any value should do
        enemy_location = None # any value should do
        reaction = robot.reaction(field, robot_location, enemy_location)
        self.assertEqual(None, reaction.action_type)
        self.assertEqual(None, reaction.direction)
