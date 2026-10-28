from typing import *
from bisect import bisect_left, bisect_right


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        pts = sorted(range(n), key=lambda i: -nums1[i])
        order = sorted(range(len(queries)), key=lambda q: -queries[q][0])
        # keys: nums2 values ascending; nv: negated sums, ascending
        # (sums strictly decreasing as keys increase in the true stack)
        keys: List[int] = []
        nv: List[int] = []
        ans = [-1] * len(queries)
        p = 0
        for q in order:
            x, y = queries[q]
            while p < n and nums1[pts[p]] >= x:
                idx = pts[p]
                a = nums2[idx]
                s = nums1[idx] + a
                p += 1
                i = bisect_left(keys, a)
                if i < len(keys) and -nv[i] >= s:
                    continue  # dominated by a point with nums2>=a and sum>=s
                k = bisect_right(keys, a)
                # first index j with val <= s  <=>  nv[j] >= -s
                j = bisect_left(nv, -s)
                pos = min(j, k)
                del keys[pos:k]
                del nv[pos:k]
                keys.insert(pos, a)
                nv.insert(pos, -s)
            pi = bisect_left(keys, y)
            if pi < len(keys):
                ans[q] = -nv[pi]
        return ans
