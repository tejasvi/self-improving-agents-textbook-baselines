from typing import *
from bisect import bisect_right


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n) if a[j] - a[i] > 0})

        def count(d: int) -> int:
            # p[j] = largest index i with a[i] <= a[j] - d (or -1)
            p = [bisect_right(a, a[j] - d) - 1 for j in range(n)]
            dp = [1] * n  # ways with 1 element ending at j
            for _ in range(k - 1):
                # prefix sums of dp
                pre = [0] * (n + 1)
                for i in range(n):
                    pre[i + 1] = (pre[i] + dp[i]) % MOD
                dp = [pre[p[j] + 1] for j in range(n)]
            return sum(dp) % MOD

        total = 0
        prev = 0
        for d in diffs:
            total = (total + (d - prev) * count(d)) % MOD
            prev = d
        return total % MOD
