from .coordinate import Coordinate

class Arena:
    def __init__(self, field, display, red_side, red_side_location, blue_side, blue_side_location):
        self.field = field
        self.__display = display
        self.__robots = [red_side, blue_side]
        self.__robot_location_mapping = {
            red_side: red_side_location,
            blue_side: blue_side_location
        }
        self.robot_defend_mapping = {
            red_side: None,
            blue_side: None
        }

        self.__penalty_mapping = {
            red_side: False,
            blue_side: False,
        }

        self.status = "IN-PROGRESS"

    def game_in_progress(self):
        return "IN-PROGRESS" == self.status

    def act(self, playing_robot):
        if self.__is_on_penalty(playing_robot):
            self.__free_from_penalty(playing_robot)
            return

        other_robot = next(
            robot for robot in self.__robots if robot != playing_robot
        )
        playing_robot_coordinate = self.__robot_location_mapping[playing_robot]
        other_robot_coordinate = self.__robot_location_mapping[other_robot]
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
        [red, blue] = self.__robots
        red_location = self.__robot_location_mapping[red]
        blue_location = self.__robot_location_mapping[blue]
        self.__display.draw(red_location, blue_location)

    def __move(self, robot, direction):
        robot_location = self.__robot_location_mapping[robot]
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
            self.__robot_location_mapping[robot] = copy_robot_location
        else:
            self.__penalty(robot)

    def __push(self, playing_robot, direction):
        robot_location = self.__robot_location_mapping[playing_robot]
        other_robot = next(
            robot for robot in self.__robots if robot != playing_robot
        )
        if self.__valid_push_location(playing_robot, direction):
            if self.__robot_can_pushed_from(robot_location, other_robot):
                self.__force_moved(other_robot, direction)
            else:
                self.__knockback(playing_robot, direction)
        else:
            self.__penalty(playing_robot)

    def __defend(self, robot, direction):
        robot_location = self.__robot_location_mapping[robot]
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
        robot_location = self.__robot_location_mapping[robot]
        if "N" == direction:
            robot_location.y += 2
        elif "E" == direction:
            robot_location.x += 2
        elif "S" == direction:
            robot_location.y -= 2
        elif "W" == direction:
            robot_location.x -= 2

        if self.__valid_move_location(robot, robot_location):
            self.__robot_location_mapping[robot] = robot_location
        else:
            self.status = robot.name + " lose"

    def __knockback(self, robot, direction):
        (width, height) = self.field.get_dimension()
        robot_location = self.__robot_location_mapping[robot]
        if "N" == direction:
            robot_location.y -= 1
        elif "E" == direction:
            robot_location.x -= 1
        elif "S" == direction:
            robot_location.y += 1
        elif "W" == direction:
            robot_location.x += 1

        if self.__valid_move_location(robot, robot_location):
            self.__robot_location_mapping[robot] = robot_location
        else:
            self.status = robot.name + " lose"

    def __valid_push_location(self, playing_robot, direction):
        robot_location = self.__robot_location_mapping[playing_robot]
        other_robot = next(
            robot for robot in self.__robots if robot != playing_robot
        )
        other_robot_location = self.__robot_location_mapping[other_robot]

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
            robot for robot in self.__robots if robot != moving_robot
        )
        other_robot_coordinate = self.__robot_location_mapping[other_robot]

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
        return self.__penalty_mapping[robot]

    def __free_from_penalty(self, robot):
        self.__penalty_mapping[robot] = False

    def __penalty(self, robot):
        print("{} penalized".format(robot.name))
        self.__penalty_mapping[robot] = True

