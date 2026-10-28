from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Find the maximum possible minimum value in gameScore after at most m moves.
        
        Strategy:
        1. Binary search on the answer (the minimum value we want to achieve)
        2. For each candidate answer, check if it's achievable within m moves
        3. To check if a target is achievable:
           - Try all possible contiguous ranges [left, right]
           - For each range, calculate minimum moves needed to make all elements >= target
           - If any range can be done in <= m moves, the target is achievable
        """
        n = len(points)
        
        def can_achieve(target):
            """Check if we can make all gameScores >= target within m moves"""
            
            # Try all possible contiguous ranges
            for left in range(n):
                for right in range(left, n):
                    moves_needed = calculate_min_moves(left, right, target)
                    if moves_needed <= m:
                        return True
            return False
        
        def calculate_min_moves(left, right, target):
            """
            Calculate minimum moves needed to make all indices in [left, right] >= target.
            We start at -1 and need to visit indices multiple times if needed.
            """
            # For each index, calculate how many times we need to visit it
            visits_needed = []
            for i in range(left, right + 1):
                times_needed = (target + points[i] - 1) // points[i]  # ceil division
                visits_needed.append(times_needed)
            
            # Now calculate the minimum moves to visit all these positions with required counts
            # Start from -1, need to visit each position in [left, right] v[i] times
            
            # The optimal strategy is to traverse back and forth
            # Pattern: -1 -> left -> right -> left -> right ...
            
            dist_to_left = left + 1  # From -1 to left
            dist_range = right - left  # Distance from left to right
            
            # Maximum visits needed at any position
            max_visits = max(visits_needed)
            
            # Minimum moves strategy:
            # Go to left position, then oscillate between left and right
            # Number of full oscillations = max_visits - 1
            # Cost = dist_to_left + dist_range + (max_visits - 1) * 2 * dist_range
            
            moves = dist_to_left + dist_range + (max_visits - 1) * 2 * dist_range
            
            return moves
        
        # Binary search for the answer
        left_search = 0
        right_search = sum(points)  # Upper bound on achievable minimum
        
        result = 0
        
        # Use binary search for efficiency
        while left_search <= right_search:
            mid = (left_search + right_search) // 2
            if can_achieve(mid):
                result = mid
                left_search = mid + 1
            else:
                right_search = mid - 1
        
        return result
