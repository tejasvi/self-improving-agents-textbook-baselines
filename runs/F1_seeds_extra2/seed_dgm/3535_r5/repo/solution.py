from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums)
        # dp[a] = number of valid prefixes ending with arr1[i] == a
        dp = [1] * (nums[0] + 1) + [0] * (M - nums[0])
        for i in range(1, len(nums)):
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of dp
            pre = [0] * (M + 1)
            s = 0
            for v in range(M + 1):
                s = (s + dp[v]) % MOD
                pre[v] = s
            new = [0] * (M + 1)
            for a in range(nums[i] + 1):
                if a - d >= 0:
                    new[a] = pre[a - d]
            dp = new
        return sum(dp) % MOD
