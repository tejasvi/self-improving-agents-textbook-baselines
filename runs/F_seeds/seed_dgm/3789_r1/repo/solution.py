from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Pairs grouped by their larger element.
        by_max = [[] for _ in range(n + 1)]
        for idx, (a, b) in enumerate(conflictingPairs):
            by_max[max(a, b)].append((min(a, b), idx))

        # For each r, the valid subarrays ending at r start after L1(r),
        # where L1 is the largest "min" among pairs with max <= r.
        # Removing the pair achieving L1 raises the bound to L2 (second largest).
        base = 0
        extra = [0] * len(conflictingPairs)
        best1 = (0, -1)  # (value, index)
        best2 = 0
        for r in range(1, n + 1):
            for val, idx in by_max[r]:
                if val > best1[0]:
                    best2 = best1[0]
                    best1 = (val, idx)
                elif val > best2:
                    best2 = val
            L1 = best1[0]
            base += r - L1
            if best1[1] >= 0:
                extra[best1[1]] += L1 - best2

        return base + max(extra)
