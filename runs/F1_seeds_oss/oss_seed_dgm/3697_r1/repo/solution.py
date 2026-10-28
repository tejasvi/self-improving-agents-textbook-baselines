from typing import List
import math

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full_mask = (1 << m) - 1
        # Precompute lcm for each subset of target
        lcm_mask = [1] * (1 << m)
        for mask in range(1, 1 << m):
            # find least significant set bit
            lsb = mask & -mask
            idx = (lsb.bit_length() - 1)  # index of that bit
            prev = mask ^ lsb
            if prev == 0:
                lcm_mask[mask] = target[idx]
            else:
                lcm_mask[mask] = lcm_mask[prev] * target[idx] // math.gcd(lcm_mask[prev], target[idx])
        INF = 10 ** 18
        dp = [INF] * (1 << m)
        dp[0] = 0
        for num in nums:
            # cost for using this num to cover any subset
            cost_subset = [0] * (1 << m)
            for mask in range(1, 1 << m):
                L = lcm_mask[mask]
                # minimal multiple of L not less than num
                multiple = ((num + L - 1) // L) * L
                cost_subset[mask] = multiple - num
            new_dp = dp[:]
            for prev_mask in range(1 << m):
                if dp[prev_mask] == INF:
                    continue
                for mask in range(1, 1 << m):
                    new_mask = prev_mask | mask
                    new_cost = dp[prev_mask] + cost_subset[mask]
                    if new_cost < new_dp[new_mask]:
                        new_dp[new_mask] = new_cost
            dp = new_dp
        return dp[full_mask]
