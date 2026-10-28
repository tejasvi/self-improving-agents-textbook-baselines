import bisect
from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)

        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        # L[i][v] computed on the fly: largest p < i with a[i]-a[p] >= v
        def count_at_least(v):
            # dp[i] = number of ways to pick j elements ending at index i
            dp = [1] * n
            for _ in range(k - 1):
                # prefix sums of dp
                pref = [0] * (n + 1)
                for i in range(n):
                    pref[i + 1] = pref[i] + dp[i]
                new = [0] * n
                for i in range(n):
                    # valid p satisfy a[p] <= a[i] - v, p < i
                    lim = bisect.bisect_right(a, a[i] - v, 0, i)  # p in [0, lim)
                    new[i] = pref[lim] % MOD
                dp = new
            return sum(dp) % MOD

        ans = 0
        prev = 0
        for d in diffs:
            if d == 0:
                prev = d
                continue
            ans = (ans + count_at_least(d) * (d - prev)) % MOD
            prev = d
        return ans % MOD
