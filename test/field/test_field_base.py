from unittest import TestCase

from robotarena import Coordinate
from robotarena.field import FieldBase

class TestFieldBase(TestCase):
    def test_get_dimension_should_return_dimension_tuple(self):
        field_base = FieldBase()
        expected_width = 5
        expected_height = 5
        (actual_width, actual_height) = field_base.get_dimension()
        self.assertEqual(expected_width, actual_width)
        self.assertEqual(expected_height, actual_height)

    def test_get_layout_should_return_layout(self):
        field_base = FieldBase()
        expected_layout = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ]
        self.assertEqual(expected_layout, field_base.get_layout())

    def test_is_obstructed_should_return_FALSE_if_field_code_is_0(self):
        field_base = FieldBase()
        check_location = Coordinate(0,0)
        expected_obstructed = False
        self.assertEqual(expected_obstructed, field_base.is_obstructed(check_location))
