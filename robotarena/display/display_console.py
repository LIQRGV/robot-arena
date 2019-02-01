class DisplayConsole:
    def __init__(self, field):
        self.field = field

    def draw(self, red_location, blue_location):
        field_and_player_matrix = self.__get_field_and_player_matrix(red_location, blue_location)
        for row in field_and_player_matrix:
            for cell in row:
                print(cell, end=' ')
            print()

    def __get_field_and_player_matrix(self, red_location, blue_location):
        (width, height) = self.field.get_dimension()
        layout = self.field.get_layout()
        layout_mapping = {
            0: "o",
            1: "x",
        }

        matrix = []

        for y in range(height - 1, -1, -1):
            row = []
            for x in range(0, width):
                if red_location.x == x and red_location.y == y:
                    row.append(1)
                elif blue_location.x == x and blue_location.y == y:
                    row.append(2)
                else:
                    layout_unit = layout[x][y]
                    row.append(layout_mapping[layout_unit])
            matrix.append(row)
        return matrix

