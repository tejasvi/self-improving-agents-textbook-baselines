from typing import *
from bisect import bisect_left, bisect_right


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        points = sorted(range(n), key=lambda i: -nums1[i])
        order = sorted(range(len(queries)), key=lambda q: -queries[q][0])
        ans = [-1] * len(queries)
        # keys: nums2 ascending; vals: sums strictly descending; negv = -vals ascending
        keys: List[int] = []
        negv: List[int] = []
        p = 0
        for qi in order:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                i = points[p]
                b = nums2[i]
                s = nums1[i] + b
                p += 1
                idx = bisect_left(keys, b)
                # max sum among keys >= b is at idx (sums decrease with key)
                if idx < len(keys) and -negv[idx] >= s:
                    continue
                r = bisect_right(keys, b)
                j = bisect_left(negv, -s)  # first index with val <= s
                if j < r:
                    del keys[j:r]
                    del negv[j:r]
                keys.insert(j, b)
                negv.insert(j, -s)
            # first key >= y gives the best sum
            k = bisect_left(keys, y)
            if k < len(keys):
                ans[qi] = -negv[k]
        return ans
