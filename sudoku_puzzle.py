from collections import deque, Counter
from copy import deepcopy


class State:
    def get_applicable_actions(self):
        pass

    def get_action_result(self, action):
        pass

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass


class Add:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val


class Sudoku(State):
    EMPTY = 0

    def __init__(self, board=None):
        self.size = 9
        self._fixed_board = [Sudoku.EMPTY] * (self.size * self.size)
        if board is None:
            self._board = [Sudoku.EMPTY] * (self.size * self.size)
        else:
            self._board = deepcopy(board)
        for i in range(self.size * self.size):
            if self._board[i] != 0:
                self._fixed_board[i] = 1

    def get_board(self):
        return self._board

    def get_cell(self, row, col):
        return self._board[row * self.size + col]

    def get_cell_by_ind(self, ind):
        return self._board[ind]

    def set_cell_val(self, row, col, val):
        self._board[row * self.size + col] = val

    def set_cell_val_by_ind(self, ind, val):
        self._board[ind] = val

    def find_first_empty_slot(self):
        for row in range(self.size):
            for col in range(self.size):
                if self._board[row * self.size + col] == 0:
                    return row, col
        return -1, -1

    def check_row(self, row, value):
        for col in range(self.size):
            if value == self._board[row * self.size + col]:
                return False
        return True

    def check_col(self, col, value):
        for row in range(self.size):
            if value == self._board[row * self.size + col]:
                return False
        return True

    def check_square(self, row, col, value):
        square_row_start = (row // 3) * 3
        square_col_start = (col // 3) * 3
        for row in range(square_row_start, square_row_start + 3):
            for col in range(square_col_start, square_col_start + 3):
                if self._board[row * self.size + col] == value:
                    return False
        return True

    def get_square_values(self, row, col):
        square_values = []
        row_offset = (row // 3) * 3
        col_offset = (col // 3) * 3

        for r in range(row_offset, row_offset + 3):
            for c in range(col_offset, col_offset + 3):
                if self._board[r * self.size + c] != 0:
                    square_values.append(self._board[r * self.size + c])
        return square_values

    def get_applicable_actions(self):
        actions = set()
        row, col = self.find_first_empty_slot()
        for val in range(1, 10):
            if self.check_square(row, col, val) and self.check_row(row, val) and self.check_col(col, val):
                actions.add(Add(row, col, val))
        return actions

    def is_valid_val(self, row, col, val):
        if self.check_square(row, col, val) and self.check_row(row, val) and self.check_col(col, val):
            return True
        return False

    def is_valid_board(self):
        for row in range(9):
            count_values = Counter([self._board[row * 9 + col] for col in range(9)])
            for val, count in count_values.items():
                if count > 1 and val != 0:
                    print(val)
                    return False

        for col in range(9):
            count_values = Counter([self._board[row * 9 + col] for row in range(9)])
            for val, count in count_values.items():
                if count > 1 and val != 0:
                    print(val)
                    return False

        for row in range(0, 9):
            for col in range(0, 9):
                count_values = Counter(self.get_square_values(row, col))
                for val, count in count_values.items():
                    if count > 1 and val != 0:
                        return False
        return True

    def get_action_result(self, add):
        new_board = self._board.copy()
        new_board[add.row * self.size + add.col] = add.val
        result = Sudoku(new_board)
        return result

    def get_fixed_board(self):
        return self._fixed_board

    def __eq__(self, other):
        return self._board == other.get_board()

    def __hash__(self):
        return hash(tuple(self._board))


class GoalTest:
    def is_goal(self, state):
        pass


class BoardTerminalTest(GoalTest):
    def is_goal(self, state):
        for row in range(9):
            for col in range(9):
                if state.get_cell(row, col) == 0:
                    return False
        return True


class Printing:
    @classmethod
    def print_solution(cls, solution):
        if not solution:
            print('No solution found!')
        else:
            stack = deque()
            node = solution
            while node:
                stack.append(node)
                node = node.parent
            stepNo = 0
            while stack:
                node = stack.pop()
                print(stepNo, end='')
                stepNo += 1
                if not node.parent:
                    print(': start')
                else:
                    print(': ', end='')
                    cls.print_action(node.action)
                    print()
                print()
                cls.print_state(node.state)
                print()

    @staticmethod
    def print_action(action):
        pass

    @staticmethod
    def print_state(state):
        pass


class PuzzlePrinting(Printing):
    @staticmethod
    def print_action(add):
        print('add value {} to {} row and {} col'.format(add.val, add.row, add.col), sep='', end='')

    @staticmethod
    def print_state(board):
        print('-' * 25, end='\n')
        for row in range(board.size):
            print('|', end=' ')
            c_count = 0
            for col in range(board.size):
                print(board.get_cell(row, col), end=' ')
                if c_count in [2, 5, 8]:
                    print('|', end=' ')
                c_count += 1
            print()
            if row in [2, 5, 8]:
                print('-' * 25, end='\n')
