import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    # grid[i][j] = 1 if free (not holed), 0 if holed (0-indexed)
    grid = [[1] * W for _ in range(H)]
    idx = 3
    for _ in range(N):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        grid[a][b] = 0

    total = 0
    prev_up = [0] * W      # consecutive free run upward ending at row i-1
    INF = 1 << 30
    prev_dp = [INF] * W    # largest square with bottom-right at row i-1
    for i in range(H):
        row = grid[i]
        # up run: (prev_up+1) where free, else 0
        up = [(u + 1) * f for u, f in zip(prev_up, row)]
        # left run within the row
        left = list(accumulate(row, lambda a, f: (a + 1) * f))
        # diagonal: prev_dp shifted right by one, plus 1
        diag = [INF] + [d + 1 for d in prev_dp[:-1]]
        cur = list(map(min, up, left, diag))
        total += sum(cur)
        prev_up = up
        prev_dp = cur
    print(total)


main()
