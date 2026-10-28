from typing import *
from bisect import bisect_right

MOD = 10**9 + 7


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n) if a[j] - a[i] > 0})

        def count(t: int) -> int:
            # lo[i]: smallest index j such that a[i]-a[j] >= t (valid predecessors are j < lo[i])
            lo = [bisect_right(a, a[i] - t) for i in range(n)]
            # pre[m][c] = sum over j < m of dp[j][c]
            pre = [[0] * (k + 1) for _ in range(n + 1)]
            total = 0
            for i in range(n):
                dp = [0] * (k + 1)
                dp[1] = 1
                m = lo[i]
                for c in range(2, k + 1):
                    dp[c] = pre[m][c - 1]
                total += dp[k]
                row_prev = pre[i]
                row = pre[i + 1]
                for c in range(k + 1):
                    row[c] = (row_prev[c] + dp[c]) % MOD
            return total % MOD

        ans = 0
        prev = 0
        for t in diffs:
            ans = (ans + (t - prev) * count(t)) % MOD
            prev = t
        return ans
