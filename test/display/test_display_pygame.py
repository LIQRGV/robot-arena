import sys
from unittest import (
    TestCase,
    mock,
)

from robotarena import (
    Coordinate,
)
from robotarena.display import DisplayPygame
from robotarena.field import FieldBase as Field

class TestDisplayPygame(TestCase):
    def test_draw_should_draw_player_location_on_pygame(self):
        field = Field()

        display = None
        with mock.patch('pygame.display.set_mode'):
            display = DisplayPygame(field)
        mock_red_location = Coordinate(0,0)
        mock_blue_location = Coordinate(4,4)

        mock_circle_black = object() #any object would do
        mock_circle_white = object() #any object would do
        mock_tile = object() #any object would do
        display._DisplayPygame__circle_black = mock_circle_black
        display._DisplayPygame__circle_white = mock_circle_white
        display._DisplayPygame__tile = mock_tile

        with mock.patch.object(display._DisplayPygame__screen, 'blit') as mock_screen, \
                mock.patch('pygame.display.flip'):
            display.draw(mock_red_location, mock_blue_location)
            circle_white_pix = self.__pos_to_pix(mock_blue_location)
            circle_black_pix = self.__pos_to_pix(mock_red_location)
            tiles_pix = [self.__pos_to_pix(Coordinate(x,y)) for y in range(0,5) for x in range(0,5)]
            players_call = [mock.call(mock_circle_black, circle_black_pix), mock.call(mock_circle_white, circle_white_pix)]
            tiles_call = [mock.call(mock_tile, pix) for pix in tiles_pix]
            expected_call = players_call + tiles_call
            mock_screen.assert_has_calls(expected_call, any_order=True)

    def __pos_to_pix(self, coordinate):
        PIXEL_UNIT = 36
        TOP_PAD = 0
        normalized_coordinate = self.__normalized_coordinate(coordinate)
        return (
            normalized_coordinate.x * PIXEL_UNIT,
            normalized_coordinate.y * PIXEL_UNIT + TOP_PAD
        )

    def __normalized_coordinate(self, coordinate):
        field = Field()
        (_, height) = field.get_dimension()
        return Coordinate(
            coordinate.x,
            (height - 1) - coordinate.y
        )
