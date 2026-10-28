from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible value for maximum distance between any two points 
        by removing exactly one point.
        
        The key insight is to use coordinate transformation:
        For points (x, y), we transform to (u, v) where:
        - u = x + y
        - v = x - y
        
        The Manhattan distance between two points equals the Chebyshev distance
        in the transformed space, which is max(|u1 - u2|, |v1 - v2|).
        
        The maximum Manhattan distance in a set is:
        max(max_u - min_u, max_v - min_v)
        """
        n = len(points)
        
        # Transform all points
        transformed = [(x + y, x - y) for x, y in points]
        
        # Find the top 2 max and min values for both dimensions
        u_vals = [u for u, v in transformed]
        v_vals = [v for u, v in transformed]
        
        # Sort to get top 2 max and min
        u_sorted = sorted(u_vals)
        v_sorted = sorted(v_vals)
        
        # Get the two largest and two smallest values
        u_max1, u_max2 = u_sorted[-1], u_sorted[-2]
        u_min1, u_min2 = u_sorted[0], u_sorted[1]
        
        v_max1, v_max2 = v_sorted[-1], v_sorted[-2]
        v_min1, v_min2 = v_sorted[0], v_sorted[1]
        
        min_result = float('inf')
        
        # Try removing each point
        for i in range(n):
            u, v = transformed[i]
            
            # Determine the new max and min for u dimension after removing point i
            if u == u_max1:
                # If this is the max, we need to check if it's the only max
                if u_vals.count(u_max1) == 1:
                    new_u_range = u_max2 - (u_min1 if u != u_min1 else u_min2)
                else:
                    new_u_range = u_max1 - (u_min1 if u != u_min1 else u_min2)
            elif u == u_min1:
                # If this is the min, we need to check if it's the only min
                if u_vals.count(u_min1) == 1:
                    new_u_range = (u_max1 if u != u_max1 else u_max2) - u_min2
                else:
                    new_u_range = (u_max1 if u != u_max1 else u_max2) - u_min1
            else:
                # This point is neither max nor min
                new_u_range = u_max1 - u_min1
            
            # Determine the new max and min for v dimension after removing point i
            if v == v_max1:
                # If this is the max, we need to check if it's the only max
                if v_vals.count(v_max1) == 1:
                    new_v_range = v_max2 - (v_min1 if v != v_min1 else v_min2)
                else:
                    new_v_range = v_max1 - (v_min1 if v != v_min1 else v_min2)
            elif v == v_min1:
                # If this is the min, we need to check if it's the only min
                if v_vals.count(v_min1) == 1:
                    new_v_range = (v_max1 if v != v_max1 else v_max2) - v_min2
                else:
                    new_v_range = (v_max1 if v != v_max1 else v_max2) - v_min1
            else:
                # This point is neither max nor min
                new_v_range = v_max1 - v_min1
            
            # The maximum distance after removing this point
            max_distance = max(new_u_range, new_v_range)
            min_result = min(min_result, max_distance)
        
        return min_result
