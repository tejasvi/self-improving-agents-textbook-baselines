from bisect import bisect_left, bisect_right
from typing import List

class BIT:
    """Fenwick Tree for prefix maximum query and point update (max)."""
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (self.n + 1)  # stores max, 0 is safe because sums are positive

    def update(self, idx: int, value: int):
        # update index idx (1‑based) with max
        while idx <= self.n:
            if value > self.tree[idx]:
                self.tree[idx] = value
            idx += idx & -idx

    def query(self, idx: int) -> int:
        # max in prefix [1..idx]
        res = 0
        while idx > 0:
            if self.tree[idx] > res:
                res = self.tree[idx]
            idx -= idx & -idx
        return res

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        # Prepare points
        points = [(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)]
        # Coordinate compression for nums2 (ascending order)
        sorted_vals = sorted(set(nums2))
        m = len(sorted_vals)
        # Helper to get reversed index for BIT (so that suffix >= y becomes prefix)
        def rev_idx(val: int) -> int:
            # position in ascending list (0‑based)
            pos = bisect_left(sorted_vals, val)
            # all values >= val correspond to indices pos..m-1 in ascending order
            # reversed index = m - pos
            return m - pos
        # Sort points by nums1 descending
        points.sort(key=lambda x: -x[0])
        # Prepare queries with original order
        q_with_idx = [(queries[i][0], queries[i][1], i) for i in range(len(queries))]
        q_with_idx.sort(key=lambda x: -x[0])
        bit = BIT(m)
        ans = [-1] * len(queries)
        p = 0
        for x, y, qi in q_with_idx:
            # add all points with nums1 >= x
            while p < n and points[p][0] >= x:
                _, v2, s = points[p]
                idx = rev_idx(v2)
                bit.update(idx, s)
                p += 1
            # query for nums2 >= y
            # find smallest position in ascending where value >= y
            pos = bisect_left(sorted_vals, y)
            if pos == m:  # no value >= y
                ans[qi] = -1
            else:
                idx = m - pos  # prefix length in reversed indexing
                max_sum = bit.query(idx)
                ans[qi] = max_sum if max_sum != 0 else -1
        return ans
