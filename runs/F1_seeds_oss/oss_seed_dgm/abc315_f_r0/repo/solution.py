"""Solution for the Shortcuts problem.

We have N checkpoints with coordinates (X_i, Y_i). We must travel from checkpoint 1 to N in order,
but we may skip any intermediate checkpoints. If we skip C checkpoints in total (C>0) we incur a
penalty 2^{C-1}; if C=0 the penalty is 0. The total cost is the sum of Euclidean distances of the
segments we actually travel plus the penalty.

We need the minimum possible total cost.

Observation:
The penalty grows exponentially, so the optimal solution will skip only a relatively small
number of checkpoints. The maximal possible travelled distance is bounded by (N-1)*sqrt(2)*10^4
≈ 1.4·10^8. 2^{30} ≈ 1.07·10^9 already exceeds this bound, therefore we can safely limit the
considered number of skipped checkpoints to at most C_MAX = 30 (or a bit larger for safety).

Dynamic programming:
Let dp[i][c] be the minimum travelled distance (without penalty) to reach checkpoint i (0‑based)
having skipped exactly c checkpoints so far, where i is a checkpoint we actually visit.
Transition:
    From a previously visited checkpoint j (< i) we skip s = i - j - 1 checkpoints.
    New total skipped count is c' = c + s.
    dp[i][c'] = min(dp[i][c'], dp[j][c] + dist(j, i))
We only need to consider j such that s ≤ C_MAX, because larger skips would already exceed the
maximum allowed skipped count we are tracking.
The DP size is O(N·C_MAX) and each state looks back at most C_MAX previous checkpoints, giving
O(N·C_MAX^2) ≈ 1e4·30·30 ≈ 9·10^5 operations, easily fast.

Finally the answer is:
    min_{c ≤ C_MAX} dp[N-1][c] + (0 if c == 0 else 2**(c-1))
We also handle the trivial case N = 2 directly.
"""

import sys
import math

def solve() -> None:
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

    if N == 2:
        # No possible skips
        dist = math.hypot(xs[1] - xs[0], ys[1] - ys[0])
        print("{:.15f}".format(dist))
        return

    C_MAX = 35  # safe upper bound; 2**34 ~ 1.7e10 which dwarfs any realistic distance
    INF = float('inf')
    # dp[i][c] = minimal travelled distance (without penalty) to reach i having skipped c
    dp = [[INF] * (C_MAX + 1) for _ in range(N)]
    dp[0][0] = 0.0

    # Precompute distances on the fly to avoid O(N^2) memory.
    for i in range(1, N):
        # Look back only a limited window where number of skips <= C_MAX
        j_start = max(0, i - C_MAX - 1)
        for j in range(j_start, i):
            skips = i - j - 1
            if skips > C_MAX:
                continue
            d = math.hypot(xs[i] - xs[j], ys[i] - ys[j])
            # combine with previous states
            # c_prev can be at most C_MAX - skips
            limit = C_MAX - skips
            row_j = dp[j]
            row_i = dp[i]
            for c_prev in range(limit + 1):
                prev_dist = row_j[c_prev]
                if prev_dist == INF:
                    continue
                c_new = c_prev + skips
                new_val = prev_dist + d
                if new_val < row_i[c_new]:
                    row_i[c_new] = new_val

    # Compute answer
    ans = INF
    final_row = dp[N - 1]
    for c in range(C_MAX + 1):
        base = final_row[c]
        if base == INF:
            continue
        penalty = 0.0 if c == 0 else float(2 ** (c - 1))
        total = base + penalty
        if total < ans:
            ans = total

    # In the extremely rare case that skipping more than C_MAX checkpoints yields a better
    # result (practically impossible given the exponential penalty), we could compute the
    # direct distance with penalty for skipping all middle points as a fallback.
    if N > 2:
        direct = math.hypot(xs[-1] - xs[0], ys[-1] - ys[0])
        skips_all = N - 2
        penalty_all = float(2 ** (skips_all - 1)) if skips_all > 0 else 0.0
        ans = min(ans, direct + penalty_all)

    # Print with sufficient precision
    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
