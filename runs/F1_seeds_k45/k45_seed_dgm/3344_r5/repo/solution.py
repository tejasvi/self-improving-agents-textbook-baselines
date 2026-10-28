from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible maximum distance between any two points
        after removing exactly one point.
        
        Key insight: Transform Manhattan distance to Chebyshev distance
        Manhattan distance |x1-x2| + |y1-y2| = max(|(x1+y1)-(x2+y2)|, |(x1-y1)-(x2-y2)|)
        
        So we can work with two transformed dimensions:
        - u = x + y
        - v = x - y
        
        The maximum distance is the maximum of the range in u and range in v.
        To minimize this, we try removing each point and compute the max distance.
        """
        n = len(points)
        
        # Transform points to (u, v) coordinates
        transformed = []
        for x, y in points:
            u = x + y
            v = x - y
            transformed.append((u, v))
        
        min_max_distance = float('inf')
        
        # Try removing each point
        for removed_idx in range(n):
            # Find the ranges in u and v dimensions after removing the point
            u_values = []
            v_values = []
            
            for i in range(n):
                if i != removed_idx:
                    u, v = transformed[i]
                    u_values.append(u)
                    v_values.append(v)
            
            # The maximum distance is the max of the ranges
            u_range = max(u_values) - min(u_values)
            v_range = max(v_values) - min(v_values)
            max_distance = max(u_range, v_range)
            
            # Update the minimum of all maximum distances
            min_max_distance = min(min_max_distance, max_distance)
        
        return min_max_distance
