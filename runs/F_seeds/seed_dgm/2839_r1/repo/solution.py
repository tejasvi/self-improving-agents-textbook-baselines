from typing import List
from bisect import bisect_left


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        pts = sorted(range(n), key=lambda i: -nums1[i])
        qs = sorted(range(len(queries)), key=lambda q: -queries[q][0])
        ans = [-1] * len(queries)

        # Pareto frontier of inserted points: bs strictly ascending,
        # ss strictly descending (ss[k] is the best sum among points with nums2 >= bs[k]).
        bs: List[int] = []
        ss: List[int] = []
        p = 0
        for q in qs:
            x, y = queries[q]
            # Activate all points with nums1 >= x (offline, sorted by nums1 descending).
            while p < n and nums1[pts[p]] >= x:
                i = pts[p]
                p += 1
                b = nums2[i]
                s = nums1[i] + b
                pos = bisect_left(bs, b)  # first index with bs >= b
                # Dominated by an existing point with nums2 >= b and sum >= s?
                if pos < len(bs) and ss[pos] >= s:
                    continue
                # Points with nums2 <= b and sum <= s are dominated; they form a
                # contiguous block ending at pos-1 (ss is descending).
                lo = pos
                while lo > 0 and ss[lo - 1] <= s:
                    lo -= 1
                end = pos
                if pos < len(bs) and bs[pos] == b:
                    end = pos + 1  # same nums2 with smaller sum -> dominated
                bs[lo:end] = [b]
                ss[lo:end] = [s]
            # Query: first point with nums2 >= y has the largest sum among them.
            pos = bisect_left(bs, y)
            if pos < len(bs):
                ans[q] = ss[pos]
        return ans
