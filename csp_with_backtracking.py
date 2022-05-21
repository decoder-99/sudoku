from copy import deepcopy
from sudoku_puzzle import Sudoku, PuzzlePrinting

class CSPSudoku:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.variables = [i for i in range(sudoku.size*sudoku.size+1)]
        self.fixed = sudoku.get_fixed_board()
        self.domains = self._get_domains(sudoku)
        CSPSudoku.num_of_calls = 0

    @staticmethod
    def get_num_of_calls():
        return CSPSudoku.num_of_calls

    def _get_domains(self, puzzle):
        dom = {}
        for row in range(9):
            for col in range(9):
                if self.fixed[row * 9 + col] == 0:
                    dom_ = []
                    for val in range(1, 10):
                        if puzzle.check_col(col, val) and puzzle.check_row(row, val) and puzzle.check_square(row, col, val):
                            dom_.append(val)
                    dom[(row, col)] = dom_
        return dom

    def MRV_heuristic(self, domains):
        actions = list()
        min_val_num = 9
        for var, vals in domains.items():
            if len(vals) < min_val_num and len(vals) != 0:
                min_val_num = len(vals)
        for var, vals in domains.items():
            if len(vals) == min_val_num:
                for val in vals:
                    row, col, val = var[0], var[1], val
                    actions.append((row, col, val))
        return actions

    def backtracking(self, puzzle, domains, heuristic):
        CSPSudoku.num_of_calls += 1
        actions = heuristic(self._get_domains(puzzle))
        if len(actions) == 0:
            return True, puzzle

        for action in actions:
            if puzzle.is_valid_val(action[0], action[1], action[2]):
                puzzle.set_cell_val(action[0], action[1], action[2])
                if self.backtracking(puzzle, domains, heuristic):
                    return True, puzzle
            puzzle.set_cell_val(action[0], action[1], 0)
        return False, None

    def backtracking_with_heuristic(self):
        CSPSudoku.num_of_calls = 0
        puzzle = deepcopy(self.sudoku)
        domains = deepcopy(self.domains)
        is_find, solution = self.backtracking(puzzle, domains, self.MRV_heuristic)
        return solution
