# Write your solution here. Read from stdin, write to stdout.
import sys
import math

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    points = [(int(next(it)), int(next(it))) for _ in range(N)]
    # Maximum possible total distance (upper bound) to limit skipped count
    max_dist = N * math.hypot(10000, 10000)  # each segment at most sqrt(2)*1e4
    # Determine a safe bound for skipped checkpoints where penalty already exceeds max_dist
    maxC = 0
    while (1 << maxC) <= max_dist * 2:  # 2^{C-1} > max_dist when 2^C > 2*max_dist
        maxC += 1
    # Add a small safety margin
    maxC = min(N-2, maxC + 2)
    INF = float('inf')
    # dp[i][c] = minimal travel distance to reach checkpoint i having skipped exactly c checkpoints total
    dp = [[INF] * (maxC + 1) for _ in range(N)]
    dp[0][0] = 0.0
    # Precompute distances on the fly when needed
    for i in range(1, N):
        # Only need to look back up to maxC+1 previous checkpoints because skipping more would exceed bound
        j_start = max(0, i - (maxC + 1))
        for j in range(j_start, i):
            skip = i - j - 1
            if skip > maxC:
                continue
            # distance between checkpoint j and i
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            d = math.hypot(dx, dy)
            # combine with previous states
            for c_prev in range(maxC - skip + 1):
                prev_val = dp[j][c_prev]
                if prev_val == INF:
                    continue
                c_new = c_prev + skip
                new_val = prev_val + d
                if new_val < dp[i][c_new]:
                    dp[i][c_new] = new_val
    # Compute final answer adding penalty
    ans = INF
    for c in range(maxC + 1):
        travel = dp[N-1][c]
        if travel == INF:
            continue
        penalty = 0.0 if c == 0 else float(1 << (c - 1))
        total = travel + penalty
        if total < ans:
            ans = total
    # Print with sufficient precision
    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
