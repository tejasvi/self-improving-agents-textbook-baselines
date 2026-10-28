from typing import List

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determines if all pairs of indices can be traversed between each other
        based on gcd(nums[i], nums[j]) > 1 constraint.
        
        Approach:
        1. If any element is 1, return false (1 has no common divisors > 1)
        2. Use Union-Find with prime factorization:
           - For each number, find its prime factors
           - Map each prime factor to indices that have it
           - Union all indices that share a prime factor
        3. Check if all indices are in the same connected component
        """
        if len(nums) == 1:
            return True
        
        # If any element is 1, it cannot connect to anything
        if any(num == 1 for num in nums):
            return False
        
        # Union-Find data structure
        parent = list(range(len(nums)))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Prime factorization and mapping
        # Map prime -> list of indices that have this prime factor
        prime_to_indices = {}
        
        for idx, num in enumerate(nums):
            # Find all prime factors
            temp = num
            d = 2
            while d * d <= temp:
                if temp % d == 0:
                    if d not in prime_to_indices:
                        prime_to_indices[d] = []
                    prime_to_indices[d].append(idx)
                    while temp % d == 0:
                        temp //= d
                d += 1
            
            # If temp > 1, it's a prime factor
            if temp > 1:
                if temp not in prime_to_indices:
                    prime_to_indices[temp] = []
                prime_to_indices[temp].append(idx)
        
        # Union all indices that share a prime factor
        for indices in prime_to_indices.values():
            for i in range(1, len(indices)):
                union(indices[0], indices[i])
        
        # Check if all indices are in the same connected component
        root = find(0)
        for i in range(1, len(nums)):
            if find(i) != root:
                return False
        
        return True
