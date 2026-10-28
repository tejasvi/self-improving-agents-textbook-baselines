from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[v] = number of valid prefixes where arr1[i] == v
        m = nums[0]
        dp = [1] * (m + 1)
        for i in range(1, len(nums)):
            prev = nums[i - 1]
            cur = nums[i]
            d = max(0, cur - prev)
            # prefix sums of dp
            pref = [0] * (len(dp) + 1)
            for v in range(len(dp)):
                pref[v + 1] = (pref[v] + dp[v]) % MOD
            new = [0] * (cur + 1)
            for v in range(cur + 1):
                # need prev value u with u + d <= v, u <= len(dp)-1
                hi = min(v - d, len(dp) - 1)
                if hi >= 0:
                    new[v] = pref[hi + 1]
            dp = new
        return sum(dp) % MOD
