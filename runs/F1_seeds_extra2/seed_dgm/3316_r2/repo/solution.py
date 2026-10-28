import bisect
from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        n = len(a)

        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        def count(d: int) -> int:
            # number of k-subsets whose adjacent (sorted) gaps are all >= d
            if d == 0:
                # every subset qualifies
                from math import comb
                return comb(n, k)
            # bound[i]: number of indices p < i with a[p] <= a[i] - d
            bound = [min(i, bisect.bisect_right(a, a[i] - d)) for i in range(n)]
            # prefix[m][j] = sum over p < m of dp[p][j]
            prefix = [[0] * (k + 1) for _ in range(n + 1)]
            dp = [[0] * (k + 1) for _ in range(n)]
            for i in range(n):
                dp[i][1] = 1
                b = bound[i]
                for j in range(2, k + 1):
                    dp[i][j] = prefix[b][j - 1]
                for j in range(1, k + 1):
                    prefix[i + 1][j] = prefix[i][j] + dp[i][j]
            return prefix[n][k]

        ans = 0
        m = len(diffs)
        f_next = 0
        for idx in range(m - 1, -1, -1):
            v = diffs[idx]
            f_v = count(v)
            ans += v * (f_v - f_next)
            f_next = f_v
        return ans % MOD
