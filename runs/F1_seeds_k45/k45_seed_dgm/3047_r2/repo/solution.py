class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """
        Find the maximum element-sum of a complete subset of indices.
        
        A subset is complete if the product of every pair of its elements 
        is a perfect square.
        
        Key insight: Two numbers can be in the same complete subset if their
        "square-free" representations are the same. The square-free representation
        is the product of all primes with odd exponents in the prime factorization.
        """
        
        def get_square_free(n):
            """
            Get the square-free representation of n.
            This is the product of all prime factors that appear an odd number of times.
            """
            square_free = 1
            d = 2
            while d * d <= n:
                count = 0
                while n % d == 0:
                    n //= d
                    count += 1
                # If count is odd, include this prime in square_free
                if count % 2 == 1:
                    square_free *= d
                d += 1
            # If n > 1, it's a prime factor with exponent 1 (odd)
            if n > 1:
                square_free *= n
            return square_free
        
        # Group indices by their square-free representation
        # Map: square_free_value -> list of (index, value) pairs
        groups = {}
        for i in range(len(nums)):
            sf = get_square_free(nums[i])
            if sf not in groups:
                groups[sf] = []
            groups[sf].append(nums[i])
        
        # For each group, find the maximum sum
        # Since indices with the same square-free can all be together,
        # we just sum all values in that group
        max_sum = 0
        for values in groups.values():
            max_sum = max(max_sum, sum(values))
        
        return max_sum
