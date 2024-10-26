class Cell:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.top_wall = True
        self.left_wall = True
        self.right_wall = True
        self.bottom_wall = True
        self.visited = False
        self.size = 180

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'top_wall': self.top_wall,
            'left_wall': self.left_wall,
            'right_wall': self.right_wall,
            'bottom_wall': self.bottom_wall,
            'visited': self.visited,
            'size': self.size
        }

    def get_size(self):
        return self.size

    def get_code(self):
        if self.top_wall is None:
            self.top_wall = False
        if self.left_wall is None:
            self.left_wall = False
        if self.right_wall is None:
            self.right_wall = False
        if self.bottom_wall is None:
            self.bottom_wall = False

        if self.top_wall and self.left_wall and self.right_wall and self.bottom_wall:
            return 15
        if self.left_wall and self.bottom_wall and self.right_wall:
            return 14
        if self.top_wall and self.left_wall and self.bottom_wall:
            return 13
        if self.left_wall and self.top_wall and self.right_wall:
            return 12
        if self.top_wall and self.right_wall and self.bottom_wall:
            return 11
        if self.top_wall and self.bottom_wall:
            return 10
        if self.left_wall and self.right_wall:
            return 9
        if self.left_wall and self.top_wall:
            return 8
        if self.top_wall and self.right_wall:
            return 7
        if self.right_wall and self.bottom_wall:
            return 6
        if self.left_wall and self.bottom_wall:
            return 5
        if self.bottom_wall:
            return 4
        if self.right_wall:
            return 3
        if self.top_wall:
            return 2
        if self.left_wall:
            return 1
        return 0