from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        """
        Maximize the minimum value in gameScore using binary search.
        
        We binary search on the answer (minimum score) and for each candidate,
        check if we can achieve it within m moves using a greedy approach.
        """
        
        def canAchieve(minScore):
            """
            Check if we can achieve minScore for all visited indices within m moves.
            We try visiting indices from 0 to k for each k from 0 to n-1.
            For each k, calculate minimum moves needed.
            """
            n = len(points)
            
            # Try visiting indices [0, rightmost]
            for rightmost in range(n):
                movesNeeded = calculateMoves(rightmost, minScore)
                if movesNeeded <= m:
                    return True
            
            return False
        
        def calculateMoves(rightmost, minScore):
            """
            Calculate minimum moves to ensure all indices [0, rightmost]
            have at least minScore.
            
            Strategy: Start at -1, move right to rightmost, then backtrack
            and revisit indices as needed.
            """
            n = len(points)
            
            # Calculate how many times we need to visit each index
            visits = [0] * (rightmost + 1)
            
            # Calculate minimum visits needed for each index
            for i in range(rightmost + 1):
                # We need points[i] * visits[i] >= minScore
                visits[i] = (minScore + points[i] - 1) // points[i]  # ceiling division
            
            # Optimal strategy: move right to rightmost, accumulating visits
            # Then backtrack if needed to ensure all positions are visited enough times
            
            # Calculate total moves needed
            # We go from -1 to rightmost, which takes rightmost + 1 moves
            # But we may need to go back and forth to visit each index multiple times
            
            # The key insight: we want to visit each index the required number of times
            # The minimum moves is when we efficiently use back-and-forth movement
            
            # Simple calculation: 
            # - Go from -1 to rightmost: rightmost + 1 moves
            # - For each index i, if we visit it visits[i] times, we get visits[i] * points[i] score
            # - But the first pass gives us each index 1 visit, so we need visits[i] - 1 additional visits
            # - Additional visits require going back to that index
            
            totalMoves = rightmost + 1  # Initial move to reach rightmost
            
            # Now we need to go back and revisit indices that need more points
            # The most efficient way is to alternate between the minimum index needing revisit
            # and the rightmost index
            
            # Actually, let's think differently:
            # We need to make sure each index i in [0, rightmost] is visited visits[i] times
            # The minimum moves to do this is:
            # - Go from -1 to rightmost (rightmost + 1 moves, each index visited once)
            # - Then go back and forth between any index needing more visits and rightmost
            
            # Calculate excess visits needed
            excessVisits = sum(max(0, visits[i] - 1) for i in range(rightmost + 1))
            
            # To get these excess visits optimally:
            # We go from -1 -> rightmost (rightmost + 1 moves)
            # Then we oscillate between leftmost index needing excess and rightmost
            # Cost of oscillation: 2 * distance for each excess visit
            
            # Find leftmost index that needs excess visits
            minIndexNeedingExcess = rightmost
            for i in range(rightmost + 1):
                if visits[i] > 1:
                    minIndexNeedingExcess = i
                    break
            
            # Cost to get all excess visits
            oscillationCost = excessVisits * 2 * (rightmost - minIndexNeedingExcess)
            
            return totalMoves + oscillationCost
        
        # Binary search on the answer
        left, right = 0, sum(points)
        
        while left < right:
            mid = (left + right + 1) // 2
            if canAchieve(mid):
                left = mid
            else:
                right = mid - 1
        
        return left
