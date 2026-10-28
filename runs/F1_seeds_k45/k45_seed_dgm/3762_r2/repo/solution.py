from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Maximize the minimum game score after at most m moves.
        
        Key insight: Use binary search on the answer.
        For a target minimum score, greedily check if we can visit a contiguous 
        range [0, i] and ensure all positions get at least the target score.
        """
        
        def minMovesToVisit(rightmost: int, points: List[int], target: int) -> int:
            """
            Calculate minimum moves to visit indices [0, rightmost] 
            such that each index gets at least 'target' points.
            Returns the minimum moves.
            """
            # Calculate how many times we need to visit each index
            # to accumulate at least 'target' points
            times_to_visit = []
            for i in range(rightmost + 1):
                times = (target + points[i] - 1) // points[i]  # Ceiling division
                times_to_visit.append(times)
            
            # Minimum moves calculation:
            # - We start at -1
            # - We need to visit each position i in [0, rightmost] exactly times_to_visit[i] times
            # - Each move changes position by 1 and adds points[i] to gameScore[i]
            
            # Optimal strategy: go to rightmost (rightmost+1 moves), 
            # visiting positions 0..rightmost once
            # Then revisit positions that need more visits
            
            total_extra_visits = sum(times_to_visit[i] - 1 for i in range(rightmost + 1))
            
            # Cost: go to rightmost once + cost of extra visits
            # Extra visits: we need to go back and forth, costing 2 moves per extra visit
            moves = (rightmost + 1) + 2 * total_extra_visits
            
            return moves
        
        def canAchieve(target: int) -> bool:
            """
            Check if we can achieve a minimum score of 'target' with m moves.
            Try all possible rightmost indices.
            """
            n = len(points)
            
            for rightmost in range(n):
                moves = minMovesToVisit(rightmost, points, target)
                if moves <= m:
                    return True
            
            return False
        
        # Binary search on the answer
        left, right = 0, sum(points)
        result = 0
        
        while left <= right:
            mid = (left + right) // 2
            if canAchieve(mid):
                result = mid
                left = mid + 1
            else:
                right = mid - 1
        
        return result
