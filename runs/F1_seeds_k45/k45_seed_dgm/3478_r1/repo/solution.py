from typing import List
import math


class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Determine if there's a path from (0, 0) to (xCorner, yCorner) that avoids all circles.
        
        Strategy: Use Union-Find to group circles that touch/overlap. 
        A connected component blocks the path if it's reachable from both corners
        simultaneously (i.e., the sum of closest distances equals 0).
        """
        
        # Filter out circles that are definitely not blocking
        # A circle can only block if it's not entirely outside the rectangle
        filtered = []
        for x, y, r in circles:
            # Circle is inside or touching the rectangle boundaries
            if not (x + r < 0 or x - r > xCorner or y + r < 0 or y - r > yCorner):
                filtered.append((x, y, r))
        
        if not filtered:
            return True
        
        n = len(filtered)
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Union circles that overlap or touch
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1, r1 = filtered[i]
                x2, y2, r2 = filtered[j]
                dist_sq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
                sum_r = r1 + r2
                # Check if circles touch or overlap (using squared distances to avoid sqrt)
                if dist_sq <= sum_r * sum_r:
                    union(i, j)
        
        # Group circles by component
        components = {}
        for i in range(n):
            root = find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)
        
        # Check if any component blocks the path
        for indices in components.values():
            # Calculate minimum distance from (0, 0) to this component
            min_dist_start = float('inf')
            for i in indices:
                x, y, r = filtered[i]
                center_dist = math.sqrt(x * x + y * y)
                closest_dist = max(0, center_dist - r)
                min_dist_start = min(min_dist_start, closest_dist)
            
            # Calculate minimum distance from (xCorner, yCorner) to this component
            min_dist_end = float('inf')
            for i in indices:
                x, y, r = filtered[i]
                center_dist = math.sqrt((x - xCorner) ** 2 + (y - yCorner) ** 2)
                closest_dist = max(0, center_dist - r)
                min_dist_end = min(min_dist_end, closest_dist)
            
            # If component touches both corners, it blocks the path
            if min_dist_start < 1e-9 and min_dist_end < 1e-9:
                return False
        
        return True
