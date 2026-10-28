from typing import List
from math import gcd

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determine if we can traverse between all pairs of indices.
        Two indices i and j can be directly connected if gcd(nums[i], nums[j]) > 1.
        We need to check if all indices are in the same connected component.
        
        Approach:
        - Use Union-Find with prime factors as intermediaries
        - Two numbers are connected if they share a prime factor
        - Group indices by prime factors and union them
        - Check if all indices belong to the same component
        """
        n = len(nums)
        
        # Edge case: if there's only one element, return true
        if n == 1:
            return True
        
        # Check if any number is 1 (has no prime factors)
        # If so, it cannot connect to anything, so return false
        if any(num == 1 for num in nums):
            return False
        
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
        
        # Get prime factors of a number
        def get_prime_factors(num):
            factors = set()
            d = 2
            while d * d <= num:
                while num % d == 0:
                    factors.add(d)
                    num //= d
                d += 1
            if num > 1:
                factors.add(num)
            return factors
        
        # Map from prime factor to list of indices that have this factor
        prime_to_indices = {}
        
        for i, num in enumerate(nums):
            primes = get_prime_factors(num)
            for p in primes:
                if p not in prime_to_indices:
                    prime_to_indices[p] = []
                prime_to_indices[p].append(i)
        
        # Union all indices that share a prime factor
        for indices in prime_to_indices.values():
            # Union all indices in this group
            for i in range(1, len(indices)):
                union(indices[0], indices[i])
        
        # Check if all indices belong to the same component
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        
        return True
