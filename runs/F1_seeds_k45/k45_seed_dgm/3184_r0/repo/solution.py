from typing import List

class SegmentTree:
    """Segment tree for range maximum query and point update"""
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
            self.update(idx, val, 2 * node + 1, start, mid)
        else:
            self.update(idx, val, 2 * node + 2, mid + 1, end)
        
        self.tree[node] = max(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def query(self, l, r, node=0, start=0, end=None):
        """Query max value in range [l, r]"""
        if end is None:
            end = self.size - 1
        
        if r < start or end < l or l > r:
            return -float('inf')
        
        if l <= start and end <= r:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_max = self.query(l, r, 2 * node + 1, start, mid)
        right_max = self.query(l, r, 2 * node + 2, mid + 1, end)
        
        return max(left_max, right_max)


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        n = len(nums)
        
        # adjusted[i] = nums[i] - i
        adjusted = [nums[i] - i for i in range(n)]
        
        # Coordinate compression for adjusted values
        sorted_adjusted = sorted(set(adjusted))
        coord_map = {v: i for i, v in enumerate(sorted_adjusted)}
        
        # Segment tree indexed by compressed coordinates
        seg_tree = SegmentTree(len(sorted_adjusted))
        
        max_sum = -float('inf')
        
        for i in range(n):
            # Get compressed coordinate for adjusted[i]
            coord = coord_map[adjusted[i]]
            
            # Query max dp value for all adjusted values <= adjusted[i]
            # This means coordinates 0 to coord
            max_prev = seg_tree.query(0, coord)
            
            # Calculate dp[i]
            if max_prev == -float('inf'):
                # No previous elements, start new subsequence
                dp_i = nums[i]
            else:
                # Extend previous subsequence
                dp_i = max_prev + nums[i]
            
            # Update segment tree with dp[i] at coordinate coord
            seg_tree.update(coord, dp_i)
            
            # Track maximum sum
            max_sum = max(max_sum, dp_i)
        
        return max_sum
