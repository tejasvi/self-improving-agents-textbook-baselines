import sys
from itertools import permutations


def solve(n, R, C):
    letters = "ABC"
    used = [[False] * n for _ in range(3)]
    top = [None] * n
    grid = [["."] * n for _ in range(n)]
    result = [None]

    def rec(i):
        if i == n:
            result[0] = [row[:] for row in grid]
            return True
        for cols in permutations(range(n), 3):
            # cols[k] is the column for letter k (A, B, C)
            ok = True
            for k in range(3):
                if used[k][cols[k]]:
                    ok = False
                    break
            if not ok:
                continue
            # leftmost letter in row must match R[i]
            leftmost = min(range(3), key=lambda k: cols[k])
            if letters[leftmost] != R[i]:
                continue
            # check column top constraints
            newtops = []
            for k in range(3):
                c = cols[k]
                if top[c] is None:
                    if letters[k] != C[c]:
                        ok = False
                        break
                    newtops.append(c)
            if not ok:
                continue
            # apply
            for k in range(3):
                used[k][cols[k]] = True
                grid[i][cols[k]] = letters[k]
            for c in newtops:
                top[c] = True
            if rec(i + 1):
                return True
            for c in newtops:
                top[c] = None
            for k in range(3):
                used[k][cols[k]] = False
                grid[i][cols[k]] = "."
        return False

    if rec(0):
        return result[0]
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
