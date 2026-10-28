from typing import *
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        points = sorted(range(n), key=lambda j: -nums1[j])
        order = sorted(range(len(queries)), key=lambda i: -queries[i][0])
        keys: List[int] = []  # nums2 values, ascending
        vals: List[int] = []  # sums, strictly descending
        ans = [-1] * len(queries)
        p = 0
        for qi in order:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                p += 1
                k2 = nums2[j]
                s = nums1[j] + k2
                i = bisect_left(keys, k2)
                # dominated: an existing point with nums2 >= k2 and sum >= s
                if i < len(keys) and vals[i] >= s:
                    continue
                # remove points with nums2 <= k2 and sum <= s (contiguous before i)
                end = i
                if end < len(keys) and keys[end] == k2:
                    end += 1  # same nums2 with smaller sum: dominated
                lo = i
                while lo > 0 and vals[lo - 1] <= s:
                    lo -= 1
                keys[lo:end] = [k2]
                vals[lo:end] = [s]
            i = bisect_left(keys, y)
            if i < len(keys):
                ans[qi] = vals[i]
        return ans
