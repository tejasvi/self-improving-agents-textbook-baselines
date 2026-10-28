from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        For each target value, we need to find a number in nums that can be 
        incremented to become a multiple of that target with minimum cost.
        
        The cost to make a number n a multiple of t is:
        ceil(n/t) * t - n = ((n + t - 1) // t) * t - n
        
        Since target.length <= 4, we can try all possible assignments.
        Each target is assigned to exactly one element in nums, but multiple
        targets can be assigned to the same nums element.
        """
        
        def cost_to_multiple(num, target_val):
            """Calculate cost to make num a multiple of target_val"""
            # Find the smallest multiple of target_val that is >= num
            multiple = ((num + target_val - 1) // target_val) * target_val
            return multiple - num
        
        # Precompute costs for all pairs
        costs = []
        for t in target:
            row = []
            for n in nums:
                row.append(cost_to_multiple(n, t))
            costs.append(row)
        
        # Now we need to assign each target to a nums element to minimize total cost
        # Since target.length <= 4, we can use recursion/backtracking
        memo = {}
        
        def solve(target_idx):
            """
            Recursively assign targets to nums elements.
            Returns minimum cost to handle targets from target_idx onwards.
            """
            if target_idx == len(target):
                return 0
            
            if target_idx in memo:
                return memo[target_idx]
            
            min_cost = float('inf')
            
            # Try assigning this target to each element in nums
            for nums_idx in range(len(nums)):
                cost = costs[target_idx][nums_idx]
                remaining = solve(target_idx + 1)
                min_cost = min(min_cost, cost + remaining)
            
            memo[target_idx] = min_cost
            return min_cost
        
        return solve(0)
