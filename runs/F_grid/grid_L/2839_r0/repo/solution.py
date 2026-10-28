from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        vals = sorted(set(nums2))
        m = len(vals)
        pos = {v: i for i, v in enumerate(vals)}
        # Fenwick tree over reversed compressed nums2 for prefix max
        # (reversed index r = m-1-i, so nums2 >= y  <=>  r <= m-1-idx(y))
        tree = [-1] * (m + 1)

        def update(r, value):
            r += 1
            while r <= m:
                if tree[r] < value:
                    tree[r] = value
                r += r & -r

        def query(r):
            # max over reversed indices in [0, r]
            res = -1
            r += 1
            while r > 0:
                if tree[r] > res:
                    res = tree[r]
                r -= r & -r
            return res

        order = sorted(range(n), key=lambda i: -nums1[i])
        q_order = sorted(range(len(queries)), key=lambda k: -queries[k][0])
        ans = [-1] * len(queries)
        p = 0
        for k in q_order:
            x, y = queries[k]
            while p < n and nums1[order[p]] >= x:
                j = order[p]
                update(m - 1 - pos[nums2[j]], nums1[j] + nums2[j])
                p += 1
            idx = bisect_left(vals, y)
            if idx >= m:
                continue
            ans[k] = query(m - 1 - idx)
        return ans
