from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible maximum Manhattan distance after removing one point.
        
        Key insight: Manhattan distance |x1-x2| + |y1-y2| can be expressed as:
        max(|(x1+y1) - (x2+y2)|, |(x1-y1) - (x2-y2)|)
        
        By transforming to (u, v) where u = x+y and v = x-y,
        we convert the problem to finding max Chebyshev distance.
        The max Chebyshev distance = max(u_max - u_min, v_max - v_min)
        """
        # Transform points to (u, v) coordinates
        transformed = []
        for x, y in points:
            u = x + y
            v = x - y
            transformed.append((u, v))
        
        # We need to try removing each point and find the minimum max distance
        min_result = float('inf')
        
        for skip_idx in range(len(transformed)):
            # Find min/max u and v after removing point at skip_idx
            u_min = float('inf')
            u_max = float('-inf')
            v_min = float('inf')
            v_max = float('-inf')
            
            for i, (u, v) in enumerate(transformed):
                if i == skip_idx:
                    continue
                u_min = min(u_min, u)
                u_max = max(u_max, u)
                v_min = min(v_min, v)
                v_max = max(v_max, v)
            
            # Maximum distance for remaining points
            max_dist = max(u_max - u_min, v_max - v_min)
            min_result = min(min_result, max_dist)
        
        return min_result
