from Client import Client
from collections import deque
from Directions import Direction


class Robot:
    BORDER_TO_GO = 150

    def __init__(self, cell, board, is_motor_used):
        self.id = "3536AF962E7A4A53"
        self.ip = "192.168.68.134"
        self.cur_cell = cell
        self.board = board
        self.board.visit_cell(cell)
        self.client = Client(self.id, self.ip)
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

        self.is_motor_used = is_motor_used
        self.base_pwm = 60
        self.adjustment_pwm = 0
        self.left_pwm = self.base_pwm
        self.right_pwm = self.base_pwm
        self.time_for_one_step = 0
        self.time_for_90_degree_turn = 0

    def scan_maze(self):
        self.calibration()
        input()
        while self.board.visited_cells != self.board.total_cells:
            is_stepped = self.make_step()
            print(f"{self.board.visited_cells} / {self.board.total_cells}")
            if not is_stepped:
                self.return_back_to_crossroad()

    def make_step(self):
        sensor_data = self.client.get_sensor_data(self.client.request_all)
        dist = Direction.get_ordered_directions(sensor_data['laser'])

        # self.check_is_centered(data)
        self.analyze_data(dist)

        for i in range(4):
            if self.can_go(dist[i], i):
                self.memory.append(i)
                next_step = self.get_cell(i)
                self.board.remove_wall(self.cur_cell, next_step)
                self.cur_cell = next_step
                self.board.visit_cell(self.cur_cell)
                self.board.print_board(self)
                self.actions[i]()
                return True
        return False

    def return_back_to_crossroad(self):
        self.turn_around()
        self.memory.append(0)
        while True:
            sensor_data = self.client.get_sensor_data(self.client.request_all)
            dist = Direction.get_ordered_directions(sensor_data['laser'])
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

    # def check_is_centered(self, sensor_data):
    #     x_wall = 166.7
    #     y_wall = 167
    #     board_x = self.cur_cell.x - 8 + 0.5
    #     board_y = self.cur_cell.y - 8 + 0.5
    #     cur_x = sensor_data['down_y_offset']
    #     cur_y = sensor_data['down_x_offset']
    #     should_be_x = x_wall * board_x
    #     should_be_y = y_wall * board_y
    #     self.diff_x = abs(cur_x - should_be_x)
    #     self.diff_y = abs(cur_y - should_be_y)
    #     self.is_centered = self.diff_x <= 25 and self.diff_y <= 25

    def go_right(self):
        self.cur_direction = (self.cur_direction + 1) % 4
        if self.is_motor_used:
            self.client.make_action_motor(self.left_pwm, -self.right_pwm, self.time_for_90_degree_turn)
            self.client.make_action_motor(self.left_pwm, self.right_pwm, self.time_for_one_step)
        else:
            self.client.turn_right(self.turn_right_angle)
            self.client.go_forward(self.board.get_cell_size())

    def go_left(self):
        self.cur_direction = (self.cur_direction - 1 + 4) % 4
        if self.is_motor_used:
            self.client.make_action_motor(-self.left_pwm, self.right_pwm, self.time_for_90_degree_turn)
            self.client.make_action_motor(self.left_pwm, self.right_pwm, self.time_for_one_step)
        else:
            self.client.turn_left(self.turn_left_angle)
            self.client.go_forward(self.board.get_cell_size())

    def turn_around(self):
        self.cur_direction = (self.cur_direction + 2) % 4
        if self.is_motor_used:
            self.client.make_action_motor(self.left_pwm, -self.right_pwm, self.time_for_90_degree_turn * 2)
        else:
            self.client.turn_left(self.turn_left_angle)
            self.client.turn_left(self.turn_left_angle)

    def go_forward(self):
        if self.is_motor_used:
            self.client.make_action_motor(self.left_pwm, self.right_pwm, self.time_for_one_step)
        else:
            self.client.go_forward(self.board.get_cell_size())

    def go_back(self):
        if self.is_motor_used:
            self.client.make_action_motor(-self.left_pwm, -self.right_pwm, self.time_for_one_step)
        else:
            self.client.go_back(self.board.get_cell_size())

    def set_motor_for_direct_move(self):
        adjustment = 5
        test_time = 300

        for _ in range(10):
            initial_yaw = self.client.get_sensor_data(self.client.request_all)['imu']['yaw']

            self.client.make_action_motor(self.left_pwm, self.right_pwm, test_time)

            final_yaw = self.client.get_sensor_data(self.client.request_all)['imu']['yaw']

            yaw_error = final_yaw - initial_yaw

            self.client.make_action_motor(-self.left_pwm, -self.right_pwm, test_time)

            print(f"(dirct move)initial yaw: {initial_yaw}, final_yaw : {final_yaw}")

            if yaw_error > 1:  # The robot goes to the right, we slow down the right engine
                self.right_pwm -= adjustment
            elif yaw_error < -1:  # The robot goes to the left, we slow down the left motor
                self.left_pwm -= adjustment
            else:
                break  # The robot is moving straight, calibration is complete

        difference = abs(self.left_pwm - self.right_pwm)
        # if self.right_pwm < self.left_pwm:
        #     self.left_pwm = 255
        #     self.right_pwm = 255 - difference
        # else:
        #     self.right_pwm = 255
        #     self.left_pwm = 255 - difference

    def set_time_for_one_step(self):
        self.time_for_one_step = 300
        for _ in range(4):
            initial_front_distance = self.client.get_sensor_data(self.client.request_all)['laser'][
                Direction.FORWARD.value]
            self.client.make_action_motor(self.left_pwm, self.right_pwm, self.time_for_one_step)
            final_front_distance = self.client.get_sensor_data(self.client.request_all)['laser'][
                Direction.FORWARD.value]
            self.client.make_action_motor(-self.left_pwm, -self.right_pwm, self.time_for_one_step)
            print(f"(distance)initial front dist: {initial_front_distance}, final front dist : {final_front_distance}")
            distance = abs(final_front_distance - initial_front_distance)
            speed = distance / self.time_for_one_step
            self.time_for_one_step = self.board.get_cell_size() / speed

    def set_time_for_90_degree_turn(self):
        self.time_for_90_degree_turn = 300
        for _ in range(4):
            initial_yaw = self.client.get_sensor_data(self.client.request_all)['imu']['yaw']
            self.client.make_action_motor(self.left_pwm, -self.right_pwm, self.time_for_90_degree_turn)
            final_yaw = self.client.get_sensor_data(self.client.request_all)['imu']['yaw']
            self.client.make_action_motor(-self.left_pwm, self.right_pwm, self.time_for_90_degree_turn)
            print(f"(90 degree)initial yaw: {initial_yaw}, final_yaw : {final_yaw}")
            difference_yaw = abs(final_yaw - initial_yaw)
            speed = min(abs(360 - difference_yaw), abs(difference_yaw)) / self.time_for_90_degree_turn
            self.time_for_90_degree_turn = 90 / speed

    def calibration(self):
        self.set_motor_for_direct_move()
        self.set_time_for_one_step()
        self.set_time_for_90_degree_turn()








