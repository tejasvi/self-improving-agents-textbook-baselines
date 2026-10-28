from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        points = sorted(range(n), key=lambda j: -nums1[j])
        order = sorted(range(len(queries)), key=lambda i: -queries[i][0])
        answer = [-1] * len(queries)

        # Monotonic stack: keys (nums2) strictly ascending, sums strictly descending.
        # Max sum among points with key >= y is sums[bisect_left(keys, y)].
        keys: List[int] = []
        sums: List[int] = []
        p = 0
        for qi in order:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                a, s = nums2[j], nums1[j] + nums2[j]
                p += 1
                idx = bisect_left(keys, a)
                # Dominated if a point with key >= a has sum >= s.
                if idx < len(keys) and sums[idx] >= s:
                    continue
                # Evict points just before idx whose sum <= s (they are dominated).
                start = idx
                while start > 0 and sums[start - 1] <= s:
                    start -= 1
                keys[start:idx] = [a]
                sums[start:idx] = [s]
            idx = bisect_left(keys, y)
            if idx < len(keys):
                answer[qi] = sums[idx]
        return answer
