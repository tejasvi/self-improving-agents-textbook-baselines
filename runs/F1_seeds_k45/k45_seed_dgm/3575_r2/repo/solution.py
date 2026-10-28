from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of a subsequence of size 2*k.
        The value is: (OR of first k elements) XOR (OR of last k elements)
        """
        n = len(nums)
        
        # dp_left[i][j] = set of all possible OR values when selecting j elements from nums[0:i]
        dp_left = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        dp_left[0][0].add(0)
        
        for i in range(1, n + 1):
            # Copy previous state (not taking nums[i-1])
            for j in range(k + 1):
                dp_left[i][j] = dp_left[i][j].union(dp_left[i-1][j])
            
            # Take nums[i-1]
            for j in range(1, k + 1):
                for val in dp_left[i-1][j-1]:
                    dp_left[i][j].add(val | nums[i-1])
        
        # dp_right[i][j] = set of all possible OR values when selecting j elements from nums[i:n]
        dp_right = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        dp_right[n][0].add(0)
        
        for i in range(n - 1, -1, -1):
            # Copy previous state (not taking nums[i])
            for j in range(k + 1):
                dp_right[i][j] = dp_right[i][j].union(dp_right[i+1][j])
            
            # Take nums[i]
            for j in range(1, k + 1):
                for val in dp_right[i+1][j-1]:
                    dp_right[i][j].add(val | nums[i])
        
        max_value = 0
        
        # Try all split points
        for i in range(k, n - k + 1):
            # dp_left[i][k] contains all OR values for selecting k elements from nums[0:i]
            # dp_right[i][k] contains all OR values for selecting k elements from nums[i:n]
            left_ors = dp_left[i][k]
            right_ors = dp_right[i][k]
            
            for left_or in left_ors:
                for right_or in right_ors:
                    max_value = max(max_value, left_or ^ right_or)
        
        return max_value
