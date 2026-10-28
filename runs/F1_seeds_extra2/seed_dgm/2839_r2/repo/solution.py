from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        vals = sorted(set(nums2))
        m = len(vals)
        rank = {v: i for i, v in enumerate(vals)}
        # Fenwick tree for prefix max over reversed ranks (so prefix == suffix in nums2)
        tree = [-1] * (m + 1)

        def update(pos, value):
            pos += 1
            while pos <= m:
                if tree[pos] < value:
                    tree[pos] = value
                pos += pos & -pos

        def query(pos):
            # max over reversed positions [0, pos]
            res = -1
            pos += 1
            while pos > 0:
                if tree[pos] > res:
                    res = tree[pos]
                pos -= pos & -pos
            return res

        points = sorted(range(n), key=lambda i: -nums1[i])
        q_order = sorted(range(len(queries)), key=lambda i: -queries[i][0])
        ans = [-1] * len(queries)
        p = 0
        for qi in q_order:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                update(m - 1 - rank[nums2[j]], nums1[j] + nums2[j])
                p += 1
            idx = bisect_left(vals, y)  # first value >= y
            if idx < m:
                ans[qi] = query(m - 1 - idx)
        return ans
