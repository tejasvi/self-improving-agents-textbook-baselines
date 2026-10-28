from typing import List
from math import gcd

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count connected components in a graph where nodes are connected
        if lcm(nums[i], nums[j]) <= threshold.
        
        Key insight: Use Union-Find to efficiently track connected components.
        Instead of checking all pairs (O(n^2)), we iterate through divisors.
        For each number, we find its divisors and check multiples of those
        divisors that are <= threshold to find connections.
        """
        if not nums:
            return 0
        
        n = len(nums)
        
        # Union-Find data structure
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_x] = root_y
        
        # Map from value to index for quick lookup
        value_to_index = {num: i for i, num in enumerate(nums)}
        
        # Create a list of divisors for each threshold value
        # divisors[d] contains a list of indices whose nums[i] is divisible by d
        divisors_map = {}
        
        # For each number, find all its divisors up to threshold
        for i, num in enumerate(nums):
            # Find divisors of num
            d = 1
            while d * d <= num:
                if num % d == 0:
                    # d is a divisor
                    if d <= threshold:
                        if d not in divisors_map:
                            divisors_map[d] = []
                        divisors_map[d].append(i)
                    
                    # num // d is also a divisor
                    other_d = num // d
                    if other_d <= threshold and other_d != d:
                        if other_d not in divisors_map:
                            divisors_map[other_d] = []
                        divisors_map[other_d].append(i)
                d += 1
        
        # Connect nodes that share a common divisor
        # If two numbers share a common divisor d and both a*d and b*d <= threshold,
        # then lcm(a*d, b*d) <= threshold
        for d in divisors_map:
            indices = divisors_map[d]
            # Connect all pairs that share this divisor
            for i in range(1, len(indices)):
                union(indices[0], indices[i])
        
        # Count connected components
        components = len(set(find(i) for i in range(n)))
        return components
