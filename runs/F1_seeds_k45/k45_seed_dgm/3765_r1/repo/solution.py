from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)
        
        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]
        
        # dp[i] = (min_cost, num_subarrays) to divide nums[0..i-1]
        # We need to track the number of subarrays used to get to each position
        dp = [(float('inf'), 0)] * (n + 1)
        dp[0] = (0, 0)
        
        for i in range(1, n + 1):
            # Try all possible last subarrays ending at position i
            for j in range(i):
                prev_cost, prev_num_subarrays = dp[j]
                
                if prev_cost == float('inf'):
                    continue
                
                # Last subarray is nums[j..i-1]
                num_subarrays = prev_num_subarrays + 1
                sum_nums_prefix = prefix_nums[i]  # sum of all elements up to i
                sum_cost_subarray = prefix_cost[i] - prefix_cost[j]  # sum of costs for subarray
                
                subarray_cost = (sum_nums_prefix + k * num_subarrays) * sum_cost_subarray
                total_cost = prev_cost + subarray_cost
                
                if total_cost < dp[i][0]:
                    dp[i] = (total_cost, num_subarrays)
        
        return dp[n][0]
