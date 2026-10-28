from typing import List
import math

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Check if there's a path from (0,0) to (xCorner, yCorner) that avoids all circles.
        
        Key insight: We need to check if any circle completely blocks the path.
        A circle blocks the path if it separates (0,0) from (xCorner, yCorner).
        
        The diagonal distance from (0,0) to (xCorner, yCorner) is sqrt(xCorner^2 + yCorner^2).
        
        A circle with center (x, y) and radius r blocks the path if:
        - It's positioned such that any path from (0,0) to (xCorner, yCorner) must pass through it.
        
        We can use a Union-Find approach or check if circles can collectively block all paths.
        
        Better approach: Use geometry. A circle blocks all paths if:
        - dist((x,y), (0,0)) - r <= 0 OR dist((x,y), (xCorner, yCorner)) - r <= 0 
          (circle touches/contains a corner - impossible path)
        - OR: dist((x,y), (0,0)) + dist((x,y), (xCorner, yCorner)) - 2*r <= diagonal distance
          (circle is on all possible paths)
        """
        
        # Filter circles that are relevant (might affect path)
        # A circle is irrelevant if it's far from the rectangle
        relevant_circles = []
        
        for x, y, r in circles:
            # Check if circle is completely outside the rectangle
            if x + r < 0 or x - r > xCorner or y + r < 0 or y - r > yCorner:
                continue
            
            # Check distance to (0, 0)
            dist_to_start = math.sqrt(x*x + y*y)
            # Check distance to (xCorner, yCorner)
            dist_to_end = math.sqrt((x - xCorner)**2 + (y - yCorner)**2)
            
            # Only keep circles that could potentially block the path
            # A circle can block if it reaches both towards (0,0) and towards (xCorner, yCorner)
            if dist_to_start - r < 0 or dist_to_end - r < 0:
                # Circle contains or touches a corner - path is blocked
                return False
            
            # Keep circles that are close enough to potentially block
            # The diagonal distance
            diagonal = math.sqrt(xCorner*xCorner + yCorner*yCorner)
            
            # A circle is relevant if: dist_to_start + dist_to_end - 2*r <= diagonal
            # This means the circle might be on all possible paths
            if dist_to_start + dist_to_end - 2*r <= diagonal:
                relevant_circles.append((x, y, r))
        
        # If we have no relevant circles, path exists
        if not relevant_circles:
            return True
        
        # Build a graph where nodes are:
        # - start node (0, 0)
        # - end node (xCorner, yCorner)  
        # - relevant circles
        # Two circles are connected if we can go around them together
        # (i.e., they don't completely separate paths)
        
        # Use Union-Find to check connectivity
        # Start and end are connected if there's a path avoiding all circles
        
        n = len(relevant_circles)
        parent = list(range(n + 2))  # n circles + start + end
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        start_idx = n
        end_idx = n + 1
        
        # Check if start can reach end directly (no circles blocking)
        diagonal = math.sqrt(xCorner*xCorner + yCorner*yCorner)
        all_blocked = True
        
        for i, (x, y, r) in enumerate(relevant_circles):
            dist_to_start = math.sqrt(x*x + y*y)
            dist_to_end = math.sqrt((x - xCorner)**2 + (y - yCorner)**2)
            
            # If this circle doesn't completely block the diagonal, we might go around it
            if dist_to_start + dist_to_end - 2*r > diagonal:
                all_blocked = False
                break
        
        if not all_blocked:
            return True
        
        # All single circles block the path, but can we go around multiple circles?
        # Check if circles form a barrier
        
        # More precise check: 
        # For each circle, check the minimum distance to the path
        for x, y, r in relevant_circles:
            # Distance from circle center to the line from (0,0) to (xCorner, yCorner)
            # Using point-to-line distance formula
            # Line: y/x = yCorner/xCorner, or yCorner*x - xCorner*y = 0
            
            if xCorner == 0 or yCorner == 0:
                # Edge case (shouldn't happen based on constraints)
                distance_to_line = float('inf')
            else:
                # Distance from (x, y) to line yCorner*X - xCorner*Y = 0
                distance_to_line = abs(yCorner * x - xCorner * y) / math.sqrt(xCorner*xCorner + yCorner*yCorner)
            
            # If circle doesn't reach the line, it doesn't block
            if distance_to_line > r:
                return True
        
        # All circles block the straight-line path, but we need to check if we can go around
        # by moving along the rectangle edges
        
        # Check distance to corners
        for x, y, r in relevant_circles:
            dist_to_start = math.sqrt(x*x + y*y)
            dist_to_end = math.sqrt((x - xCorner)**2 + (y - yCorner)**2)
            
            # If circle doesn't reach a corner, we can go around via that corner
            if dist_to_start > r or dist_to_end > r:
                return True
        
        # No path found
        return False
