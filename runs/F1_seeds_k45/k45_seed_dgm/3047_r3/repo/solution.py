from typing import List
from collections import defaultdict

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """
        Find the maximum element-sum of a complete subset of indices.
        
        A set of INDICES is complete if the product of every pair of indices
        is a perfect square. (Equivalently, all indices have the same square-free part)
        
        For indices to form a complete subset, they must all share the same square-free part.
        If all indices in a subset have square-free part s, then any product of indices
        in that subset will have square-free part s (and count will be even), making it
        a perfect square.
        
        Algorithm:
        1. For each index i (1-indexed), extract its square-free part
        2. Group indices by their square-free part
        3. For each group, sum the corresponding values in nums
        4. Return the maximum sum among all groups
        """
        
        def get_square_free_part(n):
            """
            Extract the square-free part of a number.
            Returns the product of all prime factors with odd exponent.
            """
            square_free = 1
            d = 2
            while d * d <= n:
                count = 0
                while n % d == 0:
                    n //= d
                    count += 1
                # If count is odd, d contributes to square-free part
                if count % 2 == 1:
                    square_free *= d
                d += 1
            # If n > 1, then it's a prime factor with exponent 1
            if n > 1:
                square_free *= n
            return square_free
        
        # Group by square-free part of indices
        # Indices are 1-indexed from 1 to n
        groups = defaultdict(int)  # square_free_part -> sum of corresponding nums values
        
        n = len(nums)
        for i in range(n):
            idx = i + 1  # Convert to 1-indexed
            square_free = get_square_free_part(idx)
            groups[square_free] += nums[i]
        
        # Return the maximum sum across all groups
        return max(groups.values())
