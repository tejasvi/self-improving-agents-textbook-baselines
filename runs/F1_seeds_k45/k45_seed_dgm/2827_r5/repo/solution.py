from typing import List

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determine if all pairs of indices can be traversed through
        when we can only move between indices i and j if gcd(nums[i], nums[j]) > 1
        """
        n = len(nums)
        
        if n == 1:
            return True
        
        # If any number is 1, it has gcd 1 with everything else
        if any(num == 1 for num in nums):
            return False
        
        # Union-Find data structure using list for faster access
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
                return True
            return False
        
        # Get prime factors for a number
        def get_prime_factors(num):
            factors = []
            d = 2
            while d * d <= num:
                if num % d == 0:
                    factors.append(d)
                    while num % d == 0:
                        num //= d
                d += 1
            if num > 1:
                factors.append(num)
            return factors
        
        # Map from prime to list of indices having that prime
        prime_to_indices = {}
        
        for idx, num in enumerate(nums):
            primes = get_prime_factors(num)
            for p in primes:
                if p not in prime_to_indices:
                    prime_to_indices[p] = []
                prime_to_indices[p].append(idx)
        
        # Union indices that share a prime factor
        for p, indices in prime_to_indices.items():
            for i in range(1, len(indices)):
                union(indices[0], indices[i])
        
        # Check if all indices are in same component
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        
        return True
