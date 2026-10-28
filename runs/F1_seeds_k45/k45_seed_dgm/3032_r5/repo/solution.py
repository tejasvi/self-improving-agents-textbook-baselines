from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        """
        Find the maximum value of f(x) where f(x) = x + sum of k passes.
        
        Since k can be very large (up to 10^10), we can't simulate all passes naively.
        Key insight: Since there are only n players, eventually we'll enter a cycle.
        
        We use binary lifting to efficiently compute the sum:
        - For each player, precompute: next[i][j] = player we reach after 2^j passes from player i
        - Also precompute: sum[i][j] = sum of players visited in 2^j passes from player i
        """
        n = len(receiver)
        max_power = 40  # 2^40 > 10^10
        
        # next[i][j] = player reached after 2^j passes starting from player i
        # sum[i][j] = sum of players visited in 2^j passes starting from player i
        next_player = [[0] * max_power for _ in range(n)]
        path_sum = [[0] * max_power for _ in range(n)]
        
        # Base case: 2^0 = 1 pass
        for i in range(n):
            next_player[i][0] = receiver[i]
            path_sum[i][0] = receiver[i]
        
        # Build binary lifting table
        for j in range(1, max_power):
            for i in range(n):
                # After 2^j passes, we first do 2^(j-1) passes, then another 2^(j-1) passes
                mid = next_player[i][j-1]
                next_player[i][j] = next_player[mid][j-1]
                path_sum[i][j] = path_sum[i][j-1] + path_sum[mid][j-1]
        
        # Try each starting player
        max_value = 0
        
        for start in range(n):
            current = start
            total_sum = start
            remaining = k
            
            # Use binary lifting to compute the sum of k passes
            for j in range(max_power - 1, -1, -1):
                if remaining >= (1 << j):  # If we can do 2^j passes
                    total_sum += path_sum[current][j]
                    current = next_player[current][j]
                    remaining -= (1 << j)
            
            max_value = max(max_value, total_sum)
        
        return max_value
