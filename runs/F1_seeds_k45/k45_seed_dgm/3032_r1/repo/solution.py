from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        max_value = 0
        
        # Try each starting player
        for start in range(n):
            value = self._compute_f(start, receiver, k)
            max_value = max(max_value, value)
        
        return max_value
    
    def _compute_f(self, start: int, receiver: List[int], k: int) -> int:
        """
        Compute f(start) for the given starting player.
        f(start) = start + receiver[start] + receiver[receiver[start]] + ... (k times)
        """
        # Track the sequence of players and their cumulative sums
        current = start
        total_sum = start
        visited = {}  # player -> (pass_number, cumulative_sum_at_this_point)
        
        for pass_num in range(1, k + 1):
            # Check if we've seen this player before (cycle detection)
            if current in visited:
                cycle_start_pass, cycle_start_sum = visited[current]
                cycle_length = pass_num - cycle_start_pass
                cycle_sum = total_sum - cycle_start_sum
                
                remaining_passes = k - pass_num + 1
                complete_cycles = remaining_passes // cycle_length
                remaining_after_cycles = remaining_passes % cycle_length
                
                # Add complete cycles
                total_sum += complete_cycles * cycle_sum
                
                # Add remaining passes
                current = start
                for i in range(cycle_start_pass - 1):
                    current = receiver[current]
                
                for i in range(remaining_after_cycles):
                    current = receiver[current]
                    total_sum += current
                
                return total_sum
            
            visited[current] = (pass_num, total_sum)
            current = receiver[current]
            total_sum += current
        
        return total_sum
