from typing import List
from math import gcd

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count connected components in an LCM graph.
        Two nodes i and j are connected if lcm(nums[i], nums[j]) <= threshold.
        
        Approach:
        1. Use Union-Find (Disjoint Set Union) to track connected components
        2. For efficiency, iterate through multiples from 1 to threshold
        3. For each multiple, find which numbers divide it
        4. Connect all numbers that divide the same multiple via Union-Find
        5. Count the number of distinct components at the end
        """
        n = len(nums)
        
        # Union-Find data structure
        parent = list(range(n))
        
        def find(x):
            """Find the root of x with path compression"""
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            """Union two elements"""
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_x] = root_y
        
        # Create a mapping from each number to its index
        num_to_indices = {}
        for i, num in enumerate(nums):
            num_to_indices[num] = i
        
        # For each multiple from 1 to threshold, find which numbers divide it
        # and connect them using Union-Find
        for multiple in range(1, threshold + 1):
            indices = []
            
            # Find all numbers that divide this multiple
            for i, num in enumerate(nums):
                if multiple % num == 0:
                    indices.append(i)
            
            # Connect all pairs of numbers that divide this multiple
            # They all have lcm <= multiple <= threshold
            if len(indices) > 1:
                for j in range(1, len(indices)):
                    union(indices[0], indices[j])
        
        # Count distinct components (distinct roots)
        components = len(set(find(i) for i in range(n)))
        return components
