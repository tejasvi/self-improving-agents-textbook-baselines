from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        ys = sorted(set(nums2))
        m = len(ys)
        # Fenwick tree for prefix max over reversed rank (so prefix == suffix of nums2 values)
        tree = [-1] * (m + 1)

        def update(pos, val):
            # pos is 1-based reversed index
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

        order = sorted(range(n), key=lambda i: -nums1[i])
        qorder = sorted(range(len(queries)), key=lambda q: -queries[q][0])
        answer = [-1] * len(queries)
        p = 0
        for q in qorder:
            x, y = queries[q]
            while p < n and nums1[order[p]] >= x:
                i = order[p]
                r = bisect_left(ys, nums2[i])  # 0-based rank
                update(m - r, nums1[i] + nums2[i])
                p += 1
            # values with nums2 >= y: ranks r >= bisect_left(ys, y) -> reversed pos m - r <= m - lo
            lo = bisect_left(ys, y)
            if lo < m:
                answer[q] = query(m - lo)
        return answer
