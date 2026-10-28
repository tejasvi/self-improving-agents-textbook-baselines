import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    L = "ABC"
    cidx = {ch: k for k, ch in enumerate(L)}
    Cv = [cidx[ch] for ch in C]
    Rv = [cidx[ch] for ch in R]

    # Precompute for each row: candidate placements (cells[letter] = column)
    # Each row: exactly one of each letter in distinct columns.
    rowopts = []
    for i in range(n):
        opts = []
        for cols in permutations(range(n), 3):
            # cols[k] is the column for letter k
            if min(cols) >= 0:
                first_col = min(cols)
                leftletter = None
                for k in range(3):
                    if cols[k] == first_col:
                        leftletter = k
                if leftletter == Rv[i]:
                    opts.append(cols)
        rowopts.append(opts)

    failed = set()
    grid = [["."] * n for _ in range(n)]
    sys.setrecursionlimit(10000)

    def dfs(r, masks):
        if r == n:
            return all(m == 7 for m in masks)
        key = (r, masks)
        if key in failed:
            return False
        for cols in rowopts[r]:
            ok = True
            newm = list(masks)
            for k in range(3):
                j = cols[k]
                m = newm[j]
                if m & (1 << k):
                    ok = False
                    break
                if m == 0 and Cv[j] != k:
                    ok = False
                    break
                newm[j] = m | (1 << k)
            if not ok:
                continue
            # Remaining rows must be able to fill columns: check counts
            if dfs(r + 1, tuple(newm)):
                for k in range(3):
                    grid[r][cols[k]] = L[k]
                return True
        failed.add(key)
        return False

    if dfs(0, tuple([0] * n)):
        out = ["Yes"] + ["".join(row) for row in grid]
        print("\n".join(out))
    else:
        print("No")


main()
