from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[a] = number of valid prefixes with arr1[i] == a
        m = nums[0]
        dp = [1] * (m + 1)
        for i in range(1, n):
            prev_max = nums[i - 1]
            cur_max = nums[i]
            d = max(0, cur_max - nums[i - 1])
            # prefix sums of dp
            pref = [0] * (prev_max + 2)
            for a in range(prev_max + 1):
                pref[a + 1] = (pref[a] + dp[a]) % MOD
            new = [0] * (cur_max + 1)
            for b in range(cur_max + 1):
                # need a <= b - d, a in [0, prev_max]
                hi = min(b - d, prev_max)
                if hi >= 0:
                    new[b] = pref[hi + 1]
            dp = new
        return sum(dp) % MOD
