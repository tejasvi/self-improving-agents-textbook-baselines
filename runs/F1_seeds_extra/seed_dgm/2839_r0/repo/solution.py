from typing import List
import bisect


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        # Compress nums2 values; reversed index so that "nums2 >= y" is a prefix.
        vals = sorted(set(nums2))
        m = len(vals)
        tree = [-1] * (m + 1)

        def update(pos, val):
            # pos is 1-based
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

        points = sorted(range(n), key=lambda i: -nums1[i])
        qs = sorted(range(len(queries)), key=lambda i: -queries[i][0])
        ans = [-1] * len(queries)
        p = 0
        for qi in qs:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                idx = bisect.bisect_left(vals, nums2[j])  # 0-based
                # reversed position: larger values -> smaller positions
                update(m - idx, nums1[j] + nums2[j])
                p += 1
            # values >= y: indices idx >= bisect_left(vals, y) -> reversed pos <= m - that
            start = bisect.bisect_left(vals, y)
            ans[qi] = query(m - start)
        return ans
