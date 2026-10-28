from typing import List
import bisect


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        points = sorted(range(n), key=lambda j: -nums1[j])
        order = sorted(range(len(queries)), key=lambda i: -queries[i][0])
        answer = [-1] * len(queries)

        # Staircase of non-dominated points: keys (nums2) strictly increasing,
        # sums strictly decreasing. negs holds -sums (strictly increasing).
        keys: List[int] = []
        negs: List[int] = []
        p = 0
        for qi in order:
            x, y = queries[qi]
            while p < n and nums1[points[p]] >= x:
                j = points[p]
                b, s = nums2[j], nums1[j] + nums2[j]
                p += 1
                lo = bisect.bisect_left(keys, b)
                # Dominated by an existing point with key >= b and sum >= s.
                if lo < len(keys) and -negs[lo] >= s:
                    continue
                # Entries with key <= b and sum <= s are dominated by the new point.
                t = bisect.bisect_left(negs, -s)
                e = bisect.bisect_right(keys, b)
                keys[t:e] = [b]
                negs[t:e] = [-s]
            i = bisect.bisect_left(keys, y)
            if i < len(keys):
                answer[qi] = -negs[i]
        return answer
