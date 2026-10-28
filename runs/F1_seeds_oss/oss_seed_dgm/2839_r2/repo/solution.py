from typing import List
import bisect

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        # Pair up values
        points = list(zip(nums1, nums2))
        # Coordinate compression for nums2 values
        uniq = sorted(set(nums2))
        m = len(uniq)
        idx_map = {v: i for i, v in enumerate(uniq)}
        # Sort points by nums1 descending
        points_sorted = sorted(points, key=lambda p: -p[0])
        # Prepare queries with original indices and sort by x descending
        qlist = [(x, y, i) for i, (x, y) in enumerate(queries)]
        qlist.sort(key=lambda q: -q[0])
        # Segment tree for range maximum on compressed nums2 index
        size = 1
        while size < m:
            size <<= 1
        seg = [-1] * (2 * size)
        
        def seg_update(pos: int, value: int) -> None:
            i = pos + size
            if seg[i] >= value:
                return
            seg[i] = value
            i //= 2
            while i:
                seg[i] = max(seg[2 * i], seg[2 * i + 1])
                i //= 2
        
        def seg_query(l: int, r: int) -> int:
            # query maximum on inclusive range [l, r]
            l += size
            r += size
            res = -1
            while l <= r:
                if l & 1:
                    res = max(res, seg[l])
                    l += 1
                if not (r & 1):
                    res = max(res, seg[r])
                    r -= 1
                l //= 2
                r //= 2
            return res
        
        ans = [-1] * len(queries)
        pt = 0
        for x, y, idx in qlist:
            # insert all points with nums1 >= x into the segment tree
            while pt < n and points_sorted[pt][0] >= x:
                a, b = points_sorted[pt]
                pos = idx_map[b]
                seg_update(pos, a + b)
                pt += 1
            # find the smallest compressed index where nums2 >= y
            left = bisect.bisect_left(uniq, y)
            if left < m:
                best = seg_query(left, m - 1)
                ans[idx] = best if best != -1 else -1
            else:
                ans[idx] = -1
        return ans
