from Client import Client
from collections import deque

class Robot:
    BORDER_TO_GO = 150

    def __init__(self, cell, board):
        self.id = ""
        self.cur_cell = cell
        self.board = board
        self.board.visit_cell(cell)
        self.client = Client()
        self.cur_direction = 0
        self.is_centered = True
        self.diff_x = 0
        self.diff_y = 0
        self.memory = deque()
        self.actions = [
            self.go_forward,
            self.go_right,
            self.go_back,
            self.go_left
        ]
        self.turn_right_angle = 90
        self.turn_left_angle = 270

    def make_step(self):
        data = self.client.get_data()
        dist = [
            data['front_distance'],
            data['right_side_distance'],
            data['back_distance'],
            data['left_side_distance']
        ]

        self.check_is_centered(data)
        self.analyze_data(dist)

        for i in range(4):
            if self.can_go(dist[i], i):
                self.memory.append(i)
                self.cur_cell = self.get_cell(i)
                self.board.visit_cell(self.cur_cell)
                self.actions[i]()
                return True
        return False

    def return_back_to_crossroad(self):
        self.turn_around()
        self.memory.append(0)
        while True:
            data = self.client.get_data()
            dist = [
                data['front_distance'],
                data['right_side_distance'],
                data['back_distance'],
                data['left_side_distance']
            ]
            self.analyze_data(dist)

            can_move = False
            for i in range(4):
                if self.can_go(dist[i], i):
                    can_move = True
            if can_move:
                break

            move = self.memory.pop()
            move = move if move == 0 else (move + 2) % 4
            self.cur_cell = self.get_cell(move)
            self.actions[move]()

        last_move = self.memory.pop()
        if last_move == 0:
            self.turn_around()
        elif last_move == 1:
            self.client.turn_right(self.turn_right_angle)
            self.cur_direction = (self.cur_direction + 1) % 4
        elif last_move == 4:
            self.client.turn_left(self.turn_left_angle)
            self.cur_direction = (self.cur_direction + 3) % 4

    def get_cell(self, direction):
        dydx = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        cur_dd = dydx[(direction + self.cur_direction) % 4]
        return self.board.get_cell(self.cur_cell.y + cur_dd[0], self.cur_cell.x + cur_dd[1])

    def can_go(self, dist, direction):
        if dist <= self.BORDER_TO_GO:
            return False
        next_cell = self.get_cell(direction)
        return not next_cell.visited

    def analyze_data(self, dist):
        for i in range(4):
            direction = (self.cur_direction + i) % 4
            if direction == 0:
                self.cur_cell.top_wall = dist[i] <= self.BORDER_TO_GO
            elif direction == 1:
                self.cur_cell.right_wall = dist[i] <= self.BORDER_TO_GO
            elif direction == 2:
                self.cur_cell.bottom_wall = dist[i] <= self.BORDER_TO_GO
            elif direction == 3:
                self.cur_cell.left_wall = dist[i] <= self.BORDER_TO_GO

    def check_is_centered(self, sensor_data):
        x_wall = 166.7
        y_wall = 167
        board_x = self.cur_cell.x - 8 + 0.5
        board_y = self.cur_cell.y - 8 + 0.5
        cur_x = sensor_data['down_y_offset']
        cur_y = sensor_data['down_x_offset']
        should_be_x = x_wall * board_x
        should_be_y = y_wall * board_y
        self.diff_x = abs(cur_x - should_be_x)
        self.diff_y = abs(cur_y - should_be_y)
        self.is_centered = self.diff_x <= 25 and self.diff_y <= 25

    def go_right(self):
        self.cur_direction = (self.cur_direction + 1) % 4
        self.client.turn_right(self.turn_right_angle)
        self.client.go_forward(self.board.get_cell_size())

    def go_left(self):
        self.cur_direction = (self.cur_direction - 1 + 4) % 4
        self.client.turn_left(self.turn_left_angle)
        self.client.go_forward(self.board.get_cell_size())

    def turn_around(self):
        self.cur_direction = (self.cur_direction + 2) % 4
        self.client.turn_left(self.turn_left_angle)
        self.client.turn_left(self.turn_left_angle)

    def go_forward(self):
        self.client.go_forward(self.board.get_cell_size())

    def go_back(self):
        self.client.go_back(self.board.get_cell_size())