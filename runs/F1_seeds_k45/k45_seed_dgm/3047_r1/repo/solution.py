from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """
        Find the maximum element-sum of a complete subset of indices.
        
        A set of indices is complete if the product of every pair is a perfect square.
        For indices i and j, i*j is a perfect square iff they have the same square-free part.
        
        The square-free part of n is the product of all primes with odd exponents in n's factorization.
        """
        
        def get_square_free_part(n):
            """
            Get the square-free part of n.
            A number is square-free if no prime appears more than once in its factorization.
            """
            square_free = 1
            d = 2
            
            while d * d <= n:
                count = 0
                while n % d == 0:
                    n //= d
                    count += 1
                
                # If count is odd, d appears odd times in factorization
                if count % 2 == 1:
                    square_free *= d
                
                d += 1
            
            # If n > 1, then it's a prime factor that appears once (odd)
            if n > 1:
                square_free *= n
            
            return square_free
        
        # Group indices by their square-free part
        # For 1-indexed array, we use indices 1 to n (not 0 to n-1)
        groups = {}
        
        for i in range(1, len(nums) + 1):
            square_free = get_square_free_part(i)
            
            if square_free not in groups:
                groups[square_free] = 0
            
            groups[square_free] += nums[i - 1]  # nums is 0-indexed
        
        # Return the maximum sum among all groups
        return max(groups.values())
