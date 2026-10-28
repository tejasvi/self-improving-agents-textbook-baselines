from typing import *
from math import comb
from bisect import bisect_right


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        D = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})
        if not D:
            return 0

        def count(t):
            # number of k-subsets (sorted order) with all adjacent gaps >= t
            # dp[j]: ways to pick l elements ending at j
            # valid predecessors i of j: a[i] <= a[j]-t, i.e. i < p_j
            p = [bisect_right(a, a[j] - t) for j in range(n)]
            dp = [1] * n
            for _ in range(k - 1):
                pref = [0] * (n + 1)
                for i in range(n):
                    pref[i + 1] = pref[i] + dp[i]
                dp = [pref[p[j]] for j in range(n)]
            return sum(dp)

        total = D[0] * comb(n, k)
        for i in range(1, len(D)):
            total += (D[i] - D[i - 1]) * count(D[i])
        return total % MOD
