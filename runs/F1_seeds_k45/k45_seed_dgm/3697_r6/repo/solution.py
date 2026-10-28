from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        For each target value, we need at least one element in nums that is a multiple of it.
        We can increment elements in nums to achieve this.
        
        Approach:
        1. For each target value, find the best element in nums to increment to make it a multiple
        2. The best element is the one that requires minimum increments
        3. Use greedy approach: process targets and assign elements to them
        
        For a number x and target t, the cost to make x a multiple of t is:
        - If x % t == 0, cost is 0
        - Otherwise, cost is t - (x % t) (increment to next multiple)
        """
        
        # For each element in nums, calculate the cost to make it a multiple of each target
        # Then find the minimum cost assignment
        
        n = len(nums)
        m = len(target)
        
        # For each target, find the minimum cost to satisfy it
        # We need to assign each element in nums to at most one target
        
        # Since target.length <= 4, we can use recursive backtracking or dynamic programming
        # Let's use a greedy approach with backtracking
        
        def get_cost(num, t):
            """Get the cost to make num a multiple of t"""
            remainder = num % t
            if remainder == 0:
                return 0
            return t - remainder
        
        # Try to find minimum operations using backtracking
        # used[i] indicates if nums[i] has been assigned to a target
        used = [False] * n
        
        def backtrack(target_idx):
            """Try to satisfy targets starting from target_idx"""
            if target_idx == m:
                return 0  # All targets satisfied
            
            t = target[target_idx]
            min_ops = float('inf')
            
            # Try each element in nums
            for i in range(n):
                if not used[i]:
                    cost = get_cost(nums[i], t)
                    used[i] = True
                    # Recursively try to satisfy remaining targets
                    remaining_ops = backtrack(target_idx + 1)
                    if remaining_ops != float('inf'):
                        min_ops = min(min_ops, cost + remaining_ops)
                    used[i] = False
            
            return min_ops
        
        result = backtrack(0)
        return result if result != float('inf') else 0
