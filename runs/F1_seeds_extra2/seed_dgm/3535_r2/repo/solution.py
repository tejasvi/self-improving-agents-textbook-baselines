from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[a] = number of valid prefixes where arr1[i] == a
        dp = [1] * (nums[0] + 1)
        for i in range(1, n):
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of previous dp
            pref = [0] * (len(dp) + 1)
            for a, v in enumerate(dp):
                pref[a + 1] = (pref[a] + v) % MOD
            new = [0] * (nums[i] + 1)
            for b in range(nums[i] + 1):
                hi = b - d  # previous a must satisfy a <= b - d
                if hi < 0:
                    continue
                hi = min(hi, len(dp) - 1)
                new[b] = pref[hi + 1]
            dp = new
        return sum(dp) % MOD
