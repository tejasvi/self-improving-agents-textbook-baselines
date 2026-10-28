from typing import *

MOD = 10**9 + 7


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        n = len(nums)
        M = max(nums)
        # dp[a] = number of valid prefixes ending with arr1[i] = a
        dp = [1 if a <= nums[0] else 0 for a in range(M + 1)]
        for i in range(1, n):
            d = nums[i] - nums[i - 1]
            # prefix sums of dp
            pre = [0] * (M + 2)
            s = 0
            for b in range(M + 1):
                s += dp[b]
                pre[b + 1] = s % MOD
            ndp = [0] * (M + 1)
            for a in range(min(M, nums[i]) + 1):
                hi = min(a, a - d)  # need b <= hi
                if hi < 0:
                    continue
                ndp[a] = pre[min(hi, M) + 1]
            dp = ndp
        return sum(dp) % MOD
