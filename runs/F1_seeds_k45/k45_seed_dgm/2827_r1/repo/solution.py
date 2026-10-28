from typing import List
from math import gcd

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determine if all pairs of indices can be traversed.
        Two indices can be directly connected if gcd(nums[i], nums[j]) > 1.
        
        The approach:
        1. Use Union-Find (DSU) to group indices
        2. For each number, decompose it into prime factors
        3. Indices sharing a prime factor should be in the same component
        4. Check if all indices are in one connected component
        """
        
        n = len(nums)
        
        # Edge case: single element
        if n == 1:
            return True
        
        # Check if any number is 1 (can't connect to anything)
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
        
        # Helper function to get prime factors of a number
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
            
            # If num is still greater than 1, it's a prime factor
            if num > 1:
                factors.add(num)
            
            return factors
        
        # Map from prime to an index that has this prime factor
        prime_to_index = {}
        
        for i, num in enumerate(nums):
            primes = get_prime_factors(num)
            
            for prime in primes:
                if prime in prime_to_index:
                    # Union current index with the previous index that had this prime
                    union(i, prime_to_index[prime])
                else:
                    # Record this prime with current index
                    prime_to_index[prime] = i
        
        # Check if all indices are in the same component
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        
        return True
