import sys
from itertools import permutations


def solve(n, R, C):
    L = {'A': 0, 'B': 1, 'C': 2}
    LET = 'ABC'
    pc = [bin(m).count('1') for m in range(8)]
    failed = set()
    rows = []

    def dfs(i, masks):
        if i == n:
            return all(m == 7 for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        remaining = n - i - 1
        target = L[R[i]]
        for pa, pb, pp in permutations(range(n), 3):
            pos = (pa, pb, pp)
            # leftmost letter must match R[i]
            mn = min(pos)
            leftmost = pos.index(mn)
            if leftmost != target:
                continue
            ok = True
            nm = list(masks)
            for letter in range(3):
                j = pos[letter]
                bit = 1 << letter
                if nm[j] & bit:
                    ok = False
                    break
                if nm[j] == 0 and C[j] != LET[letter]:
                    ok = False
                    break
                nm[j] |= bit
            if not ok:
                continue
            if any(3 - pc[m] > remaining for m in nm):
                continue
            rows.append(pos)
            if dfs(i + 1, tuple(nm)):
                return True
            rows.pop()
        failed.add(key)
        return False

    if dfs(0, tuple([0] * n)):
        grid = [['.'] * n for _ in range(n)]
        for i, pos in enumerate(rows):
            for letter in range(3):
                grid[i][pos[letter]] = LET[letter]
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
