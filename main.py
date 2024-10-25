import os
import time
from Board import Board
from Robot import Robot

def main():
    board = Board()
    cell = board.get_cell(0, 0)
    robot = Robot(cell, board)
    board.print_board(robot)
    robot.scan_maze()
    
    sensor_data = robot.client.get_sensor_data(robot.client.request_all)
    dist = [
        sensor_data['front_distance'],
        sensor_data['right_side_distance'],
        sensor_data['back_distance'],
        sensor_data['left_side_distance']
    ]
    robot.analyze_data(dist)

    matrix = robot.board.board_to_code_matrix()
    for row in matrix:
        print(" ".join(map(str, row)))

    robot.client.send_matrix(matrix)

if __name__ == "__main__":
    os.system("pip install requests")
    time.sleep(10)
    main()

