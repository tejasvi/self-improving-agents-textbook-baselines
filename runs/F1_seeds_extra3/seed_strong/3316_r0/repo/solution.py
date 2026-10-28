from typing import *
from bisect import bisect_right

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        def count(v: int) -> int:
            # number of k-subsequences whose sorted adjacent gaps are all >= v
            # cnt_i: number of indices p with a[p] <= a[i]-v, capped at i (p < i)
            lim = [min(i, bisect_right(a, a[i] - v)) for i in range(n)]
            # dp[i][j]: ways choosing j elements, last one is index i
            # pre[c][j] = sum_{p<c} dp[p][j]
            pre = [[0] * (k + 1) for _ in range(n + 1)]
            dp_k_total = 0
            dp = [[0] * (k + 1) for _ in range(n)]
            for i in range(n):
                dp[i][1] = 1
                if k >= 2:
                    row_pre = pre[lim[i]]
                    for j in range(2, k + 1):
                        dp[i][j] = row_pre[j - 1]
                dp_k_total += dp[i][k]
                # build pre[i+1]
                prev = pre[i]
                cur = pre[i + 1]
                di = dp[i]
                for j in range(1, k + 1):
                    cur[j] = (prev[j] + di[j]) % MOD
            return dp_k_total % MOD

        ans = 0
        prev_d = 0
        for d in diffs:
            ans = (ans + (d - prev_d) * count(d)) % MOD
            prev_d = d
        return ans % MOD
