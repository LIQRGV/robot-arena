import pygame

from ..coordinate import Coordinate

class DisplayPygame:
    __PIXEL_UNIT = 36
    __FONT_SIZE = 0
    def __init__(self, field):
        pygame.init()
        self.__field = field
        (self.__width, self.__height) = field.get_dimension()
        self.__top_pad = self.__FONT_SIZE * 2
        self.__screen = self.__create_screen()
        self.__clock = pygame.time.Clock()
        self.__init_image()

    def draw(self, red_location, blue_location):
        (width, __height) = self.__field.get_dimension()
        layout = self.__field.get_layout()
        for y in range(0, __height):
            for x in range(0, width):
                tile_pix = self.__pos_to_pix(Coordinate(x,y))
                self.__screen.blit(self.__tile, tile_pix) # draw tile to next screen
                if red_location.x == x and red_location.y == y:
                    circle_black_pix = self.__pos_to_pix(red_location)
                    self.__screen.blit(self.__circle_black, circle_black_pix) # draw black circle to next screen
                elif blue_location.x == x and blue_location.y == y:
                    circle_white_pix = self.__pos_to_pix(blue_location)
                    self.__screen.blit(self.__circle_white, circle_white_pix) # draw black circle to next screen
        pygame.display.flip()
        self.__clock.tick(120)

    def __init_image(self):
        self.__circle_black = pygame.image.load("images/circle_black.png")
        self.__circle_white = pygame.image.load("images/circle_white.png")
        self.__tile = pygame.image.load("images/tile.png")

    def __create_screen(self):
        return pygame.display.set_mode(
            (
                self.__PIXEL_UNIT * self.__width,
                self.__PIXEL_UNIT * self.__height + self.__top_pad
            )
        )

    def __pos_to_pix(self, coordinate):
        normalized_coordinate = self.__normalized_coordinate(coordinate)
        return (
            normalized_coordinate.x * self.__PIXEL_UNIT,
            normalized_coordinate.y * self.__PIXEL_UNIT + self.__top_pad
        )

    def __normalized_coordinate(self, coordinate):
        return Coordinate(
            coordinate.x,
            (self.__height - 1) - coordinate.y
        )
