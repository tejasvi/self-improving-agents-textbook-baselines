from typing import List
from collections import defaultdict

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """
        Find the maximum element-sum of a complete subset of indices.
        
        A set of indices is complete if the product of every pair of indices
        is a perfect square. This is equivalent to grouping indices by their
        square-free representation.
        """
        
        def get_square_free(n):
            """Get the square-free part of a number."""
            square_free = 1
            original_n = n
            
            # Check all prime factors
            i = 2
            while i * i <= original_n:
                count = 0
                while n % i == 0:
                    n //= i
                    count += 1
                # If count is odd, include this prime in square-free part
                if count % 2 == 1:
                    square_free *= i
                i += 1
            
            # If n > 1 at this point, it's a prime factor with count 1
            if n > 1:
                square_free *= n
            
            return square_free
        
        # Group indices by their square-free representation
        # groups[square_free] = list of values
        groups = defaultdict(list)
        
        for i in range(len(nums)):
            index = i + 1  # 1-indexed
            square_free = get_square_free(index)
            groups[square_free].append(nums[i])
        
        # For each group, find the maximum sum
        max_sum = 0
        for square_free_key, values in groups.items():
            # Sum all values in this group (they can all be together)
            group_sum = sum(values)
            max_sum = max(max_sum, group_sum)
        
        return max_sum
