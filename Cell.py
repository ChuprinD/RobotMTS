class Cell:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.top_wall = None
        self.left_wall = None
        self.right_wall = None
        self.bottom_wall = None
        self.visited = False
        self.size = 180

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