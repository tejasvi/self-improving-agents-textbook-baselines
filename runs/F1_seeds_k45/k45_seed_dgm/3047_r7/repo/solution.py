from typing import List
from collections import defaultdict

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """
        Find the maximum element-sum of a complete subset of indices.
        
        A set of indices is complete if the product of every pair of indices 
        is a perfect square. This happens when all indices in the set have 
        the same square-free factorization.
        
        The square-free part of a number is the product of its prime factors
        with odd exponents.
        """
        
        def get_square_free(n):
            """
            Returns the square-free part of n.
            The square-free part is the product of prime factors with odd exponents.
            For example:
            - get_square_free(8) = 2 (since 8 = 2^3 = 2^2 * 2)
            - get_square_free(12) = 3 (since 12 = 2^2 * 3)
            - get_square_free(6) = 6 (since 6 = 2 * 3)
            """
            square_free = 1
            d = 2
            
            while d * d <= n:
                count = 0
                while n % d == 0:
                    count += 1
                    n //= d
                
                # If the exponent is odd, multiply square_free by d
                if count % 2 == 1:
                    square_free *= d
                
                d += 1
            
            # If n > 1, then it's a prime with exponent 1 (odd)
            if n > 1:
                square_free *= n
            
            return square_free
        
        # Group indices by their square-free factorization
        groups = defaultdict(int)
        
        for idx in range(1, len(nums) + 1):
            square_free_part = get_square_free(idx)
            groups[square_free_part] += nums[idx - 1]  # idx is 1-indexed
        
        # Return the maximum sum among all groups
        return max(groups.values())
