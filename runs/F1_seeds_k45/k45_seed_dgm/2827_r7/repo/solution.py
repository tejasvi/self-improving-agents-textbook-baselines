from typing import List

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        """
        Determine if we can traverse between all pairs of indices.
        We can traverse from i to j if gcd(nums[i], nums[j]) > 1.
        
        Strategy:
        - Use Union-Find to group indices that are connected
        - Connect indices by their prime factors
        - If all indices are in one connected component, return True
        """
        n = len(nums)
        
        # Edge case: single element
        if n == 1:
            return True
        
        # Edge case: if any element is 1, we can't connect it to anything
        if any(num == 1 for num in nums):
            return False
        
        # Union-Find data structure
        parent = list(range(n + 100))  # Extra space for prime factors
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # For each number, find its prime factors and connect index to them
        # We use n as a starting point for prime factor nodes
        prime_index = n
        prime_to_index = {}
        
        for i, num in enumerate(nums):
            # Find prime factors of nums[i]
            temp = num
            d = 2
            while d * d <= temp:
                if temp % d == 0:
                    # d is a prime factor
                    if d not in prime_to_index:
                        prime_to_index[d] = prime_index
                        prime_index += 1
                    
                    # Connect index i to the prime factor
                    union(i, prime_to_index[d])
                    
                    # Remove all occurrences of d from temp
                    while temp % d == 0:
                        temp //= d
                
                d += 1
            
            # If temp > 1, it's a prime factor
            if temp > 1:
                if temp not in prime_to_index:
                    prime_to_index[temp] = prime_index
                    prime_index += 1
                
                union(i, prime_to_index[temp])
        
        # Check if all indices belong to the same connected component
        root = find(0)
        for i in range(1, n):
            if find(i) != root:
                return False
        
        return True
