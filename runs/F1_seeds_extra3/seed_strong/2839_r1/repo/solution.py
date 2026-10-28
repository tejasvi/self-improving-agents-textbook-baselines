from typing import *
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        pts = sorted(range(n), key=lambda i: -nums1[i])
        qs = sorted(range(len(queries)), key=lambda q: -queries[q][0])
        keys: List[int] = []  # nums2 ascending
        vals: List[int] = []  # sums strictly descending
        ans = [-1] * len(queries)
        p = 0
        for q in qs:
            x, y = queries[q]
            while p < n and nums1[pts[p]] >= x:
                i = pts[p]
                a = nums2[i]
                s = nums1[i] + a
                p += 1
                pos = bisect_left(keys, a)
                if pos < len(keys) and vals[pos] >= s:
                    continue  # dominated by an existing point
                end = pos
                if end < len(keys) and keys[end] == a:
                    end += 1  # its sum is < s here, so it is dominated
                start = pos
                while start > 0 and vals[start - 1] <= s:
                    start -= 1
                keys[start:end] = [a]
                vals[start:end] = [s]
            k = bisect_left(keys, y)
            if k < len(keys):
                ans[q] = vals[k]
        return ans
