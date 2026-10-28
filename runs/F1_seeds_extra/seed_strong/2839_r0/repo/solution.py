from typing import *
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        ys = sorted(set(nums2))
        m = len(ys)
        pos = {v: i for i, v in enumerate(ys)}
        # Fenwick tree for prefix max over reversed compressed index
        tree = [-1] * (m + 1)

        def update(i, val):
            # i: reversed index (0-based) -> 1-based i+1
            i += 1
            while i <= m:
                if tree[i] < val:
                    tree[i] = val
                i += i & -i

        def query(i):
            # max over reversed indices [0, i)
            res = -1
            while i > 0:
                if tree[i] > res:
                    res = tree[i]
                i -= i & -i
            return res

        points = sorted(range(n), key=lambda j: -nums1[j])
        qs = sorted(range(len(queries)), key=lambda k: -queries[k][0])
        ans = [-1] * len(queries)
        p = 0
        for k in qs:
            x, y = queries[k]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                update(m - 1 - pos[nums2[j]], nums1[j] + nums2[j])
                p += 1
            # indices with nums2 >= y: compressed idx >= t
            t = bisect_left(ys, y)
            if t >= m:
                continue
            # reversed indices r = m-1-c for c in [t, m-1] -> r in [0, m-1-t]
            ans[k] = query(m - t)
        return ans
