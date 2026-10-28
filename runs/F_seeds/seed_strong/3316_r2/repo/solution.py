from typing import *
from bisect import bisect_right


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n) if a[j] - a[i] > 0})

        def count(d: int) -> int:
            # number of k-subsequences (sorted indices) with consecutive gaps >= d
            # lim[i] = number of indices p with a[p] <= a[i] - d (all such p < i)
            lim = [bisect_right(a, a[i] - d) for i in range(n)]
            dp = [1] * n  # dp for length 1
            for _ in range(k - 1):
                pref = [0] * (n + 1)
                for i in range(n):
                    pref[i + 1] = pref[i] + dp[i]
                dp = [pref[lim[i]] for i in range(n)]
            return sum(dp)

        total = 0
        prev = 0
        for v in diffs:
            total += (v - prev) * count(v)
            prev = v
        return total % MOD
