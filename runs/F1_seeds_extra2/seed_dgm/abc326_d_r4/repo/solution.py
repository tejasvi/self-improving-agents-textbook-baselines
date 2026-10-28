import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    Cc = data[2]
    letters = "ABC"
    bit = {"A": 1, "B": 2, "C": 4}
    colLetter = [bit[ch] for ch in Cc]  # required top letter bit per column

    # Precompute row options: for each row letter-needed, list of placements.
    # A placement: tuple of (col, letter_index) for the three letters.
    options_for = {}
    for lt in letters:
        opts = []
        for cols in permutations(range(n), 3):
            # cols[k] = column of letter letters[k]
            if min(cols) == cols[letters.index(lt)]:
                opts.append(cols)
        options_for[lt] = opts

    full = 7
    sys.setrecursionlimit(10000)
    failed = set()
    solution_rows = []

    def dfs(i, masks):
        if i == n:
            return all(m == full for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        lt = R[i]
        for cols in options_for[lt]:
            ok = True
            new = list(masks)
            for k in range(3):
                c = cols[k]
                b = bit[letters[k]]
                m = new[c]
                if m & b:
                    ok = False
                    break
                if m == 0 and b != colLetter[c]:
                    ok = False
                    break
                new[c] = m | b
            if not ok:
                continue
            solution_rows.append(cols)
            if dfs(i + 1, tuple(new)):
                return True
            solution_rows.pop()
        failed.add(key)
        return False

    if not dfs(0, tuple([0] * n)):
        print("No")
        return

    grid = [["."] * n for _ in range(n)]
    for i, cols in enumerate(solution_rows):
        for k in range(3):
            grid[i][cols[k]] = letters[k]
    out = ["Yes"] + ["".join(r) for r in grid]
    print("\n".join(out))


main()
