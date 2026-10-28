class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """
        Minimum cost to paint all walls using a paid painter and a free painter.
        
        The paid painter paints wall i in time[i] units and costs cost[i].
        The free painter paints any wall in 1 unit of time but only when paid painter is busy.
        
        Key insight: If we sort walls by cost and use DP, we can decide which walls 
        the paid painter should paint to minimize total cost.
        
        DP[i] = minimum cost to paint first i walls
        """
        n = len(cost)
        
        # Create list of (cost, time, index) and sort by cost
        walls = sorted([(cost[i], time[i]) for i in range(n)])
        
        # dp[i] = minimum cost to paint first i walls
        # We need to paint all n walls, so answer is dp[n]
        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0  # 0 cost to paint 0 walls
        
        # For each number of walls painted
        for i in range(n):
            # Current wall the paid painter will paint
            paid_cost, paid_time = walls[i]
            
            # Try using paid painter on this wall
            # This contributes paid_cost to total cost
            # And gives us paid_time units for free painter to work
            # Free painter can paint up to paid_time walls
            
            # dp[j] is the minimum cost to paint j walls before we use paid painter on current wall
            # After using paid painter, we can have free painter paint up to paid_time additional walls
            # So we can cover walls from j to min(j + paid_time, n)
            
            for j in range(i + 1):
                # j walls already painted by free painter (from previous paid painter uses)
                # Use paid painter on wall i, which takes paid_time units
                # Free painter can paint up to paid_time more walls
                walls_painted = j + paid_time + 1  # j + 1 (current wall) + paid_time (free painter)
                walls_painted = min(walls_painted, n)
                
                dp[walls_painted] = min(dp[walls_painted], dp[j] + paid_cost)
        
        return dp[n]
