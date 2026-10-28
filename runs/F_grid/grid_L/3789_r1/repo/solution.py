from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # For a subarray [s..r] to contain a pair (lo, hi) we need s <= lo and hi <= r.
        # For fixed r, the valid starts are s > L(r), where L(r) is the max lo over
        # pairs with hi <= r (0 if none). So the count ending at r is r - L(r).
        # Removing the pair providing the max changes L(r) to the second max.
        m = len(conflictingPairs)
        gain = [0] * m  # gain[p]: extra subarrays gained by removing pair p
        # Track top two (value, pair index) over pairs with hi <= r.
        best1 = best2 = 0
        idx1 = -1
        # Indices of pairs grouped by hi, to map back from values to indices.
        pairs_by_hi = [[] for _ in range(n + 1)]
        for p, (a, b) in enumerate(conflictingPairs):
            pairs_by_hi[max(a, b)].append(p)

        base = 0
        for r in range(1, n + 1):
            for p in pairs_by_hi[r]:
                lo = min(conflictingPairs[p][0], conflictingPairs[p][1])
                if lo > best1:
                    best2 = best1
                    best1 = lo
                    idx1 = p
                elif lo > best2:
                    best2 = lo
            base += r - best1
            if idx1 != -1:
                gain[idx1] += best1 - best2

        return base + max(gain) if m else base
