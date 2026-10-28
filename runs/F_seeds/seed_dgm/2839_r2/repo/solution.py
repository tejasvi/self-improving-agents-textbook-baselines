from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        # Compress nums2 values for a Fenwick tree supporting suffix max.
        vals = sorted(set(nums2))
        m = len(vals)
        tree = [-1] * (m + 1)

        def update(pos, val):
            # pos is 1-based index in reversed order so prefix max == suffix max in vals
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            res = -1
            while pos > 0:
                if tree[pos] > res:
                    res = tree[pos]
                pos -= pos & -pos
            return res

        # Reversed index: vals[k] maps to m - k (1-based), so larger nums2 -> smaller index.
        rank = {v: m - k for k, v in enumerate(vals)}

        points = sorted(range(n), key=lambda i: -nums1[i])
        q_order = sorted(range(len(queries)), key=lambda i: -queries[i][0])
        ans = [-1] * len(queries)
        p = 0
        for qi in q_order:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                i = points[p]
                update(rank[nums2[i]], nums1[i] + nums2[i])
                p += 1
            # need nums2 >= y: vals index >= bisect_left(vals, y), reversed index <= m - idx
            idx = bisect_left(vals, y)
            if idx < m:
                ans[qi] = query(m - idx)
        return ans
