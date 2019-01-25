from robotarena import (
    Arena,
    Coordinate,
    Field,
    RobotRandom as Robot,
)

field = Field()
robot1_coordinate = Coordinate(0,0)
robot2_coordinate = Coordinate(4,4)

robot1 = Robot("robi")
robot2 = Robot("robo")

arena = Arena(field, robot1, robot1_coordinate, robot2, robot2_coordinate)

turn_count = 1

while arena.game_in_progress():
    print("Turn", turn_count)

    active_robot = None
    if turn_count % 2 == 1:
        active_robot = robot1
    else:
        active_robot = robot2

    arena.act(active_robot)
    arena.draw()

    turn_count += 1

print(arena.status)
