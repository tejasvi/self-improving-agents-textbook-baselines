from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        """
        Find the maximum value of a subsequence of size 2*k.
        
        The value is defined as:
        (OR of first k elements) XOR (OR of last k elements)
        
        Approach:
        1. Use DP to find all possible OR values when selecting exactly j elements 
           from the first i elements
        2. For left half, compute all possible OR values selecting k elements
        3. For right half, compute all possible OR values selecting k elements
        4. Find the maximum XOR between left and right OR values
        """
        n = len(nums)
        
        # dp_left[j] = set of all possible OR values when selecting exactly j elements 
        # from the left part
        dp_left = [set() for _ in range(k + 1)]
        dp_left[0].add(0)  # Base case: selecting 0 elements gives OR value 0
        
        # Build all possible OR values for left half by considering each element
        for num in nums:
            # Traverse backwards to avoid using the same element twice
            new_dp_left = [s.copy() for s in dp_left]
            for j in range(k):
                for or_val in dp_left[j]:
                    new_dp_left[j + 1].add(or_val | num)
            dp_left = new_dp_left
        
        # Get all possible OR values when selecting exactly k elements
        left_or_values = dp_left[k]
        
        # Now do the same for the right half
        dp_right = [set() for _ in range(k + 1)]
        dp_right[0].add(0)
        
        for num in nums:
            new_dp_right = [s.copy() for s in dp_right]
            for j in range(k):
                for or_val in dp_right[j]:
                    new_dp_right[j + 1].add(or_val | num)
            dp_right = new_dp_right
        
        # Get all possible OR values when selecting exactly k elements
        right_or_values = dp_right[k]
        
        # Find maximum XOR value
        max_xor = 0
        for left_or in left_or_values:
            for right_or in right_or_values:
                max_xor = max(max_xor, left_or ^ right_or)
        
        return max_xor
