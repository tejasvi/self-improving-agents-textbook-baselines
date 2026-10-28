from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        max_value = 0
        
        # Try each starting player
        for start in range(n):
            value = self.compute_f(start, receiver, k)
            max_value = max(max_value, value)
        
        return max_value
    
    def compute_f(self, start: int, receiver: List[int], k: int) -> int:
        """
        Compute f(start) given the receiver array and k passes.
        Handles the cycle detection to avoid simulating all k steps.
        """
        current = start
        total_sum = start  # Start with the initial player's id
        
        # Track the path: list of (player_id, cumulative_sum)
        path = [(start, start)]
        seen = {start: 0}  # Maps player_id to first occurrence index in path
        
        step = 0
        # Simulate until we find a cycle or complete k steps
        # Since there are only n players, a cycle must occur within n steps
        while step < k and step < n:
            step += 1
            current = receiver[current]
            new_sum = total_sum + current
            
            if current in seen:
                # Found a cycle at position seen[current]
                cycle_start = seen[current]
                cycle_length = step - cycle_start
                
                # Sum in one cycle
                cycle_sum = new_sum - path[cycle_start][1]
                
                # How many more steps after detecting cycle?
                remaining = k - step
                
                # Complete cycles we can fit
                full_cycles = remaining // cycle_length
                partial = remaining % cycle_length
                
                # Current sum + full cycles
                result = new_sum + full_cycles * cycle_sum
                
                # Add partial cycle
                if partial > 0:
                    result += path[cycle_start + partial][1] - path[cycle_start][1]
                
                return result
            
            path.append((current, new_sum))
            seen[current] = step
            total_sum = new_sum
        
        # If we exit the loop without finding a cycle, we completed k steps
        return total_sum
