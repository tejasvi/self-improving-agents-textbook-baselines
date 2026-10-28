from typing import List
from math import gcd

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count the number of connected components in a graph where nodes are connected
        if their LCM is <= threshold.
        
        Strategy:
        1. Use Union-Find (Disjoint Set Union) to track connected components
        2. For efficiency, instead of checking all pairs, we use prime factors
        3. Numbers that share prime factors (and satisfy LCM constraint) are connected
        4. We track which prime factors connect to which numbers
        """
        n = len(nums)
        
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
            return a * b // gcd(a, b)
        
        # Filter out numbers > threshold (they can't connect to anything except themselves)
        # But we still need to track all original numbers
        valid_indices = [i for i in range(n) if nums[i] <= threshold]
        
        # For each valid number, find its prime factors up to threshold
        # and use them to connect numbers that share factors
        prime_to_index = {}  # Maps prime factor to the index of a number having it
        
        def get_prime_factors(num, limit):
            """Get all prime factors of num up to limit"""
            factors = []
            # Check small primes
            d = 2
            while d * d <= num and d <= limit:
                if num % d == 0:
                    factors.append(d)
                    while num % d == 0:
                        num //= d
                d += 1
            # If num > 1 and num <= limit, it's a prime factor
            if num > 1 and num <= limit:
                factors.append(num)
            return factors
        
        # Connect numbers through their prime factors
        for i in valid_indices:
            factors = get_prime_factors(nums[i], threshold)
            for factor in factors:
                if factor in prime_to_index:
                    # Check if LCM condition is satisfied
                    prev_i = prime_to_index[factor]
                    if lcm(nums[prev_i], nums[i]) <= threshold:
                        union(i, prev_i)
                    else:
                        # Update to current index (try to connect with newer numbers)
                        prime_to_index[factor] = i
                else:
                    prime_to_index[factor] = i
        
        # Count unique connected components
        components = len(set(find(i) for i in range(n)))
        return components
