from typing import *


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        M = max(nums)
        # dp[a] = number of valid prefixes ending with arr1[i] = a
        dp = [1 if a <= nums[0] else 0 for a in range(M + 1)]
        for i in range(1, n):
            d = nums[i] - nums[i - 1]
            pre = [0] * (M + 2)
            for b in range(M + 1):
                pre[b + 1] = (pre[b] + dp[b]) % MOD
            new = [0] * (M + 1)
            for a in range(0, min(nums[i], M) + 1):
                # prev b: b <= a and a - b >= d, b <= nums[i-1]
                lo = 0
                hi = min(a, nums[i - 1], a - d)
                if lo <= hi:
                    new[a] = (pre[hi + 1] - pre[lo]) % MOD
            dp = new
        return sum(dp) % MOD
