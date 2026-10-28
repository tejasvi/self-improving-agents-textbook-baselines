from typing import List
from math import gcd

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count the number of connected components in an LCM graph.
        
        Key insight:
        - Two nodes i and j are connected if lcm(nums[i], nums[j]) <= threshold
        - For lcm(a, b) <= threshold, both a and b must be <= threshold
        - We use Union-Find to track connected components
        - Instead of checking all pairs, we iterate through multiples up to threshold
          and check if they correspond to numbers in our array
        """
        
        n = len(nums)
        
        # Union-Find data structure
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x == root_y:
                return
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1
        
        # Helper function to compute LCM
        def lcm(a, b):
            return a * b // gcd(a, b)
        
        # Create a mapping from value to index
        value_to_index = {nums[i]: i for i in range(n)}
        
        # For efficient connection, iterate through multiples up to threshold
        # For each multiple m <= threshold, find all numbers in nums that are divisors of m
        # and check if their LCM is <= threshold
        
        # Create a list of indices sorted by their values for easier processing
        indices_by_value = sorted(range(n), key=lambda i: nums[i])
        
        # For each value, check all multiples up to threshold
        for idx in indices_by_value:
            val = nums[idx]
            
            # If the value itself is > threshold, it can only connect to other values
            # Let's check all multiples of val up to threshold
            multiple = val
            while multiple <= threshold:
                # Check if this multiple corresponds to another number in our array
                if multiple in value_to_index:
                    other_idx = value_to_index[multiple]
                    if idx != other_idx:
                        # Check if lcm(val, nums[other_idx]) <= threshold
                        if lcm(val, nums[other_idx]) <= threshold:
                            union(idx, other_idx)
                multiple += val
        
        # Count unique roots
        roots = set()
        for i in range(n):
            roots.add(find(i))
        
        return len(roots)
