from typing import List


class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        """
        Find the maximum sum of a balanced subsequence.
        
        Key insight: A subsequence is balanced if:
        nums[i_j] - nums[i_j-1] >= i_j - i_j-1
        
        Rearranging: nums[i_j] - i_j >= nums[i_j-1] - i_j-1
        
        If we define arr[i] = nums[i] - i, then we need:
        arr[i_j] >= arr[i_j-1]
        
        DP approach: For each position, find the maximum sum of a balanced
        subsequence ending at that position by looking at all previous
        positions with arr value >= current arr value.
        """
        n = len(nums)
        
        # Transform: arr[i] = nums[i] - i
        arr = [nums[i] - i for i in range(n)]
        
        # Coordinate compression for arr values
        sorted_arr = sorted(set(arr))
        arr_to_idx = {v: i for i, v in enumerate(sorted_arr)}
        
        # Segment tree to query max dp value in range of arr values
        class SegmentTree:
            def __init__(self, size):
                self.size = size
                self.tree = [float('-inf')] * (4 * size)
            
            def update(self, v, tl, tr, pos, val):
                """Update position pos with value val (take max)"""
                if tl == tr:
                    self.tree[v] = max(self.tree[v], val)
                else:
                    tm = (tl + tr) // 2
                    if pos <= tm:
                        self.update(2*v, tl, tm, pos, val)
                    else:
                        self.update(2*v+1, tm+1, tr, pos, val)
                    self.tree[v] = max(self.tree[2*v], self.tree[2*v+1])
            
            def query(self, v, tl, tr, l, r):
                """Query max value in range [l, r]"""
                if l > r:
                    return float('-inf')
                if l == tl and r == tr:
                    return self.tree[v]
                tm = (tl + tr) // 2
                return max(self.query(2*v, tl, tm, l, min(r, tm)),
                          self.query(2*v+1, tm+1, tr, max(l, tm+1), r))
        
        st = SegmentTree(len(sorted_arr))
        
        max_sum = float('-inf')
        
        for i in range(n):
            # Get coordinate of current arr[i]
            curr_arr_idx = arr_to_idx[arr[i]]
            
            # Query max dp value for all previous positions with arr >= arr[i]
            # This is range [curr_arr_idx, len(sorted_arr)-1] in compressed coords
            prev_max = st.query(1, 0, len(sorted_arr)-1, curr_arr_idx, len(sorted_arr)-1)
            
            # dp[i] = max sum ending at i
            if prev_max == float('-inf'):
                # No previous element satisfies the condition
                dp_i = nums[i]
            else:
                dp_i = max(nums[i], prev_max + nums[i])
            
            max_sum = max(max_sum, dp_i)
            
            # Update segment tree with dp[i] at position curr_arr_idx
            st.update(1, 0, len(sorted_arr)-1, curr_arr_idx, dp_i)
        
        return max_sum
