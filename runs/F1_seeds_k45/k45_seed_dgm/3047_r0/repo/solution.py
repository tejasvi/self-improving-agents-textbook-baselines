from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """
        Find the maximum element-sum of a complete subset of indices.
        
        A complete subset is one where the product of every pair of elements
        is a perfect square. This happens when all elements have the same
        "square-free" part.
        
        The square-free part of a number is what remains after removing
        all perfect square factors.
        """
        
        def get_square_free(n):
            """
            Get the square-free part of n by dividing out all square factors.
            """
            square_free = 1
            i = 2
            while i * i <= n:
                count = 0
                while n % i == 0:
                    n //= i
                    count += 1
                # If count is odd, i remains in the square-free part
                if count % 2 == 1:
                    square_free *= i
                i += 1
            # If n > 1, then it's a prime factor with odd count
            if n > 1:
                square_free *= n
            return square_free
        
        # Group indices by their square-free part
        groups = {}
        for idx in range(len(nums)):
            square_free = get_square_free(nums[idx])
            if square_free not in groups:
                groups[square_free] = 0
            groups[square_free] += nums[idx]
        
        # Return the maximum sum among all groups
        return max(groups.values())
