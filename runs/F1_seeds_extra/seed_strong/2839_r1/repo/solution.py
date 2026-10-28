from typing import *
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        vals = sorted(set(nums2))
        m = len(vals)
        idx_of = {v: i for i, v in enumerate(vals)}
        # Fenwick tree for prefix max over reversed index: r = m - i (1-based, i 0-based)
        tree = [-1] * (m + 1)

        order = sorted(range(n), key=lambda j: -nums1[j])
        qorder = sorted(range(len(queries)), key=lambda q: -queries[q][0])
        ans = [-1] * len(queries)
        p = 0
        for q in qorder:
            x, y = queries[q]
            while p < n and nums1[order[p]] >= x:
                j = order[p]
                s = nums1[j] + nums2[j]
                # reversed 1-based index of nums2[j]
                i = m - idx_of[nums2[j]]
                while i <= m:
                    if tree[i] < s:
                        tree[i] = s
                    i += i & (-i)
                p += 1
            # values >= y correspond to reversed indices 1..m - bisect_left(vals, y)
            k = m - bisect_left(vals, y)
            best = -1
            while k > 0:
                if tree[k] > best:
                    best = tree[k]
                k -= k & (-k)
            ans[q] = best
        return ans
