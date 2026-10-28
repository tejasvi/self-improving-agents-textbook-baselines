from typing import List

MOD = 10**9 + 7

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        n = len(nums)
        a = sorted(nums)
        # Special case k == 2: sum over all pairwise absolute differences
        if k == 2:
            total = 0
            for i in range(n):
                for j in range(i + 1, n):
                    total += abs(a[j] - a[i])
            return total % MOD
        # For k >= 3, the minimum difference in a subsequence equals the minimum gap
        # between consecutive elements after sorting the chosen elements, which must be one
        # of the adjacent gaps in the whole sorted array.
        gaps = [a[i + 1] - a[i] for i in range(n - 1)]
        if not gaps:
            return 0
        unique_vals = sorted(set(gaps))
        # Helper: count subsets of size k where every adjacent selected pair has gap >= t
        def count_at_least(t: int) -> int:
            # dp[i][c] = number of ways to choose c elements ending at index i (i selected)
            dp = [[0] * (k + 1) for _ in range(n)]
            for i in range(n):
                dp[i][1] = 1
            for c in range(2, k + 1):
                for i in range(n):
                    total = 0
                    for p in range(i):
                        if a[i] - a[p] >= t:
                            total += dp[p][c - 1]
                    dp[i][c] = total % MOD
            return sum(dp[i][k] for i in range(n)) % MOD
        # Pre‑compute f(t) for each unique gap value
        f = {}
        for val in unique_vals:
            f[val] = count_at_least(val)
        # Compute contribution of each exact minimum gap value
        ans = 0
        next_f = 0  # f for the next larger gap (initially 0 for beyond max gap)
        for val in reversed(unique_vals):
            cnt_exact = (f[val] - next_f) % MOD  # subsets where min gap == val
            ans = (ans + (val % MOD) * cnt_exact) % MOD
            next_f = f[val]
        return ans
