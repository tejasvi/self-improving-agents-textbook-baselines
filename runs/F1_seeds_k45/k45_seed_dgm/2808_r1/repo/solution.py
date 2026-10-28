class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """
        Minimum cost to paint all n walls.
        
        Key insight: If paid painter paints k walls with total time T,
        free painter can paint (n-k) walls in that time T.
        We need: T >= n - k  (free painter has enough time)
        
        Strategy: 
        1. Sort walls by (cost - time) ratio - walls with high time and low cost 
           are better for paid painter (we want to use paid painter to buy time)
        2. Use DP: dp[i][j] = (min_cost, total_time) to paint i walls with j paid painter walls
        """
        n = len(cost)
        
        # Create list of (cost, time) pairs and sort by cost - time
        walls = sorted(zip(cost, time), key=lambda x: x[0] - x[1])
        
        # dp[i][j] = minimum cost to paint first i walls using exactly j paid painter walls
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        time_sum = [[0] * (n + 1) for _ in range(n + 1)]
        
        dp[0][0] = 0
        time_sum[0][0] = 0
        
        for i in range(1, n + 1):
            c, t = walls[i - 1]
            
            for j in range(i + 1):
                # Option 1: Paint wall i with free painter (j stays the same)
                if j <= i - 1 and dp[i - 1][j] < INF:
                    if dp[i - 1][j] < dp[i][j]:
                        dp[i][j] = dp[i - 1][j]
                        time_sum[i][j] = time_sum[i - 1][j]
                
                # Option 2: Paint wall i with paid painter (j increases)
                if j > 0 and j - 1 <= i - 1 and dp[i - 1][j - 1] < INF:
                    new_cost = dp[i - 1][j - 1] + c
                    new_time = time_sum[i - 1][j - 1] + t
                    if new_cost < dp[i][j]:
                        dp[i][j] = new_cost
                        time_sum[i][j] = new_time
        
        # Find answer: min cost where paid painter's time >= free painter's walls
        ans = INF
        for j in range(n + 1):
            if dp[n][j] < INF:
                # j walls painted by paid painter
                # n - j walls painted by free painter
                paid_time = time_sum[n][j]
                free_walls = n - j
                
                if paid_time >= free_walls:
                    ans = min(ans, dp[n][j])
        
        return ans
