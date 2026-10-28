from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """
        Find the minimum cost to paint all walls using two painters:
        - A paid painter that takes time[i] to paint wall i, costing cost[i]
        - A free painter that takes 1 unit of time per wall, but only works when paid painter is occupied
        
        Key insight: If paid painter works for t units of time, free painter can paint t additional walls.
        
        Problem formulation:
        - Select a subset S of walls for the paid painter
        - Paid painter paints |S| walls and accumulates sum(time[i] for i in S) units of time
        - Free painter can paint sum(time[i] for i in S) walls while paid painter is working
        - Total walls painted: |S| + sum(time[i] for i in S)
        - We need: |S| + sum(time[i] for i in S) >= n
        - Minimize: sum(cost[i] for i in S)
        
        DP approach:
        - dp[k] = minimum cost to select k walls for paid painter such that
                  k + sum(time of selected) >= n (equivalently, sum(time) >= n - k)
        """
        n = len(cost)
        INF = float('inf')
        
        # dp[k] stores (min_cost, time_sum) for selecting k walls
        # We track time sum to validate the constraint sum(time) >= n - k
        dp = [INF] * (n + 1)
        time_sum = [0] * (n + 1)
        dp[0] = 0
        
        for j in range(n):
            # Process wall j - decide whether to select it for paid painter
            # Traverse in reverse to avoid using the same wall multiple times
            for k in range(min(j + 1, n), 0, -1):
                if dp[k-1] < INF:
                    new_cost = dp[k-1] + cost[j]
                    new_time = time_sum[k-1] + time[j]
                    
                    # Update state if this gives lower cost for k walls
                    # Check if the new state satisfies: k + new_time >= n
                    if k + new_time >= n:
                        if new_cost < dp[k]:
                            dp[k] = new_cost
                            time_sum[k] = new_time
                    # Also update if not yet satisfied but we'll consider it
                    # (might become valid when more walls are added)
                    elif new_cost < dp[k]:
                        dp[k] = new_cost
                        time_sum[k] = new_time
        
        # Find minimum cost among all valid states
        result = INF
        for k in range(n + 1):
            if k + time_sum[k] >= n:
                result = min(result, dp[k])
        
        return result
