from typing import List

class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """Return the maximum number of groups with strictly increasing lengths.

        We need to form groups of sizes 1, 2, ..., k (for some k) such that each
        number i (0-indexed) is used at most usageLimits[i] times in total and
        appears at most once in each group.  For a given candidate k, a number i
        can contribute to at most min(usageLimits[i], k) positions (once per each
        of the k groups).  Hence the total number of usable slots is
        sum_i min(usageLimits[i], k).  The groups require exactly k*(k+1)//2
        slots.  The condition

            sum_i min(usageLimits[i], k) >= k*(k+1)//2

        is necessary and sufficient for the existence of such a grouping.

        We binary‑search the largest k that satisfies the condition.
        """
        total = sum(usageLimits)
        import math
        # Upper bound using quadratic formula: k(k+1)/2 <= total
        high = int((-1 + math.isqrt(1 + 8 * total)) // 2) + 1  # exclusive upper bound
        low = 0
        while low < high:
            mid = (low + high + 1) // 2
            required = mid * (mid + 1) // 2
            slots = 0
            for lim in usageLimits:
                slots += lim if lim < mid else mid
                if slots >= required:
                    break
            if slots >= required:
                low = mid
            else:
                high = mid - 1
        return low
