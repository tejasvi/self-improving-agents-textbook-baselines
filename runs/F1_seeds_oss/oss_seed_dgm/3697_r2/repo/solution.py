from typing import List
import math

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Number of target elements is small (<=4). We'll use DP over subsets.
        k = len(target)
        full_mask = (1 << k) - 1
        # Precompute LCM for each subset mask
        lcm_mask = [1] * (1 << k)
        for mask in range(1, 1 << k):
            # find least significant set bit
            lsb = mask & -mask
            idx = (lsb.bit_length() - 1)  # index of that bit
            prev = mask ^ lsb
            lcm_mask[mask] = math.lcm(lcm_mask[prev], target[idx])

        INF = 10 ** 18
        dp = [INF] * (1 << k)
        dp[0] = 0
        for x in nums:
            # cost for each subset using this element
            cost = [0] * (1 << k)
            for mask in range(1, 1 << k):
                L = lcm_mask[mask]
                # smallest multiple of L not less than x
                mul = ((x + L - 1) // L) * L
                cost[mask] = mul - x
            # DP transition using this element (it can be used at most once)
            new_dp = dp[:]  # copy current dp for this iteration
            for cur_mask in range(1 << k):
                if dp[cur_mask] == INF:
                    continue
                # try adding any non-empty subset
                sub = full_mask ^ cur_mask  # remaining targets to cover (but we can also add subset of already covered, no benefit)
                # iterate over subsets of remaining targets
                submask = sub
                while submask:
                    c = cost[submask]
                    nxt = cur_mask | submask
                    if dp[cur_mask] + c < new_dp[nxt]:
                        new_dp[nxt] = dp[cur_mask] + c
                    submask = (submask - 1) & sub
            dp = new_dp
        return dp[full_mask]
