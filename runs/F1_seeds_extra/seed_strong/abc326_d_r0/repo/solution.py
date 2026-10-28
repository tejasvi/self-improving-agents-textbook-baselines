import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    L = "ABC"
    rc = [L.index(ch) for ch in R]
    cc = [L.index(ch) for ch in C]

    # options per row: list of (col_for_letter0, col_for_letter1, col_for_letter2)
    # as placements: tuple of (col, letter) with 3 entries
    opts = []
    for cols in permutations(range(n), 3):
        # cols[k] is the column of letter k
        opts.append(cols)

    failed = set()
    grid = [[-1] * n for _ in range(n)]

    def dfs(i, masks):
        if i == n:
            return all(m == 7 for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        for cols in opts:
            # leftmost cell in row i must be R[i]
            left_col = min(cols)
            if cols[0] == left_col:
                lt = 0
            elif cols[1] == left_col:
                lt = 1
            else:
                lt = 2
            if lt != rc[i]:
                continue
            ok = True
            for letter in range(3):
                j = cols[letter]
                m = masks[j]
                if m & (1 << letter):
                    ok = False
                    break
                if m == 0 and letter != cc[j]:
                    ok = False
                    break
            if not ok:
                continue
            nm = list(masks)
            for letter in range(3):
                j = cols[letter]
                nm[j] |= 1 << letter
                grid[i][j] = letter
            if dfs(i + 1, tuple(nm)):
                return True
            for letter in range(3):
                grid[i][cols[letter]] = -1
        failed.add(key)
        return False

    if not dfs(0, tuple([0] * n)):
        print("No")
        return
    out = ["Yes"]
    for i in range(n):
        out.append("".join("." if v < 0 else L[v] for v in grid[i]))
    print("\n".join(out))


main()
