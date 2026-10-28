from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """
        Find the maximum sum of a balanced subsequence.
        
        A subsequence is balanced if:
        nums[i_j] - nums[i_j-1] >= i_j - i_j-1
        
        Which rearranges to:
        nums[i_j] - i_j >= nums[i_j-1] - i_j-1
        
        So if we define b[i] = nums[i] - i, we need b values to be non-decreasing.
        """
        n = len(nums)
        
        # Transform: b[i] = nums[i] - i
        # We need to find max sum subsequence where b[i] is non-decreasing
        
        # dp[i] = max sum of balanced subsequence ending at index i
        # For each i, we can extend from any j < i where b[j] <= b[i]
        
        # We'll use a segment tree to efficiently query the max dp value
        # for all j where b[j] <= b[i]
        
        # Coordinate compression for b values
        b_values = [nums[i] - i for i in range(n)]
        sorted_b = sorted(set(b_values))
        b_to_idx = {v: i for i, v in enumerate(sorted_b)}
        compressed_b = [b_to_idx[b_values[i]] for i in range(n)]
        
        # Segment tree for range maximum query
        class SegmentTree:
            def __init__(self, size):
                self.size = size
                self.tree = [float('-inf')] * (4 * size)
            
            def update(self, idx, val, node=0, start=0, end=None):
                if end is None:
                    end = self.size - 1
                
                if start == end:
                    self.tree[node] = max(self.tree[node], val)
                    return
                
                mid = (start + end) // 2
                if idx <= mid:
                    self.update(idx, val, 2*node+1, start, mid)
                else:
                    self.update(idx, val, 2*node+2, mid+1, end)
                
                self.tree[node] = max(self.tree[2*node+1], self.tree[2*node+2])
            
            def query(self, l, r, node=0, start=0, end=None):
                if end is None:
                    end = self.size - 1
                
                if r < start or l > end:
                    return float('-inf')
                
                if l <= start and end <= r:
                    return self.tree[node]
                
                mid = (start + end) // 2
                left_max = self.query(l, r, 2*node+1, start, mid)
                right_max = self.query(l, r, 2*node+2, mid+1, end)
                
                return max(left_max, right_max)
        
        seg_tree = SegmentTree(len(sorted_b))
        result = float('-inf')
        
        for i in range(n):
            # Query for max dp value where b[j] <= b[i]
            compressed_idx = compressed_b[i]
            max_prev_dp = seg_tree.query(0, compressed_idx)
            
            # Current dp value
            current_dp = nums[i]
            if max_prev_dp != float('-inf'):
                current_dp = max(current_dp, max_prev_dp + nums[i])
            
            result = max(result, current_dp)
            
            # Update segment tree
            seg_tree.update(compressed_idx, current_dp)
        
        return result
