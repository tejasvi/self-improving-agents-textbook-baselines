from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        Find minimum operations to make each target value have at least one multiple in nums.
        
        For each target value, we need to pick one element from nums and increment it
        to become a multiple of that target value.
        
        We use backtracking to try all possible assignments of targets to nums elements.
        """
        n = len(nums)
        m = len(target)
        
        # For each element in nums, calculate the cost to make it a multiple of each target
        # cost[i][j] = cost to make nums[i] a multiple of target[j]
        cost = []
        for num in nums:
            costs_for_num = []
            for t in target:
                # Find the smallest multiple of t that is >= num
                # That would be: ceil(num / t) * t
                # Cost is: ceil(num / t) * t - num
                multiple = ((num + t - 1) // t) * t  # This is ceil(num / t) * t
                cost_val = multiple - num
                costs_for_num.append(cost_val)
            cost.append(costs_for_num)
        
        # Now we need to assign each target index to a nums index
        # such that each target index is assigned to exactly one nums index
        # and we minimize the total cost
        # This is a minimum cost assignment problem
        
        # Since target.length <= 4, we can use bitmask DP or backtracking
        used = [False] * n
        min_ops = float('inf')
        
        def backtrack(target_idx, current_cost):
            nonlocal min_ops
            
            # Base case: all targets are assigned
            if target_idx == m:
                min_ops = min(min_ops, current_cost)
                return
            
            # Try assigning target[target_idx] to each unused nums element
            for nums_idx in range(n):
                if not used[nums_idx]:
                    used[nums_idx] = True
                    backtrack(target_idx + 1, current_cost + cost[nums_idx][target_idx])
                    used[nums_idx] = False
        
        backtrack(0, 0)
        return min_ops
