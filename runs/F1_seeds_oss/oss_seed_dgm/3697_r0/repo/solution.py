from math import gcd
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """Return the minimum total increments needed so that each value in ``target``
        has at least one multiple present in ``nums`` after increment operations.

        We may increment any element of ``nums`` by 1 any number of times; the cost is the
        total number of increments performed. After all increments each element of
        ``target`` must divide at least one element of the (modified) ``nums`` array.

        Because ``len(target)`` ≤ 4, we can consider every subset of target values.
        For a given subset we compute the least cost of turning a particular ``num``
        into a multiple of the *least common multiple* (LCM) of the subset – that value
        will be a multiple of every element of the subset.

        The problem then reduces to selecting, for each ``num``, at most one subset
        (possibly empty) such that the union of the selected subsets covers all target
        indices, and the sum of the associated costs is minimal.  This is a classic
        DP over bit‑masks where each ``num`` is processed like an item in a knapsack.
        """
        m = len(target)
        if m == 0:
            return 0
        full_mask = (1 << m) - 1

        # Pre‑compute LCM for every non‑empty subset of target indices.
        lcm_of_mask = [1] * (1 << m)
        for mask in range(1, 1 << m):
            l = 1
            for i in range(m):
                if mask >> i & 1:
                    t = target[i]
                    l = l * t // gcd(l, t)
            lcm_of_mask[mask] = l

        # DP over masks. dp[mask] = minimal cost after processing some prefix of nums.
        INF = 10 ** 18
        dp = [INF] * (1 << m)
        dp[0] = 0

        for a in nums:
            # cost_i[mask] = increments needed to turn a into a multiple of lcm_of_mask[mask]
            cost_i = [0] * (1 << m)
            for mask in range(1, 1 << m):
                l = lcm_of_mask[mask]
                # minimal increments to reach next multiple of l
                inc = (l - a % l) % l
                cost_i[mask] = inc
            newdp = dp[:]  # we may also choose to ignore this num
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                # try to use this num for any non‑empty subset
                sub = 1
                while sub < (1 << m):
                    # we only care about subsets that add new uncovered bits
                    new_mask = mask | sub
                    if new_mask != mask:  # sub adds something
                        newdp[new_mask] = min(newdp[new_mask], dp[mask] + cost_i[sub])
                    sub += 1
            dp = newdp

        return dp[full_mask]
