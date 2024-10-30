from Client import Client
from collections import deque
from Directions import Direction


class Robot:
    BORDER_TO_GO = 150

    def __init__(self, cell, board, is_motor_used, logging):
        self.id = "3536AF962E7A4A53"
        self.ip = "192.168.68.134"
        self.logging = logging
        self.cur_cell = cell
        self.board = board
        self.board.visit_cell(cell)
        #self.client = Client(self.id, self.ip, logging)
        self.cur_direction = 0
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
        self.time_for_turn = dict()

    def scan_maze(self):
        #self.calibration()
        #input("3")
        while self.board.visited_cells != self.board.total_cells:
            is_stepped = self.make_step()
            print(f"{self.board.visited_cells} / {self.board.total_cells}")
            if not is_stepped:
                self.return_back_to_crossroad()

    def make_step(self):
        sensor_data = self.client.get_sensor_data(self.client.request_all)
        dist = Direction.get_ordered_directions(sensor_data['laser'])

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

        if self.cur_cell.x == 6 and self.cur_cell.y == 8 and next_cell.x != 7 and next_cell.y != 8:
            return False
        
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

    def go_right(self):
        self.cur_direction = (self.cur_direction + 1) % 4
        if self.is_motor_used:
            self.client.make_action_motor(self.left_pwm, -self.right_pwm, self.time_for_turn[90])
            self.client.make_action_motor(self.left_pwm, self.right_pwm, self.time_for_one_step)
        else:
            self.client.turn_right(self.turn_right_angle)
            self.client.go_forward(self.board.get_cell_size())

    def go_left(self):
        self.cur_direction = (self.cur_direction - 1 + 4) % 4
        if self.is_motor_used:
            self.client.make_action_motor(-self.left_pwm, self.right_pwm, self.time_for_turn[90])
            self.client.make_action_motor(self.left_pwm, self.right_pwm, self.time_for_one_step)
        else:
            self.client.turn_left(self.turn_left_angle)
            self.client.go_forward(self.board.get_cell_size())

    def turn_around(self):
        self.cur_direction = (self.cur_direction + 2) % 4
        if self.is_motor_used:
            self.client.make_action_motor(self.left_pwm, -self.right_pwm, self.time_for_turn[90])
            self.client.make_action_motor(self.left_pwm, -self.right_pwm, self.time_for_turn[90])
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

            yaw_change = final_yaw - initial_yaw

            self.client.make_action_motor(-self.left_pwm, -self.right_pwm, test_time)

            self.logging.info(f"initial yaw: {initial_yaw}, final yaw : {final_yaw}, yaw change : {yaw_change}")

            if yaw_change > 1:  # The robot goes to the right, we slow down the right engine
                self.right_pwm -= adjustment
            elif yaw_change < -1:  # The robot goes to the left, we slow down the left motor
                self.left_pwm -= adjustment
            else:
                break  # The robot is moving straight, calibration is complete

    def set_time_for_one_step(self):
        self.time_for_one_step = 300
        time_step = self.time_for_one_step / 2
        tolerance = 2

        while time_step >= 1:
            initial_distance = self.client.get_sensor_data(self.client.request_all)['laser'][Direction.BACKWARD.value]
            self.client.make_action_motor(self.left_pwm, self.right_pwm, self.time_for_one_step)

            final_distance = self.client.get_sensor_data(self.client.request_all)['laser'][Direction.BACKWARD.value]
            self.client.make_action_motor(-self.left_pwm, -self.right_pwm, self.time_for_one_step)

            distance = abs(final_distance - initial_distance)

            self.logging.info(f"initial distance: {initial_distance}, final distance : {final_distance}, distance : {distance}")

            if abs(distance - self.board.get_cell_size()) <= tolerance:
                break

            if distance < self.board.get_cell_size():
                self.time_for_one_step += time_step
            else:
                self.time_for_one_step -= time_step
            
            time_step /= 2

    def set_time_for_turn(self, target_angle):
        current_time = 300
        time_step = current_time / 2
        tolerance = 2

        while time_step >= 1:
            initial_yaw = self.client.get_sensor_data(self.client.request_all)['imu']['yaw']
            self.client.make_action_motor(self.left_pwm, -self.right_pwm, current_time)
            
            final_yaw = self.client.get_sensor_data(self.client.request_all)['imu']['yaw']
            self.client.make_action_motor(-self.left_pwm, self.right_pwm, current_time)

            yaw_change = abs(final_yaw - initial_yaw)

            self.logging.info(f"initial yaw: {initial_yaw}, final yaw : {final_yaw}, yaw change : {yaw_change}")
            
            if abs(yaw_change - target_angle) <= tolerance:
                self.time_for_turn[target_angle] = current_time
                break
            
            if yaw_change < target_angle:
                current_time += time_step
            else:
                current_time -= time_step
            
            time_step /= 2

        self.time_for_turn[target_angle] = current_time

    def calibration(self):
        #self.set_motor_for_direct_move()
        self.logging.debug(f"right_pwm={self.right_pwm}, left_pwm={self.left_pwm}")
        input("1")
        #self.set_time_for_one_step()
        self.logging.debug(f"time_for_one_step={self.time_for_one_step}")
        input("2")
        #self.set_time_for_turn(target_angle=90)
        self.logging.debug(f"time_for_turn[90]={self.time_for_turn[90]}")








