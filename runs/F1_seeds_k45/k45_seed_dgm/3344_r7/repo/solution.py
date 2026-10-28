from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible maximum Manhattan distance after removing exactly one point.
        
        Key insight: Manhattan distance |x1-x2| + |y1-y2| can be transformed to Chebyshev distance:
        max(|(x1+y1)-(x2+y2)|, |(x1-y1)-(x2-y2)|)
        
        The maximum Manhattan distance between any two points equals:
        max(max(x+y) - min(x+y), max(x-y) - min(x-y))
        
        We try removing each point and compute the resulting maximum distance.
        """
        n = len(points)
        
        # Transform points to the new coordinate system
        # For each point (x, y), compute (x+y) and (x-y)
        transformed = [(p[0] + p[1], p[0] - p[1]) for p in points]
        
        min_result = float('inf')
        
        # Try removing each point
        for skip_idx in range(n):
            # Find max and min of (x+y) and (x-y) excluding skip_idx
            max_sum = float('-inf')
            min_sum = float('inf')
            max_diff = float('-inf')
            min_diff = float('inf')
            
            for i in range(n):
                if i == skip_idx:
                    continue
                s, d = transformed[i]
                max_sum = max(max_sum, s)
                min_sum = min(min_sum, s)
                max_diff = max(max_diff, d)
                min_diff = min(min_diff, d)
            
            # Maximum Manhattan distance when skipping this point
            max_distance = max(max_sum - min_sum, max_diff - min_diff)
            min_result = min(min_result, max_distance)
        
        return min_result
