from typing import List

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        # Offline solution using a segment tree (range maximum) and sorting.
        # For each query (x, y) we need max(nums1[i] + nums2[i]) where nums1[i] >= x and nums2[i] >= y.
        # Sort the points by nums1 descending and process queries in the same order.
        # Maintain a segment tree keyed by nums2 (compressed) storing the maximum sum for each nums2 value.
        # Query the segment tree for the maximum over all nums2 >= y.
        
        n = len(nums1)
        # Pair each index with its values and pre‑compute the sum.
        points = [(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)]
        points.sort(key=lambda x: -x[0])  # descending by nums1
        
        # Prepare queries with original indices.
        q_with_idx = [(queries[i][0], queries[i][1], i) for i in range(len(queries))]
        q_with_idx.sort(key=lambda x: -x[0])  # descending by x
        
        # Coordinate compression for nums2 values.
        all_vals = list(set(nums2 + [q[1] for q in queries]))
        all_vals.sort()  # ascending
        idx_of = {v: i for i, v in enumerate(all_vals)}
        m = len(all_vals)
        
        # Segment tree for range maximum.
        size = 1
        while size < m:
            size <<= 1
        seg = [-1] * (2 * size)
        
        def seg_update(pos: int, value: int) -> None:
            # set position to max(existing, value)
            i = pos + size
            if value > seg[i]:
                seg[i] = value
                i >>= 1
                while i:
                    seg[i] = max(seg[i << 1], seg[(i << 1) | 1])
                    i >>= 1
        
        def seg_query(l: int, r: int) -> int:
            # inclusive range query max on [l, r]
            l += size
            r += size
            res = -1
            while l <= r:
                if l & 1:
                    if seg[l] > res:
                        res = seg[l]
                    l += 1
                if not (r & 1):
                    if seg[r] > res:
                        res = seg[r]
                    r -= 1
                l >>= 1
                r >>= 1
            return res
        
        ans = [-1] * len(queries)
        p = 0  # pointer in points
        for x, y, qi in q_with_idx:
            # Insert all points with nums1 >= x
            while p < n and points[p][0] >= x:
                _, b, s = points[p]
                pos = idx_of[b]
                seg_update(pos, s)
                p += 1
            # Query for nums2 >= y => indices of values >= y in ascending order correspond to suffix [pos, m-1]
            # Find first position where value >= y using bisect_left.
            import bisect
            pos = bisect.bisect_left(all_vals, y)
            if pos < m:
                ans[qi] = seg_query(pos, m - 1)
            else:
                ans[qi] = -1
        return ans
