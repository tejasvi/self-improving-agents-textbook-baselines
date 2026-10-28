from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # group pairs by right endpoint (max of the two values)
        by_right = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            by_right[hi].append((lo, idx))

        m = len(conflictingPairs)
        extra = [0] * m  # extra subarrays gained when pair i is removed
        base = 0
        best1 = 0   # largest left endpoint among pairs with right <= r
        owner = -1  # index of pair achieving best1
        best2 = 0   # second largest (from a different pair)

        for r in range(1, n + 1):
            for lo, idx in by_right[r]:
                if lo > best1:
                    best2 = best1
                    best1 = lo
                    owner = idx
                elif lo == best1:
                    best2 = lo
                elif lo > best2:
                    best2 = lo
            base += r - best1
            if owner >= 0:
                extra[owner] += best1 - best2

        return base + max(extra)
