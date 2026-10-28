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
    rows = list(R)
    cols = list(C)
    indices = list(range(N))
    # Precompute all permutations of columns for each letter placement (one per row)
    perms = list(itertools.permutations(indices))
    # Iterate over permutations for A, B, C placements
    for permA in perms:
        # Inverse mapping: column -> row for A
        invA = [0] * N
        for i, j in enumerate(permA):
            invA[j] = i
        for permB in perms:
            # In same row, A and B must be in different columns
            conflict = False
            for i in range(N):
                if permB[i] == permA[i]:
                    conflict = True
                    break
            if conflict:
                continue
            invB = [0] * N
            for i, j in enumerate(permB):
                invB[j] = i
            for permC in perms:
                # Ensure each row has distinct columns for A, B, C
                ok = True
                for i in range(N):
                    if permC[i] == permA[i] or permC[i] == permB[i]:
                        ok = False
                        break
                if not ok:
                    continue
                # Inverse mapping for C
                invC = [0] * N
                for i, j in enumerate(permC):
                    invC[j] = i
                # Check leftmost character in each row matches R
                good = True
                for i in range(N):
                    colA = permA[i]
                    colB = permB[i]
                    colC = permC[i]
                    # Find smallest column index among the three letters in this row
                    min_col = colA
                    letter = 'A'
                    if colB < min_col:
                        min_col = colB
                        letter = 'B'
                    if colC < min_col:
                        min_col = colC
                        letter = 'C'
                    if letter != rows[i]:
                        good = False
                        break
                if not good:
                    continue
                # Check topmost character in each column matches C
                for j in range(N):
                    rowA = invA[j]
                    rowB = invB[j]
                    rowC = invC[j]
                    min_row = rowA
                    letter = 'A'
                    if rowB < min_row:
                        min_row = rowB
                        letter = 'B'
                    if rowC < min_row:
                        min_row = rowC
                        letter = 'C'
                    if letter != cols[j]:
                        good = False
                        break
                if not good:
                    continue
                # All conditions satisfied – build the grid
                grid = [['.' for _ in range(N)] for _ in range(N)]
                for i in range(N):
                    grid[i][permA[i]] = 'A'
                    grid[i][permB[i]] = 'B'
                    grid[i][permC[i]] = 'C'
                print('Yes')
                for i in range(N):
                    print(''.join(grid[i]))
                return
    print('No')

if __name__ == "__main__":
    solve()
