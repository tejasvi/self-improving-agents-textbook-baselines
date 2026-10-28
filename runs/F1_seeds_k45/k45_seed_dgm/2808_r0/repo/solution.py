from typing import List

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """
        DP solution for painting walls.
        
        Simplified approach:
        - dp[i] = minimum cost to paint i walls
        - We track: (walls_by_paid, total_time_by_paid) for each configuration
        - But we only care about: can we paint n walls?
        
        Even simpler DP:
        - dp[i][j] = minimum cost to paint i walls, where j = total_time - i (excess)
        - We only process each wall once
        """
        n = len(cost)
        INF = float('inf')
        
        # dp[i][j] = min cost to achieve state: painted i walls with paid painter,
        # excess time j = sum(time) - i
        # We cap j at n to keep the state space manageable
        
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        
        # For each wall
        for c, t in zip(cost, time):
            # New DP table for this iteration
            new_dp = [[INF] * (n + 1) for _ in range(n + 1)]
            
            # Copy existing states (not using this wall)
            for i in range(n + 1):
                for j in range(n + 1):
                    new_dp[i][j] = min(new_dp[i][j], dp[i][j])
            
            # Update states by using this wall with paid painter
            for i in range(n):
                for j in range(n + 1):
                    if dp[i][j] == INF:
                        continue
                    
                    # Add this wall with paid painter
                    new_i = i + 1
                    new_j_exact = j + t - 1  # new excess = old excess + time - 1
                    new_j = min(new_j_exact, n)  # Cap at n
                    
                    new_dp[new_i][new_j] = min(new_dp[new_i][new_j], dp[i][j] + c)
            
            dp = new_dp
        
        # Find minimum cost
        result = INF
        for i in range(n + 1):
            for j in range(n + 1):
                # Check if we can paint n walls total
                # i walls painted by paid, n-i walls painted by free
                # Constraint: j >= n - 2*i
                if j >= n - 2 * i and dp[i][j] != INF:
                    result = min(result, dp[i][j])
        
        return result
