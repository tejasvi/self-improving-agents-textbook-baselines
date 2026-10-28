from typing import List
from math import gcd

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count the number of connected components in a graph where two nodes i and j
        are connected if lcm(nums[i], nums[j]) <= threshold.
        
        The key optimization is that:
        1. If nums[i] > threshold, it can't connect to anything (lcm(a,b) >= max(a,b))
        2. We use divisors of threshold to find potential connections
        3. Union-Find is used to track connected components
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
        
        def lcm(a, b):
            return a * b // gcd(a, b)
        
        # Map each divisor of threshold to the list of indices with that divisor
        divisor_to_indices = {}
        
        for i, num in enumerate(nums):
            # If num > threshold, it can't connect to anything
            if num > threshold:
                continue
            
            # Find all divisors of num within threshold
            # We iterate through divisors up to sqrt(num)
            divisors = set()
            d = 1
            while d * d <= num:
                if num % d == 0:
                    divisors.add(d)
                    divisors.add(num // d)
                d += 1
            
            # For each divisor, find multiples up to threshold
            # and union them if lcm condition is satisfied
            for div in divisors:
                if div not in divisor_to_indices:
                    divisor_to_indices[div] = []
                
                # Connect to all previous numbers that share this divisor
                for prev_idx in divisor_to_indices[div]:
                    # Check if lcm condition is satisfied
                    if lcm(nums[i], nums[prev_idx]) <= threshold:
                        union(i, prev_idx)
                
                divisor_to_indices[div].append(i)
        
        # Count unique components
        components = len(set(find(i) for i in range(n)))
        return components
