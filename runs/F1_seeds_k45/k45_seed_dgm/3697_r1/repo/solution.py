from typing import List
from math import gcd
from functools import reduce

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        For each target value, we need to ensure there's at least one element in nums
        that is a multiple of it.
        
        The cost to make a number n a multiple of t is:
        - 0 if n % t == 0
        - t - (n % t) otherwise
        
        We need to find the minimum cost assignment of target values to nums elements.
        Since target.length <= 4, we can try all possible assignments.
        """
        
        def cost_to_multiple(num, t):
            """Calculate cost to make num a multiple of t"""
            remainder = num % t
            if remainder == 0:
                return 0
            return t - remainder
        
        m = len(target)
        n = len(nums)
        
        # Precompute costs: cost[i][j] = cost to make nums[j] a multiple of target[i]
        costs = []
        for i in range(m):
            row = []
            for j in range(n):
                row.append(cost_to_multiple(nums[j], target[i]))
            costs.append(row)
        
        # Use bitmask DP where state represents which targets have been covered
        # We try to assign each nums element to cover a subset of targets
        # INF represents an impossible state
        INF = float('inf')
        
        # dp[mask] = minimum cost to satisfy targets in the bitmask
        dp = [INF] * (1 << m)
        dp[0] = 0
        
        for j in range(n):  # For each element in nums
            # For this element nums[j], we can cover any subset of targets
            # We try all possible subsets of targets to cover with this element
            new_dp = dp[:]
            
            for mask in range(1 << m):  # For each possible subset of targets
                if dp[mask] == INF:
                    continue
                
                # Try to extend by covering additional targets with nums[j]
                # We can cover any subset of targets not yet covered
                for submask in range(1 << m):
                    # Check if submask uses only targets not in mask
                    if mask & submask == 0:  # No overlap
                        # Cost to cover submask with nums[j]
                        cost = 0
                        valid = True
                        for i in range(m):
                            if submask & (1 << i):
                                cost += costs[i][j]
                        
                        new_mask = mask | submask
                        new_dp[new_mask] = min(new_dp[new_mask], dp[mask] + cost)
            
            dp = new_dp
        
        return dp[(1 << m) - 1]
