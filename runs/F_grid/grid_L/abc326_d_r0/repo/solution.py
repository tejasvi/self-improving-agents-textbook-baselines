import sys
from itertools import permutations


def solve(n, R, C):
    letters = "ABC"
    # colUsed[j] = set of letters already placed in column j
    colUsed = [set() for _ in range(n)]
    colFirst = [None] * n  # topmost letter in column j
    grid = [["."] * n for _ in range(n)]

    def dfs(i):
        if i == n:
            return True
        for pa, pb, pc in permutations(range(n), 3):
            pos = {"A": pa, "B": pb, "C": pc}
            # leftmost letter in row i must be R[i]
            left = min(pos, key=lambda x: pos[x])
            if left != R[i]:
                continue
            ok = True
            placed = []
            for L in letters:
                j = pos[L]
                if L in colUsed[j]:
                    ok = False
                    break
                # topmost letter in column j must be C[j]
                first = colFirst[j]
                if first is None:
                    if L != C[j]:
                        ok = False
                        break
                placed.append((L, j, first))
            if not ok:
                continue
            # apply
            for L, j, first in placed:
                colUsed[j].add(L)
                if first is None:
                    colFirst[j] = L
                grid[i][j] = L
            if dfs(i + 1):
                return True
            # undo
            for L, j, first in placed:
                colUsed[j].discard(L)
                colFirst[j] = first
                grid[i][j] = "."
        return False

    if dfs(0):
        return ["".join(r) for r in grid]
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
        out = ["Yes"] + res
        print("\n".join(out))


if __name__ == "__main__":
    main()
