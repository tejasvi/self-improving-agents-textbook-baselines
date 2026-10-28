from typing import List
from bisect import bisect_right


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)

        # distinct pairwise differences
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        # p[j] = number of indices i with a[i] <= a[j] - d  (computed per d)
        def count(d: int) -> int:
            # for each j, the valid predecessors are indices i < p[j]
            p = [bisect_right(a, a[j] - d) for j in range(n)]
            # dp[c][j]: ways to pick c elements ending at j, gaps >= d
            dp = [1] * n
            for _ in range(k - 1):
                # prefix sums of dp
                pref = [0] * (n + 1)
                for i in range(n):
                    pref[i + 1] = (pref[i] + dp[i]) % MOD
                new = [0] * n
                for j in range(n):
                    # predecessors i < p[j] (and p[j] <= j automatically when d>=0)
                    lim = min(p[j], j)
                    new[j] = pref[lim]
                dp = new
            return sum(dp) % MOD

        ans = 0
        prev = 0
        for v in diffs:
            if v > 0:
                ans = (ans + (v - prev) * count(v)) % MOD
            prev = v
        return ans % MOD
