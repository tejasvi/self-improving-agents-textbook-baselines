from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        nums_prefix = [0] * (n + 1)
        cost_prefix = [0] * (n + 1)
        
        for i in range(n):
            nums_prefix[i + 1] = nums_prefix[i] + nums[i]
            cost_prefix[i + 1] = cost_prefix[i] + cost[i]
        
        # dp[i] = (minimum_cost, number_of_subarrays)
        # minimum_cost to divide nums[0..i-1] into subarrays
        # number_of_subarrays is the number of subarrays in the optimal division
        dp = [(float('inf'), 0)] * (n + 1)
        dp[0] = (0, 0)
        
        for i in range(1, n + 1):
            # Try all possible positions for the start of the last subarray
            for j in range(i):
                # Last subarray is nums[j..i-1]
                # This is the (num_subarrays + 1)-th subarray
                prev_cost, num_subarrays = dp[j]
                
                if prev_cost == float('inf'):
                    continue
                
                current_subarray_index = num_subarrays + 1
                
                # Sum of all nums from 0 to i-1
                nums_sum = nums_prefix[i]
                # Sum of costs from j to i-1
                cost_sum = cost_prefix[i] - cost_prefix[j]
                
                # Cost of this subarray
                subarray_cost = (nums_sum + k * current_subarray_index) * cost_sum
                
                total_cost = prev_cost + subarray_cost
                
                if total_cost < dp[i][0]:
                    dp[i] = (total_cost, current_subarray_index)
        
        return dp[n][0]
