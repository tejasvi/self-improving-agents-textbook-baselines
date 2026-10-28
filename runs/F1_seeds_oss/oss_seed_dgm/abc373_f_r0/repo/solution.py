"""Solution for Knapsack with Diminishing Values.

We have N item types, each with weight w_i and value v_i. We may take any non‑negative integer k_i of type i,
with happiness k_i * v_i - k_i^2. The total weight must not exceed W and we want to maximise total happiness.

For a fixed type the contribution is a concave quadratic in k, therefore it is optimal to take at most
k_max = min(W // w_i, v_i // 2) items of that type – after that the marginal gain becomes non‑positive.
Thus each type behaves like a bounded knapsack with up to k_max copies, but a naïve O(N * W * k_max) DP is too
slow (W ≤ 3000, N ≤ 3000).

The transition for one type can be written as a *max‑plus* convolution which can be optimised with the
convex‑hull trick (CHT).  For a residue class r (0 ≤ r < w_i) we consider the weights
    j = r + m * w_i   (m = 0,1,2,…)
Let dp_prev be the DP after processing previous types.  When we decide to take y items of the current type
and end at weight j we come from weight j - y * w_i = r + t * w_i with t = m - y.
The resulting happiness is
    dp_prev[r + t*w_i] + y * v_i - y^2
with the restriction 0 ≤ y ≤ k_max, i.e. t ∈ [m - k_max, m].
Re‑expressing with t gives a linear function of m:
    (dp_prev[r + t*w_i] - t*v_i - t^2) + (2*t) * m + (m*v_i - m^2).
For a fixed m the term (m*v_i - m^2) is constant, so we need the maximum over t of
    (2*t) * m + (dp_prev[r + t*w_i] - t*v_i - t^2).
Thus each possible t defines a line with slope = 2*t and intercept = dp_prev[...]-t*v_i-t^2.
When we sweep m increasing we can maintain a convex hull of these lines, discarding lines whose t is too
small (t < m - k_max).  Queries are performed at x = m, giving the best value for this residue.
Overall each weight is processed O(1) times, yielding O(N·W) time.

The implementation below follows exactly this plan.
"""

import sys

INF_NEG = -10**18  # sufficiently small sentinel


def solve() -> None:
    it = iter(sys.stdin.read().strip().split())
    N = int(next(it))
    W = int(next(it))
    items = [(int(next(it)), int(next(it))) for _ in range(N)]

    dp = [INF_NEG] * (W + 1)
    dp[0] = 0  # no items, zero happiness

    for w, v in items:
        # maximum useful count of this item type
        k_max = min(W // w, v // 2)  # because marginal gain v - 2k becomes non‑positive after k >= v/2
        new_dp = [INF_NEG] * (W + 1)

        # Process each residue class separately
        for r in range(w):
            # collect positions j = r + m*w (≤ W) and corresponding m values
            positions = []   # actual weight values
            ms = []          # the index m for each position
            j = r
            m = 0
            while j <= W:
                positions.append(j)
                ms.append(m)
                j += w
                m += 1
            if not positions:
                continue

            # Convex hull stored as deque of tuples (slope, intercept, t)
            # slopes (2*t) are strictly increasing as we add lines with larger t.
            from collections import deque
            hull = deque()

            # Iterate over increasing m (i.e. increasing weight in this residue class)
            for idx, cur_m in enumerate(ms):
                # ------- add line for t = cur_m (using dp value at current position) -------
                cur_weight = positions[idx]
                base = dp[cur_weight]
                if base > INF_NEG // 2:  # reachable state
                    slope = 2 * cur_m
                    intercept = base - cur_m * v - cur_m * cur_m
                    # Remove last line(s) if they become unnecessary
                    while len(hull) >= 2:
                        m1, b1, _ = hull[-2]
                        m2, b2, _ = hull[-1]
                        m3, b3, _ = slope, intercept, cur_m
                        # If the intersection of (m1,b1) & (m2,b2) is to the right of intersection of
                        # (m1,b1) & (m3,b3), then middle line is never optimal and can be popped.
                        # Using cross‑multiplication to avoid floating point:
                        # (b3-b1)*(m1-m2) <= (b2-b1)*(m1-m3)
                        if (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3):
                            hull.pop()
                        else:
                            break
                    hull.append((slope, intercept, cur_m))

                # ------- discard lines whose t is out of the allowed window -------
                while hull and hull[0][2] < cur_m - k_max:
                    hull.popleft()

                # ------- query the hull for best line at x = cur_m -------
                if hull:
                    # Since x (=cur_m) is non‑decreasing, we can pop from the front while the next line
                    # gives a better value.
                    while len(hull) >= 2:
                        val0 = hull[0][0] * cur_m + hull[0][1]
                        val1 = hull[1][0] * cur_m + hull[1][1]
                        if val1 >= val0:
                            hull.popleft()
                        else:
                            break
                    best = hull[0][0] * cur_m + hull[0][1]
                    # Add the remaining part of the formula: m*v - m^2
                    new_dp[cur_weight] = best + cur_m * v - cur_m * cur_m
                else:
                    # No feasible previous state – stay at -INF
                    new_dp[cur_weight] = INF_NEG
        dp = new_dp

    # The answer is the maximum happiness achievable with any weight ≤ W
    print(max(dp))


if __name__ == "__main__":
    solve()
