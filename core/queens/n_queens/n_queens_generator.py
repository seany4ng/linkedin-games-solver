import random

def random_n_queens_solution(n: int):
    """
    Returns a random valid n-Queens solution in the form of a 1D integer array
    of length n, where the value at index i is the column of the queen in row i.
    If no solution exists (e.g., n=2 or n=3), returns an empty list.
    """
    solutions = []
    board = [-1] * n  # board[i] = column of queen in row i

    def is_safe(row, col):
        for r in range(row):
            # Same column or on the same diagonal
            if board[r] == col or abs(board[r] - col) == abs(r - row):
                return False
        return True

    def backtrack(row):
        if row == n:
            # Found a valid solution; store a copy
            solutions.append(board[:])
            return
        # Try every column in this row
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Reset before trying next column

    # 1. Find all solutions
    backtrack(0)

    # Write to File
    with open(str(n)+'_queens_solutions.txt', 'w') as f:
        for solution in solutions:
            solution_formatted = ' '.join(map(str, solution)) 
            f.write(solution_formatted + '\n')

for i in range(7, 11):
    random_n_queens_solution(i)
