# Solution for "Knapsack with Diminishing Values"
# Implements DP with convex hull optimization for each item type.

import sys

INF_NEG = -10**30  # sufficiently small

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    W = int(next(it))
    items = []
    for _ in range(N):
        w = int(next(it))
        v = int(next(it))
        items.append((w, v))

    dp = [INF_NEG] * (W + 1)
    dp[0] = 0

    for w, v in items:
        # dp after processing this type
        new_dp = [INF_NEG] * (W + 1)
        # Process each residue class modulo w independently
        for r in range(w):
            # collect the sequence of reachable states for this residue
            max_m = (W - r) // w
            if max_m < 0:
                continue
            f = [dp[r + m * w] for m in range(max_m + 1)]
            # result array for this residue
            new_f = [INF_NEG] * (max_m + 1)
            # convex hull (deque) of lines: y = m_slope * x + b
            from collections import deque
            hull = deque()
            # helper to check if middle line is unnecessary
            def is_bad(l1, l2, l3):
                # l = (slope, intercept)
                m1, b1 = l1
                m2, b2 = l2
                m3, b3 = l3
                # intersection(l1,l2) >= intersection(l2,l3) => l2 is bad
                # (b3 - b1)*(m1 - m2) <= (b2 - b1)*(m1 - m3)
                return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)

            for m in range(max_m + 1):
                # add line for s = m (if reachable)
                if f[m] > INF_NEG // 2:
                    slope = 2 * m
                    intercept = f[m] - m * m - v * m
                    # maintain convex hull property
                    while len(hull) >= 2 and is_bad(hull[-2], hull[-1], (slope, intercept)):
                        hull.pop()
                    hull.append((slope, intercept))
                # query best line for x = m
                if not hull:
                    new_f[m] = INF_NEG
                else:
                    while len(hull) >= 2 and (hull[0][0] * m + hull[0][1]) <= (hull[1][0] * m + hull[1][1]):
                        hull.popleft()
                    best = hull[0][0] * m + hull[0][1]
                    new_f[m] = -m * m + v * m + best
            # write back to new_dp
            for m, val in enumerate(new_f):
                weight = r + m * w
                new_dp[weight] = val
        dp = new_dp

    # answer is maximum dp[w] for w <= W (dp already only for exactly weight)
    # Since we may leave unused capacity, we take max over all weights.
    ans = max(dp)
    print(ans)

if __name__ == "__main__":
    solve()
