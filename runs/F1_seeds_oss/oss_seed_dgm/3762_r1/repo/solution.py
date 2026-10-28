from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """Return the maximum possible minimum value in gameScore after at most m moves.

        The problem reduces to finding the largest X such that we can ensure every index i
        receives a total score of at least X using at most m moves. Each move lands on an
        index and adds points[i] to that index's score. To achieve a score of at least X on
        index i we need to land on it at least ceil(X / points[i]) times. Since every move
        contributes to exactly one index, the total number of required moves is the sum of
        those ceil values. Extra moves are allowed because they only increase scores.

        Therefore we need the maximum X satisfying:
            sum_i ceil(X / points[i]) <= m
        This condition is monotonic in X, allowing binary search over the answer range.
        """
        # Helper to check feasibility of a candidate X.
        def feasible(X: int) -> bool:
            total = 0
            for p in points:
                # ceil division without floating point
                need = (X + p - 1) // p
                total += need
                if total > m:
                    return False
            return True

        # Binary search for the greatest feasible X.
        lo, hi = 0, max(points) * m  # inclusive lower bound, exclusive upper bound
        while lo < hi:
            mid = (lo + hi + 1) // 2  # upper mid to avoid infinite loop
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
