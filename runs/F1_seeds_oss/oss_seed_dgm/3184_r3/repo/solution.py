'''Solution for maximum-balanced-subsequence-sum problem.

The condition for a balanced subsequence can be rewritten as:
    nums[j] - nums[i] >= j - i   ⇔   (nums[j] - j) >= (nums[i] - i).
Thus, for each index we define a transformed value a[i] = nums[i] - i.
A subsequence is balanced iff the sequence of a[i] values is non‑decreasing.

The task then becomes: choose a subsequence with non‑decreasing a[i] that maximises the
sum of the original nums values. This is exactly the "maximum sum increasing subsequence"
problem on the array a, where the weight of each element is nums[i] (instead of a[i]).

We can compute dp[i] – the best sum of a balanced subsequence ending at i – as:
    dp[i] = nums[i] + max(0, max{ dp[j] | j < i and a[j] <= a[i] })
The extra max(0, …) allows starting a new subsequence at i.

To obtain the maximum over all previous j efficiently we use a Fenwick (Binary Indexed)
Tree that supports prefix‑maximum queries. After compressing the distinct a[i] values
to a small range we process the array left‑to‑right in O(n log n).
'''

from typing import List
import bisect


class FenwickMax:
    """Fenwick Tree (Binary Indexed Tree) for prefix maximum queries.

    The tree is 1‑indexed. `update(i, val)` stores the maximum value at position i.
    `query(i)` returns max{tree[1..i]}.
    """

    def __init__(self, size: int):
        self.n = size
        self.bit = [-10**18] * (size + 1)  # initialise with very small numbers

    def update(self, idx: int, value: int) -> None:
        while idx <= self.n:
            if value > self.bit[idx]:
                self.bit[idx] = value
            idx += idx & -idx

    def query(self, idx: int) -> int:
        res = -10**18
        while idx > 0:
            if self.bit[idx] > res:
                res = self.bit[idx]
            idx -= idx & -idx
        return res


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """Return the maximum sum of a balanced subsequence.

        Parameters
        ----------
        nums: List[int]
            The input integer array.

        Returns
        -------
        int
            Maximum possible sum of elements in a balanced subsequence.
        """
        n = len(nums)
        # Transform values
        transformed = [num - i for i, num in enumerate(nums)]
        # Coordinate compression
        uniq = sorted(set(transformed))
        # Fenwick tree for prefix maximums; we start with 0 as the neutral value
        ft = FenwickMax(len(uniq))
        # Initialise the tree with 0 at every index so that a new subsequence can start.
        for i in range(1, len(uniq) + 1):
            ft.update(i, 0)
        best_overall = -10**18
        for i, num in enumerate(nums):
            key = transformed[i]
            idx = bisect.bisect_left(uniq, key) + 1  # 1‑based index for BIT
            prev_best = ft.query(idx)  # max dp for a[j] <= a[i]
            # Start new subsequence or extend the best previous one
            cur = num + max(0, prev_best)
            best_overall = max(best_overall, cur)
            ft.update(idx, cur)
        return best_overall
