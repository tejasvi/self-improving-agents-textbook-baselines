import sys
from itertools import permutations


def solve(n, R, C):
    grid = [['.'] * n for _ in range(n)]
    # colused[j][k]: letter k already used in column j
    colused = [[False] * 3 for _ in range(n)]
    coltop = [None] * n  # topmost letter of column j (set on first placement)
    letters = 'ABC'

    def dfs(i):
        if i == n:
            return True
        for cols in permutations(range(n), 3):
            # cols[k] = column for letter k
            ok = True
            used_cols = set()
            for k in range(3):
                j = cols[k]
                if colused[j][k]:
                    ok = False
                    break
            if not ok:
                continue
            # leftmost letter of row i must be R[i]
            left = min(cols)
            if letters[cols.index(left)] != R[i]:
                continue
            # topmost letter for each column must match C[j] when first placed
            for k in range(3):
                j = cols[k]
                if coltop[j] is None and letters[k] != C[j]:
                    ok = False
                    break
            if not ok:
                continue
            # apply
            changed = []
            for k in range(3):
                j = cols[k]
                if coltop[j] is None:
                    coltop[j] = letters[k]
                    changed.append((j, True))
                else:
                    changed.append((j, False))
                colused[j][k] = True
                grid[i][j] = letters[k]
            if dfs(i + 1):
                return True
            for k in range(3):
                j = cols[k]
                colused[j][k] = False
                grid[i][j] = '.'
                if changed[k][1]:
                    coltop[j] = None
        return False

    if dfs(0):
        return grid
    return None


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    res = solve(n, R, C)
    if res is None:
        print("No")
    else:
        out = ["Yes"] + ["".join(row) for row in res]
        print("\n".join(out))


if __name__ == "__main__":
    main()
