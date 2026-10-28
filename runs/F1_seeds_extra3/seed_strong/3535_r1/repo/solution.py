from typing import *

MOD = 10**9 + 7


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        # v = arr1[i], arr2[i] = nums[i] - v, need 0 <= v <= nums[i].
        # arr1 non-decreasing: v_i >= v_{i-1}
        # arr2 non-increasing: v_i >= v_{i-1} + (nums[i] - nums[i-1])
        # So v_i >= v_{i-1} + max(0, nums[i] - nums[i-1]).
        n = len(nums)
        M = nums[0]
        dp = [1] * (M + 1)
        for i in range(1, n):
            prev_max = nums[i - 1]
            cur_max = nums[i]
            d = max(0, cur_max - prev_max)
            # prefix sums of dp over u in [0, prev_max]
            pref = [0] * (prev_max + 2)
            for u in range(prev_max + 1):
                pref[u + 1] = (pref[u] + dp[u]) % MOD
            new = [0] * (cur_max + 1)
            for v in range(cur_max + 1):
                hi = v - d  # u <= hi
                if hi < 0:
                    new[v] = 0
                else:
                    if hi > prev_max:
                        hi = prev_max
                    new[v] = pref[hi + 1]
            dp = new
        return sum(dp) % MOD
