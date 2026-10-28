import sys
from itertools import permutations


def solve(N, R, C):
    letters = "ABC"
    # colmask[j]: bitmask of letters already placed in column j (bit k for letters[k])
    # colfirst[j]: whether column j has any letter placed (equivalent to colmask != 0)
    colmask = [0] * N
    grid = [["."] * N for _ in range(N)]
    full = 7

    def row_options(i):
        opts = []
        for cols in permutations(range(N), 3):
            # cols[k] = column of letter k
            # leftmost letter must be R[i]
            order = sorted(range(3), key=lambda k: cols[k])
            if letters[order[0]] != R[i]:
                continue
            opts.append(cols)
        return opts

    options = [row_options(i) for i in range(N)]

    def dfs(i):
        if i == N:
            return all(m == full for m in colmask)
        remaining = N - i - 1  # rows after this one
        for cols in options[i]:
            ok = True
            # check placements
            for k in range(3):
                j = cols[k]
                bit = 1 << k
                if colmask[j] & bit:
                    ok = False
                    break
                if colmask[j] == 0 and letters[k] != C[j]:
                    ok = False
                    break
            if not ok:
                continue
            # apply
            for k in range(3):
                colmask[cols[k]] |= 1 << k
            # prune: each column's missing letters must fit in remaining rows
            good = True
            for j in range(N):
                missing = 3 - bin(colmask[j]).count("1")
                if missing > remaining:
                    good = False
                    break
            if good:
                for k in range(3):
                    grid[i][cols[k]] = letters[k]
                if dfs(i + 1):
                    return True
                for k in range(3):
                    grid[i][cols[k]] = "."
            for k in range(3):
                colmask[cols[k]] &= ~(1 << k)
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
        out = ["Yes"] + res
        print("\n".join(out))


if __name__ == "__main__":
    main()
