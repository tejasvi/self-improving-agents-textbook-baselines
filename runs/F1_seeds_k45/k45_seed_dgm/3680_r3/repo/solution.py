from typing import List
from math import gcd

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count connected components in a graph where nodes are connected if their LCM <= threshold.
        
        Key insight: For each number, we iterate through all its divisors.
        For each divisor d, we check all multiples of d up to threshold.
        If a multiple m has a number in nums that is divisible by d,
        and lcm(current_num, that_num) <= threshold, we union them.
        """
        
        n = len(nums)
        if n == 0:
            return 0
        
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
            return (a * b) // gcd(a, b)
        
        # Create a mapping from value to index
        num_to_index = {num: i for i, num in enumerate(nums)}
        
        # Track which divisors we've already processed to avoid redundant work
        # For each divisor, store which numbers are divisible by it
        divisor_map = {}
        
        for i, num in enumerate(nums):
            # Find all divisors of num
            d = 1
            divisors = []
            while d * d <= num:
                if num % d == 0:
                    divisors.append(d)
                    if d != num // d:
                        divisors.append(num // d)
                d += 1
            
            # For each divisor of current number
            for div in divisors:
                if div not in divisor_map:
                    divisor_map[div] = []
                
                # Check all previous numbers that share this divisor
                for prev_idx in divisor_map[div]:
                    prev_num = nums[prev_idx]
                    if lcm(prev_num, num) <= threshold:
                        union(prev_idx, i)
                
                # Add current number to this divisor's list
                divisor_map[div].append(i)
        
        # Count unique components
        components = len(set(find(i) for i in range(n)))
        return components
