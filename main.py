import os
import time
from Board import Board
from Robot import Robot
from Client import Client

def main():
    board = Board()
    cell = board.get_cell(0, 0)
    robot = Robot(cell, board)
    client = Client()
    prev = client.get_data()

    while board.visited_cells != board.total_cells:
        sensor_data = client.get_data()
        is_stepped = robot.make_step()
        print(f"{board.visited_cells} / {board.total_cells}")
        if not is_stepped:
            robot.return_back_to_crossroad()
        prev = sensor_data

    sensor_data = client.get_data()
    dist = [
        sensor_data['front_distance'],
        sensor_data['right_side_distance'],
        sensor_data['back_distance'],
        sensor_data['left_side_distance']
    ]
    robot.analyze_data(dist)

    matrix = board.board_to_code_matrix()
    for row in matrix:
        print(" ".join(map(str, row)))

    client.send_matrix(matrix)


if __name__ == "__main__":
    os.system("pip install requests")
    time.sleep(10)
    main()

