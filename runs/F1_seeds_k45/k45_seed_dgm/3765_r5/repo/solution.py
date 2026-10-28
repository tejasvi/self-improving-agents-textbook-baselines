from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        """
        Problem: Divide nums into subarrays to minimize total cost.
        
        Cost of i-th subarray (nums[l..r]):
        (sum(nums[0..r]) + k*i) * sum(cost[l..r])
        
        Key insight: The first part includes prefix sum of ALL nums up to position r
        (not just the subarray), plus k*i where i is the subarray number.
        
        DP approach:
        dp[i][j] = minimum cost to partition nums[0:i] into j subarrays
        
        For each position i and number of subarrays j:
        - Try all possible last subarray starting positions p
        - Last subarray is nums[p:i] with j-th subarray number
        - Cost = (prefix_sum[i] + k*j) * (cost_sum[p:i])
        """
        n = len(nums)
        
        # Precompute prefix sums
        nums_prefix = [0] * (n + 1)
        for i in range(n):
            nums_prefix[i + 1] = nums_prefix[i] + nums[i]
        
        cost_prefix = [0] * (n + 1)
        for i in range(n):
            cost_prefix[i + 1] = cost_prefix[i] + cost[i]
        
        # dp[i][j] = min cost to partition nums[0:i] into j subarrays
        # Initialize with infinity
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        
        # Fill DP table
        for i in range(1, n + 1):  # position in nums
            for j in range(1, i + 1):  # number of subarrays
                # Try all possible starting positions for the j-th subarray
                for p in range(j - 1, i):  # p is the end of previous partition
                    # j-th subarray is nums[p:i]
                    # Cost of this subarray:
                    # (prefix_sum_of_nums_up_to_i + k*j) * (sum_of_costs_in_subarray)
                    nums_sum = nums_prefix[i]  # sum from 0 to i-1
                    cost_sum = cost_prefix[i] - cost_prefix[p]  # sum from p to i-1
                    subarray_cost = (nums_sum + k * j) * cost_sum
                    
                    if dp[p][j - 1] != INF:
                        dp[i][j] = min(dp[i][j], dp[p][j - 1] + subarray_cost)
        
        # Find the minimum cost across all possible number of subarrays
        result = min(dp[n])
        return result if result != INF else 0
