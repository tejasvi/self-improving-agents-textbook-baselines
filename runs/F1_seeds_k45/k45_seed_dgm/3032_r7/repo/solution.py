from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        """
        Find the maximum value of f(x) where:
        f(x) = x + sum of all IDs of players who receive the ball in k passes
        
        Using Binary Lifting (Jump Pointers) approach:
        - Since k can be very large (10^10), we can't simulate each step
        - We precompute jumps for powers of 2: 1, 2, 4, 8, ..., 2^log_k
        - For each starting position, we use the precomputed jumps to quickly
          reach the final position after k steps
        """
        n = len(receiver)
        
        # Determine the maximum power of 2 we need
        # log2(10^10) ≈ 34, so we need arrays of size ~35
        max_pow = 40  # Safe upper bound
        
        # next[i][j] = position after jumping 2^j steps from position i
        # sum_jump[i][j] = sum of node IDs visited in 2^j steps from position i
        next_pos = [[0] * max_pow for _ in range(n)]
        sum_jump = [[0] * max_pow for _ in range(n)]
        
        # Base case: 2^0 = 1 step
        for i in range(n):
            next_pos[i][0] = receiver[i]
            sum_jump[i][0] = receiver[i]
        
        # Build the jump table for 2^1, 2^2, ..., 2^(max_pow-1) steps
        for j in range(1, max_pow):
            for i in range(n):
                # After 2^(j-1) steps from i, we're at next_pos[i][j-1]
                # Then we jump another 2^(j-1) steps from there
                mid = next_pos[i][j-1]
                next_pos[i][j] = next_pos[mid][j-1]
                sum_jump[i][j] = sum_jump[i][j-1] + sum_jump[mid][j-1]
        
        # Compute f(x) for each starting position x
        max_value = 0
        
        for start in range(n):
            # Calculate f(start) = start + sum of receivers for k passes
            current_sum = start
            current_pos = start
            remaining = k
            
            # Greedily use the largest jumps we can make
            for j in range(max_pow - 1, -1, -1):
                if remaining >= (1 << j):  # Can we jump 2^j steps?
                    current_sum += sum_jump[current_pos][j]
                    current_pos = next_pos[current_pos][j]
                    remaining -= (1 << j)
            
            max_value = max(max_value, current_sum)
        
        return max_value
