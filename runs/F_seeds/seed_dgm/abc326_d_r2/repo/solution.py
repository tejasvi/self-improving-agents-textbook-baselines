import sys
from itertools import permutations


def solve(n, R, C):
    letters = "ABC"
    # used[j] = set of letters already placed in column j
    used = [set() for _ in range(n)]
    # top[j] = letter at top of column j (None if column empty so far)
    top = [None] * n
    grid = [["."] * n for _ in range(n)]

    def dfs(i):
        if i == n:
            return all(len(u) == 3 for u in used)
        for cols in permutations(range(n), 3):
            # cols[k] is the column for letters[k]
            ok = True
            for k in range(3):
                j = cols[k]
                if letters[k] in used[j]:
                    ok = False
                    break
            if not ok:
                continue
            # Leftmost letter in row i must be R[i]
            leftmost_col = min(cols)
            leftmost_letter = letters[cols.index(leftmost_col)]
            if leftmost_letter != R[i]:
                continue
            # Topmost letter in each column touched for the first time must be C[j]
            bad = False
            for k in range(3):
                j = cols[k]
                if not used[j] and letters[k] != C[j]:
                    bad = True
                    break
            if bad:
                continue
            # Place
            firsts = []
            for k in range(3):
                j = cols[k]
                if not used[j]:
                    firsts.append(j)
                used[j].add(letters[k])
                grid[i][j] = letters[k]
            if dfs(i + 1):
                return True
            for k in range(3):
                j = cols[k]
                used[j].discard(letters[k])
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
        print("Yes")
        print("\n".join(res))


if __name__ == "__main__":
    main()
