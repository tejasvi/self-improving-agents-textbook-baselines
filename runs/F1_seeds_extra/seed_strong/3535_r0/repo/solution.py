from typing import *

MOD = 10**9 + 7


class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        # v = arr1[i], arr2[i] = nums[i] - v, 0 <= v <= nums[i].
        # Constraint: v_i >= v_{i-1} + max(0, nums[i] - nums[i-1]).
        n = len(nums)
        prev = [1] * (nums[0] + 1)
        for i in range(1, n):
            m = nums[i]
            pm = nums[i - 1]
            d = max(0, m - pm)
            # prefix sums of prev: pre[k] = sum of prev[0..k-1]
            pre = [0] * (len(prev) + 1)
            for k, x in enumerate(prev):
                pre[k + 1] = (pre[k] + x) % MOD
            cur = [0] * (m + 1)
            total = len(prev)
            for v in range(m + 1):
                u_max = v - d  # u <= u_max
                if u_max < 0:
                    continue
                if u_max >= total:
                    u_max = total - 1
                cur[v] = pre[u_max + 1]
            prev = cur
        return sum(prev) % MOD
