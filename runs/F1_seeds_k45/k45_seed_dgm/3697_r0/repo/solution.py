from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        Find minimum increments needed so each element in target 
        has at least one multiple in nums.
        
        Approach:
        1. For each element in nums, compute which target elements it can satisfy
           and at what cost (operations needed)
        2. Use dynamic programming with bitmask to find the minimum cost
           to satisfy all target elements
        """
        n = len(nums)
        m = len(target)
        
        # For each num, compute the cost to make it a multiple of each target
        # cost[i][j] = cost to make nums[i] a multiple of target[j]
        costs = []
        for num in nums:
            num_costs = []
            for t in target:
                # Find the next multiple of t that is >= num
                # Cost is that multiple minus num
                next_multiple = ((num // t) + 1) * t
                cost = next_multiple - num
                num_costs.append(cost)
            costs.append(num_costs)
        
        # DP with bitmask
        # dp[mask] = minimum cost to satisfy target elements indicated by mask
        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0
        
        # Try assigning each num to cover some subset of targets
        for i in range(n):
            # For each state, we can use nums[i] to cover additional targets
            new_dp = dp[:]
            
            # Generate all non-empty subsets of targets
            for subset in range(1, 1 << m):
                # Cost to make nums[i] a multiple of all targets in subset
                cost = 0
                valid = True
                for j in range(m):
                    if subset & (1 << j):
                        cost = max(cost, costs[i][j])
                    
                # With this num, we can reach this subset
                # Update all states that can be extended
                for prev_mask in range(1 << m):
                    if dp[prev_mask] < INF:
                        new_mask = prev_mask | subset
                        new_dp[new_mask] = min(new_dp[new_mask], dp[prev_mask] + cost)
            
            dp = new_dp
        
        return dp[(1 << m) - 1]
