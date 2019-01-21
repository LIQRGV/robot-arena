from .coordinate import Coordinate
import pygame

class Arena:
    __PIXEL_UNIT = 36
    __FONT_SIZE = 0
    def __init__(self, field, red_side, red_side_location, blue_side, blue_side_location):
        self.field = field
        self.robots = [red_side, blue_side]
        self.robot_location_mapping = {
            red_side: red_side_location,
            blue_side: blue_side_location
        }
        self.robot_defend_mapping = {
            red_side: None,
            blue_side: None
        }

        self.penalty_mapping = {
            red_side: False,
            blue_side: False,
        }

        self.status = "IN-PROGRESS"
        pygame.init()
        self.top_pad = self.__FONT_SIZE * 2
        self.screen = self.__create_screen()
        self.clock = pygame.time.Clock()
        self.__init_image()

    def game_in_progress(self):
        return "IN-PROGRESS" == self.status

    def act(self, playing_robot):
        if self.__is_on_penalty(playing_robot):
            self.__free_from_penalty(playing_robot)
            return

        other_robot = next(
            robot for robot in self.robots if robot != playing_robot
        )
        playing_robot_coordinate = self.robot_location_mapping[playing_robot]
        other_robot_coordinate = self.robot_location_mapping[other_robot]
        action = playing_robot.reaction(self.field, playing_robot, other_robot_coordinate)

        print(
            "{} {} to {}".format(
                playing_robot.name, action.action_type, action.direction
            )
        )
        if "move" == action.action_type:
            self.__move(playing_robot, action.direction)
        elif "push" == action.action_type:
            self.__push(playing_robot, action.direction)
        elif "defend" == action.action_type:
            self.__defend(playing_robot, action.direction)
        else:
            self.__penalty(playing_robot)

    def draw(self):
        [red, blue] = self.robots
        red_location = self.robot_location_mapping[red]
        blue_location = self.robot_location_mapping[blue]
        (width, height) = self.field.get_dimension()
        layout = self.field.get_layout()
        layout_mapping = {
            0: "o",
            1: "x",
        }
        screen = self.screen
        for y in range(height - 1, -1, -1):
            for x in range(0, width):
                if red_location.x == x and red_location.y == y:
                    circle_black_pix = self.__pos_to_pix(red_location)
                    screen.blit(self.circle_black, circle_black_pix) # draw black circle to next screen
                    print(1, end=' ')
                elif blue_location.x == x and blue_location.y == y:
                    circle_white_pix = self.__pos_to_pix(blue_location)
                    screen.blit(self.circle_white, circle_white_pix) # draw black circle to next screen
                    print(2, end=' ')
                else:
                    tile_pix = self.__pos_to_pix(Coordinate(x,y))
                    screen.blit(self.tile, tile_pix) # draw black circle to next screen
                    print(layout_mapping[layout[x][y]], end=' ')
            print()
        pygame.display.flip()
        self.clock.tick(120)



    def __move(self, robot, direction):
        robot_location = self.robot_location_mapping[robot]
        copy_robot_location = Coordinate(robot_location.x, robot_location.y)
        if "N" == direction:
            copy_robot_location.y += 1
        elif "E" == direction:
            copy_robot_location.x += 1
        elif "S" == direction:
            copy_robot_location.y -= 1
        elif "W" == direction:
            copy_robot_location.x -= 1
        else:
            self.__penalty(robot)
            return

        if self.__valid_move_location(robot, copy_robot_location):
            self.robot_location_mapping[robot] = copy_robot_location
        else:
            self.__penalty(robot)

    def __push(self, playing_robot, direction):
        robot_location = self.robot_location_mapping[playing_robot]
        other_robot = next(
            robot for robot in self.robots if robot != playing_robot
        )
        if self.__valid_push_location(playing_robot, direction):
            if self.__robot_can_pushed_from(robot_location, other_robot):
                self.__force_moved(other_robot, direction)
            else:
                self.__knockback(playing_robot, direction)
        else:
            self.__penalty(playing_robot)

    def __defend(self, robot, direction):
        robot_location = self.robot_location_mapping[robot]
        copy_robot_location = Coordinate(robot_location.x, robot_location.y)
        if "N" == direction:
            copy_robot_location.y += 1
        elif "E" == direction:
            copy_robot_location.x += 1
        elif "S" == direction:
            copy_robot_location.y -= 1
        elif "W" == direction:
            copy_robot_location.x -= 1
        else:
            self.__penalty(robot)
            return
        self.robot_defend_mapping[robot] = copy_robot_location


    def __force_moved(self, robot, direction):
        (width, height) = self.field.get_dimension()
        robot_location = self.robot_location_mapping[robot]
        if "N" == direction:
            robot_location.y += 2
        elif "E" == direction:
            robot_location.x += 2
        elif "S" == direction:
            robot_location.y -= 2
        elif "W" == direction:
            robot_location.x -= 2

        if self.__valid_move_location(robot, robot_location):
            self.robot_location_mapping[robot] = robot_location
        else:
            self.status = robot.name + " lose"

    def __knockback(self, robot, direction):
        (width, height) = self.field.get_dimension()
        robot_location = self.robot_location_mapping[robot]
        if "N" == direction:
            robot_location.y -= 1
        elif "E" == direction:
            robot_location.x -= 1
        elif "S" == direction:
            robot_location.y += 1
        elif "W" == direction:
            robot_location.x += 1

        if self.__valid_move_location(robot, robot_location):
            self.robot_location_mapping[robot] = robot_location
        else:
            self.status = robot.name + " lose"

    def __valid_push_location(self, playing_robot, direction):
        robot_location = self.robot_location_mapping[playing_robot]
        other_robot = next(
            robot for robot in self.robots if robot != playing_robot
        )
        other_robot_location = self.robot_location_mapping[other_robot]

        copy_robot_location = Coordinate(robot_location.x, robot_location.y)
        if "N" == direction:
            copy_robot_location.y += 1
        elif "E" == direction:
            copy_robot_location.x += 1
        elif "S" == direction:
            copy_robot_location.y -= 1
        elif "W" == direction:
            copy_robot_location.x -= 1

        return (
            copy_robot_location.x == other_robot_location.x and
            copy_robot_location.y == other_robot_location.y
        )

    def __valid_move_location(self, moving_robot, location):
        (width, height) = self.field.get_dimension()
        within_field = (
            location.x >= 0 and location.y >= 0
            and location.x < width and location.y < height
        )

        if not within_field:
            return False

        other_robot = next(
            robot for robot in self.robots if robot != moving_robot
        )
        other_robot_coordinate = self.robot_location_mapping[other_robot]

        field_not_obstructed = not self.field.is_obstructed(location)
        not_obstructed_by_another_robot = not (
            location.x == other_robot_coordinate.x and
            location.y == other_robot_coordinate.y

        )

        return field_not_obstructed and not_obstructed_by_another_robot

    def __robot_can_pushed_from(self, pusher_location, robot):
        robot_defend_to_location = self.robot_defend_mapping[robot]
        if robot_defend_to_location is None:
            return True

        return not (
            robot_defend_to_location.x == pusher_location.x and
            robot_defend_to_location.y == pusher_location.y
        )

    def __is_on_penalty(self, robot):
        return self.penalty_mapping[robot]

    def __free_from_penalty(self, robot):
        self.penalty_mapping[robot] = False

    def __penalty(self, robot):
        print("{} penalized".format(robot.name))
        self.penalty_mapping[robot] = True

    def __init_image(self):
        self.circle_black = pygame.image.load("images/circle_black.png")
        self.circle_white = pygame.image.load("images/circle_white.png")
        self.tile = pygame.image.load("images/tile.png")

    def __pos_to_pix(self, coordinate):
        return (
            coordinate.x * self.__PIXEL_UNIT,
            coordinate.y * self.__PIXEL_UNIT + self.top_pad
        )

    def __create_screen(self):
        (width, height) = self.field.get_dimension()
        return pygame.display.set_mode(
            (
                self.__PIXEL_UNIT * width,
                self.__PIXEL_UNIT * height + self.top_pad
            )
        )

    def __pos_to_pix(self, coordinate):
        return (
            coordinate.x * self.__PIXEL_UNIT,
            coordinate.y * self.__PIXEL_UNIT + self.top_pad
        )
