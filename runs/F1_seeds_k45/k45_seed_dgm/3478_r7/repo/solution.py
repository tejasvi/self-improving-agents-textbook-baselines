from typing import List
import math
from collections import deque

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Check if there's a path from (0,0) to (xCorner, yCorner) that doesn't touch any circles.
        
        Key insights:
        1. Filter out circles that are clearly not blocking (too far away)
        2. Check if remaining circles form a barrier that blocks all paths
        3. A circle can only block if its distance to origin or target is smaller than some threshold
        """
        
        # Filter circles: keep only those that could potentially block the path
        # A circle blocks if it's close enough to either the start or end point
        relevant_circles = []
        
        for x, y, r in circles:
            # Distance from circle center to origin (0, 0)
            dist_to_origin = math.sqrt(x*x + y*y)
            
            # Distance from circle center to corner (xCorner, yCorner)
            dist_to_corner = math.sqrt((x - xCorner)**2 + (y - yCorner)**2)
            
            # A circle is relevant if it's close enough to origin or corner
            # We need to be careful about the threshold
            # If a circle's center is more than its radius away from both origin and corner,
            # we need to check if it can block the diagonal path
            
            # More careful: a circle blocks if:
            # - It overlaps with origin or corner area (dist <= r), OR
            # - It's positioned such that going around it requires leaving the rectangle
            
            # Check distance to the line from (0,0) to (xCorner, yCorner)
            # Distance from point (x, y) to line from (0,0) to (xCorner, yCorner):
            # Line equation: yCorner * x - xCorner * y = 0
            # Distance = |yCorner * x - xCorner * y| / sqrt(xCorner^2 + yCorner^2)
            
            line_dist = abs(yCorner * x - xCorner * y) / math.sqrt(xCorner*xCorner + yCorner*yCorner)
            
            # A circle is relevant if:
            # 1. It blocks the origin (close enough)
            # 2. It blocks the corner (close enough)
            # 3. It blocks the direct path (close to the line and has large enough radius)
            
            # Check if circle blocks origin
            if dist_to_origin <= r:
                return False
            
            # Check if circle blocks corner
            if dist_to_corner <= r:
                return False
            
            # Check if circle could block the path
            # The circle is relevant if it's close to the diagonal line
            if line_dist < r:
                # Check if the circle is positioned between origin and corner on the line
                # Project center onto line: parameter t = (x*xCorner + y*yCorner) / (xCorner^2 + yCorner^2)
                t = (x * xCorner + y * yCorner) / (xCorner*xCorner + yCorner*yCorner)
                
                # Circle is relevant if projection is between 0 and 1 (or close to it)
                if -0.5 <= t <= 1.5:  # Be generous with the range
                    relevant_circles.append((x, y, r))
        
        if not relevant_circles:
            return True
        
        # Now check if relevant circles form a barrier
        # Use graph approach: two circles are "adjacent" if they overlap or touch
        # If we can find a path from origin to corner that doesn't get blocked by connected circles
        
        # Alternative approach: check if any circle (or group of connected circles)
        # completely blocks the path
        
        # Check if a single circle or connected group blocks all possible paths
        # A circle blocks if no path can go around it (both upper and lower paths blocked)
        
        # For each circle, check if we can go around it
        return self._check_path_exists(xCorner, yCorner, relevant_circles)
    
    def _check_path_exists(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Check if path exists using BFS on circle "blocks"
        Two circles block the path if they're close enough together
        """
        if not circles:
            return True
        
        # Build a graph of circles
        n = len(circles)
        
        # For each circle, check if it completely blocks the path
        # A circle blocks if we must enter it to reach the corner
        
        # Key insight: if we need to go around a circle, we need to move away from diagonal
        # A circle completely blocks the path if:
        # - It blocks the path so far that going around it would mean exiting the rectangle
        
        # Check using Union-Find or graph connectivity
        # Two circles are "touching/blocking" if they're close enough
        
        # Use BFS starting from "unblocked region near origin" to "unblocked region near corner"
        # Alternatively: check for each circle if it's truly blocking
        
        for i, (cx, cy, r) in enumerate(circles):
            # Check if this circle or connected circle group blocks the path
            if self._is_blocking_group(xCorner, yCorner, circles, i):
                return False
        
        return True
    
    def _is_blocking_group(self, xCorner: int, yCorner: int, circles: List[List[int]], start_idx: int) -> bool:
        """
        Check if a connected group of circles (starting from start_idx) blocks the path
        """
        # Find all connected circles using BFS
        visited = set()
        queue = deque([start_idx])
        visited.add(start_idx)
        group = []
        
        while queue:
            idx = queue.popleft()
            cx, cy, cr = circles[idx]
            group.append((cx, cy, cr))
            
            # Find nearby circles
            for j, (nx, ny, nr) in enumerate(circles):
                if j not in visited:
                    dist = math.sqrt((cx - nx)**2 + (cy - ny)**2)
                    # If circles are close enough, they're in the same blocking group
                    if dist <= cr + nr:
                        visited.add(j)
                        queue.append(j)
        
        # Check if this group blocks the path
        # A group blocks if going around it would exit the rectangle
        return self._group_blocks_path(xCorner, yCorner, group)
    
    def _group_blocks_path(self, xCorner: int, yCorner: int, group: List[tuple]) -> bool:
        """
        Check if a group of connected circles blocks the path from (0,0) to (xCorner, yCorner)
        """
        # Find the bounding circle/region of the group
        # Check if we can go around the group
        
        # For a group to block the path, it must:
        # 1. Touch both the upper and lower boundaries, OR
        # 2. Touch both the left and right boundaries, OR
        # 3. Form a connected barrier from one corner region to another
        
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for cx, cy, cr in group:
            min_x = min(min_x, cx - cr)
            max_x = max(max_x, cx + cr)
            min_y = min(min_y, cy - cr)
            max_y = max(max_y, cy + cr)
        
        # The group blocks if it touches top and bottom OR left and right
        # or more precisely: if going around it requires exiting the rectangle
        
        # Check if group blocks bottom (y=0) and top (y=yCorner)
        blocks_y = (min_y <= 0 and max_y >= yCorner)
        
        # Check if group blocks left (x=0) and right (x=xCorner)  
        blocks_x = (min_x <= 0 and max_x >= xCorner)
        
        # If it blocks both dimensions, no path exists
        if blocks_y and blocks_x:
            return True
        
        # More sophisticated check: even if not blocking both dimensions,
        # the group might still block the diagonal path
        
        # Check if all paths around the group must exit the rectangle
        # This is the case if the group forms a "barrier" from one corner to another
        
        # For now, the two-dimension check should be sufficient
        # But we might need to add more sophisticated checks
        
        return False
