from typing import List
from collections import defaultdict

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determine if all pairs of indices can be traversed given gcd constraint.
        
        Approach:
        - Use prime factors as intermediate nodes
        - Two indices can be reached if they share a prime factor
        - Use Union-Find to track connectivity through prime factors
        """
        
        n = len(nums)
        
        # Edge case: single element is always traversable
        if n == 1:
            return True
        
        # If any element is 1, it can't connect to anything
        # So if we have more than 1 element and any is 1, return False
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
        
        # Helper function to get prime factors
        def get_prime_factors(num):
            factors = set()
            # Check for 2
            if num % 2 == 0:
                factors.add(2)
                while num % 2 == 0:
                    num //= 2
            
            # Check for odd factors from 3 onwards
            d = 3
            while d * d <= num:
                if num % d == 0:
                    factors.add(d)
                    while num % d == 0:
                        num //= d
                d += 2
            
            # If num > 1, then it's a prime factor
            if num > 1:
                factors.add(num)
            
            return factors
        
        # Map each prime factor to indices containing it
        prime_to_indices = defaultdict(list)
        
        for idx, num in enumerate(nums):
            primes = get_prime_factors(num)
            for prime in primes:
                prime_to_indices[prime].append(idx)
        
        # Union indices that share a prime factor
        for prime, indices in prime_to_indices.items():
            # Connect the first index with all others sharing this prime
            for i in range(1, len(indices)):
                union(indices[0], indices[i])
        
        # Check if all indices are in the same connected component
        root = find(0)
        return all(find(i) == root for i in range(n))
