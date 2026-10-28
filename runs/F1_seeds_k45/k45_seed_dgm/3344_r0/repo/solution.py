from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible value for maximum distance between any two points
        by removing exactly one point.
        
        Key insight: Manhattan distance |x1-x2| + |y1-y2| can be transformed to
        Chebyshev distance using coordinates (u, v) = (x+y, x-y).
        
        The maximum Manhattan distance between any two points equals:
        max(max(u) - min(u), max(v) - min(v))
        
        Strategy:
        - Transform each point to (u, v) coordinates
        - For each possible point to remove, calculate max distance in remaining set
        - The max distance is determined by the u and v ranges
        - We only need to check removing each point that lies on the boundary
        """
        n = len(points)
        
        # Transform points to (x+y, x-y) coordinates
        transformed = [(x + y, x - y) for x, y in points]
        
        # Get all u and v values, sorted
        u_vals = sorted([u for u, v in transformed])
        v_vals = sorted([v for u, v in transformed])
        
        # Collect all candidate points to remove
        # We need to check removing points that achieve the current max/min
        candidates = set()
        
        # Find points with extreme u or v values
        min_u_val = u_vals[0]
        max_u_val = u_vals[-1]
        min_v_val = v_vals[0]
        max_v_val = v_vals[-1]
        
        for i, (u, v) in enumerate(transformed):
            if u == min_u_val or u == max_u_val or v == min_v_val or v == max_v_val:
                candidates.add(i)
        
        result = float('inf')
        
        # Try removing each candidate point
        for remove_idx in candidates:
            # Calculate ranges for remaining points
            new_u_vals = [transformed[i][0] for i in range(n) if i != remove_idx]
            new_v_vals = [transformed[i][1] for i in range(n) if i != remove_idx]
            
            if not new_u_vals:  # All points removed (shouldn't happen with n >= 3)
                continue
            
            new_min_u = min(new_u_vals)
            new_max_u = max(new_u_vals)
            new_min_v = min(new_v_vals)
            new_max_v = max(new_v_vals)
            
            max_dist = max(new_max_u - new_min_u, new_max_v - new_min_v)
            result = min(result, max_dist)
        
        return result
