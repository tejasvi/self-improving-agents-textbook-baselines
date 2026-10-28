import sys
from itertools import permutations, combinations


def solve(N, R, C):
    # Enumerate all row patterns: choose 3 distinct positions, assign A,B,C.
    patterns = []
    for pos in combinations(range(N), 3):
        for perm in permutations("ABC"):
            row = ["."] * N
            for p, ch in zip(pos, perm):
                row[p] = ch
            patterns.append(row)

    # colLetters[j] = set of letters already placed in column j
    # colTop[j] = letter at top of column j (None if nothing placed yet)
    grid = [None] * N
    col_used = [set() for _ in range(N)]
    col_top = [None] * N

    def dfs(i):
        if i == N:
            return True
        for row in patterns:
            first = next(ch for ch in row if ch != ".")
            if first != R[i]:
                continue
            ok = True
            for j in range(N):
                ch = row[j]
                if ch == ".":
                    continue
                if ch in col_used[j]:
                    ok = False
                    break
                if col_top[j] is None and ch != C[j]:
                    ok = False
                    break
            if not ok:
                continue
            # apply
            changed = []
            for j in range(N):
                ch = row[j]
                if ch == ".":
                    continue
                col_used[j].add(ch)
                if col_top[j] is None:
                    col_top[j] = ch
                    changed.append(j)
            grid[i] = row
            if dfs(i + 1):
                return True
            for j in range(N):
                ch = row[j]
                if ch == ".":
                    continue
                col_used[j].discard(ch)
            for j in changed:
                col_top[j] = None
        return False

    if dfs(0):
        return grid
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
        out = ["Yes"] + ["".join(r) for r in res]
        print("\n".join(out))


if __name__ == "__main__":
    main()
