from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        For each element in target, we need to find at least one multiple in nums.
        We can increment any element in nums by 1.
        Return the minimum number of operations.
        
        Strategy:
        - For each target element t, find the cost to make each nums element a multiple of t
        - The cost is: the difference between the nums element and the nearest multiple of t >= nums element
        - Use backtracking to assign each target element to a nums element (each nums element can be used once)
        - Find the assignment with minimum total cost
        """
        n = len(nums)
        m = len(target)
        
        # Calculate cost matrix: cost[i][j] = cost to make nums[i] a multiple of target[j]
        cost = []
        for num in nums:
            row = []
            for t in target:
                # Find the nearest multiple of t that is >= num
                nearest_multiple = ((num + t - 1) // t) * t
                row.append(nearest_multiple - num)
            cost.append(row)
        
        # Use backtracking to find the minimum cost assignment
        # We need to assign each target element to a different nums element
        used = [False] * n
        
        def backtrack(target_idx, current_cost):
            # If we've assigned all target elements, return the current cost
            if target_idx == m:
                return current_cost
            
            min_cost = float('inf')
            
            # Try assigning target[target_idx] to each unused nums element
            for i in range(n):
                if not used[i]:
                    used[i] = True
                    total = backtrack(target_idx + 1, current_cost + cost[i][target_idx])
                    min_cost = min(min_cost, total)
                    used[i] = False
            
            return min_cost
        
        return backtrack(0, 0)
