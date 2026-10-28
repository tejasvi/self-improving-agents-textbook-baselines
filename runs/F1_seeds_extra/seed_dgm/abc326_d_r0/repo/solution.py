import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    letters = "ABC"
    colTopLetter = list(C)

    failed = set()
    rows_choice = []  # chosen placements per row: list of (letter, col)

    def dfs(i, masks):
        if i == n:
            return all(m == 7 for m in masks)
        key = (i, masks)
        if key in failed:
            return False
        # Prune: remaining rows must be able to fill remaining bits
        for perm in permutations(range(n), 3):
            # perm[k] is the column for letter k (A,B,C)
            # leftmost placed letter must be R[i]
            cols = [(perm[k], k) for k in range(3)]
            cols.sort()
            if letters[cols[0][1]] != R[i]:
                continue
            ok = True
            newmasks = list(masks)
            for k in range(3):
                j = perm[k]
                bit = 1 << k
                m = newmasks[j]
                if m & bit:
                    ok = False
                    break
                if m == 0 and colTopLetter[j] != letters[k]:
                    ok = False
                    break
                newmasks[j] = m | bit
            if not ok:
                continue
            rows_choice.append([(letters[k], perm[k]) for k in range(3)])
            if dfs(i + 1, tuple(newmasks)):
                return True
            rows_choice.pop()
        failed.add(key)
        return False

    if dfs(0, tuple([0] * n)):
        grid = [["."] * n for _ in range(n)]
        for i, placements in enumerate(rows_choice):
            for ch, j in placements:
                grid[i][j] = ch
        out = ["Yes"] + ["".join(r) for r in grid]
        print("\n".join(out))
    else:
        print("No")


main()
