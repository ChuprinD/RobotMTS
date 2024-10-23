from Cell import Cell

class Board:
    def __init__(self):
        self.total_cells = 16 * 16
        self.visited_cells = 0
        self.matrix = []
        for i in range(15, -1, -1):
            row = []
            for j in range(16):
                row.append(Cell(i, j))
            self.matrix.append(row)

    def get_cell_size(self):
        return self.matrix[0][0].get_size()

    def get_cell(self, y, x):
        return self.matrix[15 - y][x]

    def visit_cell(self, cell):
        cell.visited = True
        self.visited_cells += 1

    def board_to_code_matrix(self):
        ans = [[0 for _ in range(16)] for _ in range(16)]
        for i in range(16):
            for j in range(16):
                ans[i][j] = self.matrix[i][j].get_code()
        return ans