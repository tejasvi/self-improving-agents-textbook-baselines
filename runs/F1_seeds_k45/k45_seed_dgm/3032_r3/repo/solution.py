from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        max_value = 0
        
        # Try each starting player
        for x in range(n):
            value = self._calculateFunctionValue(receiver, x, k)
            max_value = max(max_value, value)
        
        return max_value
    
    def _calculateFunctionValue(self, receiver: List[int], start: int, k: int) -> int:
        """
        Calculate f(start) for the given starting player.
        
        The key insight is that since there are only n players, we must enter a cycle
        within n steps. We can detect the cycle and use it to efficiently compute
        the sum for large k values.
        """
        n = len(receiver)
        
        # Track the sequence of players and when we visit them
        visited = {}  # player_id -> step number when first visited
        current = start
        total_sum = start
        
        # Simulate passes until we detect a cycle or reach k passes
        for step in range(k):
            current = receiver[current]
            
            if current in visited:
                # We found a cycle!
                cycle_start_step = visited[current]
                cycle_length = step - cycle_start_step
                
                # How many complete cycles can we fit in the remaining passes?
                remaining_passes = k - step
                complete_cycles = remaining_passes // cycle_length
                remaining_steps = remaining_passes % cycle_length
                
                # Sum of one cycle
                cycle_sum = self._getCycleSum(receiver, current, cycle_length)
                
                # Add complete cycles
                total_sum += complete_cycles * cycle_sum
                
                # Add remaining partial cycle
                temp = current
                for _ in range(remaining_steps):
                    temp = receiver[temp]
                    total_sum += temp
                
                return total_sum
            
            visited[current] = step
            total_sum += current
        
        return total_sum
    
    def _getCycleSum(self, receiver: List[int], start: int, cycle_length: int) -> int:
        """Calculate the sum of one complete cycle starting from 'start'."""
        cycle_sum = 0
        current = start
        for _ in range(cycle_length):
            cycle_sum += current
            current = receiver[current]
        return cycle_sum
