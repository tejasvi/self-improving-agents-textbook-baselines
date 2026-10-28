from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        """
        For each starting player x, calculate f(x) = x + sum of k receivers.
        
        Key insights:
        1. k can be up to 10^10, so we can't simulate directly
        2. Since there are only n players, a path must eventually cycle
        3. We can detect the cycle and use it to compute the sum efficiently
        
        Approach:
        - For each starting player, follow the path until we either:
          a) Complete k passes
          b) Detect a cycle
        - If we detect a cycle before k passes, we can calculate the contribution
          from the cycle and the remainder
        """
        n = len(receiver)
        max_value = 0
        
        for start in range(n):
            value = self._compute_f(start, receiver, k)
            max_value = max(max_value, value)
        
        return max_value
    
    def _compute_f(self, start: int, receiver: List[int], k: int) -> int:
        """
        Compute f(start) = start + sum of k passes from start.
        """
        total = start
        current = start
        visited = {}  # Maps position to (step, cumulative_sum)
        step = 0
        cumulative_sum = 0
        
        # Follow the path until we either:
        # 1. Complete k passes
        # 2. Detect a cycle
        while step < k:
            if current in visited:
                # We found a cycle
                cycle_start_step, cycle_start_sum = visited[current]
                cycle_length = step - cycle_start_step
                cycle_sum = cumulative_sum - cycle_start_sum
                
                # How many passes are left after reaching this point
                remaining_passes = k - step
                
                # How many complete cycles can we fit in the remaining passes
                complete_cycles = remaining_passes // cycle_length
                remainder = remaining_passes % cycle_length
                
                # Add contribution from complete cycles
                total += complete_cycles * cycle_sum
                
                # Add contribution from remainder passes
                current = start
                for i in range(cycle_start_step + remainder):
                    current = receiver[current]
                    total += current
                
                return total
            
            visited[current] = (step, cumulative_sum)
            current = receiver[current]
            cumulative_sum += current
            step += 1
        
        # If we completed k passes without finding a cycle
        total += cumulative_sum
        return total
