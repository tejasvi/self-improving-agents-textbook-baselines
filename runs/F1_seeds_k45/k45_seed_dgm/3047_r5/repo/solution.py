class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """
        Find the maximum element-sum of a complete subset of indices.
        
        A complete subset means the product of every pair of indices' numbers is a perfect square.
        
        Key insight: Two numbers have a perfect square product if they have the same 
        "square-free" representation (the product of prime factors with odd exponents).
        
        Strategy:
        1. For each number, compute its square-free form
        2. Group numbers by their square-free form
        3. For each group, find the maximum sum (sum of all elements in that group)
        4. Return the overall maximum
        """
        
        def get_square_free(n):
            """
            Get the square-free representation of a number.
            This is the product of all prime factors with odd exponents.
            """
            square_free = 1
            d = 2
            
            # Process factor 2
            count = 0
            while n % 2 == 0:
                count += 1
                n //= 2
            if count % 2 == 1:
                square_free *= 2
            
            # Process odd factors from 3 onwards
            d = 3
            while d * d <= n:
                count = 0
                while n % d == 0:
                    count += 1
                    n //= d
                if count % 2 == 1:
                    square_free *= d
                d += 2
            
            # If n > 1, then it's a prime factor with exponent 1
            if n > 1:
                square_free *= n
            
            return square_free
        
        # Group numbers by their square-free form
        square_free_groups = {}
        
        for num in nums:
            sf = get_square_free(num)
            if sf not in square_free_groups:
                square_free_groups[sf] = 0
            square_free_groups[sf] += num
        
        # Return the maximum sum among all groups
        return max(square_free_groups.values())
