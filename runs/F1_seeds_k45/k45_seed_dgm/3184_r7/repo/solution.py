from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """
        Find the maximum sum of a balanced subsequence.
        
        A subsequence is balanced if: nums[i_j] - nums[i_j-1] >= i_j - i_j-1
        This can be rearranged as: nums[i_j] - i_j >= nums[i_j-1] - i_j-1
        
        Let transformed[i] = nums[i] - i. Then we need transformed values to be non-decreasing
        in the subsequence, and we want to maximize the sum of nums values.
        
        Approach:
        - Use DP where dp[i] = max sum of balanced subsequence ending at i
        - For each i, we can extend from any j where transformed[j] <= transformed[i]
        - Use a segment tree with coordinate compression to efficiently query max dp[j]
        """
        n = len(nums)
        
        # Create transformed array and prepare for coordinate compression
        transformed = [nums[i] - i for i in range(n)]
        
        # Coordinate compression
        sorted_transformed = sorted(set(transformed))
        coord_map = {v: i for i, v in enumerate(sorted_transformed)}
        
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
                else:
                    mid = (start + end) // 2
                    if idx <= mid:
                        self.update(idx, val, 2*node+1, start, mid)
                    else:
                        self.update(idx, val, 2*node+2, mid+1, end)
                    self.tree[node] = max(self.tree[2*node+1], self.tree[2*node+2])
            
            def query(self, left, right, node=0, start=0, end=None):
                if end is None:
                    end = self.size - 1
                
                if left > right or left > end or right < start:
                    return float('-inf')
                
                if left <= start and end <= right:
                    return self.tree[node]
                
                mid = (start + end) // 2
                left_max = self.query(left, right, 2*node+1, start, mid)
                right_max = self.query(left, right, 2*node+2, mid+1, end)
                return max(left_max, right_max)
        
        seg_tree = SegmentTree(len(sorted_transformed))
        
        result = float('-inf')
        
        for i in range(n):
            # Get coordinate of transformed[i]
            coord = coord_map[transformed[i]]
            
            # Query maximum dp value for all j where transformed[j] <= transformed[i]
            max_prev = seg_tree.query(0, coord)
            
            # Current dp value
            current_dp = nums[i]
            if max_prev != float('-inf'):
                current_dp = max(current_dp, max_prev + nums[i])
            
            # Update segment tree
            seg_tree.update(coord, current_dp)
            
            # Update result
            result = max(result, current_dp)
        
        return result
