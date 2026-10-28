from bisect import bisect_right
from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        n = len(a)

        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        def count(v: int) -> int:
            # number of size-k subsequences whose adjacent (sorted) gaps are all >= v
            # p[i] = number of indices j < i with a[i] - a[j] >= v
            p = [min(bisect_right(a, a[i] - v), i) for i in range(n)]
            # dp for c = 1
            dp = [1] * n
            for _ in range(k - 1):
                # prefix sums of dp: pre[x] = sum_{j<x} dp[j]
                pre = [0] * (n + 1)
                for j in range(n):
                    pre[j + 1] = (pre[j] + dp[j]) % MOD
                dp = [pre[p[i]] for i in range(n)]
            return sum(dp) % MOD

        ans = 0
        prev = 0
        for v in diffs:
            ans = (ans + (v - prev) * count(v)) % MOD
            prev = v
        return ans % MOD
