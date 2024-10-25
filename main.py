import os
import time
from Board import Board
from Robot import Robot


def main():
    board = Board()
    cell = board.get_cell(0, 0)
    robot = Robot(cell, board)
    robot.scan_maze()

    sensor_data = robot.client.get_sensor_data(robot.client.request_all)
    dist = [
        sensor_data['laser']['4'],
        sensor_data['laser']['5'],
        sensor_data['laser']['1'],
        sensor_data['laser']['2']
    ]
    robot.analyze_data(dist)

    matrix = robot.board.board_to_code_matrix()
    for row in matrix:
        print(" ".join(map(str, row)))

    robot.board.save_matrix_to_json("matrix.json")

if __name__ == "__main__":
    # os.system("pip install requests")
    # time.sleep(10)
    main()

