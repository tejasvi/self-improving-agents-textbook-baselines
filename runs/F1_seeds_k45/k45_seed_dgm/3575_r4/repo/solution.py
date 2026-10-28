from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of a subsequence of size 2*k.
        
        The value is defined as:
        (OR of first k elements) XOR (OR of last k elements)
        
        Approach:
        1. Use DP to compute all possible OR values when selecting exactly i elements
           from the first j elements.
        2. Do the same for all possible OR values when selecting exactly i elements
           from the last j elements.
        3. Try all combinations and find the maximum XOR value.
        """
        n = len(nums)
        
        # dp_left[i][j] = set of all possible OR values when selecting exactly i elements
        # from the first j elements of nums
        dp_left = [[set() for _ in range(n + 1)] for _ in range(k + 1)]
        dp_left[0][0].add(0)
        
        for j in range(1, n + 1):
            for i in range(k + 1):
                # Don't take nums[j-1]
                dp_left[i][j] = dp_left[i][j].union(dp_left[i][j - 1])
                
                # Take nums[j-1]
                if i > 0:
                    for or_val in dp_left[i - 1][j - 1]:
                        dp_left[i][j].add(or_val | nums[j - 1])
        
        # Get all possible OR values when selecting exactly k elements from any prefix
        left_or_values = dp_left[k][n]
        
        # dp_right[i][j] = set of all possible OR values when selecting exactly i elements
        # from the last j elements of nums (processing from right to left)
        dp_right = [[set() for _ in range(n + 1)] for _ in range(k + 1)]
        dp_right[0][0].add(0)
        
        for j in range(1, n + 1):
            for i in range(k + 1):
                # Don't take nums[n-j]
                dp_right[i][j] = dp_right[i][j].union(dp_right[i][j - 1])
                
                # Take nums[n-j]
                if i > 0:
                    for or_val in dp_right[i - 1][j - 1]:
                        dp_right[i][j].add(or_val | nums[n - j])
        
        # Get all possible OR values when selecting exactly k elements from any suffix
        right_or_values = dp_right[k][n]
        
        # Find maximum XOR value
        max_xor = 0
        for left_or in left_or_values:
            for right_or in right_or_values:
                max_xor = max(max_xor, left_or ^ right_or)
        
        return max_xor
