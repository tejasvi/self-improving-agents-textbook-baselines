class Solution:
    def paintWalls(self, cost: list[int], time: list[int]) -> int:
        """
        Minimum cost to paint all walls.
        
        Key insight: 
        If paid painter paints walls with total cost C and total time T,
        then free painter can paint min(T, remaining_walls) walls in parallel.
        
        We need: time_from_paid >= (n - walls_painted_by_paid)
        
        DP State: dp[i][j] = minimum cost to:
        - Consider first i walls
        - Have paid painter work for at least j units of time
        
        Transition:
        - Skip wall i: dp[i+1][j] = min(dp[i+1][j], dp[i][j])
        - Paint with paid painter: dp[i+1][j + time[i]] = min(..., dp[i][j] + cost[i])
        
        Answer: min(dp[n][j]) where j >= n - number_of_walls_painted_by_paid
        But we don't track that explicitly...
        
        Better formulation: 
        dp[i] = minimum cost to have paid painter provide at least i units of time
        
        We iterate through walls, and for each wall, we can choose to add it to paid painter or not.
        """
        n = len(cost)
        
        # dp[i] = minimum cost to get paid painter to work for at least i time
        # We need i >= n for free painter to paint all n walls
        # But actually, we might need less if some walls are painted by paid painter
        
        # Initialize: dp[0] = 0 (no time needed, no cost)
        # dp[i] = infinity for i > 0 initially
        
        # Create DP table with enough space
        # Maximum useful time is n (can cover all walls)
        # But actually could be more, so let's use 2*n to be safe
        max_time = 2 * n
        
        dp = [float('inf')] * (max_time + 1)
        dp[0] = 0
        
        # Process each wall
        for j in range(n):
            # Go backwards to avoid using same wall multiple times
            new_dp = dp.copy()
            
            for t in range(max_time + 1):
                if dp[t] < float('inf'):
                    # Option: use paid painter for wall j
                    new_time = min(t + time[j], max_time)
                    new_cost = dp[t] + cost[j]
                    new_dp[new_time] = min(new_dp[new_time], new_cost)
            
            dp = new_dp
        
        # Now dp[i] = minimum cost to achieve time i from paid painter
        # We need time >= n to ensure all walls can be painted
        # (free painter can paint up to time[paid] walls, and we need to paint n walls total)
        
        # But wait, this doesn't account for the fact that paid painter also paints some walls
        # Let me reconsider...
        
        # If paid painter works for time T and paints walls in set S:
        # - Cost = sum(cost[i] for i in S)
        # - Time = sum(time[i] for i in S) = T
        # - Free painter can paint min(T, n - |S|) walls
        # - Total painted = |S| + min(T, n - |S|)
        # - We need total painted >= n
        # - So min(|S| + T, |S| + n - |S|) >= n
        # - If T >= n - |S|: total = |S| + n - |S| = n ✓
        # - If T < n - |S|: total = |S| + T < n ✗
        # - So we need T >= n - |S|
        
        # In our DP, if we select |S| walls with total time T:
        # - We need T >= n - |S|
        # - As |S| increases, the requirement on T decreases
        # - Maximum |S| = n (all walls), requiring T >= 0
        # - Minimum |S| = 1, requiring T >= n - 1
        
        # The issue is our DP doesn't track |S|
        # Let me add that dimension: dp[num_walls][time]
        
        # Actually, I realize we can solve this differently:
        # Sort by cost/time ratio or some heuristic? No, we need DP.
        
        # Let me redefine: dp[i][j] = min cost to paint exactly i walls with paid painter
        # and have them work for at least j time total
        
        # Simpler: dp[walls][time_balance] where time_balance = time - (n - walls)
        # When time_balance >= 0, all walls can be painted
        
        # Let me implement a cleaner version:
        return self._solve_dp(cost, time, n)
    
    def _solve_dp(self, cost, time, n):
        # dp[walls_count][time_balance] = minimum cost
        # time_balance = total_time - (n - walls_count)
        # When time_balance >= 0, we can paint all walls
        
        # We want to find minimum cost where time_balance >= 0
        
        # Another way: dp[i] = (min_cost, time_sum) when we've selected i walls
        # But we need to track both dimensions
        
        # Let's use: dp[walls][time] = min cost where paid painter paints 'walls' walls
        # and has total time 'time'
        
        # Simpler approach using realization that we want to maximize time per cost
        # (or minimize cost for a given time)
        
        # Use dynamic programming where:
        # dp[remaining_walls] = minimum cost to ensure painted walls >= n - remaining_walls
        # But this is confusing
        
        # Clearest formulation:
        # dp[i] = minimum cost to paint all n walls, where we select walls 0..i-1
        # Track: number of walls painted by paid painter, total time
        
        # Actually, let me use a different approach altogether:
        # For each wall j, track: can we paint all walls if paid painter paints exactly this subset?
        
        # Simplest: dp[j][t] = minimum cost to paint j walls with paid painter with total time t
        # But t can be large
        
        # Let me use DP with state: dp[j][time_available]
        # where time_available = sum of times - (n - j)
        # When time_available >= 0, we're done
        
        # Maximum time available we need to track is n (when we can paint all with free)
        # Actually, let's just track time directly
        
        # Final version: dp[i] = min cost to get at least i units of paid painter time
        # We need at least n units to guarantee painting all walls
        # (unless some are painted by paid painter, but in worst case none are)
        
        # Wait, I think there's a simpler insight:
        # We must paint at least 1 wall with paid painter (otherwise no time for free painter)
        # If paid painter works for time T and paints p walls:
        # - Free painter paints min(T, n - p) walls
        # - We need p + min(T, n - p) >= n
        # - If T >= n - p: p + n - p = n ✓
        # - So we need T >= n - p, or T + p >= n
        
        # So the constraint is: total_time_of_selected_walls + number_of_selected_walls >= n
        
        # DP: dp[k] = minimum cost when (total_time + number_of_walls_selected) >= k
        # We want to find minimum over all k >= n
        
        INF = float('inf')
        m = len(cost)
        
        # dp[gap] = minimum cost where gap = (number of walls - total time of paid painter)
        # When gap <= 0, all walls are painted
        # Initially, gap = n (all walls not painted)
        
        dp = [INF] * (n + 1)
        dp[0] = 0  # gap = 0 means all painted (dummy state)
        
        # Actually, let me track gap = n - (total_time_of_paid)
        # Initially gap = n (need to paint all n walls, paid painter provides 0 time)
        
        dp = [INF] * (n + 1)
        dp[n] = 0  # gap = n, cost = 0 (haven't used paid painter yet)
        
        for i in range(m):
            # Consider wall i
            new_dp = dp.copy()
            
            for gap in range(n, -1, -1):  # gap >= 0
                if dp[gap] < INF:
                    # Add wall i to paid painter
                    # gap decreases by (time[i] - 1)
                    # because we paint 1 more wall (gap decreases by 1)
                    # and gain time[i] (gap decreases by time[i])
                    # net change: gap decreases by (time[i] - (-1)) = time[i] + 1
                    # wait: if gap = n - (total_time_of_paid), then
                    # new_gap = n - (total_time_of_paid + time[i])
                    # delta_gap = gap - new_gap = time[i]
                    # and we also painted 1 more wall, so additional delta = -1
                    # total delta_gap = time[i] - 1
                    # no wait, let me recalculate
                    
                    # gap = n - total_time_of_paid (initially n, decreases as we add walls)
                    # When we add wall i:
                    # new_gap = n - (total_time_of_paid + time[i])
                    #         = (n - total_time_of_paid) - time[i]
                    #         = gap - time[i]
                    # But we also painted 1 wall, so need to account for that
                    # Actually, gap doesn't directly account for paid painter walls
                    
                    # Let me redefine: gap = n - (number_of_walls_painted_by_paid + total_time_of_paid)
                    # Initially: gap = n (nothing painted/worked)
                    # When we add wall i to paid painter:
                    # - number_of_walls_painted_by_paid increases by 1
                    # - total_time_of_paid increases by time[i]
                    # - gap decreases by 1 + time[i]
                    
                    new_gap = gap - (1 + time[i])
                    new_gap = max(new_gap, 0)  # gap can't go below 0 (means all painted)
                    
                    new_cost = dp[gap] + cost[i]
                    new_dp[new_gap] = min(new_dp[new_gap], new_cost)
            
            dp = new_dp
        
        return dp[0]
