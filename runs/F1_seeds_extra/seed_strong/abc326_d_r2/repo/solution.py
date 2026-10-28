import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    Cs = data[2]
    letters = "ABC"
    bit = {"A": 1, "B": 2, "C": 4}

    # Row options: for each row i, list of (assignment: list of (col, letter))
    row_opts = []
    for i in range(n):
        opts = []
        for cols in permutations(range(n), 3):
            # cols[k] is column of letters[k]
            pairs = sorted((cols[k], letters[k]) for k in range(3))
            if pairs[0][1] != R[i]:
                continue
            opts.append(tuple(pairs))
        row_opts.append(opts)

    failed = set()
    chosen = []

    def dfs(i, masks):
        if i == n:
            return all(m == 7 for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        # Feasibility: each column needs (3 - popcount) more letters from remaining rows
        rem = n - i
        for j in range(n):
            m = masks[j]
            need = 3 - bin(m).count("1")
            if need > rem:
                failed.add(key)
                return False
        for opt in row_opts[i]:
            ok = True
            new = list(masks)
            for c, L in opt:
                b = bit[L]
                m = new[c]
                if m & b:
                    ok = False
                    break
                if m == 0 and L != Cs[c]:
                    ok = False
                    break
                new[c] = m | b
            if not ok:
                continue
            chosen.append(opt)
            if dfs(i + 1, tuple(new)):
                return True
            chosen.pop()
        failed.add(key)
        return False

    if dfs(0, tuple([0] * n)):
        grid = [["."] * n for _ in range(n)]
        for i, opt in enumerate(chosen):
            for c, L in opt:
                grid[i][c] = L
        out = ["Yes"] + ["".join(r) for r in grid]
        print("\n".join(out))
    else:
        print("No")


main()
