from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """
        Find the maximum sum of a balanced subsequence.
        
        Key insight: The constraint nums[i_j] - nums[i_j-1] >= i_j - i_j-1
        can be rearranged as: nums[i_j] - i_j >= nums[i_j-1] - i_j-1
        
        If we define adjusted[i] = nums[i] - i, then we need the adjusted values
        to be non-decreasing in the subsequence.
        
        This becomes a problem: find the maximum sum subsequence where adjusted
        values are non-decreasing.
        
        We use a segment tree to efficiently track the maximum sum for each
        adjusted value prefix.
        """
        n = len(nums)
        
        # Calculate adjusted values
        adjusted = [nums[i] - i for i in range(n)]
        
        # We need coordinate compression for the segment tree
        # Collect all adjusted values and sort them
        sorted_adjusted = sorted(set(adjusted))
        
        # Create a mapping from adjusted value to compressed coordinate
        coord_map = {v: i for i, v in enumerate(sorted_adjusted)}
        
        # Segment tree to store maximum sum for each adjusted value
        segment_tree = SegmentTree(len(sorted_adjusted))
        
        max_sum = float('-inf')
        
        for i in range(n):
            adj_val = adjusted[i]
            comp_idx = coord_map[adj_val]
            
            # Query the maximum sum for all values <= current adjusted value
            # This gives us the best previous element we can connect to
            prev_max = segment_tree.query(0, comp_idx)
            
            # Current best sum if we include nums[i]
            current_sum = nums[i]
            if prev_max is not None and prev_max > float('-inf'):
                current_sum = max(current_sum, prev_max + nums[i])
            
            # Update the segment tree with the new maximum sum for this adjusted value
            segment_tree.update(comp_idx, current_sum)
            
            max_sum = max(max_sum, current_sum)
        
        return max_sum


class SegmentTree:
    """
    A segment tree that supports:
    - Range maximum query
    - Point update
    """
    
    def __init__(self, n):
        self.n = n
        self.tree = [float('-inf')] * (4 * n)
    
    def update(self, idx, val):
        """Update position idx with value val (or keep maximum if val is larger)"""
        self._update(0, 0, self.n - 1, idx, val)
    
    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = max(self.tree[node], val)
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2 * node + 1, start, mid, idx, val)
            else:
                self._update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = max(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def query(self, l, r):
        """Query maximum value in range [l, r]"""
        if l > r or l < 0 or r >= self.n:
            return float('-inf')
        result = self._query(0, 0, self.n - 1, l, r)
        return result if result != float('-inf') else None
    
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return float('-inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_max = self._query(2 * node + 1, start, mid, l, r)
        right_max = self._query(2 * node + 2, mid + 1, end, l, r)
        return max(left_max, right_max)
