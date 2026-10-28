import sys
from itertools import permutations


def solve(n, R, C):
    # colused[j][k]: letter k used in column j; coltop[j]: top letter of column j or None
    colused = [[False] * 3 for _ in range(n)]
    coltop = [None] * n
    grid = [['.'] * n for _ in range(n)]
    L = "ABC"
    idx = {ch: k for k, ch in enumerate(L)}
    cidx = [idx[c] for c in C]

    def feasible(row_rem):
        # each column needs all letters not yet used; must be <= remaining rows
        for j in range(n):
            missing = sum(1 for k in range(3) if not colused[j][k])
            if missing > row_rem:
                return False
        return True

    def dfs(i):
        if i == n:
            return all(all(colused[j]) for j in range(n))
        if not feasible(n - i):
            return False
        target = idx[R[i]]
        for cols in permutations(range(n), 3):
            # cols[k] = column for letter k
            # leftmost letter in row must be R[i]
            order = sorted(range(3), key=lambda k: cols[k])
            if order[0] != target:
                continue
            ok = True
            for k in range(3):
                j = cols[k]
                if colused[j][k]:
                    ok = False
                    break
                if coltop[j] is None:
                    if k != cidx[j]:
                        ok = False
                        break
                    # column top is k; but must be topmost placed: this is the first letter
            if not ok:
                continue
            # apply
            changed = []
            for k in range(3):
                j = cols[k]
                if coltop[j] is None:
                    coltop[j] = k
                    changed.append((j, True))
                colused[j][k] = True
                grid[i][j] = L[k]
            if dfs(i + 1):
                return True
            for k in range(3):
                j = cols[k]
                colused[j][k] = False
                grid[i][j] = '.'
            for j, _ in changed:
                coltop[j] = None
        return False

    if dfs(0):
        return ["".join(r) for r in grid]
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
        print("Yes")
        print("\n".join(res))


if __name__ == "__main__":
    main()
