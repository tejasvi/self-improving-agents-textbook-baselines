from typing import *


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        # dp[v] = number of ways where arr1[i] == v
        n = len(nums)
        dp = [1] * (nums[0] + 1)
        for i in range(1, n):
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of previous dp
            pref = [0] * (len(dp) + 1)
            for v, c in enumerate(dp):
                pref[v + 1] = (pref[v] + c) % MOD
            new = [0] * (nums[i] + 1)
            for w in range(nums[i] + 1):
                hi = w - d  # need v <= w - d
                if hi < 0:
                    continue
                hi = min(hi, len(dp) - 1)
                new[w] = pref[hi + 1]
            dp = new
        return sum(dp) % MOD
