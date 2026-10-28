from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Group pairs by their larger element (hi); store smaller element (lo).
        by_hi = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            lo, hi = min(a, b), max(a, b)
            by_hi[hi].append((lo, idx))

        m = len(conflictingPairs)
        extra = [0] * m  # extra subarrays gained by removing pair idx
        base = 0
        m1val, m1idx, m2val = 0, -1, 0  # top two lo values among pairs with hi <= r

        for r in range(1, n + 1):
            for lo, idx in by_hi[r]:
                if lo > m1val:
                    m2val = m1val
                    m1val, m1idx = lo, idx
                elif lo > m2val:
                    m2val = lo
            base += r - m1val
            if m1idx != -1:
                extra[m1idx] += m1val - m2val

        return base + (max(extra) if m > 0 else 0)
