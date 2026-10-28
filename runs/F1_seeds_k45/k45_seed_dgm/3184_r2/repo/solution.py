from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """
        Find the maximum sum of a balanced subsequence.
        
        A subsequence is balanced if for consecutive elements at indices i_{j-1} and i_j:
        nums[i_j] - nums[i_{j-1}] >= i_j - i_{j-1}
        
        Rearranging: nums[i_j] - i_j >= nums[i_{j-1}] - i_{j-1}
        
        So if we define adjusted[i] = nums[i] - i, we need adjusted values to be non-decreasing
        in the subsequence.
        
        DP approach:
        - dp[i] = maximum sum of balanced subsequence ending at index i
        - For each position i, we can extend from any position j < i where adjusted[j] <= adjusted[i]
        - dp[i] = max(nums[i], max(dp[j] + nums[i]) for all j where adjusted[j] <= adjusted[i])
        
        To efficiently find the maximum dp value among all j with adjusted[j] <= adjusted[i],
        we use a segment tree with coordinate compression.
        """
        n = len(nums)
        
        # Calculate adjusted values: nums[i] - i
        adjusted = [nums[i] - i for i in range(n)]
        
        # Coordinate compression for adjusted values
        sorted_adjusted = sorted(set(adjusted))
        coord_map = {v: i for i, v in enumerate(sorted_adjusted)}
        
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
        
        seg_tree = SegmentTree(len(sorted_adjusted))
        
        result = float('-inf')
        
        for i in range(n):
            coord = coord_map[adjusted[i]]
            
            # Query maximum dp value for all adjusted values <= adjusted[i]
            max_prev_dp = seg_tree.query(0, coord)
            
            # Current dp value: either start fresh with nums[i], or extend previous subsequence
            current_dp = nums[i]
            if max_prev_dp != float('-inf'):
                current_dp = max(current_dp, max_prev_dp + nums[i])
            
            # Update segment tree at this coordinate
            seg_tree.update(coord, current_dp)
            
            # Update result
            result = max(result, current_dp)
        
        return result
