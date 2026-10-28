from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # bucket pairs by their larger endpoint
        by_max = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            by_max[hi].append((lo, i))

        base = 0
        loss = [0] * m  # gain from removing each pair
        # top two (value, pair id) among pairs with max <= r
        best1_v, best1_id = 0, -1
        best2_v = 0
        for r in range(1, n + 1):
            for lo, i in by_max[r]:
                if lo > best1_v:
                    best2_v = best1_v
                    best1_v, best1_id = lo, i
                elif lo > best2_v:
                    best2_v = lo
            # subarrays ending at r with no conflicting pair
            base += r - best1_v
            if best1_id >= 0:
                # removing the owner pair raises L_r to best2_v
                loss[best1_id] += best1_v - best2_v

        return base + max(loss)
