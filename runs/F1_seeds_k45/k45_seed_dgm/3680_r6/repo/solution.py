from typing import List
import math

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count connected components in a graph where nodes i and j are connected
        if lcm(nums[i], nums[j]) <= threshold.
        
        Uses Union-Find with an optimization: instead of checking all pairs O(n²),
        we iterate through divisors and their multiples up to threshold.
        """
        n = len(nums)
        
        # Union-Find data structure
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Helper function to compute LCM
        def lcm(a, b):
            return a * b // math.gcd(a, b)
        
        # Helper function to get all divisors of a number
        def get_divisors(num):
            divisors = []
            i = 1
            while i * i <= num:
                if num % i == 0:
                    divisors.append(i)
                    if i != num // i:
                        divisors.append(num // i)
                i += 1
            return divisors
        
        # Map from value to index for quick lookup
        value_to_idx = {num: i for i, num in enumerate(nums)}
        
        # For each number, find its divisors and check multiples
        for i, num in enumerate(nums):
            # Get all divisors of num
            divisors = get_divisors(num)
            
            # For each divisor, check all multiples of it up to threshold
            for divisor in divisors:
                # Check multiples of this divisor
                multiple = divisor
                while multiple <= threshold:
                    if multiple in value_to_idx:
                        j = value_to_idx[multiple]
                        if i != j:
                            # Check if lcm(nums[i], nums[j]) <= threshold
                            if lcm(nums[i], nums[j]) <= threshold:
                                union(i, j)
                    multiple += divisor
        
        # Count unique components
        return len(set(find(i) for i in range(n)))
