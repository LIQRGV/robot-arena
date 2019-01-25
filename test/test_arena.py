from unittest import TestCase
from unittest.mock import (
    Mock,
    patch
)

from robotarena import (
    Arena,
    FieldBase,
    RobotRandom,
)

class TestArena(TestCase):
    def setUp(self):
        self.patcher = patch('pygame.display.set_mode')
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_game_in_progress_should_return_TRUE_when_status_is_inprogress(self):
        width = 5
        height = 5
        partial_mock_field = FieldBase()
        partial_mock_field.get_dimension = Mock()
        partial_mock_field.get_dimension.return_value = (width, height)
        arena = Arena(partial_mock_field, None, None, None, None)
        expected_progress_status = True
        self.assertEqual(expected_progress_status, arena.game_in_progress())

    def test_game_in_progress_should_return_FALSE_when_status_is_not_inprogress(self):
        width = 5
        height = 5
        partial_mock_field = FieldBase()
        partial_mock_field.get_dimension = Mock()
        partial_mock_field.get_dimension.return_value = (width, height)
        arena = Arena(partial_mock_field, None, None, None, None)
        arena.status = "NOT-IN-PROGRESS"
        expected_progress_status = False
        self.assertEqual(expected_progress_status, arena.game_in_progress())

    def test_act_when_unit_on_penalty_will_skip_turn_and_free_unit_from_penalty(self):
        width = 5
        height = 5
        partial_mock_field = FieldBase()
        partial_mock_field.get_dimension = Mock()
        partial_mock_field.get_dimension.return_value = (width, height)
        test_robot = RobotRandom("test_robo")
        arena = Arena(partial_mock_field, None, None, None, None)
        mock_mapping = {
            test_robot: True
        }

        with patch.dict(arena._Arena__penalty_mapping, mock_mapping) as _, patch('__main__.next') as new_next:
            arena._Arena__robots = [test_robot]
            penalized = True
            self.assertEqual(arena._Arena__penalty_mapping[test_robot], penalized)
            arena.act(test_robot)
            penalized = False
            self.assertEqual(arena._Arena__penalty_mapping[test_robot], penalized)
            new_next.assert_not_called()

    def test_act_move(self):
        pass

    def test_act_push(self):
        pass

    def test_act_defend(self):
        pass

    def test_act_invalid(self):
        pass

