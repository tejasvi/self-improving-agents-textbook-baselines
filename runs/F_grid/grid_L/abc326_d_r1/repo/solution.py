import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    Cs = data[2]
    bit = {'A': 1, 'B': 2, 'C': 4}
    letters = 'ABC'
    full = 7

    # Row options: list of (grid_row_string, list of (col, letter_bit)) for placements
    # Each row: choose 3 distinct columns for A,B,C (each letter exactly once)
    row_opts = {}
    for ch in 'ABC':
        opts = []
        for cols in permutations(range(n), 3):
            # cols[k] is column for letter letters[k]
            cells = [(cols[k], letters[k]) for k in range(3)]
            leftmost = min(cells, key=lambda t: t[0])[1]
            if leftmost == ch:
                opts.append(cells)
        row_opts[ch] = opts

    failed = set()
    colmask = [0] * n
    choice = [None] * n

    def dfs(i):
        if i == n:
            return all(m == full for m in colmask)
        key = (i, tuple(colmask))
        if key in failed:
            return False
        for cells in row_opts[R[i]]:
            ok = True
            changed = []
            for col, L in cells:
                b = bit[L]
                if colmask[col] & b:
                    ok = False
                    break
                if colmask[col] == 0 and L != Cs[col]:
                    ok = False
                    break
            if ok:
                # check: each column's remaining missing letters fit remaining rows
                for col, L in cells:
                    colmask[col] |= bit[L]
                    changed.append(col)
                rem = n - i - 1
                feasible = True
                for c in range(n):
                    missing = 3 - bin(colmask[c]).count('1')
                    if missing > rem:
                        feasible = False
                        break
                if feasible:
                    choice[i] = cells
                    if dfs(i + 1):
                        return True
                for col, L in cells:
                    colmask[col] &= ~bit[L]
        failed.add(key)
        return False

    if not dfs(0):
        print("No")
        return
    grid = [['.'] * n for _ in range(n)]
    for i in range(n):
        for col, L in choice[i]:
            grid[i][col] = L
    out = ["Yes"] + ["".join(r) for r in grid]
    print("\n".join(out))


main()
