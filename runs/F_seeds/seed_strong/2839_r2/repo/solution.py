from typing import *
import bisect


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        pts = sorted(range(n), key=lambda j: -nums1[j])
        qs = sorted(range(len(queries)), key=lambda i: -queries[i][0])
        keys: List[int] = []  # nums2 values, ascending
        sums: List[int] = []  # sums, strictly decreasing
        ans = [-1] * len(queries)
        p = 0
        for qi in qs:
            x, y = queries[qi]
            while p < n and nums1[pts[p]] >= x:
                j = pts[p]
                p += 1
                a = nums2[j]
                s = nums1[j] + a
                idx = bisect.bisect_left(keys, a)
                if idx < len(keys) and sums[idx] >= s:
                    continue  # dominated
                # remove points with nums2 >= a and sum <= s (contiguous from idx)
                end = idx
                if end < len(keys) and keys[end] == a:
                    end += 1  # same key, smaller sum: dominated
                start = idx
                while start > 0 and sums[start - 1] <= s:
                    start -= 1  # smaller key, not larger sum: dominated
                keys[start:end] = [a]
                sums[start:end] = [s]
            k = bisect.bisect_left(keys, y)
            if k < len(keys):
                ans[qi] = sums[k]
        return ans
