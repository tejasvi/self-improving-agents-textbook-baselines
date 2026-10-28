import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    L = "ABC"
    bit = {"A": 1, "B": 2, "C": 4}

    # Row patterns: for each row, placements of A, B, C in distinct cells,
    # with leftmost letter equal to R[i].
    patterns = []
    for cols in permutations(range(n), 3):
        # cols[k] is the column of letter L[k]
        row = ["."] * n
        for k in range(3):
            row[cols[k]] = L[k]
        leftmost = min(range(3), key=lambda k: cols[k])
        patterns.append((cols, row, L[leftmost]))

    sys.setrecursionlimit(10000)
    failed = set()
    chosen = []

    def dfs(i, masks):
        if i == n:
            return all(m == 7 for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        for cols, row, lm in patterns:
            if lm != R[i]:
                continue
            ok = True
            new = list(masks)
            for k in range(3):
                j = cols[k]
                x = L[k]
                b = bit[x]
                if masks[j] & b:
                    ok = False
                    break
                if masks[j] == 0 and x != C[j]:
                    ok = False
                    break
                new[j] |= b
            if not ok:
                continue
            # Remaining rows must be able to supply missing letters.
            rem = n - i - 1
            if any(3 - bin(m).count("1") > rem for m in new):
                continue
            chosen.append(row)
            if dfs(i + 1, tuple(new)):
                return True
            chosen.pop()
        failed.add(key)
        return False

    if dfs(0, tuple([0] * n)):
        out = ["Yes"] + ["".join(r) for r in chosen]
        print("\n".join(out))
    else:
        print("No")


main()
