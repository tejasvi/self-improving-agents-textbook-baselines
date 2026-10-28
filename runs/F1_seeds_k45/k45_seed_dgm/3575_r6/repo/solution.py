from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of any subsequence of nums with size 2*k.
        Value = (OR of first k elements) XOR (OR of last k elements)
        """
        n = len(nums)
        
        # Strategy: Use DP with split point
        # For each position i, we compute:
        # - all possible OR values by choosing exactly k elements from nums[0:i]
        # - all possible OR values by choosing exactly k elements from nums[i:n]
        # Then we try all combinations
        
        max_value = 0
        
        # dp_left[i][j] = set of possible OR values by selecting j elements from nums[0:i]
        # dp_right[i][j] = set of possible OR values by selecting j elements from nums[i:n]
        
        for split_idx in range(k, n - k + 1):
            # Left part: choose k elements from nums[0:split_idx]
            dp_left = [[set() for _ in range(k + 1)] for _ in range(split_idx + 1)]
            
            # Base case
            for i in range(split_idx + 1):
                dp_left[i][0].add(0)
            
            # Fill left DP
            for i in range(1, split_idx + 1):
                for j in range(k + 1):
                    # Don't take nums[i-1]
                    dp_left[i][j] = dp_left[i][j].union(dp_left[i-1][j])
                    # Take nums[i-1]
                    if j > 0:
                        for or_val in dp_left[i-1][j-1]:
                            dp_left[i][j].add(or_val | nums[i-1])
            
            # Right part: choose k elements from nums[split_idx:n]
            remaining = n - split_idx
            dp_right = [[set() for _ in range(k + 1)] for _ in range(remaining + 1)]
            
            # Base case
            for i in range(remaining + 1):
                dp_right[i][0].add(0)
            
            # Fill right DP
            for i in range(1, remaining + 1):
                for j in range(k + 1):
                    # Don't take nums[split_idx + i - 1]
                    dp_right[i][j] = dp_right[i][j].union(dp_right[i-1][j])
                    # Take nums[split_idx + i - 1]
                    if j > 0:
                        for or_val in dp_right[i-1][j-1]:
                            dp_right[i][j].add(or_val | nums[split_idx + i - 1])
            
            # Find maximum XOR
            left_ors = dp_left[split_idx][k]
            right_ors = dp_right[remaining][k]
            
            for left_or in left_ors:
                for right_or in right_ors:
                    max_value = max(max_value, left_or ^ right_or)
        
        return max_value
