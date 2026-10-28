# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = int(next(it))
    # rows are 1-indexed
    holes_row = [set() for _ in range(H + 1)]
    for _ in range(N):
        a = int(next(it))
        b = int(next(it))
        holes_row[a].add(b)

    prev = [0] * (W + 1)  # dp values for previous row, 0-index dummy column
    total = 0
    for i in range(1, H + 1):
        cur = [0] * (W + 1)
        row_holes = holes_row[i]
        # iterate columns
        for j in range(1, W + 1):
            if j in row_holes:
                cur[j] = 0
            else:
                # size of largest hole‑free square with bottom‑right corner (i, j)
                v = min(prev[j], cur[j - 1], prev[j - 1]) + 1
                cur[j] = v
                total += v
        prev = cur
    print(total)

if __name__ == "__main__":
    solve()
