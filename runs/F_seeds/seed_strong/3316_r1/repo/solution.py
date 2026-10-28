from typing import *


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        def count(g: int) -> int:
            # p[i] = largest j with a[i] - a[j] >= g, or -1
            p = [-1] * n
            j = 0
            for i in range(n):
                while j < n and a[i] - a[j] >= g:
                    j += 1
                p[i] = j - 1
            # dp[i] = number of valid subsets of current size ending at i
            dp = [1] * n
            for _ in range(k - 1):
                pref = [0] * (n + 1)
                for i in range(n):
                    pref[i + 1] = (pref[i] + dp[i]) % MOD
                dp = [pref[p[i] + 1] if p[i] >= 0 else 0 for i in range(n)]
            return sum(dp) % MOD

        ans = 0
        prev = 0
        for g in diffs:
            if g <= 0:
                prev = g
                continue
            ans = (ans + (g - prev) * count(g)) % MOD
            prev = g
        return ans % MOD
