from typing import List
import math

class FenwickMax:
    """Fenwick Tree (Binary Indexed Tree) for prefix maximum queries."""
    def __init__(self, size: int):
        self.n = size
        self.tree = [-math.inf] * (self.n + 1)

    def update(self, index: int, value: int) -> None:
        """Set position `index` (1‑based) to max(current, value)."""
        i = index
        while i <= self.n:
            if value > self.tree[i]:
                self.tree[i] = value
            i += i & -i

    def query(self, index: int) -> int:
        """Return max value in prefix [1, index]. Returns -inf if none."""
        res = -math.inf
        i = index
        while i > 0:
            if self.tree[i] > res:
                res = self.tree[i]
            i -= i & -i
        return res


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """Return the maximum sum of a balanced subsequence.

        The condition nums[i_j] - nums[i_{j-1}] >= i_j - i_{j-1} is equivalent to
        (nums[i] - i) being non‑decreasing along the chosen indices.  Hence we need
        the maximum‑sum subsequence where the transformed values a_i = nums[i] - i
        are non‑decreasing.  This is a classic maximum‑sum increasing (non‑decreasing)
        subsequence problem that can be solved in O(N log N) using a Fenwick tree
        (or segment tree) over the compressed coordinates of a_i.
        """
        n = len(nums)
        if n == 0:
            return 0

        # Transform the array.
        transformed = [nums[i] - i for i in range(n)]
        # Coordinate compression.
        uniq = sorted(set(transformed))
        comp = {v: i + 1 for i, v in enumerate(uniq)}  # 1‑based indices for Fenwick

        ft = FenwickMax(len(uniq))
        answer = -math.inf

        for i in range(n):
            idx = comp[transformed[i]]
            best_prev = ft.query(idx)  # max dp for a_j <= a_i
            # If there is no valid previous subsequence, best_prev is -inf.
            # In that case we start a new subsequence with nums[i] alone.
            add = 0 if best_prev == -math.inf else max(0, best_prev)
            dp = nums[i] + add
            # Update structures.
            ft.update(idx, dp)
            if dp > answer:
                answer = dp

        return answer
