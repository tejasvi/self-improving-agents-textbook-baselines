from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """
        Find minimum cost to paint all walls using paid and free painters.
        
        Key insight: If paid painter paints k walls taking total time T, 
        the free painter can paint up to T walls in parallel (since free painter 
        paints each wall in 1 unit of time).
        
        For all n walls to be painted, we need: T >= n - k
        
        We use DP where dp[i][j] = minimum cost to handle first i walls,
        with j walls painted by paid painter and considering accumulated time.
        
        Actually, we use: dp[i][j] = (min_cost, time_sum) where:
        - i = first i walls considered
        - j = number of walls painted by paid painter
        - We track minimum cost and corresponding time sum
        """
        n = len(cost)
        INF = float('inf')
        
        # Create list of walls with indices to track original order if needed
        walls = [(cost[i], time[i]) for i in range(n)]
        # Sort by cost to process cheaper walls first (greedy consideration)
        walls.sort()
        
        # dp[j] = minimum cost when exactly j walls are painted by paid painter
        # We process all n walls and track all possible states
        # But we also need to track the time sum for each state
        
        # Better: use a dictionary to store dp[walls_painted] = list of (cost, time_sum) pairs
        # Keep only pareto-optimal solutions
        
        # Actually simpler: dp[i][j] where:
        # i = number of walls processed
        # j = number of walls painted by paid painter
        # dp[i][j] = minimum cost
        # time_dp[i][j] = time sum for that minimum cost configuration
        
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        time_dp = [[0] * (n + 1) for _ in range(n + 1)]
        
        dp[0][0] = 0
        
        for i in range(n):
            cost_i, time_i = walls[i]
            for j in range(i + 1):  # j walls already painted by paid painter
                if dp[i][j] == INF:
                    continue
                
                # Option 1: Paint current wall with free painter
                # We can do this if j > 0 (paid painter must be occupied for free painter to work)
                if j > 0 and dp[i][j] < dp[i + 1][j]:
                    dp[i + 1][j] = dp[i][j]
                    time_dp[i + 1][j] = time_dp[i][j]
                
                # Option 2: Paint current wall with paid painter
                new_cost = dp[i][j] + cost_i
                new_time = time_dp[i][j] + time_i
                if new_cost < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = new_cost
                    time_dp[i + 1][j + 1] = new_time
        
        result = INF
        for j in range(1, n + 1):
            if dp[n][j] != INF:
                # Check validity: time_sum >= n - j
                if time_dp[n][j] >= n - j:
                    result = min(result, dp[n][j])
        
        return result
