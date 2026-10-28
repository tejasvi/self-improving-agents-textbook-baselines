# Write your solution here. Read from stdin, write to stdout.
import sys, math

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    points = [(int(next(it)), int(next(it))) for _ in range(N)]
    # Maximum number of skips to consider (penalty grows exponentially)
    MAX_SKIP = 30  # 2^{29} ~ 5e8, larger than any possible total distance
    INF = float('inf')
    # dp[i][c] = minimal travel distance (without penalty) to reach checkpoint i having skipped exactly c checkpoints so far
    dp = [[INF] * (MAX_SKIP + 1) for _ in range(N)]
    dp[0][0] = 0.0
    # Precompute distances on the fly, only need recent positions due to skip limit
    for i in range(1, N):
        xi, yi = points[i]
        # we only need to look back at most MAX_SKIP+1 positions because skips cannot exceed MAX_SKIP overall
        j_start = max(0, i - (MAX_SKIP + 1))
        for j in range(j_start, i):
            xj, yj = points[j]
            dist = math.hypot(xi - xj, yi - yj)
            skips = i - j - 1  # number of checkpoints skipped between j and i
            if skips > MAX_SKIP:
                continue
            for c_prev in range(MAX_SKIP - skips + 1):
                if dp[j][c_prev] == INF:
                    continue
                c_new = c_prev + skips
                new_dist = dp[j][c_prev] + dist
                if new_dist < dp[i][c_new]:
                    dp[i][c_new] = new_dist
    # compute answer adding the penalty based on total skips
    ans = INF
    for c in range(MAX_SKIP + 1):
        travel = dp[N-1][c]
        if travel == INF:
            continue
        penalty = 0 if c == 0 else (1 << (c - 1))
        total = travel + penalty
        if total < ans:
            ans = total
    # output with sufficient precision
    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
