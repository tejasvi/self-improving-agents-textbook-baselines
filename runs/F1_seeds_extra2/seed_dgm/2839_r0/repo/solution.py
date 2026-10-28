from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        vals = sorted(set(nums2))
        m = len(vals)
        # Fenwick tree over reversed compressed index for suffix max of nums2 >= value
        tree = [-1] * (m + 1)

        def update(pos, val):
            # pos: 0-based index in vals; reversed index so suffix becomes prefix
            i = m - pos
            while i <= m:
                if tree[i] < val:
                    tree[i] = val
                i += i & -i

        def query(pos):
            # max over compressed indices >= pos
            i = m - pos
            res = -1
            while i > 0:
                if tree[i] > res:
                    res = tree[i]
                i -= i & -i
            return res

        pts = sorted(range(n), key=lambda j: nums1[j], reverse=True)
        order = sorted(range(len(queries)), key=lambda q: queries[q][0], reverse=True)
        ans = [-1] * len(queries)
        p = 0
        for q in order:
            x, y = queries[q]
            while p < n and nums1[pts[p]] >= x:
                j = pts[p]
                update(bisect_left(vals, nums2[j]), nums1[j] + nums2[j])
                p += 1
            start = bisect_left(vals, y)
            if start < m:
                ans[q] = query(start)
        return ans
