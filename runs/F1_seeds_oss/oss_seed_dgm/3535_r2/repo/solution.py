from typing import List

MOD = 10 ** 9 + 7


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        max_val = max(nums)  # maximum possible value for arr1 elements
        # dp for previous index: dp[v] = ways where previous a = v
        prev = [0] * (max_val + 1)
        # initialize for i = 0
        for v in range(nums[0] + 1):
            prev[v] = 1
        # iterate over the rest of positions
        for i in range(1, n):
            cur = [0] * (max_val + 1)
            # minimum required increase from a_{i-1} to a_i
            min_inc = max(0, nums[i] - nums[i - 1])
            # prefix sums of prev for fast range sum queries
            prefix = [0] * (max_val + 2)
            for v in range(max_val + 1):
                prefix[v + 1] = (prefix[v] + prev[v]) % MOD
            # compute cur[v] for all feasible v (0..nums[i])
            for v in range(nums[i] + 1):
                # a_{i-1} must be <= v - min_inc and also <= nums[i-1]
                upper = v - min_inc
                if upper < 0:
                    continue  # no valid previous value
                upper = min(upper, nums[i - 1])
                # sum of prev[0..upper]
                cur[v] = prefix[upper + 1]
            prev = cur
        # total ways is sum over all possible a_{n-1}
        return sum(prev) % MOD
