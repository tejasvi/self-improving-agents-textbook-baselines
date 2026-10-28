from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums)
        # dp[a] = number of valid prefixes ending with arr1[i] == a
        dp = [0] * (M + 1)
        for a in range(nums[0] + 1):
            dp[a] = 1
        for i in range(1, len(nums)):
            prev = nums[i - 1]
            cur = nums[i]
            step = max(0, cur - prev)
            # prefix sums of dp
            pre = [0] * (M + 2)
            for a in range(M + 1):
                pre[a + 1] = (pre[a] + dp[a]) % MOD
            new = [0] * (M + 1)
            for b in range(cur + 1):
                hi = b - step  # need a <= b - step, and a <= prev
                if hi < 0:
                    continue
                hi = min(hi, prev)
                new[b] = pre[hi + 1]
            dp = new
        return sum(dp) % MOD
