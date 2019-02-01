import io
from unittest import (
    TestCase,
    mock,
)

from robotarena import (
    Coordinate,
)
from robotarena.display import DisplayConsole
from robotarena.field import FieldBase as Field

class TestDisplayConsole(TestCase):
    def test_draw_should_show_player_location_properly(self):
        field = Field()
        display = DisplayConsole(field)
        mock_red_location = Coordinate(0,0)
        mock_blue_location = Coordinate(4,4)
        expected_output = [
            ['o', 'o', 'o', 'o', '2'],
            ['o', 'o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o', 'o'],
            ['1', 'o', 'o', 'o', 'o'],
        ]

        expected_console_output = self.__list_to_console_output(expected_output)

        with mock.patch('sys.stdout', new_callable=io.StringIO) as console_output:
            display.draw(mock_red_location, mock_blue_location)
            striped_console_output_value = console_output.getvalue().rstrip()
            self.assertEqual(striped_console_output_value, expected_console_output)


    def __list_to_console_output(self, input_list):
        return '\n'.join(
            z for z in (
                ' '.join(
                    (str(y) for y in x)
                )
                for x in input_list
            )
        )

