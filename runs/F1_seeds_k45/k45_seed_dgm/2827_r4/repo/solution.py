from typing import List

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determine if all pairs of indices can be traversed between.
        Two indices can be directly connected if gcd(nums[i], nums[j]) > 1.
        We use Union-Find with prime factors as the key insight:
        - If two numbers share a prime factor, they're connected
        - We connect all indices that share the same prime factor
        """
        n = len(nums)
        
        # Edge case: single element
        if n == 1:
            return True
        
        # If any number is 1, it can't be connected to anything (gcd with any number is 1)
        if 1 in nums:
            return False
        
        # Union-Find data structure
        parent = list(range(n))
        
        def find(x):
            # Iterative find with path compression
            root = x
            while parent[root] != root:
                root = parent[root]
            # Path compression
            while parent[x] != root:
                next_x = parent[x]
                parent[x] = root
                x = next_x
            return root
        
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
            # Check for odd factors
            i = 3
            while i * i <= num:
                if num % i == 0:
                    factors.add(i)
                    while num % i == 0:
                        num //= i
                i += 2
            if num > 1:
                factors.add(num)
            return factors
        
        # Map prime factor to indices that have it
        prime_to_indices = {}
        
        for idx, num in enumerate(nums):
            primes = get_prime_factors(num)
            for prime in primes:
                if prime not in prime_to_indices:
                    prime_to_indices[prime] = []
                prime_to_indices[prime].append(idx)
        
        # Union all indices that share a prime factor
        for prime, indices in prime_to_indices.items():
            # Connect all indices with this prime factor
            for i in range(1, len(indices)):
                union(indices[0], indices[i])
        
        # Check if all indices are in the same connected component
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        
        return True
