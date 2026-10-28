from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """
        Find minimum cost to paint all walls using a paid painter and a free painter.
        
        The paid painter can paint wall i in time[i] units and costs cost[i] money.
        The free painter can paint any wall in 1 unit of time for free, but only while
        the paid painter is busy.
        
        This is a DP problem where we decide which walls to paint with the paid painter.
        
        DP State: dp[i][j] = minimum cost to paint first i walls where the paid painter
        has j units of remaining time.
        
        For each wall, we either:
        1. Paint it with the paid painter (costs cost[i], gives time[i] units for free painter)
        2. Paint it with the free painter (costs 0, requires 1 unit of paid painter time)
        """
        n = len(cost)
        
        # dp[i][j] = min cost to paint first i walls with j time remaining for free painter
        # j can be negative initially (meaning free painter still has work to do)
        # We use a dictionary for sparse DP with negative indices
        
        # Alternative cleaner approach: dp[i] with explicit time tracking
        # Let's use: dp[i][time_balance] where time_balance is paid_time - free_time_needed
        
        INF = float('inf')
        
        # dp[j] = minimum cost to reach a state where paid painter has j time remaining
        # j represents the net time available (paid time - walls painted by free painter)
        
        # Initialize: no walls painted yet, no time spent
        dp = {0: 0}  # {time_remaining: min_cost}
        
        for i in range(n):
            new_dp = {}
            
            for time_remaining, cost_so_far in dp.items():
                # Option 1: Paint wall i with paid painter
                # This adds time[i] to our available time (for free painter)
                # and costs cost[i]
                new_time = time_remaining + time[i]
                new_cost = cost_so_far + cost[i]
                
                if new_time not in new_dp or new_dp[new_time] > new_cost:
                    new_dp[new_time] = new_cost
                
                # Option 2: Paint wall i with free painter
                # This requires 1 unit of time from paid painter
                # Costs 0, but reduces available time by 1
                if time_remaining > 0:  # Only if paid painter has time available
                    new_time2 = time_remaining - 1
                    new_cost2 = cost_so_far
                    
                    if new_time2 not in new_dp or new_dp[new_time2] > new_cost2:
                        new_dp[new_time2] = new_cost2
            
            dp = new_dp
        
        # Find minimum cost where time_remaining >= 0 (all walls painted)
        result = INF
        for time_remaining, cost_total in dp.items():
            if time_remaining >= 0:
                result = min(result, cost_total)
        
        return result
