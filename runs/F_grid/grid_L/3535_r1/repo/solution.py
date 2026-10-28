from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        M = max(nums)
        # dp[x] = number of valid prefixes ending with arr1[i] = x
        dp = [0] * (M + 1)
        for x in range(nums[0] + 1):
            dp[x] = 1
        for i in range(1, n):
            # prefix sums of dp
            pref = [0] * (M + 2)
            for x in range(M + 1):
                pref[x + 1] = (pref[x] + dp[x]) % MOD
            d = max(0, nums[i] - nums[i - 1])
            new = [0] * (M + 1)
            for y in range(nums[i] + 1):
                # need x <= y - d
                hi = y - d
                if hi >= 0:
                    new[y] = pref[hi + 1]
            dp = new
        return sum(dp) % MOD
