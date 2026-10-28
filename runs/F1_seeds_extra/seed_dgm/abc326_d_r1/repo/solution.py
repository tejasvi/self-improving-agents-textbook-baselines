import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    letters = "ABC"

    # All valid row patterns: exactly one A, one B, one C, rest empty.
    patterns = []
    for pos in permutations(range(n), 3):
        row = ['.'] * n
        for k in range(3):
            row[pos[k]] = letters[k]
        patterns.append(row)

    # Pre-filter by leftmost character requirement for each row.
    def leftmost(row):
        for ch in row:
            if ch != '.':
                return ch
        return None

    cand = {}
    for i in range(n):
        cand[i] = [p for p in patterns if leftmost(p) == R[i]]

    bit = {'A': 1, 'B': 2, 'C': 4}
    grid = [None] * n
    colmask = [0] * n  # letters already used in each column

    def solve(i):
        if i == n:
            return all(m == 7 for m in colmask)
        for p in cand[i]:
            ok = True
            changed = []
            for j in range(n):
                ch = p[j]
                if ch == '.':
                    continue
                b = bit[ch]
                if colmask[j] & b:
                    ok = False
                    break
                if colmask[j] == 0 and ch != C[j]:
                    ok = False
                    break
                colmask[j] |= b
                changed.append((j, b))
            if ok:
                grid[i] = p
                if solve(i + 1):
                    return True
            for j, b in changed:
                colmask[j] &= ~b
        return False

    if solve(0):
        out = ["Yes"] + ["".join(r) for r in grid]
        print("\n".join(out))
    else:
        print("No")


main()
