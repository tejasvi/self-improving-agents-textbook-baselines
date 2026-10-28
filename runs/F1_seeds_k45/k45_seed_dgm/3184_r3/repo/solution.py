from typing import List

class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """
        Find the maximum sum of a balanced subsequence.
        
        A subsequence is balanced if: nums[i_j] - nums[i_j-1] >= i_j - i_j-1
        Which rearranges to: nums[i_j] - i_j >= nums[i_j-1] - i_j-1
        
        Key insight: Define adjusted[i] = nums[i] - i
        Then we need a subsequence where adjusted values are non-decreasing
        and we maximize the sum of original nums values.
        
        Approach:
        - dp[i] = maximum sum of balanced subsequence ending at index i
        - For each i, we query the maximum dp[j] for all j < i where adjusted[j] <= adjusted[i]
        - Use a segment tree with coordinate compression to efficiently query and update
        """
        n = len(nums)
        
        # Calculate adjusted values
        adjusted = [nums[i] - i for i in range(n)]
        
        # Coordinate compression - map adjusted values to indices
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
                """Query maximum value in range [l, r]"""
                if end is None:
                    end = self.size - 1
                
                if l > r or l > end or r < start:
                    return float('-inf')
                
                if l <= start and end <= r:
                    return self.tree[node]
                
                mid = (start + end) // 2
                left_max = self.query(l, r, 2*node+1, start, mid)
                right_max = self.query(l, r, 2*node+2, mid+1, end)
                return max(left_max, right_max)
        
        # Initialize segment tree
        st = SegmentTree(len(sorted_adjusted))
        
        # DP: for each position, calculate max balanced subsequence sum ending here
        result = float('-inf')
        
        for i in range(n):
            coord = coord_map[adjusted[i]]
            
            # Query maximum dp value for all adjusted[j] <= adjusted[i] where j < i
            max_prev = st.query(0, coord)
            
            # Current dp value
            current_sum = max(nums[i], max_prev + nums[i])
            
            # Update segment tree
            st.update(coord, current_sum)
            
            # Update result
            result = max(result, current_sum)
        
        return result
