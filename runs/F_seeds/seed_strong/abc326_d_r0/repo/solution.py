import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    letters = "ABC"
    bit = {"A": 1, "B": 2, "C": 4}
    cbit = [bit[c] for c in C]
    rbit = [bit[c] for c in R]
    # Row patterns: for each row, list of (cells tuple of (col, letter_index)), leftmost letter
    # Enumerate positions for A,B,C: choose 3 distinct columns, ordered by letter.
    from itertools import combinations
    patterns = []
    for cols in combinations(range(n), 3):
        for perm in permutations(range(3)):
            # cell at cols[k] gets letter perm[k]
            cells = [(cols[k], perm[k]) for k in range(3)]
            leftmost = min(cols)
            leftletter = None
            for c, l in cells:
                if c == leftmost:
                    leftletter = l
            patterns.append((cells, leftletter))

    sys.setrecursionlimit(10000)
    failed = set()
    grid = [["."] * n for _ in range(n)]

    def dfs(i, masks):
        if i == n:
            return all(m == 7 for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        for cells, leftletter in patterns:
            if rbit[i] != (1 << leftletter):
                continue
            ok = True
            newmasks = list(masks)
            for c, l in cells:
                b = 1 << l
                m = newmasks[c]
                if m & b:
                    ok = False
                    break
                if m == 0 and b != cbit[c]:
                    ok = False
                    break
                newmasks[c] = m | b
            if not ok:
                continue
            nm = tuple(newmasks)
            if dfs(i + 1, nm):
                for c, l in cells:
                    grid[i][c] = letters[l]
                return True
        failed.add(key)
        return False

    # Fix leftover: rows with no letter placed must not exist; grid is filled on success.
    if dfs(0, tuple([0] * n)):
        out = ["Yes"]
        for r in grid:
            out.append("".join(r))
        print("\n".join(out))
    else:
        print("No")


main()
