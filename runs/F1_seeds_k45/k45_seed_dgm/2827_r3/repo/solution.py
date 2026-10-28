class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determine if all pairs of indices can be traversed.
        
        Two indices i and j are connected if gcd(nums[i], nums[j]) > 1.
        We need to check if all indices form a single connected component.
        
        Approach:
        1. Use Union-Find to group indices
        2. For each number, find its prime factors
        3. Connect indices that share a prime factor
        4. Check if all valid indices are in the same component
        """
        
        n = len(nums)
        
        # Edge case: single element is always connectable
        if n == 1:
            return True
        
        # If any number is 1, it can't connect to anything
        # So if there's a 1 with other numbers, return False
        if 1 in nums:
            return False
        
        # Union-Find data structure
        parent = list(range(n))
        
        def find(x):
            """Find the root parent of x with path compression"""
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            """Union two elements"""
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_x] = root_y
        
        def get_prime_factors(num):
            """Get all prime factors of a number"""
            factors = set()
            # Check for factor 2
            if num % 2 == 0:
                factors.add(2)
                while num % 2 == 0:
                    num //= 2
            
            # Check for odd factors from 3 onwards
            i = 3
            while i * i <= num:
                if num % i == 0:
                    factors.add(i)
                    while num % i == 0:
                        num //= i
                i += 2
            
            # If num > 1, then it's a prime factor
            if num > 1:
                factors.add(num)
            
            return factors
        
        # Map each prime factor to indices that contain it
        prime_to_indices = {}
        
        for idx, num in enumerate(nums):
            primes = get_prime_factors(num)
            for prime in primes:
                if prime not in prime_to_indices:
                    prime_to_indices[prime] = []
                prime_to_indices[prime].append(idx)
        
        # Union indices that share a prime factor
        for indices in prime_to_indices.values():
            # Connect all indices that share this prime factor
            for i in range(1, len(indices)):
                union(indices[0], indices[i])
        
        # Check if all indices have the same root
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        
        return True
