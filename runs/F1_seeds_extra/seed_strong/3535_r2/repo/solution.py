from typing import *

MOD = 10**9 + 7


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        # a_i = arr1[i]; arr2[i] = nums[i] - a_i.
        # Conditions: 0 <= a_i <= nums[i], a_i >= a_{i-1},
        # a_i - a_{i-1} >= nums[i] - nums[i-1] (= d).
        M = max(nums)
        dp = [0] * (M + 1)
        for a in range(nums[0] + 1):
            dp[a] = 1
        for i in range(1, len(nums)):
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of previous dp
            pre = [0] * (M + 2)
            for v in range(M + 1):
                pre[v + 1] = (pre[v] + dp[v]) % MOD
            new = [0] * (M + 1)
            for a in range(nums[i] + 1):
                # previous b in [0, a - d]
                hi = a - d
                if hi < 0:
                    continue
                new[a] = pre[hi + 1] % MOD
            dp = new
        return sum(dp) % MOD
