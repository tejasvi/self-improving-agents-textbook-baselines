from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible value for maximum distance between any two points
        by removing exactly one point.
        
        The key insight is to use the coordinate transformation:
        u = x + y
        v = x - y
        
        Then Manhattan distance |x1-x2| + |y1-y2| = max(|u1-u2|, |v1-v2|)
        
        For each candidate point to remove, we calculate the maximum distance
        as max(max_u - min_u, max_v - min_v) and take the minimum across all choices.
        """
        n = len(points)
        
        # Transform all points to (u, v) coordinates
        transformed = [(x + y, x - y) for x, y in points]
        
        min_result = float('inf')
        
        # Try removing each point
        for i in range(n):
            # Calculate min and max for u and v coordinates without point i
            min_u = float('inf')
            max_u = float('-inf')
            min_v = float('inf')
            max_v = float('-inf')
            
            for j in range(n):
                if i == j:
                    continue
                u, v = transformed[j]
                min_u = min(min_u, u)
                max_u = max(max_u, u)
                min_v = min(min_v, v)
                max_v = max(max_v, v)
            
            # Maximum distance for this configuration
            max_distance = max(max_u - min_u, max_v - min_v)
            min_result = min(min_result, max_distance)
        
        return min_result
