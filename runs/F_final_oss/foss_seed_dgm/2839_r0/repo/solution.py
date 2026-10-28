from typing import List
import bisect

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.tree = [float('-inf')] * (n + 1)  # 1-indexed

    def update(self, i: int, value: int):
        # set position i to max of existing and value
        while i <= self.n:
            if value > self.tree[i]:
                self.tree[i] = value
            i += i & -i

    def query(self, i: int) -> int:
        # maximum in prefix [1..i]
        res = float('-inf')
        while i > 0:
            if self.tree[i] > res:
                res = self.tree[i]
            i -= i & -i
        return res


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        # Coordinate compression for nums2 values
        uniq = sorted(set(nums2))
        m = len(uniq)
        # Helper to get reversed index for BIT (so that larger nums2 correspond to smaller indices)
        def rev_idx(val: int) -> int:
            # rank in ascending order (0‑based)
            rank = bisect.bisect_left(uniq, val)
            # reversed 1‑based index
            return m - rank

        # Prepare points sorted by nums1 descending
        points = [(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(len(nums1))]
        points.sort(key=lambda x: -x[0])

        # Prepare queries with original positions, sort by x descending
        q_with_idx = [(queries[i][0], queries[i][1], i) for i in range(len(queries))]
        q_with_idx.sort(key=lambda x: -x[0])

        bit = Fenwick(m)
        ans = [-1] * len(queries)
        p = 0
        n_points = len(points)
        for x, y, idx in q_with_idx:
            # insert all points with nums1 >= x
            while p < n_points and points[p][0] >= x:
                _, n2, s = points[p]
                bit.update(rev_idx(n2), s)
                p += 1
            # query for nums2 >= y
            # find first position in uniq where value >= y
            rank = bisect.bisect_left(uniq, y)
            if rank == m:
                # no nums2 large enough
                ans[idx] = -1
            else:
                limit = m - rank  # maximum reversed index to include
                best = bit.query(limit)
                ans[idx] = best if best != float('-inf') else -1
        return ans
