from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums
        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)
        
        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]
        
        # dp[i][m] = minimum cost to divide nums[0..i-1] into exactly m subarrays
        # Initialize with infinity
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        
        # Base case: empty array with 0 subarrays costs 0
        dp[0][0] = 0
        
        # Fill DP table
        for i in range(1, n + 1):  # i is the end position (exclusive)
            for m in range(1, i + 1):  # m is the number of subarrays
                # Try all possible starting positions for the m-th subarray
                for j in range(m - 1, i):  # j is the start position (inclusive) of m-th subarray
                    if dp[j][m - 1] == INF:
                        continue
                    
                    # Cost of m-th subarray (elements from j to i-1)
                    sum_nums_so_far = prefix_nums[i]  # sum of all nums from 0 to i-1
                    sum_cost_subarray = prefix_cost[i] - prefix_cost[j]  # sum of costs from j to i-1
                    
                    subarray_cost = (sum_nums_so_far + k * m) * sum_cost_subarray
                    
                    dp[i][m] = min(dp[i][m], dp[j][m - 1] + subarray_cost)
        
        # Find minimum cost among all possible numbers of subarrays
        result = min(dp[n])
        return result
