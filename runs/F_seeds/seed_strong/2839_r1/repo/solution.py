from typing import *
from bisect import bisect_left, bisect_right


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        points = sorted(range(n), key=lambda i: -nums1[i])
        q = len(queries)
        order = sorted(range(q), key=lambda i: -queries[i][0])
        ans = [-1] * q

        # Monotonic stack: keys ascending (nums2), vals strictly descending (sums).
        keys: List[int] = []
        vals: List[int] = []
        p = 0
        for qi in order:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                idx = points[p]
                yy = nums2[idx]
                s = nums1[idx] + yy
                p += 1
                i = bisect_left(keys, yy)
                if i < len(keys) and vals[i] >= s:
                    continue  # dominated by an entry with key >= yy and sum >= s
                r = bisect_right(keys, yy)
                j = r
                while j > 0 and vals[j - 1] <= s:
                    j -= 1
                keys[j:r] = [yy]
                vals[j:r] = [s]
            i = bisect_left(keys, y)
            if i < len(keys):
                ans[qi] = vals[i]
        return ans
