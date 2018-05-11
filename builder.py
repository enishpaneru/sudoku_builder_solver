import random, math


class Builder():
    board = []
    num_grid = 9
    avail_val = list(range(1, 10))
    start_grid = 4
    cell_map = {0: {'row': [1, 2], 'col': [3, 6]}, 1: {'row': [0, 2], 'col': [4, 7]}, 2: {'row': [0, 1], 'col': [5, 8]},
                3: {'row': [4, 5], 'col': [0, 6]}, 4: {'row': [3, 5], 'col': [1, 7]}, 5: {'row': [3, 4], 'col': [2, 8]},
                6: {'row': [7, 8], 'col': [0, 3]}, 7: {'row': [6, 8], 'col': [1, 4]},
                8: {'row': [6, 7], 'col': [2, 5]}, }
    cell_fill_order = [8, 6, 2, 0, 7, 1, 3, 5, 4]
    loop_limit = 5

    def __init__(self):
        finished_cells = []
        for each in range(self.num_grid):
            self.board.append([])
        while self.cell_fill_order != []:
            loop_limit = self.loop_limit
            current_cell = self.cell_fill_order[-1]
            while loop_limit != 0:
                good_fill = self.fill_cell(current_cell)
                if good_fill:
                    self.cell_fill_order.remove(current_cell)
                    finished_cells.append(current_cell)
                    break
                loop_limit -= 1
            if loop_limit == 0:
                attaching_cell = finished_cells[-1]
                finished_cells.remove(attaching_cell)
                self.cell_fill_order.append(attaching_cell)
                self.board[attaching_cell] = []

    def fill_cell(self, cell_no):
        avail_val = self.avail_val.copy()
        random.shuffle(avail_val)
        for row in range(int(math.sqrt(self.num_grid))):
            self.board[cell_no].append([])
            for col in range(int(math.sqrt(self.num_grid))):
                temp_avail = avail_val.copy()
                while temp_avail != []:
                    random_val = random.choice(temp_avail)
                    is_good = self.good_insert(cell_no, random_val, row, col)
                    if is_good:
                        self.board[cell_no][row].append(random_val)
                        avail_val.remove(random_val)
                        break
                    else:
                        temp_avail.remove(random_val)
                if temp_avail == []:
                    self.board[cell_no] = []
                    return False
        return True

    def good_insert(self, cell_no, random_val, row, col):
        for row_peer in self.cell_map[cell_no]['row']:
            if self.board[row_peer] != [] and random_val in self.board[row_peer][row]:
                return False
        for col_peer in self.cell_map[cell_no]['col']:
            if self.board[col_peer] != [] and random_val in [val[col] for val in self.board[col_peer]]:
                return False
        return True

    def get_grid(self):
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

    def obtain_puzzle(self):
        temp_board = self.board.copy()
        for cell in self.board:
            avail_val = self.avail_val.copy()
            num = random.randint(4, 5)
            while num != 0:
                to_rem = random.choice(avail_val)
                for i in range(3):
                    for j in range(3):
                        if cell[i][j] == to_rem:
                            cell[i][j] = '.'
                            avail_val.remove(to_rem)
                            num -= 1
