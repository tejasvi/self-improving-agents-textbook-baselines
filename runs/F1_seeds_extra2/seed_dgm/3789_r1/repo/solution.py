from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # A subarray [l, r] is bad iff some pair (a, b) has
        # l <= min(a, b) and max(a, b) <= r.
        # For each r, the number of good subarrays ending at r is
        # r - L[r], where L[r] = max over pairs with max(a, b) <= r of min(a, b).
        # Removing the pair that attains L[r] raises L[r] to the second best.
        # Gains are accumulated per pair id; the answer is base + max gain.
        by_max = [[] for _ in range(n + 1)]
        for idx, (x, y) in enumerate(conflictingPairs):
            by_max[max(x, y)].append((min(x, y), idx))

        v1 = v2 = 0          # best and second-best minima (0 = none)
        id1 = -1             # pair id attaining v1
        gain = {}
        base = 0
        for r in range(1, n + 1):
            for mn, idx in by_max[r]:
                if mn > v1:
                    v2 = v1
                    v1 = mn
                    id1 = idx
                elif mn > v2:
                    v2 = mn
            base += r - v1
            if id1 >= 0:
                gain[id1] = gain.get(id1, 0) + (v1 - v2)

        best_gain = max(gain.values(), default=0)
        return base + best_gain
