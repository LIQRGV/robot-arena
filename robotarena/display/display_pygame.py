import pygame

from ..coordinate import Coordinate

class DisplayPygame:
    __PIXEL_UNIT = 36
    __FONT_SIZE = 0
    def __init__(self, field):
        pygame.init()
        self.field = field
        (self.width, self.height) = field.get_dimension()
        self.top_pad = self.__FONT_SIZE * 2
        self.screen = self.__create_screen()
        self.clock = pygame.time.Clock()
        self.__init_image()

    def draw(self, red_location, blue_location):
        (width, height) = self.field.get_dimension()
        layout = self.field.get_layout()
        for y in range(height - 1, -1, -1):
            for x in range(0, width):
                tile_pix = self.__pos_to_pix(Coordinate(x,y))
                self.screen.blit(self.tile, tile_pix) # draw tile to next screen
                if red_location.x == x and red_location.y == y:
                    circle_black_pix = self.__pos_to_pix(red_location)
                    self.screen.blit(self.circle_black, circle_black_pix) # draw black circle to next screen
                elif blue_location.x == x and blue_location.y == y:
                    circle_white_pix = self.__pos_to_pix(blue_location)
                    self.screen.blit(self.circle_white, circle_white_pix) # draw black circle to next screen
        pygame.display.flip()
        self.clock.tick(120)

    def __init_image(self):
        self.circle_black = pygame.image.load("images/circle_black.png")
        self.circle_white = pygame.image.load("images/circle_white.png")
        self.tile = pygame.image.load("images/tile.png")

    def __create_screen(self):

        return pygame.display.set_mode(
            (
                self.__PIXEL_UNIT * self.width,
                self.__PIXEL_UNIT * self.height + self.top_pad
            )
        )

    def __pos_to_pix(self, coordinate):
        return (
            coordinate.x * self.__PIXEL_UNIT,
            coordinate.y * self.__PIXEL_UNIT + self.top_pad
        )
