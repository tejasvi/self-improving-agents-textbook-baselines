from typing import List


class Solution:
    def maxFrequencyScore(self, nums: List[int], k: int) -> int:
        a = sorted(nums)
        n = len(a)
        P = [0] * (n + 1)
        for i, x in enumerate(a):
            P[i + 1] = P[i] + x

        def feasible(f: int) -> bool:
            for l in range(n - f + 1):
                r = l + f - 1
                m = (l + r) // 2
                med = a[m]
                cost = (med * (m - l) - (P[m] - P[l])
                        + (P[r + 1] - P[m + 1]) - med * (r - m))
                if cost <= k:
                    return True
            return False

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
