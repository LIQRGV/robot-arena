from unittest import TestCase

from robotarena import Action

class TestAction(TestCase):
    def test_init_should_assign_action_and_direction(self):
        action_type = "some_action"
        direction = "some_direction"
        action = Action(action_type, direction)
        self.assertEqual(action_type, action.action_type)
        self.assertEqual(direction, action.direction)

