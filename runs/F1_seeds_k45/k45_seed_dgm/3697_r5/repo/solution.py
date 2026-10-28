from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        Find the minimum number of operations to make each target element have at least one multiple in nums.
        
        Strategy:
        1. For each target element, calculate the cost to make each num element a multiple of it
        2. Use backtracking to find the optimal assignment of nums to targets
        3. Each num can only be assigned to one target
        """
        
        # Sort nums in ascending order for better pruning
        nums = sorted(nums)
        
        # Calculate cost matrix: cost[i][j] = cost to make nums[i] a multiple of target[j]
        # If nums[i] > target[j] * some_large_multiple, the cost might be large
        # But we only care about the next multiple >= nums[i]
        cost_matrix = []
        for num in nums:
            costs = []
            for t in target:
                # Find the smallest multiple of t that is >= num
                multiple = ((num + t - 1) // t) * t
                cost = multiple - num
                costs.append(cost)
            cost_matrix.append(costs)
        
        # Use backtracking to find minimum cost assignment
        # We assign each target element to exactly one num element
        n_nums = len(nums)
        n_targets = len(target)
        used = [False] * n_nums
        
        def backtrack(target_idx, current_cost):
            # Base case: all targets assigned
            if target_idx == n_targets:
                return current_cost
            
            min_cost = float('inf')
            # Try assigning each unused num to the current target
            for num_idx in range(n_nums):
                if not used[num_idx]:
                    used[num_idx] = True
                    cost = backtrack(target_idx + 1, current_cost + cost_matrix[num_idx][target_idx])
                    min_cost = min(min_cost, cost)
                    used[num_idx] = False
            
            return min_cost
        
        return backtrack(0, 0)
