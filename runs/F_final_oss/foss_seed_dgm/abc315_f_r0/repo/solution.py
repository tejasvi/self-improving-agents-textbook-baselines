# Write your solution here. Read from stdin, write to stdout.

import sys
import math

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    xs = []
    ys = []
    for _ in range(N):
        xs.append(int(next(it)))
        ys.append(int(next(it)))
    # Maximum possible distance sum if we visit all consecutive points
    max_dist = math.hypot(10000, 10000) * (N - 1)
    # Determine a reasonable bound for number of skipped checkpoints.
    # Since penalty grows as 2^{C-1}, we only need to consider C where penalty <= max_dist + some margin.
    # Choose a safe constant bound.
    C_MAX = 30  # works for given constraints
    INF = float('inf')
    dp = [[INF] * (C_MAX + 1) for _ in range(N)]
    dp[0][0] = 0.0
    for i in range(N):
        for c in range(C_MAX + 1):
            cur = dp[i][c]
            if cur == INF:
                continue
            # we can jump to j where skipped checkpoints = j-i-1
            max_jump = min(N - 1, i + C_MAX + 1)  # because skip cannot exceed remaining allowed skips
            for j in range(i + 1, max_jump + 1):
                skip = j - i - 1
                new_c = c + skip
                if new_c > C_MAX:
                    continue
                dx = xs[i] - xs[j]
                dy = ys[i] - ys[j]
                dist = math.hypot(dx, dy)
                nd = cur + dist
                if nd < dp[j][new_c]:
                    dp[j][new_c] = nd
    ans = INF
    for c in range(C_MAX + 1):
        val = dp[N - 1][c]
        if val == INF:
            continue
        if c == 0:
            total = val
        else:
            total = val + (1 << (c - 1))  # 2^{c-1}
        if total < ans:
            ans = total
    # print with sufficient precision
    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
