from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        
        # Create adjusted values: adjusted[i] = nums[i] - i
        adjusted = [nums[i] - i for i in range(n)]
        
        # Coordinate compression for adjusted values
        sorted_adjusted = sorted(set(adjusted))
        coord_map = {v: idx for idx, v in enumerate(sorted_adjusted)}
        
        # Segment tree for range maximum query
        class SegmentTree:
            def __init__(self, size):
                self.size = size
                self.tree = [-float('inf')] * (4 * size)
            
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
                    return -float('inf')
                
                if l <= start and end <= r:
                    return self.tree[node]
                
                mid = (start + end) // 2
                left_max = self.query(l, r, 2*node+1, start, mid)
                right_max = self.query(l, r, 2*node+2, mid+1, end)
                return max(left_max, right_max)
        
        seg_tree = SegmentTree(len(sorted_adjusted))
        
        result = -float('inf')
        
        for i in range(n):
            # Get the compressed coordinate for adjusted[i]
            coord = coord_map[adjusted[i]]
            
            # Query the maximum dp value for all previous indices with adjusted value <= adjusted[i]
            max_prev_dp = seg_tree.query(0, coord)
            
            # Calculate dp[i]
            current_dp = max(nums[i], max_prev_dp + nums[i])
            
            # Update segment tree
            seg_tree.update(coord, current_dp)
            
            # Update result
            result = max(result, current_dp)
        
        return result
