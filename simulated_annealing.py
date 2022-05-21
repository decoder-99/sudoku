import random
import statistics
from math import exp
from copy import deepcopy
from collections import Counter
from sudoku_puzzle import Sudoku, PuzzlePrinting


class SimulatedAnnealing:
    def __init__(self, puzzle, decrease_factor=0.9999, num_of_iterations=400000):
        self._sudoku = puzzle
        self._decrease_factor = decrease_factor
        self._num_of_iterations = num_of_iterations
        SimulatedAnnealing.num_of_calls = 0

    @staticmethod
    def get_num_of_calls():
        return SimulatedAnnealing.num_of_calls

    def _get_block_indices(self, block_num):
        row_offset = (block_num // 3) * 3
        col_offset = (block_num % 3) * 3
        indices = [col_offset + (j % 3) + 9 * (row_offset + (j // 3)) for j in range(9)]
        return indices

    def _get_fixed_values(self, indices):
        val = set()
        fixed_board = self._sudoku.get_fixed_board()
        for ind in indices:
            if fixed_board[ind] == 1:
                val.add(self._sudoku.get_cell_by_ind(ind))
        return val

    def _fill_randomly(self):
        random_puzzle = Sudoku(deepcopy(self._sudoku.get_board()))
        for i in range(9):
            block_indices = self._get_block_indices(i)
            fixed_values = self._get_fixed_values(block_indices)
            values = [j for j in range(1, 10) if j not in fixed_values]
            not_fixed_ind = [ind for ind in block_indices if self._sudoku.get_fixed_board()[ind] == 0]
            for ind, val in zip(not_fixed_ind, values):
                random_puzzle.set_cell_val_by_ind(ind, val)
        return random_puzzle

    def _get_t0(self, puzzle):
        costs = []
        for i in range(9):
            candidate = self._get_candidate(puzzle)
            costs.append(self._calc_cost(candidate))
        return statistics.pstdev(costs)

    def _calc_cost(self, board):
        cost = 0
        for row in range(9):
            count_values = Counter([board.get_cell(row, col) for col in range(9)])
            for val, count in count_values.items():
                if count > 1 and val != 0:
                    cost += 1

        for col in range(9):
            count_values = Counter([board.get_cell(row, col) for row in range(9)])
            for val, count in count_values.items():
                if count > 1 and val != 0:
                    cost += 1

        return cost

    def _get_candidate(self, sudoku):
        while True:
            block = random.randint(0, 8)
            block_indices = self._get_block_indices(block)
            ind1, ind2 = random.sample(block_indices, 2)
            if self._sudoku.get_fixed_board()[ind1] == 0 and self._sudoku.get_fixed_board()[ind2] == 0:
                candidate = Sudoku(deepcopy(sudoku.get_board()))
                tmp = candidate.get_cell_by_ind(ind1)
                candidate.set_cell_val_by_ind(ind1, candidate.get_cell_by_ind(ind2))
                candidate.set_cell_val_by_ind(ind2, tmp)
                return candidate

    def get_solution(self):
        SimulatedAnnealing.num_of_calls = 0
        solution = self._fill_randomly()
        best_puzzle = Sudoku(deepcopy(solution.get_board()))
        current_score = self._calc_cost(solution)
        best_score = current_score
        T = self._get_t0(solution)
        count = 0

        while count < self._num_of_iterations:
            SimulatedAnnealing.num_of_calls += 1
            candidate = self._get_candidate(solution)
            candidate_score = self._calc_cost(candidate)
            delta_S = float(current_score - candidate_score)

            if exp((delta_S / T)) > random.random():
                solution = candidate
                current_score = candidate_score

            if current_score < best_score:
                best_puzzle = Sudoku(deepcopy(candidate.get_board()))
                best_score = self._calc_cost(best_puzzle)

            if candidate_score == 0:
                solution = candidate
                break

            T = self._decrease_factor * T
            count += 1

        return solution









