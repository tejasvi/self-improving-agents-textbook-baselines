from typing import List
import bisect

class SegmentTree:
    def __init__(self, size: int):
        self.N = 1
        while self.N < size:
            self.N <<= 1
        self.data = [-float('inf')] * (2 * self.N)

    def update(self, idx: int, value: int):
        # set position idx to max(current, value)
        i = idx + self.N
        if value > self.data[i]:
            self.data[i] = value
            i >>= 1
            while i:
                self.data[i] = max(self.data[i << 1], self.data[(i << 1) | 1])
                i >>= 1

    def query(self, left: int, right: int) -> int:
        # query max in [left, right) range
        res = -float('inf')
        l = left + self.N
        r = right + self.N
        while l < r:
            if l & 1:
                res = max(res, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                res = max(res, self.data[r])
            l >>= 1
            r >>= 1
        return res


class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        # Pair points with their sum
        points = [(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)]
        # Coordinate compression for nums2 and query y values
        all_y = [p[1] for p in points]
        all_y += [q[1] for q in queries]
        sorted_y = sorted(set(all_y))
        comp = {v: i for i, v in enumerate(sorted_y)}
        m = len(comp)
        seg = SegmentTree(m)
        # Sort points by nums1 descending
        points.sort(key=lambda x: -x[0])
        # Prepare queries with original index
        queries_with_idx = [(queries[i][0], queries[i][1], i) for i in range(len(queries))]
        queries_with_idx.sort(key=lambda x: -x[0])
        ans = [-1] * len(queries)
        pt = 0
        for x, y, idx in queries_with_idx:
            # Insert all points with nums1 >= x
            while pt < n and points[pt][0] >= x:
                _, b, w = points[pt]
                seg.update(comp[b], w)
                pt += 1
            # Query for b >= y
            # find first compressed index with value >= y
            i = bisect.bisect_left(sorted_y, y)
            if i < m:
                best = seg.query(i, m)
                ans[idx] = best if best != -float('inf') else -1
            else:
                ans[idx] = -1
        return ans
