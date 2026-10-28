from bisect import bisect_right
from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n) if a[j] - a[i] > 0})

        def count(m: int) -> int:
            # number of k-subsequences (sorted order) with all adjacent gaps >= m
            # p[j] = number of indices i with a[i] <= a[j] - m (all such i < j)
            p = [bisect_right(a, a[j] - m) for j in range(n)]
            # dp[j] for current c: ways to pick c elements ending at j
            dp = [1] * n
            for _ in range(k - 1):
                # prefix sums of dp
                pre = [0] * (n + 1)
                for i in range(n):
                    pre[i + 1] = pre[i] + dp[i]
                dp = [pre[p[j]] for j in range(n)]
            return sum(dp) % MOD

        total = 0
        prev = 0
        for d in diffs:
            total = (total + (d - prev) * count(d)) % MOD
            prev = d
        return total % MOD
