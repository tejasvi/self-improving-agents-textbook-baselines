from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums
        prefix_nums = [0] * (n + 1)
        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
        
        # Precompute prefix sums for cost
        prefix_cost = [0] * (n + 1)
        for i in range(n):
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]
        
        # dp[i] = (minimum cost to partition nums[0..i-1], number of subarrays used)
        # We store a tuple to keep track of the number of subarrays for each position
        INF = float('inf')
        
        # Better approach: dp[i][j] = minimum cost to partition nums[0..i-1] into j subarrays
        # But we need to figure out the optimal number of subarrays
        
        # Actually, simpler approach:
        # dp[i] = minimum cost considering all possible partitions ending at position i-1
        # We need to track both the cost and the number of partitions
        
        # Let's use: dp[i] = list of (cost, num_subarrays) tuples representing Pareto frontier
        # Actually, let's think differently...
        
        # dp[i][j] = minimum cost to partition nums[0..i-1] into exactly j subarrays
        # Initialize with infinity
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        
        # Base case: empty array with 0 subarrays has cost 0
        dp[0][0] = 0
        
        # Fill the DP table
        for i in range(1, n + 1):  # i is the end position (1-indexed)
            for j in range(1, i + 1):  # j is the number of subarrays
                # Try all possible start positions for the j-th subarray
                for start in range(j - 1, i):  # start is 0-indexed, we need at least j-1 elements before
                    if dp[start][j - 1] == INF:
                        continue
                    
                    # The j-th subarray is nums[start..i-1]
                    # Sum of all elements from 0 to i-1
                    sum_nums = prefix_nums[i]
                    
                    # Sum of cost from start to i-1
                    sum_cost = prefix_cost[i] - prefix_cost[start]
                    
                    # Cost of this subarray
                    subarray_cost = (sum_nums + k * j) * sum_cost
                    
                    # Update dp[i][j]
                    dp[i][j] = min(dp[i][j], dp[start][j - 1] + subarray_cost)
        
        # The answer is the minimum cost among all possible numbers of subarrays
        return min(dp[n])
