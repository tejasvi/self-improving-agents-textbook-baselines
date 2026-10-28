from typing import List
from math import gcd

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        """
        Count connected components in a graph where nodes are connected if their LCM <= threshold.
        
        Strategy:
        1. Use Union-Find to efficiently track connected components
        2. Instead of checking all O(n^2) pairs directly, use a smarter approach:
           - For each number, find all its multiples up to threshold
           - Check which other numbers in the array are divisible by these multiples
           - Connect numbers that share common multiples leading to LCM <= threshold
        
        The key insight is that if lcm(a, b) <= threshold, then we can connect them.
        LCM(a, b) = (a * b) / gcd(a, b)
        """
        
        if not nums:
            return 0
        
        n = len(nums)
        
        # Union-Find data structure
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]
        
        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            
            if root_x == root_y:
                return
            
            # Union by rank
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1
        
        # Create a mapping from value to index for quick lookup
        value_to_idx = {nums[i]: i for i in range(n)}
        
        # For each number, find all its multiples up to threshold
        # and check if they divide any other number in the array
        for i in range(n):
            num = nums[i]
            # Find all multiples of num up to threshold
            multiple = num
            while multiple <= threshold:
                # Check if this multiple divides any other number
                if multiple % num == 0:
                    # For each divisor of multiple that is in our nums array
                    # Check if lcm(num, that_num) <= threshold
                    for j in range(i + 1, n):
                        other_num = nums[j]
                        if multiple % other_num == 0:
                            # Both num and other_num divide multiple
                            # This means lcm(num, other_num) divides multiple
                            # So lcm(num, other_num) <= multiple <= threshold
                            union(i, j)
                multiple += num
        
        # Count the number of distinct roots (connected components)
        components = len(set(find(i) for i in range(n)))
        return components
