from typing import *

MOD = 10**9 + 7


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        # dp[v] = number of valid prefixes where arr1[i] == v
        # Transition: arr1[i] = v requires u = arr1[i-1] satisfy
        #   u <= v - max(0, d), u <= nums[i-1], where d = nums[i] - nums[i-1]
        # and 0 <= v <= nums[i].
        n = len(nums)
        prev = [1] * (nums[0] + 1)
        for i in range(1, n):
            d = nums[i] - nums[i - 1]
            sd = max(0, d)
            # prefix sums of prev: pre[k] = sum(prev[0..k-1])
            pre = [0] * (len(prev) + 1)
            for k, x in enumerate(prev):
                pre[k + 1] = (pre[k] + x) % MOD
            cur = [0] * (nums[i] + 1)
            top_prev = len(prev) - 1
            for v in range(nums[i] + 1):
                hi = min(v - sd, top_prev)
                if hi >= 0:
                    cur[v] = pre[hi + 1]
            prev = cur
        return sum(prev) % MOD
