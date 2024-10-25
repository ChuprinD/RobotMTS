import json
from Cell import Cell

class Board:
    def __init__(self):
        self.board_size = 16
        self.total_cells = self.board_size  * self.board_size 
        self.visited_cells = 0
        self.matrix = []
        for i in range(self.board_size - 1, -1, -1):
            row = []
            for j in range(self.board_size ):
                row.append(Cell(i, j))
            self.matrix.append(row)

    def print_board(self, robot):
        for i in range(self.board_size ):
            for j in range(self.board_size ):
                cell = self.matrix[i][j]
                top_wall = "───" if cell.top_wall else "   "
                print(f"+{top_wall}", end="")
            print("+")
            
            for j in range(self.board_size ):
                cell = self.matrix[i][j]
                left_wall = "│" if cell.left_wall else " "
                if robot.cur_cell.x == cell.x and robot.cur_cell.y == cell.y:
                    content = "R"
                else:
                    content = " "
                print(f"{left_wall} {content} ", end="")
            print("│")
                
        for j in range(self.board_size ):
            bottom_wall = "───" if self.matrix[15][j].bottom_wall else "   "
            print(f"+{bottom_wall}", end="")
        print("+") 

    def remove_wall(self, cell1, cell2):
        dx = cell1.x - cell2.x
        dy = cell1.y - cell2.y 

        if dx == -1:  # Right wall
            cell1.right_wall = False
            cell2.left_wall = False
        elif dx == 1:  # Left wall
            cell1.left_wall = False
            cell2.right_wall = False
        elif dy == 1:  # Bottom wall
            cell1.bottom_wall = False
            cell2.top_wall = False
        elif dy == -1:  # Top wall
            cell1.top_wall = False
            cell2.bottom_wall = False

    def save_matrix_to_json(self, filename):
        matrix_dict = [[cell.to_dict() for cell in row] for row in self.matrix]
        with open(filename, 'w') as f:
            json.dump(matrix_dict, f)

    def load_matrix_from_json(self, filename):
        with open(filename, 'r') as f:
            matrix_dict = json.load(f)
        self.matrix = [[Cell(**cell_dict) for cell_dict in row] for row in matrix_dict]

    def get_cell_size(self):
        return self.matrix[0][0].get_size()

    def get_cell(self, y, x):
        return self.matrix[self.board_size - 1 - y][x]

    def visit_cell(self, cell):

        cell.visited = True
        self.visited_cells += 1

    def board_to_code_matrix(self):
        ans = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                ans[i][j] = self.matrix[i][j].get_code()
        return ans