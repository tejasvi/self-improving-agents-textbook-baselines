from typing import List


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        # dp[a] = number of valid prefixes where arr1[i] == a
        dp = [1] * (nums[0] + 1)
        for i in range(1, len(nums)):
            prev_max = nums[i - 1]
            cur_max = nums[i]
            shift = max(0, nums[i] - nums[i - 1])
            # prefix sums of dp
            pref = [0] * (len(dp) + 1)
            for a, v in enumerate(dp):
                pref[a + 1] = (pref[a] + v) % MOD
            new = [0] * (cur_max + 1)
            for b in range(cur_max + 1):
                hi = b - shift  # need a <= hi
                if hi < 0:
                    continue
                hi = min(hi, len(dp) - 1)
                new[b] = pref[hi + 1]
            dp = new
        return sum(dp) % MOD
