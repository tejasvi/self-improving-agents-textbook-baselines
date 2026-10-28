import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    Cs = data[2]

    # Precompute all possible row patterns (exactly one A, B, C) per starting letter.
    row_opts = {ch: [] for ch in "ABC"}
    for cols in permutations(range(n), 3):
        # cols[0] -> A, cols[1] -> B, cols[2] -> C
        row = ['.'] * n
        row[cols[0]] = 'A'
        row[cols[1]] = 'B'
        row[cols[2]] = 'C'
        leftmost = min(cols)
        row_opts[row[leftmost]].append(row)

    # used[j][letter] : whether column j already has this letter
    used = [dict(A=False, B=False, C=False) for _ in range(n)]
    # top[j]: letter at top of column j, None if no letters placed yet
    top = [None] * n
    grid = [None] * n

    sys.setrecursionlimit(10000)

    def dfs(i):
        if i == n:
            return True
        for row in row_opts[R[i]]:
            ok = True
            placed = []
            for j in range(n):
                ch = row[j]
                if ch == '.':
                    continue
                if top[j] is None:
                    if ch != Cs[j]:
                        ok = False
                        break
                if used[j][ch]:
                    ok = False
                    break
                placed.append((j, ch, top[j]))
                used[j][ch] = True
                if top[j] is None:
                    top[j] = ch
            if ok:
                grid[i] = row
                if dfs(i + 1):
                    return True
            # undo
            for j, ch, prev_top in placed:
                used[j][ch] = False
                top[j] = prev_top
        return False

    if dfs(0):
        out = ["Yes"] + ["".join(r) for r in grid]
        print("\n".join(out))
    else:
        print("No")


main()
