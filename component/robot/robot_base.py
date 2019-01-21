class RobotBase:
    def __init__(self, name):
        self.name = name

    # this should return object `Action`
    def reaction(self, field, self_location, enemy_location):
        return Action(None, None)


