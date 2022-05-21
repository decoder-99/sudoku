# Sudoku Solver

SudokuSolver is a python package for solving Sudoku - one of the most popular logic puzzles.

## Algorithms

-  Breadth-fist search
-  Depth-first search
-  CSP with backtraking (Heuristic is Minimum Remaining Values)
-  Simulated Annealing

## Installation

To solve Sudoku run

```sh
python3 sudoku_solver.py --algorithm=alg --puzzle_number=number
```
> Note: `--algorithm=alg` instead of alg use one of the options - `bfs_tree, dfs_tree, bfs_graph, dfs_graph, sim_anneal, csp`
`--puzzle_number=number` instead of number use one of the options - `1, 2, 3, 4, 5` or add another puzzle into `Puzzles and solutions` directory

## License

MIT
