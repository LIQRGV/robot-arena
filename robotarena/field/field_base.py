class FieldBase:
    OBSCTRUCTED_CODE = 1
    NOT_OBSCTRUCTED_CODE = 0
    def __init__(self):
        self.__layout = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ]

    def get_dimension(self):
        return (len(self.__layout), len(self.__layout[0]))

    def get_layout(self):
        return self.__layout

    def is_obstructed(self, location):
        return self.__layout[location.x][location.y] == self.OBSCTRUCTED_CODE
