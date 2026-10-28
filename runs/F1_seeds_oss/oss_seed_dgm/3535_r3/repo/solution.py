from typing import List

MOD = 10**9 + 7

class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        max_val = max(nums)
        # dp for previous index, size max_val+1, initialize for i=0
        dp_prev = [0] * (max_val + 1)
        for v in range(nums[0] + 1):
            dp_prev[v] = 1
        # iterate over positions
        for i in range(1, n):
            inc = nums[i] - nums[i-1]
            inc_pos = inc if inc > 0 else 0  # max(0, inc)
            # prefix sums of dp_prev
            prefix = [0] * (max_val + 1)
            cur = 0
            for v in range(max_val + 1):
                cur = (cur + dp_prev[v]) % MOD
                prefix[v] = cur
            dp_cur = [0] * (max_val + 1)
            # possible a_i values are 0..nums[i]
            for v in range(nums[i] + 1):
                upper = v - inc_pos
                if upper < 0:
                    dp_cur[v] = 0
                else:
                    # also cannot exceed previous max a value nums[i-1]
                    if upper > nums[i-1]:
                        upper = nums[i-1]
                    dp_cur[v] = prefix[upper]
            dp_prev = dp_cur
        # sum over final a_n-1 values
        ans = sum(dp_prev[v] for v in range(nums[-1] + 1)) % MOD
        return ans
