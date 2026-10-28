from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        ys = sorted(set(nums2))
        m = len(ys)
        rank = {v: i for i, v in enumerate(ys)}
        # Fenwick tree for prefix max over reversed ranks (so suffix in ys becomes prefix)
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

        points = sorted(range(n), key=lambda j: nums1[j], reverse=True)
        qorder = sorted(range(len(queries)), key=lambda i: queries[i][0], reverse=True)
        ans = [-1] * len(queries)
        p = 0
        for qi in qorder:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                r = rank[nums2[j]]  # 0-based rank in ys
                # reversed 1-based position: larger values -> smaller position
                update(m - r, nums1[j] + nums2[j])
                p += 1
            # need nums2 >= y -> ranks >= bisect_left(ys, y) -> positions <= m - idx
            idx = bisect_left(ys, y)
            if idx < m:
                ans[qi] = query(m - idx)
        return ans
