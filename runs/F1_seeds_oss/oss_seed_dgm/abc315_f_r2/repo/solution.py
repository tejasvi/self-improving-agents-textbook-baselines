# Solution for the "Shortcuts" problem.
# We need to travel from checkpoint 1 to N, possibly skipping intermediate checkpoints.
# If we skip C>0 checkpoints in total, we incur a penalty of 2^{C-1}; otherwise no penalty.
# Goal: minimise total Euclidean distance travelled plus penalty.
# N ≤ 10^4, coordinates up to 10^4.
# Observation: the penalty grows exponentially, so the optimal solution never skips many checkpoints.
# The maximal possible Euclidean distance is bounded by (N-1) * sqrt(2) * 10^4 ≈ 1.5e8.
# 2^{30} ≈ 1.07e9 > this bound, therefore we never need to consider C > 30.
# We use dynamic programming where dp[i][c] = minimal travelled distance to reach checkpoint i (0‑based index)
# having skipped exactly c checkpoints so far. 0 ≤ c ≤ MAX_SKIP (≈35 for safety).
# Transitions consider the previous visited checkpoint j (i-gap) where gap ≤ MAX_GAP (=MAX_SKIP+1).
# Complexity O(N * MAX_GAP^2) ≈ 10^4 * 35^2 ≈ 1.2e7, which is fast enough.

import sys, math

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    xs = [0] * N
    ys = [0] * N
    for i in range(N):
        xs[i] = int(next(it))
        ys[i] = int(next(it))

    # Upper bound on total skips needed. 30 is enough, we keep a small safety margin.
    MAX_SKIP = 35
    INF = float('inf')
    # dp[i][c] as described; initialise with INF.
    dp = [[INF] * (MAX_SKIP + 1) for _ in range(N)]
    dp[0][0] = 0.0

    # Pre‑compute powers of two for penalty calculation.
    pow2 = [1]
    for _ in range(1, MAX_SKIP + 1):
        pow2.append(pow2[-1] * 2)

    # Main DP.
    for i in range(1, N):
        # Gap = number of steps back to previous visited checkpoint.
        max_gap = min(i, MAX_SKIP + 1)  # because we may skip at most MAX_SKIP checkpoints total.
        for gap in range(1, max_gap + 1):
            j = i - gap
            skipped_now = gap - 1  # checkpoints skipped in this move.
            dist = math.hypot(xs[i] - xs[j], ys[i] - ys[j])
            # Combine with all possible previous skip counts.
            for c_prev in range(0, MAX_SKIP - skipped_now + 1):
                if dp[j][c_prev] == INF:
                    continue
                c_new = c_prev + skipped_now
                new_val = dp[j][c_prev] + dist
                if new_val < dp[i][c_new]:
                    dp[i][c_new] = new_val

    # Compute final answer adding the penalty.
    ans = INF
    for c in range(0, MAX_SKIP + 1):
        if dp[N-1][c] == INF:
            continue
        penalty = 0.0 if c == 0 else pow2[c-1]
        total = dp[N-1][c] + penalty
        if total < ans:
            ans = total

    # Print with enough digits.
    # Using 15 decimal places satisfies the required 1e-5 precision.
    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
