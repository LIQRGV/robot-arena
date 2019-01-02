class Field:
    def __init__(self):
        self.layout = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ]

    def get_dimension(self):
        return (len(self.layout), len(self.layout[0]))
