from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        ys = sorted(set(nums2))
        m = len(ys)
        # Fenwick tree for prefix max over reversed compressed nums2 index.
        tree = [-1] * (m + 1)

        def update(i, val):
            i += 1
            while i <= m:
                if tree[i] < val:
                    tree[i] = val
                i += i & -i

        def query(i):
            # max over reversed indices [0, i]
            res = -1
            i += 1
            while i > 0:
                if tree[i] > res:
                    res = tree[i]
                i -= i & -i
            return res

        points = sorted(range(n), key=lambda j: nums1[j], reverse=True)
        order = sorted(range(len(queries)), key=lambda k: queries[k][0], reverse=True)
        ans = [-1] * len(queries)
        p = 0
        for k in order:
            x, y = queries[k]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                pos = bisect_left(ys, nums2[j])
                update(m - 1 - pos, nums1[j] + nums2[j])
                p += 1
            q = bisect_left(ys, y)  # first ys value >= y
            if q >= m:
                continue
            ans[k] = query(m - 1 - q)
        return ans
