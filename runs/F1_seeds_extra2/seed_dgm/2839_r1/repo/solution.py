from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        vals = sorted(set(nums2))
        m = len(vals)
        rank = {v: i for i, v in enumerate(vals)}

        # Fenwick tree for prefix max over reversed ranks (position = m - rank).
        tree = [-1] * (m + 1)

        def update(pos, val):
            while pos <= m:
                if tree[pos] < val:
                    tree[pos] = val
                pos += pos & -pos

        def query(pos):
            best = -1
            while pos > 0:
                if tree[pos] > best:
                    best = tree[pos]
                pos -= pos & -pos
            return best

        order = sorted(range(n), key=lambda i: nums1[i], reverse=True)
        qorder = sorted(range(len(queries)), key=lambda i: queries[i][0], reverse=True)
        ans = [-1] * len(queries)

        p = 0
        for qi in qorder:
            x, y = queries[qi]
            while p < n and nums1[order[p]] >= x:
                j = order[p]
                update(m - rank[nums2[j]], nums1[j] + nums2[j])
                p += 1
            r0 = bisect_left(vals, y)
            if r0 < m:
                ans[qi] = query(m - r0)
        return ans
