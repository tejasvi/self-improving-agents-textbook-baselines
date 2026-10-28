from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        """
        Find the maximum value of f(x) where f(x) = x + sum of k passes from x.
        
        Since k can be very large, we need to detect cycles in the passing sequence.
        Once a cycle is detected, we can calculate the contribution efficiently.
        """
        n = len(receiver)
        max_value = 0
        
        # Try each player as a starting point
        for start in range(n):
            value = self._calculate_f(start, receiver, k)
            max_value = max(max_value, value)
        
        return max_value
    
    def _calculate_f(self, start: int, receiver: List[int], k: int) -> int:
        """
        Calculate f(start) with cycle detection.
        
        We follow the chain and detect when we revisit a node.
        Once we find a cycle, we can calculate contributions from:
        1. Linear part (before entering cycle)
        2. Cycle part (repeated as needed)
        """
        chain = []  # Store the sequence of players the ball passes to
        visited = {}  # Map from player ID to index in chain where they first appear
        
        current = start
        total = start  # Start with the initial player's ID
        
        # Build the chain until we find a cycle or reach k passes
        for i in range(k):
            if current in visited:
                # We've found a cycle!
                cycle_start_idx = visited[current]
                cycle_length = i - cycle_start_idx
                
                # How many complete cycles can we fit in the remaining passes?
                remaining_passes = k - i
                complete_cycles = remaining_passes // cycle_length
                remainder = remaining_passes % cycle_length
                
                # Sum of one complete cycle
                cycle_sum = sum(chain[cycle_start_idx:i])
                
                # Add contribution from complete cycles
                total += complete_cycles * cycle_sum
                
                # Add contribution from the remaining passes
                for j in range(remainder):
                    idx = cycle_start_idx + j
                    total += chain[idx]
                
                return total
            
            visited[current] = i
            next_player = receiver[current]
            chain.append(next_player)
            total += next_player
            current = next_player
        
        # If we reach here, we completed k passes without finding a cycle
        return total
