import sys
from itertools import permutations

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); R = data[1]; C = data[2]
    full = (1 << n) - 1
    L = "ABC"
    failed = set()
    choice = [None] * n

    def dfs(i, masks):
        if i == n:
            return all(m == full for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        union = masks[0] | masks[1] | masks[2]
        for a, b, c in permutations(range(n), 3):
            cols = (a, b, c)
            ok = True
            for k in range(3):
                j = cols[k]
                if masks[k] >> j & 1:
                    ok = False; break
                if not (union >> j & 1) and L[k] != C[j]:
                    ok = False; break
            if not ok:
                continue
            # leftmost filled cell in this row must match R[i]
            left = min(cols)
            k_left = cols.index(left)
            if L[k_left] != R[i]:
                continue
            nm = tuple(masks[k] | (1 << cols[k]) for k in range(3))
            choice[i] = cols
            if dfs(i + 1, nm):
                return True
        failed.add(key)
        return False

    if not dfs(0, (0, 0, 0)):
        print("No")
        return
    grid = [["."] * n for _ in range(n)]
    for i in range(n):
        for k in range(3):
            grid[i][choice[i][k]] = L[k]
    print("Yes")
    for row in grid:
        print("".join(row))

main()
