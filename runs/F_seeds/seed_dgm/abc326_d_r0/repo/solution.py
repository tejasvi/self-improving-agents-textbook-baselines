import sys
from itertools import permutations


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = data[1]
    C = data[2]
    letters = "ABC"
    # Precompute row patterns: each row has exactly one A, B, C; rest empty.
    patterns = []
    for cols in permutations(range(n), 3):
        row = ['.'] * n
        for k in range(3):
            row[cols[k]] = letters[k]
        patterns.append(row)

    col_used = [0] * n   # bitmask of letters used per column
    col_started = [False] * n
    grid = []

    def solve(i):
        if i == n:
            return True
        need = R[i]
        for row in patterns:
            # leftmost letter must match R[i]
            first = next(ch for ch in row if ch != '.')
            if first != need:
                continue
            ok = True
            changed = []  # (col, previous started flag, letter bit)
            for j in range(n):
                ch = row[j]
                if ch == '.':
                    continue
                b = 1 << letters.index(ch)
                if col_used[j] & b:
                    ok = False
                    break
                if not col_started[j] and ch != C[j]:
                    ok = False
                    break
                changed.append((j, col_started[j], b))
                col_used[j] |= b
                col_started[j] = True
            if ok:
                grid.append(''.join(row))
                if solve(i + 1):
                    return True
                grid.pop()
            # undo only the cells that were actually applied
            for j, s, b in reversed(changed):
                col_used[j] &= ~b
                col_started[j] = s
        return False

    if solve(0):
        out = ["Yes"] + grid
        print("\n".join(out))
    else:
        print("No")


main()
