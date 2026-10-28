from typing import *


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums)
        # dp[v] = number of valid prefixes with arr1[i] == v
        n = len(nums)
        dp = [0] * (M + 1)
        for v in range(nums[0] + 1):
            dp[v] = 1
        for i in range(1, n):
            prev = nums[i - 1]
            cur = nums[i]
            d = max(0, cur - prev)
            # prefix sums of dp
            pref = [0] * (M + 2)
            s = 0
            for v in range(M + 1):
                s += dp[v]
                pref[v + 1] = s % MOD
            ndp = [0] * (M + 1)
            for w in range(cur + 1):
                # v + d <= w  => v <= w - d
                t = w - d
                if t >= 0:
                    ndp[w] = pref[t + 1]
            dp = ndp
        return sum(dp) % MOD
