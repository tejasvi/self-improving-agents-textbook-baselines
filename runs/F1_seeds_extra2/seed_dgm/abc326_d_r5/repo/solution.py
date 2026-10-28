import sys
from itertools import permutations


def solve(N, R, C):
    letters = "ABC"
    full = 7  # bitmask of A,B,C
    bit = {"A": 1, "B": 2, "C": 4}
    colmask = [0] * N
    colTop = [None] * N
    grid = [["."] * N for _ in range(N)]

    def feasible_cols(rows_left):
        for j in range(N):
            missing = 3 - bin(colmask[j]).count("1")
            if missing > rows_left:
                return False
        return True

    def dfs(i):
        if i == N:
            return all(colmask[j] == full for j in range(N))
        if not feasible_cols(N - i):
            return False
        for cols in permutations(range(N), 3):
            # cols[k] is column for letter letters[k]
            # leftmost cell of the row must match R[i]
            if letters[min(range(3), key=lambda k: cols[k])] != R[i]:
                continue
            ok = True
            for k in range(3):
                j = cols[k]
                L = letters[k]
                if colmask[j] & bit[L]:
                    ok = False
                    break
                if colmask[j] == 0 and C[j] != L:
                    ok = False
                    break
            if not ok:
                continue
            saved = [(colmask[cols[k]], colTop[cols[k]]) for k in range(3)]
            for k in range(3):
                j = cols[k]
                L = letters[k]
                if colmask[j] == 0:
                    colTop[j] = L
                colmask[j] |= bit[L]
                grid[i][j] = L
            if dfs(i + 1):
                return True
            for k in range(3):
                j = cols[k]
                colmask[j], colTop[j] = saved[k]
                grid[i][j] = "."
        return False

    if dfs(0):
        return ["".join(r) for r in grid]
    return None


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    R = data[1]
    C = data[2]
    res = solve(N, R, C)
    if res is None:
        print("No")
    else:
        print("Yes")
        print("\n".join(res))


if __name__ == "__main__":
    main()
