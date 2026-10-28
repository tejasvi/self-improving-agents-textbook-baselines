from typing import List
from collections import defaultdict

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        """
        Find maximum sum queries on two arrays.
        For each query (x, y), find max(nums1[j] + nums2[j]) where nums1[j] >= x and nums2[j] >= y.
        """
        n = len(nums1)
        m = len(queries)
        
        # Create pairs of (nums1[i], nums2[i], sum)
        pairs = [(nums1[i], nums2[i], nums1[i] + nums2[i]) for i in range(n)]
        
        # Sort pairs by nums1 in descending order
        pairs.sort(reverse=True)
        
        # Create indexed queries to track original positions
        indexed_queries = [(queries[i][0], queries[i][1], i) for i in range(m)]
        
        # Sort queries by x (first element) in descending order
        indexed_queries.sort(reverse=True)
        
        # Result array
        result = [0] * m
        
        # Use a simple approach with coordinate compression and segment tree
        class SegmentTree:
            def __init__(self):
                self.nodes = {}
            
            def update(self, y, sum_val):
                """Update: for y-coordinate, store the maximum sum"""
                self._update(1, 0, 10**9, y, sum_val)
            
            def query(self, y_min):
                """Query: find maximum sum for all y >= y_min"""
                result = self._query(1, 0, 10**9, y_min, 10**9)
                return result if result != -1 else -1
            
            def _update(self, node, start, end, y, val):
                if node not in self.nodes:
                    self.nodes[node] = -1
                
                if start == end:
                    self.nodes[node] = max(self.nodes[node], val)
                    return
                
                mid = (start + end) // 2
                if y <= mid:
                    self._update(2 * node, start, mid, y, val)
                else:
                    self._update(2 * node + 1, mid + 1, end, y, val)
                
                left_val = self.nodes.get(2 * node, -1)
                right_val = self.nodes.get(2 * node + 1, -1)
                self.nodes[node] = max(left_val, right_val)
            
            def _query(self, node, start, end, l, r):
                if node not in self.nodes or start > r or end < l:
                    return -1
                
                if l <= start and end <= r:
                    return self.nodes[node]
                
                mid = (start + end) // 2
                left_res = self._query(2 * node, start, mid, l, r)
                right_res = self._query(2 * node + 1, mid + 1, end, l, r)
                return max(left_res, right_res)
        
        seg_tree = SegmentTree()
        pair_idx = 0
        
        # Process queries in descending order of x
        for x, y, original_idx in indexed_queries:
            # Add all pairs with nums1 >= x to the segment tree
            while pair_idx < n and pairs[pair_idx][0] >= x:
                _, y_val, sum_val = pairs[pair_idx]
                seg_tree.update(y_val, sum_val)
                pair_idx += 1
            
            # Query the maximum sum for nums2[j] >= y
            result[original_idx] = seg_tree.query(y)
        
        return result
