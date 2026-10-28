from typing import List
from bisect import bisect_right


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        vals = sorted(nums)
        n = len(vals)

        diffs = sorted({vals[j] - vals[i]
                        for i in range(n) for j in range(i + 1, n)
                        if vals[j] - vals[i] > 0})

        def count_at_least(x: int) -> int:
            # cnt[j]: number of indices i with vals[i] <= vals[j] - x (all these are < j)
            cnt = [bisect_right(vals, vals[j] - x) for j in range(n)]
            # pref[m][c] = sum over i < m of dp[i][c]
            pref = [[0] * (k + 1) for _ in range(n + 1)]
            total = 0
            for j in range(n):
                dp = [0] * (k + 1)
                dp[1] = 1
                m = cnt[j]
                for c in range(2, k + 1):
                    dp[c] = pref[m][c - 1]
                if k >= 1:
                    total += dp[k]
                row_prev = pref[j]
                row = pref[j + 1]
                for c in range(k + 1):
                    row[c] = (row_prev[c] + dp[c]) % MOD
            return total % MOD

        ans = 0
        prev = 0
        for d in diffs:
            ans = (ans + (d - prev) * count_at_least(d)) % MOD
            prev = d
        return ans
