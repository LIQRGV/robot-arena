from unittest import TestCase

from robotarena import Coordinate

class TestCoordinate(TestCase):
    def test_init_should_assign_x_and_y(self):
        x = 1
        y = 2
        coordinate = Coordinate(x, y)
        self.assertEqual(x, coordinate.x)
        self.assertEqual(y, coordinate.y)

