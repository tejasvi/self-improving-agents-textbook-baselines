from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible value for maximum distance between any two points
        by removing exactly one point.
        
        Key insight: Manhattan distance between (x1,y1) and (x2,y2) is |x1-x2| + |y1-y2|
        This equals max(|u1-u2|, |v1-v2|) where u=x+y and v=x-y (Chebyshev distance)
        
        Strategy:
        1. Transform each point using u=x+y, v=x-y
        2. For each point removed, the max distance is max(max_u - min_u, max_v - min_v)
        3. We need to efficiently find max/min u and v when each point is removed
        """
        n = len(points)
        
        # Transform points to (u, v) coordinates where u = x+y, v = x-y
        transformed = [(x + y, x - y) for x, y in points]
        
        # For each dimension, we need to track the two largest and two smallest values
        # to handle cases where the extreme point is removed
        
        # Get all u and v values
        u_values = [u for u, v in transformed]
        v_values = [v for u, v in transformed]
        
        # Sort to find extremes
        u_sorted = sorted(u_values)
        v_sorted = sorted(v_values)
        
        # The extreme ranges (without considering which point to remove)
        u_range = u_sorted[-1] - u_sorted[0]
        v_range = v_sorted[-1] - v_sorted[0]
        
        min_max_distance = float('inf')
        
        # Try removing each point
        for i in range(n):
            u_removed, v_removed = transformed[i]
            
            # Calculate max and min u values when point i is removed
            if u_removed == u_sorted[-1] and u_sorted[-1] == u_sorted[-2]:
                # Max u appears multiple times, removing one doesn't change it
                max_u = u_sorted[-1]
            elif u_removed == u_sorted[-1]:
                # Remove the maximum u
                max_u = u_sorted[-2]
            else:
                # Removing a non-maximum point
                max_u = u_sorted[-1]
            
            if u_removed == u_sorted[0] and u_sorted[0] == u_sorted[1]:
                # Min u appears multiple times
                min_u = u_sorted[0]
            elif u_removed == u_sorted[0]:
                # Remove the minimum u
                min_u = u_sorted[1]
            else:
                # Removing a non-minimum point
                min_u = u_sorted[0]
            
            # Calculate max and min v values when point i is removed
            if v_removed == v_sorted[-1] and v_sorted[-1] == v_sorted[-2]:
                # Max v appears multiple times
                max_v = v_sorted[-1]
            elif v_removed == v_sorted[-1]:
                # Remove the maximum v
                max_v = v_sorted[-2]
            else:
                # Removing a non-maximum point
                max_v = v_sorted[-1]
            
            if v_removed == v_sorted[0] and v_sorted[0] == v_sorted[1]:
                # Min v appears multiple times
                min_v = v_sorted[0]
            elif v_removed == v_sorted[0]:
                # Remove the minimum v
                min_v = v_sorted[1]
            else:
                # Removing a non-minimum point
                min_v = v_sorted[0]
            
            # Maximum distance when point i is removed
            max_distance = max(max_u - min_u, max_v - min_v)
            min_max_distance = min(min_max_distance, max_distance)
        
        return min_max_distance
