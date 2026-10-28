from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        """
        Find the minimum number of operations to make each element in target
        have at least one multiple in nums.
        
        For each target element, we need to assign a unique num element.
        We calculate the cost to transform each num to be a multiple of each target.
        Then we use DP with bitmask to find the minimum cost assignment.
        """
        n = len(nums)
        m = len(target)
        
        # Calculate cost matrix: cost[i][j] = cost to make nums[i] a multiple of target[j]
        # Cost = number of increments needed
        cost = []
        for num in nums:
            costs_for_num = []
            for t in target:
                # Find the smallest multiple of t that is >= num
                # Number of increments needed = (t - (num % t)) % t
                increments = (t - (num % t)) % t
                costs_for_num.append(increments)
            cost.append(costs_for_num)
        
        # DP with bitmask
        # dp[mask] = minimum cost to satisfy target elements represented by mask
        # using the first few nums
        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0  # Base case: no target elements to satisfy costs 0
        
        # For each number in nums
        for i in range(n):
            # Traverse in reverse to avoid using the same number multiple times
            new_dp = dp.copy()
            
            # For each current state (satisfied target elements)
            for mask in range((1 << m) - 1, -1, -1):
                if dp[mask] == INF:
                    continue
                
                # Try to assign nums[i] to an unsatisfied target element
                for j in range(m):
                    if mask & (1 << j) == 0:  # target[j] not yet satisfied
                        new_mask = mask | (1 << j)
                        new_cost = dp[mask] + cost[i][j]
                        new_dp[new_mask] = min(new_dp[new_mask], new_cost)
            
            dp = new_dp
        
        # Return the cost to satisfy all target elements
        return dp[(1 << m) - 1]
