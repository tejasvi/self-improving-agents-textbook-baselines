# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = int(next(it))
    # Use bytearray rows for fast hole checks
    holes = [bytearray(W) for _ in range(H)]
    for _ in range(N):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        holes[a][b] = 1
    # DP with only two rows (previous and current). Extra leading zero simplifies handling borders.
    dp_prev = [0] * (W + 1)
    total = 0
    for i in range(1, H + 1):
        dp_cur = [0] * (W + 1)
        row = holes[i - 1]
        for j in range(1, W + 1):
            if row[j - 1] == 0:  # not a hole
                # size of largest square with bottom‑right corner at (i, j)
                v = 1 + min(dp_prev[j], dp_cur[j - 1], dp_prev[j - 1])
                dp_cur[j] = v
                total += v
        dp_prev = dp_cur
    print(total)

if __name__ == "__main__":
    solve()
