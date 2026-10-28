from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def get_square_free_part(n):
            """
            Returns the square-free part of n (the product of prime factors 
            that appear an odd number of times).
            
            For example:
            - get_square_free_part(8) = 2 (since 8 = 2^3)
            - get_square_free_part(18) = 2 (since 18 = 2 * 3^2)
            - get_square_free_part(12) = 3 (since 12 = 2^2 * 3)
            """
            result = 1
            i = 2
            while i * i <= n:
                count = 0
                while n % i == 0:
                    n //= i
                    count += 1
                # If prime factor i appears odd number of times, include it
                if count % 2 == 1:
                    result *= i
                i += 1
            
            # If n > 1, then it's a prime factor that appears once
            if n > 1:
                result *= n
            
            return result
        
        # Group indices by their square-free part and sum the values
        from collections import defaultdict
        groups = defaultdict(int)
        
        for i in range(len(nums)):
            # Get the square-free part of the index (1-indexed)
            index = i + 1
            key = get_square_free_part(index)
            groups[key] += nums[i]
        
        # Return the maximum sum
        return max(groups.values())
