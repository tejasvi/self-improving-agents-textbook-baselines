from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums
        nums_prefix = [0] * (n + 1)
        cost_prefix = [0] * (n + 1)
        
        for i in range(n):
            nums_prefix[i + 1] = nums_prefix[i] + nums[i]
            cost_prefix[i + 1] = cost_prefix[i] + cost[i]
        
        # dp[i][j] = minimum cost to divide nums[0..i-1] into j subarrays
        # Initialize with infinity
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        
        # Fill the DP table
        for i in range(1, n + 1):  # ending position (exclusive upper bound)
            for j in range(1, i + 1):  # number of subarrays
                # Try all possible starting positions for the j-th subarray
                for start in range(j - 1, i):  # start position of j-th subarray
                    if dp[start][j - 1] == INF:
                        continue
                    
                    # j-th subarray is nums[start..i-1]
                    # Sum of all elements up to end of this subarray
                    num_sum = nums_prefix[i]
                    # Sum of costs in this subarray
                    cost_sum = cost_prefix[i] - cost_prefix[start]
                    
                    # Cost of j-th subarray
                    subarray_cost = (num_sum + k * j) * cost_sum
                    
                    # Update dp[i][j]
                    dp[i][j] = min(dp[i][j], dp[start][j - 1] + subarray_cost)
        
        # Find the minimum cost for any valid division
        result = min(dp[n][j] for j in range(1, n + 1))
        return result
