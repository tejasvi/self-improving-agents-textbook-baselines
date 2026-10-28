# Write your solution here. Read from stdin, write to stdout.

import sys
import itertools

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    R = data[1].strip()
    C = data[2].strip()
    # Map letters to indices
    letter_to_idx = {'A': 0, 'B': 1, 'C': 2}
    idx_to_letter = ['A', 'B', 'C']

    # Grid initialized with '.'
    grid = [['.' for _ in range(N)] for _ in range(N)]
    # used[col][letter] -> bool whether column col already has that letter
    used = [[False] * 3 for _ in range(N)]
    # first_filled[col] = None if column has no letters yet, else row index of topmost letter
    first_filled = [None] * N

    # counts per column per letter (0 or 1)
    col_counts = [[0] * 3 for _ in range(N)]

    sys.setrecursionlimit(10000)
    solution = None

    def prune(row):
        """Check if remaining rows can still satisfy column requirements."""
        remaining = N - row - 1  # rows after current row are still free
        for col in range(N):
            for l in range(3):
                need = 1 - col_counts[col][l]
                if need > remaining:
                    return False
        return True

    def dfs(row):
        nonlocal solution
        if solution is not None:
            return True
        if row == N:
            # All rows placed, verify each column has exactly one of each letter
            for col in range(N):
                for l in range(3):
                    if col_counts[col][l] != 1:
                        return False
            # Build answer strings
            solution = [''.join(grid[i]) for i in range(N)]
            return True
        # Iterate over all assignments of A,B,C to distinct columns
        for perm in itertools.permutations(range(N), 3):
            cA, cB, cC = perm
            # Determine leftmost column and the letter placed there
            leftmost = min(cA, cB, cC)
            if leftmost == cA:
                left_letter = 'A'
            elif leftmost == cB:
                left_letter = 'B'
            else:
                left_letter = 'C'
            if left_letter != R[row]:
                continue
            # Preliminary checks for column constraints
            ok = True
            placements = [(cA, 0), (cB, 1), (cC, 2)]  # (col, letter_idx)
            for col, lidx in placements:
                if used[col][lidx]:
                    ok = False
                    break
                if first_filled[col] is None:
                    # This would be the topmost character in this column
                    if idx_to_letter[lidx] != C[col]:
                        ok = False
                        break
            if not ok:
                continue
            # Apply placements
            for col, lidx in placements:
                grid[row][col] = idx_to_letter[lidx]
                used[col][lidx] = True
                col_counts[col][lidx] += 1
                if first_filled[col] is None:
                    first_filled[col] = row
            # Prune using future possibilities
            if prune(row):
                if dfs(row + 1):
                    return True
            # Undo placements
            for col, lidx in placements:
                grid[row][col] = '.'
                used[col][lidx] = False
                col_counts[col][lidx] -= 1
                # Reset first_filled if we were the first entry in this column
                # Need to recompute: after removal, check if any letter remains in column above current row
                # Since we only ever add rows in increasing order, the only possible remaining entry in this column
                # (if any) would be from a previous row (< row). So if first_filled[col] == row, we set it to None.
                if first_filled[col] == row:
                    first_filled[col] = None
        return False

    dfs(0)
    if solution is None:
        print("No")
    else:
        print("Yes")
        for line in solution:
            print(line)

if __name__ == "__main__":
    solve()
