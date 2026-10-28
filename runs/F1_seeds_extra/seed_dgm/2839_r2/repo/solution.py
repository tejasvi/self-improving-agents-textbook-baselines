from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        vals = sorted(set(nums2))
        m = len(vals)
        rank = {v: i for i, v in enumerate(vals)}
        # Fenwick tree for prefix max over reversed ranks (so suffix >= y becomes prefix)
        tree = [-1] * (m + 1)

        def update(pos, val):
            # pos is 0-based reversed index
            i = pos + 1
            while i <= m:
                if tree[i] < val:
                    tree[i] = val
                i += i & -i

        def query(cnt):
            # max over first cnt reversed positions
            res = -1
            i = cnt
            while i > 0:
                if tree[i] > res:
                    res = tree[i]
                i -= i & -i
            return res

        points = sorted(range(n), key=lambda j: -nums1[j])
        q_order = sorted(range(len(queries)), key=lambda k: -queries[k][0])
        ans = [-1] * len(queries)
        p = 0
        for k in q_order:
            x, y = queries[k]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                r = m - 1 - rank[nums2[j]]
                update(r, nums1[j] + nums2[j])
                p += 1
            # values >= y in vals: indices from b to m-1 -> reversed positions 0..m-1-b
            b = bisect_left(vals, y)
            cnt = m - b
            if cnt > 0:
                ans[k] = query(cnt)
        return ans
