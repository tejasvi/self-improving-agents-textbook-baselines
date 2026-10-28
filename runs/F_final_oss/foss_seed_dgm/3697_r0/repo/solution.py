from math import gcd
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """Return the minimum total increments needed so that each target value
        has at least one multiple among the (possibly incremented) nums.
        Each element of nums can be incremented independently; the cost is the
        total amount incremented across all elements.
        """
        m = len(target)
        full_mask = (1 << m) - 1

        # Helper to compute lcm safely.
        def lcm(a: int, b: int) -> int:
            return a // gcd(a, b) * b

        # Pre‑compute LCM for every non‑empty subset of target.
        subset_lcm = [1] * (1 << m)
        for mask in range(1, 1 << m):
            cur = 1
            for i in range(m):
                if mask >> i & 1:
                    cur = lcm(cur, target[i])
            subset_lcm[mask] = cur

        # For each num, compute the cost to make it a multiple of each subset LCM.
        # cost[mask] = minimal increments needed for this particular num.
        # We'll use DP over masks, treating each num at most once.
        INF = 10**18
        dp = [INF] * (1 << m)
        dp[0] = 0

        for num in nums:
            # compute cost for all non‑empty subsets for this num
            cost = [0] * (1 << m)
            for mask in range(1, 1 << m):
                L = subset_lcm[mask]
                # next multiple of L not less than num
                nxt = ((num + L - 1) // L) * L
                cost[mask] = nxt - num
            # DP transition: try to use this num for any subset that does not
            # overlap with already satisfied targets.
            new_dp = dp[:]  # copy current state
            for used in range(1 << m):
                if dp[used] == INF:
                    continue
                remaining = full_mask ^ used
                sub = remaining
                while sub:
                    # use this num to cover 'sub' (non‑empty)
                    new_mask = used | sub
                    cand = dp[used] + cost[sub]
                    if cand < new_dp[new_mask]:
                        new_dp[new_mask] = cand
                    sub = (sub - 1) & remaining
            dp = new_dp

        return int(dp[full_mask])
