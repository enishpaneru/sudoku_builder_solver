import math, random


class Solver():
    def __init__(self, puzzle):
        self.num_grid = puzzle.num_grid
        self.cell_map = puzzle.cell_map
        self.board = self.start_search(puzzle.board)

    def start_search(self, board):
        board = self.constraint_propagation(board)
        if board == False:
            return False
        if self.solved_value_len(board) == 81:
            return board

        _, index = self.get_min_multiple(board)
        for each_val in board[index[0]][index[1]][index[2]]:
            new_board = board.copy()
            new_board[index[0]][index[1]][index[2]] = each_val
            return_value = self.start_search(new_board)
            if return_value is not False:
                return return_value

    def get_min_multiple(self, board):
        multiple_list = []
        for cell_no in range(self.num_grid):
            for row in range(int(math.sqrt(self.num_grid))):
                for col in range(int(math.sqrt(self.num_grid))):
                    if len(board[cell_no][row][col]) > 1:
                        multiple_list.append((len(board[cell_no][row][col]), (cell_no, row, col)))
        return min(multiple_list)

    def constraint_propagation(self, board):
        stalled = False
        while not stalled:
            before = self.solved_value_len(board)
            board = self.perform_elimination(board)
            board = self.fill_in_only_choice(board)
            after = self.solved_value_len(board)
            if before == after:
                stalled = True
            if self.empty_value_reached(board):
                return False

        return board

    def empty_value_reached(self, board):
        for cell_no in range(self.num_grid):
            for row in range(int(math.sqrt(self.num_grid))):
                for col in range(int(math.sqrt(self.num_grid))):
                    if len(board[cell_no][row][col]) == 0:
                        return True
        return False

    def solved_value_len(self, board):
        solved = 0
        for cell_no in range(self.num_grid):
            for row in range(int(math.sqrt(self.num_grid))):
                for col in range(int(math.sqrt(self.num_grid))):
                    if len(board[cell_no][row][col]) == 1:
                        solved += 1
        return solved

    def perform_elimination(self, board):
        for cell_no in range(self.num_grid):
            for row in range(int(math.sqrt(self.num_grid))):
                for col in range(int(math.sqrt(self.num_grid))):
                    if len(board[cell_no][row][col]) == 1:
                        board = self.remove_from_peer(cell_no, row, col, board)
        return board

    def remove_from_peer(self, cell_no, row, col, board):
        value = board[cell_no][row][col]
        for row_peer in self.cell_map[cell_no]['row']:
            for col_val in range(3):
                if value in board[row_peer][row][col_val]:
                    board[row_peer][row][col_val] = board[row_peer][row][col_val].replace(value, '')
        for col_peer in self.cell_map[cell_no]['col']:
            for row_val in range(3):
                if value in board[col_peer][row_val][col]:
                    board[col_peer][row_val][col] = board[col_peer][row_val][col].replace(value, '')

        for cell_row in range(int(math.sqrt(self.num_grid))):
            for cell_col in range(int(math.sqrt(self.num_grid))):
                if value in board[cell_no][cell_row][cell_col] and cell_row != row and cell_col != col:
                    board[cell_no][cell_row][cell_col] = board[cell_no][cell_row][cell_col].replace(value, '')
        return board

    def fill_in_only_choice(self, board):
        for digit in '123456789':
            for cell_no in range(self.num_grid):
                index_list = []
                for row in range(int(math.sqrt(self.num_grid))):
                    for col in range(int(math.sqrt(self.num_grid))):
                        if digit in board[cell_no][row][col]:
                            index_list.append({'cell_no': cell_no, 'row': row, 'col': col})
                if len(index_list) == 1:
                    board[index_list[0]['cell_no']][index_list[0]['row']][index_list[0]['col']] = digit
            for grid_row in range(0, 9, 3):
                for row in range(3):
                    index_list = []
                    for grid_col in range(3):
                        cell_no = grid_row + grid_col
                        for col in range(3):
                            if digit in board[cell_no][row][col]:
                                index_list.append({'cell_no': cell_no, 'row': row, 'col': col})
                    if len(index_list) == 1:
                        board[index_list[0]['cell_no']][index_list[0]['row']][index_list[0]['col']] = digit
            for grid_col in range(3):
                for col in range(3):
                    index_list = []
                    for grid_row in range(0, 9, 3):
                        cell_no = grid_row + grid_col
                        for row in range(3):
                            if digit in board[cell_no][row][col]:
                                index_list.append({'cell_no': cell_no, 'row': row, 'col': col})
                    if len(index_list) == 1:
                        board[index_list[0]['cell_no']][index_list[0]['row']][index_list[0]['col']] = digit
        return board

    def get_puzzle_grid(self):
        # for i in range(3):
        #     print(self.board[0][i], self.board[1][i], self.board[2][i])
        # for i in range(3):
        #     print(self.board[3][i], self.board[4][i], self.board[5][i])
        # for i in range(3):
        #     print(self.board[6][i], self.board[7][i], self.board[8][i])

        grid = ''
        num = 0
        for k in range(3):
            for i in range(3):

                for j in range(3):
                    cell = num + j
                    for each in self.board[cell][i]:
                        grid += str(each)
            num += 3
        return grid

    def display(self):
        grid = self.get_puzzle_grid()
        print('    ---------------------------------------')
        for grid_row in range(3):
            for row in range(3):
                row_string = '  |  '
                cell_row = grid_row * 3 + row
                for grid_col in range(3):
                    for col in range(3):
                        cell_col = grid_col * 3 + col
                        row_string += grid[cell_row * 9 + cell_col] + '  '
                    row_string += '  |  '
                print(row_string)
            print('    ---------------------------------------')
        print("\n\n")