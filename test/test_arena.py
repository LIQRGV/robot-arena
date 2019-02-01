from unittest import TestCase
from unittest.mock import (
    Mock,
    patch
)

from robotarena import (
    Action,
    Arena,
    Coordinate,
    DisplayConsole as Display,
    FieldBase,
    RobotRandom,
)

class TestArena(TestCase):
    def setUp(self):
        self.patcher = patch('builtins.print') # i just dont wanna print things
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_game_in_progress_should_return_TRUE_when_status_is_inprogress(self):
        field = FieldBase()
        display = Display(field)
        arena = Arena(field, display, None, None, None, None)
        expected_progress_status = True
        self.assertEqual(expected_progress_status, arena.game_in_progress())

    def test_game_in_progress_should_return_FALSE_when_status_is_not_inprogress(self):
        field = FieldBase()
        display = Display(field)
        arena = Arena(field, display, None, None, None, None)

        arena.status = "NOT-IN-PROGRESS"
        expected_progress_status = False
        self.assertEqual(expected_progress_status, arena.game_in_progress())

    def test_act_when_unit_on_penalty_will_skip_turn_and_free_unit_from_penalty(self):
        field = FieldBase()
        display = Display(field)
        test_robot = RobotRandom("test_robo")
        arena = Arena(field, display, None, None, None, None)

        mock_mapping = {
            test_robot: True
        }

        with patch.dict(arena._Arena__penalty_mapping, mock_mapping) as _, patch('__main__.next') as mock_next:
            arena._Arena__robots = [test_robot]
            penalized = True
            self.assertEqual(arena._Arena__penalty_mapping[test_robot], penalized)
            arena.act(test_robot)
            penalized = False
            self.assertEqual(arena._Arena__penalty_mapping[test_robot], penalized)
            mock_next.assert_not_called()

    def test_act_move(self):
        field = FieldBase()
        display = Display(field)
        test_robot = RobotRandom("test_robo")
        test_action = Action("move", "N")
        other_test_robot = RobotRandom("test_robo")
        test_robot.reaction = Mock()
        test_robot.reaction.return_value = test_action
        arena = Arena(field, display, None, None, None, None)

        mock_penalty_mapping = {
            test_robot: False,
            other_test_robot: False,
        }
        mock_location_mapping = {
            test_robot: Coordinate(0,0),
            other_test_robot: Coordinate(4,4),
        }

        with patch.object(arena, '_Arena__move', wraps=arena._Arena__move) as mock_move:
            arena._Arena__penalty_mapping = mock_penalty_mapping
            arena._Arena__robot_location_mapping = mock_location_mapping
            arena._Arena__robots = [other_test_robot, test_robot]
            arena.act(test_robot)
            mock_move.assert_called_once_with(test_robot, test_action.direction)

    def test_act_push(self):
        field = FieldBase()
        display = Display(field)
        test_robot = RobotRandom("test_robo")
        test_action = Action("push", "N")
        other_test_robot = RobotRandom("test_robo")
        test_robot.reaction = Mock()
        test_robot.reaction.return_value = test_action
        arena = Arena(field, display, None, None, None, None)

        mock_penalty_mapping = {
            test_robot: False,
            other_test_robot: False,
        }
        mock_location_mapping = {
            test_robot: Coordinate(0,0),
            other_test_robot: Coordinate(4,4),
        }

        with patch.object(arena, '_Arena__push', wraps=arena._Arena__push) as mock_push:
            arena._Arena__penalty_mapping = mock_penalty_mapping
            arena._Arena__robot_location_mapping = mock_location_mapping
            arena._Arena__robots = [other_test_robot, test_robot]
            arena.act(test_robot)
            mock_push.assert_called_once_with(test_robot, test_action.direction)

    def test_act_defend(self):
        field = FieldBase()
        display = Display(field)
        test_robot = RobotRandom("test_robo")
        test_action = Action("defend", "N")
        other_test_robot = RobotRandom("test_robo")
        test_robot.reaction = Mock()
        test_robot.reaction.return_value = test_action
        arena = Arena(field, display, None, None, None, None)

        mock_penalty_mapping = {
            test_robot: False,
            other_test_robot: False,
        }
        mock_location_mapping = {
            test_robot: Coordinate(0,0),
            other_test_robot: Coordinate(4,4),
        }

        with patch.object(arena, '_Arena__defend', wraps=arena._Arena__defend) as mock_defend:
            arena._Arena__penalty_mapping = mock_penalty_mapping
            arena._Arena__robot_location_mapping = mock_location_mapping
            arena._Arena__robots = [other_test_robot, test_robot]
            arena.act(test_robot)
            mock_defend.assert_called_once_with(test_robot, test_action.direction)

    def test_act_invalid(self):
        field = FieldBase()
        display = Display(field)
        test_robot = RobotRandom("test_robo")
        test_action = Action("xxx", "N")
        other_test_robot = RobotRandom("test_robo")
        test_robot.reaction = Mock()
        test_robot.reaction.return_value = test_action
        arena = Arena(field, display, None, None, None, None)

        mock_penalty_mapping = {
            test_robot: False,
            other_test_robot: False,
        }
        mock_location_mapping = {
            test_robot: Coordinate(0,0),
            other_test_robot: Coordinate(4,4),
        }

        with patch.object(arena, '_Arena__penalty', wraps=arena._Arena__penalty) as mock_penalty:
            arena._Arena__penalty_mapping = mock_penalty_mapping
            arena._Arena__robot_location_mapping = mock_location_mapping
            arena._Arena__robots = [other_test_robot, test_robot]
            arena.act(test_robot)
            mock_penalty.assert_called_once_with(test_robot)

