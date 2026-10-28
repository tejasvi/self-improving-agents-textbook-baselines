from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        M = max(nums)
        # dp[a] = number of valid prefixes ending with arr1[i] = a
        dp = [1] * (nums[0] + 1) + [0] * (M - nums[0])
        for i in range(1, n):
            d = max(0, nums[i] - nums[i - 1])
            # prefix sums of previous dp
            pref = [0] * (M + 2)
            for v in range(M + 1):
                pref[v + 1] = (pref[v] + dp[v]) % MOD
            new = [0] * (M + 1)
            for a in range(0, nums[i] + 1):
                hi = a - d  # previous b must satisfy b <= hi
                if hi < 0:
                    continue
                new[a] = pref[min(hi, M) + 1]
            dp = new
        return sum(dp) % MOD
