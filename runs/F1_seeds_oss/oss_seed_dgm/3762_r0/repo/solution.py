from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """Return the maximum possible minimum value in gameScore after at most m moves.

        The problem reduces to finding the largest X such that we can ensure each index i
        receives at least X points. Each visit to index i adds points[i] to its score.
        Thus, to achieve a score of at least X at i we need at least ceil(X / points[i]) visits.
        Since every move is a visit and we can always construct a walk that realises any
        multiset of visit counts on a line (by oscillating between neighbours), the only
        constraint is the total number of required visits.

        Therefore we binary‑search the answer X and check whether
            sum_i ceil(X / points[i]) <= m
        holds.
        """
        # Edge case: no moves
        if m == 0:
            return 0

        # Helper to decide feasibility of a candidate minimum score X
        def feasible(X: int) -> bool:
            total = 0
            for p in points:
                # ceil division without floating point
                total += (X + p - 1) // p
                if total > m:  # early exit to avoid overflow
                    return False
            return total <= m

        # Binary search for the maximum feasible X
        low, high = 0, max(points) * m  # exclusive upper bound
        while low < high:
            mid = (low + high + 1) // 2  # upper mid to avoid infinite loop
            if feasible(mid):
                low = mid
            else:
                high = mid - 1
        return low
