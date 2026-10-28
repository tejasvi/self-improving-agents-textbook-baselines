# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    R = data[1].strip()
    C = data[2].strip()

    # Prepare structures for backtracking
    permA = [-1] * N
    permB = [-1] * N
    permC = [-1] * N
    usedA = set()
    usedB = set()
    usedC = set()
    # For each column, store the symbol placed at the first (topmost) row where the column gets any symbol.
    # None means not yet assigned.
    first_symbol_in_col = [None] * N

    cols = list(range(N))

    def backtrack(row):
        if row == N:
            # All rows assigned, construct grid
            grid = [['.' for _ in range(N)] for _ in range(N)]
            for i in range(N):
                grid[i][permA[i]] = 'A'
                grid[i][permB[i]] = 'B'
                grid[i][permC[i]] = 'C'
            print('Yes')
            for i in range(N):
                print(''.join(grid[i]))
            return True
        # iterate over possible distinct columns for A, B, C in this row
        # generate all triples of distinct columns respecting unused per symbol
        for colA in cols:
            if colA in usedA:
                continue
            for colB in cols:
                if colB in usedB or colB == colA:
                    continue
                for colC in cols:
                    if colC in usedC or colC == colA or colC == colB:
                        continue
                    # leftmost condition for this row
                    mincol = min(colA, colB, colC)
                    if R[row] == 'A' and colA != mincol:
                        continue
                    if R[row] == 'B' and colB != mincol:
                        continue
                    if R[row] == 'C' and colC != mincol:
                        continue
                    # topmost condition for columns that are still empty
                    ok = True
                    # For each column we are about to fill, if it's the first symbol in that column, it must match C[col]
                    if first_symbol_in_col[colA] is None and C[colA] != 'A':
                        ok = False
                    if first_symbol_in_col[colB] is None and C[colB] != 'B':
                        ok = False
                    if first_symbol_in_col[colC] is None and C[colC] != 'C':
                        ok = False
                    if not ok:
                        continue
                    # Apply assignments
                    permA[row] = colA
                    permB[row] = colB
                    permC[row] = colC
                    usedA.add(colA)
                    usedB.add(colB)
                    usedC.add(colC)
                    # remember which columns got their first symbol now to backtrack correctly
                    newly_filled = []
                    if first_symbol_in_col[colA] is None:
                        first_symbol_in_col[colA] = 'A'
                        newly_filled.append(colA)
                    if first_symbol_in_col[colB] is None:
                        first_symbol_in_col[colB] = 'B'
                        newly_filled.append(colB)
                    if first_symbol_in_col[colC] is None:
                        first_symbol_in_col[colC] = 'C'
                        newly_filled.append(colC)
                    if backtrack(row + 1):
                        return True
                    # backtrack undo
                    for c in newly_filled:
                        first_symbol_in_col[c] = None
                    usedA.remove(colA)
                    usedB.remove(colB)
                    usedC.remove(colC)
                    permA[row] = permB[row] = permC[row] = -1
        return False

    if not backtrack(0):
        print('No')

if __name__ == "__main__":
    solve()
