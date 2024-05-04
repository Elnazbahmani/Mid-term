from z3 import *

# Sudoku instance, use '0' for empty cells
instance = (
    (0, 0, 0, 0, 6, 1, 0, 0, 2),
    (0, 7, 0, 0, 0, 0, 0, 6, 0),
    (9, 2, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 4, 5, 2, 0, 9, 0, 0),
    (0, 8, 2, 1, 0, 4, 6, 3, 0),
    (0, 0, 3, 0, 7, 6, 1, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 9, 8),
    (0, 3, 0, 0, 0, 0, 0, 4, 0),
    (6, 0, 0, 3, 8, 0, 0, 0, 0)
)

# 9x9 matrix of integer variables
cells = [[Int(f"x_{i+1}_{j+1}") for j in range(9)] for i in range(9)]

# Each cell contains a value in {1, ..., 9}
cell_constraints = [And(1 <= cells[i][j], cells[i][j] <= 9) for i in range(9) for j in range(9)]

# Each row contains a digit at most once
row_constraints = [Distinct(cells[i]) for i in range(9)]

# Each column contains a digit at most once
col_constraints = [Distinct([cells[i][j] for i in range(9)]) for j in range(9)]

# Each 3x3 square contains a digit at most once
square_constraints = [Distinct([cells[3*i0 + i][3*j0 + j] for i in range(3) for j in range(3)]) for i0 in range(3) for j0 in range(3)]

# Sudoku constraints
sudoku_constraints = cell_constraints + row_constraints + col_constraints + square_constraints

# Initial values in the Sudoku table
instance_constraints = [cells[i][j] == instance[i][j] for i in range(9) for j in range(9) if instance[i][j] != 0]

# Create solver
solver = Solver()
solver.add(sudoku_constraints + instance_constraints)

if solver.check() == sat:
    model = solver.model()
    solution = [[model.evaluate(cells[i][j]).as_long() for j in range(9)] for i in range(9)]
    print("Sudoku Solution:")
    for row in solution:
        print(row)
else:
    print("No solution exists.")
