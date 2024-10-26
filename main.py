import os
import time
import logging
from Board import Board
from Robot import Robot
from Directions import Direction

def get_log_filename(base_name):
    n = 1
    while True:
        log_filename = os.path.join('logs', f'{base_name}_{n}.log')
        if not os.path.exists(log_filename):
            return log_filename
        n += 1


def main():
    logging.basicConfig(filename=get_log_filename('robot'),  
                        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    board = Board()
    cell = board.get_cell(0, 0)
    robot = Robot(cell, board, True, logging)

    
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

