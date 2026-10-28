from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[a] = number of valid prefixes where arr1[i] == a
        dp = [1] * (nums[0] + 1)
        for i in range(1, n):
            prev_max = nums[i - 1]
            cur_max = nums[i]
            step = max(0, cur_max - prev_max)
            # prefix sums of dp
            pre = [0] * (len(dp) + 1)
            for a in range(len(dp)):
                pre[a + 1] = (pre[a] + dp[a]) % MOD
            new = [0] * (cur_max + 1)
            for b in range(cur_max + 1):
                # a <= b - step and a <= prev_max
                hi = min(prev_max, b - step)
                if hi >= 0:
                    new[b] = pre[hi + 1]
            dp = new
        return sum(dp) % MOD
