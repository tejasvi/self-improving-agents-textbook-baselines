from bisect import bisect_left
from typing import List


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        points = sorted(range(n), key=lambda j: -nums1[j])
        order = sorted(range(len(queries)), key=lambda q: -queries[q][0])
        answer = [-1] * len(queries)

        # Staircase: keys (nums2) strictly increasing, vals (sums) strictly decreasing.
        keys: List[int] = []
        vals: List[int] = []

        p = 0
        for q in order:
            x, y = queries[q]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                a = nums2[j]
                s = nums1[j] + a
                p += 1
                i = bisect_left(keys, a)
                # Dominated: some point with key >= a has sum >= s.
                if i < len(keys) and vals[i] >= s:
                    continue
                end = i + 1 if i < len(keys) and keys[i] == a else i
                k = i
                # Points with key < a and sum <= s are dominated by the new point.
                while k > 0 and vals[k - 1] <= s:
                    k -= 1
                keys[k:end] = [a]
                vals[k:end] = [s]
            idx = bisect_left(keys, y)
            if idx < len(keys):
                answer[q] = vals[idx]
        return answer
