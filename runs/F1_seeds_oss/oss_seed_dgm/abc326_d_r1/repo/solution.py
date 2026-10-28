# Write your solution here. Read from stdin, write to stdout.

import sys
from itertools import permutations

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    R = data[1].strip()
    C = data[2].strip()

    # Grid of characters, '.' for empty cells
    grid = [['.' for _ in range(N)] for _ in range(N)]
    # For each column, keep set of letters already placed there
    col_letters = [set() for _ in range(N)]

    # All possible assignments of distinct columns for (A, B, C) in a row
    all_triples = list(permutations(range(N), 3))  # (colA, colB, colC)

    # Pre‑filter triples for each row according to the leftmost requirement
    row_options = []  # list of list of triples allowed for that row
    for i in range(N):
        left = R[i]
        opts = []
        for colA, colB, colC in all_triples:
            min_col = min(colA, colB, colC)
            if (left == 'A' and colA != min_col) or \
               (left == 'B' and colB != min_col) or \
               (left == 'C' and colC != min_col):
                continue
            opts.append((colA, colB, colC))
        row_options.append(opts)

    sys.setrecursionlimit(10000)

    def dfs(row: int) -> bool:
        if row == N:
            # All rows assigned – every column must contain exactly A, B, C
            return all(s == {'A', 'B', 'C'} for s in col_letters)
        # Simple pruning: remaining rows must be enough to fill missing letters in each column
        rows_left = N - row
        for j in range(N):
            if len(col_letters[j]) + rows_left < 3:
                return False
        # Try each admissible placement for this row
        for colA, colB, colC in row_options[row]:
            # Column constraints for each placed letter
            # A
            if 'A' in col_letters[colA]:
                continue
            if not col_letters[colA] and C[colA] != 'A':
                continue
            # B
            if 'B' in col_letters[colB]:
                continue
            if not col_letters[colB] and C[colB] != 'B':
                continue
            # C
            if 'C' in col_letters[colC]:
                continue
            if not col_letters[colC] and C[colC] != 'C':
                continue
            # Place letters
            grid[row][colA] = 'A'
            grid[row][colB] = 'B'
            grid[row][colC] = 'C'
            col_letters[colA].add('A')
            col_letters[colB].add('B')
            col_letters[colC].add('C')
            if dfs(row + 1):
                return True
            # Backtrack
            grid[row][colA] = '.'
            grid[row][colB] = '.'
            grid[row][colC] = '.'
            col_letters[colA].remove('A')
            col_letters[colB].remove('B')
            col_letters[colC].remove('C')
        return False

    if dfs(0):
        print("Yes")
        for i in range(N):
            print(''.join(grid[i]))
    else:
        print("No")

if __name__ == "__main__":
    solve()
