import os
import sys
import pathlib
from argparse import ArgumentParser
from sudoku_puzzle import Sudoku, BoardTerminalTest, PuzzlePrinting
from csp_with_backtracking import CSPSudoku
from simulated_annealing import SimulatedAnnealing
from uninformed_search import BreadthFirstFrontier, DepthFirstFrontier, TreeSearch, GraphSearch


def get_puzzle(num):
    parent_path = pathlib.Path(__file__).parent.resolve()
    test_path = os.path.join(parent_path, "Puzzles and solutions", "{}.txt".format(num))
    with open(test_path) as f:
        test_puzzle = []
        sudoku_lines = f.readlines()
        for line in sudoku_lines:
            test_puzzle.extend([int(num) for num in line.split()])
    return test_puzzle


def parse_args():
    parser = ArgumentParser(description='solve Sudoku puzzle')
    parser.add_argument('-a', '--algorithm', required=True, help='algorithm for solving Sudoku, '
                                                                 '[bfs_tree, dfs_tree, bfs_graph, dfs_graph, sim_anneal, csp]')
    parser.add_argument('-n', '--puzzle_number', required=True,
                        help='number of puzzle to solve')
    args = parser.parse_args(sys.argv[1:])

    puzzle = get_puzzle(args.puzzle_number)
    sudoku_puzzle = Sudoku(puzzle)
    goal_test = BoardTerminalTest()

    print("Solution for Sudoku puzzle - {}".format(args.puzzle_number))
    print("Oirignal puzzle")
    PuzzlePrinting.print_state(sudoku_puzzle)
    print("Solved puzzle")

    if args.algorithm == "bfs_tree":
        frontier = BreadthFirstFrontier()
        tree = TreeSearch(frontier)
        solution = tree.find_solution(init_state=sudoku_puzzle, goal_test=goal_test)
        PuzzlePrinting.print_solution(solution)

    if args.algorithm == "bfs_graph":
        frontier = BreadthFirstFrontier()
        graph = GraphSearch(frontier)
        solution = graph.find_solution(init_state=sudoku_puzzle, goal_test=goal_test)
        PuzzlePrinting.print_solution(solution)

    if args.algorithm == "dfs_tree":
        frontier = DepthFirstFrontier()
        tree = TreeSearch(frontier)
        solution = tree.find_solution(init_state=sudoku_puzzle, goal_test=goal_test)
        PuzzlePrinting.print_solution(solution)

    if args.algorithm == "dfs_graph":
        frontier = DepthFirstFrontier()
        graph = GraphSearch(frontier)
        solution = graph.find_solution(init_state=sudoku_puzzle, goal_test=goal_test)
        PuzzlePrinting.print_solution(solution)

    if args.algorithm == "sim_anneal":
        solution = SimulatedAnnealing(sudoku_puzzle).get_solution()
        PuzzlePrinting.print_state(solution)

    if args.algorithm == "csp":
        solution = CSPSudoku(sudoku_puzzle).backtracking_with_heuristic()
        PuzzlePrinting.print_state(solution)


parse_args()


