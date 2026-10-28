# Write your solution here. Read from stdin, write to stdout.

import sys
import bisect

def knap_max_amount(items, X):
    """Return list dp where dp[c] = max total amount achievable with at most c calories.
    items: list of (amount, calories) for a single vitamin type.
    """
    dp = [-1] * (X + 1)
    dp[0] = 0
    for a, c in items:
        for cal in range(X, c - 1, -1):
            if dp[cal - c] != -1:
                val = dp[cal - c] + a
                if val > dp[cal]:
                    dp[cal] = val
    # make non‑decreasing (max for up to c calories)
    for cal in range(1, X + 1):
        if dp[cal - 1] > dp[cal]:
            dp[cal] = dp[cal - 1]
    return dp

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    items_by_vit = {1: [], 2: [], 3: []}
    for _ in range(N):
        v = int(next(it))
        a = int(next(it))
        c = int(next(it))
        items_by_vit[v].append((a, c))
    # DP for each vitamin type
    dp1 = knap_max_amount(items_by_vit[1], X)
    dp2 = knap_max_amount(items_by_vit[2], X)
    dp3 = knap_max_amount(items_by_vit[3], X)
    # Upper bound for answer
    upper = min(dp1[X], dp2[X], dp3[X])
    # binary search
    lo, hi = 0, upper
    while lo < hi:
        mid = (lo + hi + 1) // 2
        # find minimal calories needed for each vitamin to reach at least mid
        def min_cal(dp):
            # dp is non‑decreasing, use bisect_left on values
            idx = bisect.bisect_left(dp, mid)
            return idx if idx <= X else X + 1
        c1 = min_cal(dp1)
        c2 = min_cal(dp2)
        c3 = min_cal(dp3)
        if c1 + c2 + c3 <= X:
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
