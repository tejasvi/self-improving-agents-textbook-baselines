from typing import *
from bisect import bisect_right


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        cands = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n) if a[j] - a[i] > 0})
        # p[j]: number of indices i with a[i] <= a[j] - d, computed per threshold
        total = 0
        prev = 0
        for D in cands:
            # count subsequences of length k with all adjacent gaps >= D
            p = [bisect_right(a, a[j] - D) for j in range(n)]
            dp = [1] * n  # length 1
            for _ in range(k - 1):
                # prefix sums of dp
                pref = [0] * (n + 1)
                for i in range(n):
                    pref[i + 1] = pref[i] + dp[i]
                dp = [pref[p[j]] for j in range(n)]
            cnt = sum(dp) % MOD
            total = (total + (D - prev) * cnt) % MOD
            prev = D
        return total % MOD
