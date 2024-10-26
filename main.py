import os
import time
from Board import Board
from Robot import Robot
from Directions import Direction


def main():
    board = Board()
    cell = board.get_cell(0, 0)
    robot = Robot(cell, board, True)

    robot.scan_maze()
    sensor_data = robot.client.get_sensor_data(robot.client.request_all)
    dist = Direction.get_ordered_directions(sensor_data['laser'])
    robot.analyze_data(dist)

    matrix = robot.board.board_to_code_matrix()
    for row in matrix:
        print(" ".join(map(str, row)))

    robot.board.save_matrix_to_json("matrix.json")

if __name__ == "__main__":
    # os.system("pip install requests")
    # time.sleep(10)
    main()

