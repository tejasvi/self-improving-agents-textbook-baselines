from typing import List
import math

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Binary search on the answer combined with a greedy checking function.
        
        For each candidate minimum value, we check if it's achievable with at most m moves.
        To achieve a minimum value of 'target', each index i needs ceil(target / points[i]) visits.
        
        The optimal strategy is to visit a contiguous subarray and move back and forth.
        For a subarray [left, right], the minimum moves needed is:
        - Go from -1 to right and back to left (or vice versa)
        - Plus extra moves to make additional visits
        """
        
        def can_achieve(target: int) -> bool:
            """Check if we can achieve minimum score of 'target' with at most m moves."""
            n = len(points)
            
            # Calculate required visits for each index
            visits = [math.ceil(target / points[i]) for i in range(n)]
            
            # Try all possible contiguous subarrays [left, right]
            # We need to visit at least one element
            for left in range(n):
                for right in range(left, n):
                    # Check if we can visit indices [left, right] with required visits
                    # Starting from index -1
                    
                    # Sum of visits in the range
                    total_visits = sum(visits[i] for i in range(left, right + 1))
                    
                    # If we only need 1 visit per index and they're adjacent
                    # Moves = distance from -1 to right + (distance back and forth if needed)
                    
                    # Strategy 1: Go to left first, then sweep to right
                    # Moves: (-1 to left) + (left to right) + extra for revisits
                    moves1 = (left + 1) + (right - left) + (total_visits - (right - left + 1)) * 2
                    
                    # The logic is:
                    # - First, reach the range and distribute visits
                    # - We visit each index at least once
                    # - For additional visits, we move back and forth (costs 2 per visit)
                    
                    # Actually, let's think differently:
                    # To visit indices [left, right]:
                    # - Starting from -1, go to left: costs (left + 1) moves
                    # - From left, go to right: costs (right - left) moves
                    # - Now we've used (left + 1) + (right - left) = (right + 1) moves
                    # - We've visited each index once
                    # - For extra visits, we need to oscillate
                    
                    # Optimal oscillation: if we need k extra visits in total,
                    # we oscillate between left and right, costing 2 per extra visit
                    
                    extra_visits = total_visits - (right - left + 1)
                    if extra_visits < 0:
                        continue
                    
                    # Strategy: reach the rightmost point first, then come back
                    moves_right_first = 2 * (right + 1) + extra_visits * 2
                    
                    # Strategy: reach the leftmost point first, then go right, come back
                    moves_left_first = 2 * (left + 1) + (right - left) + extra_visits * 2
                    
                    moves_needed = min(moves_right_first, moves_left_first)
                    
                    if moves_needed <= m:
                        return True
            
            return False
        
        # Binary search on the answer
        left, right = 0, sum(points)
        
        while left < right:
            mid = (left + right + 1) // 2
            if can_achieve(mid):
                left = mid
            else:
                right = mid - 1
        
        return left
