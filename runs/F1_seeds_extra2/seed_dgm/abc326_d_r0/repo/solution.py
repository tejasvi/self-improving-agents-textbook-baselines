import sys
from itertools import combinations, permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    Cc = data[2]
    letters = "ABC"
    bit = {"A": 1, "B": 2, "C": 4}
    full = 7

    # column state: (mask, top) where top is letter of topmost written cell or ''
    init_cols = tuple((0, "") for _ in range(n))
    failed = set()
    grid = [["."] * n for _ in range(n)]

    def dfs(r, cols):
        if r == n:
            for j in range(n):
                if cols[j][0] != full or cols[j][1] != Cc[j]:
                    return False
            return True
        key = (r, cols)
        if key in failed:
            return False
        for pos in combinations(range(n), 3):
            for perm in permutations(letters):
                # leftmost written cell in row must be R[r]
                if perm[0] != R[r]:
                    continue
                ok = True
                newcols = list(cols)
                for idx, j in enumerate(pos):
                    ch = perm[idx]
                    mask, top = newcols[j]
                    if mask & bit[ch]:
                        ok = False
                        break
                    if mask == 0:
                        top = ch
                    newcols[j] = (mask | bit[ch], top)
                if not ok:
                    continue
                # leftmost of row: pos[0] gets perm[0], which is R[r]
                # topmost check: columns that just became nonempty are checked at end
                # but also ensure top letter matches when set
                for j in range(n):
                    if newcols[j][1] and cols[j][0] == 0:
                        if newcols[j][1] != Cc[j]:
                            ok = False
                            break
                if not ok:
                    continue
                for idx, j in enumerate(pos):
                    grid[r][j] = perm[idx]
                for j in range(n):
                    if j not in pos:
                        grid[r][j] = "."
                if dfs(r + 1, tuple(newcols)):
                    return True
        failed.add(key)
        return False

    if dfs(0, init_cols):
        out = ["Yes"] + ["".join(row) for row in grid]
        print("\n".join(out))
    else:
        print("No")


main()
