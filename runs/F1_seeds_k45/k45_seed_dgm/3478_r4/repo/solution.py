from typing import List
import math

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Determine if there's a path from (0,0) to (xCorner, yCorner) avoiding circles.
        
        Key insight: Use Union-Find to group overlapping circles, then check if any
        connected component of circles blocks the path.
        
        A connected component blocks the path if it forms a continuous barrier from
        one boundary to another that prevents passage between the two corners.
        """
        
        # Filter circles that are irrelevant (too far from the rectangle to affect anything)
        relevant_circles = []
        for x, y, r in circles:
            # Check if circle could possibly intersect with any path in the rectangle
            # A circle is relevant if it intersects or is very close to the rectangle
            if self._is_relevant(x, y, r, xCorner, yCorner):
                relevant_circles.append((x, y, r))
        
        if not relevant_circles:
            return True
        
        # Use Union-Find to group overlapping/touching circles
        n = len(relevant_circles)
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
                if self._circles_overlap(relevant_circles[i], relevant_circles[j]):
                    union(i, j)
        
        # Group circles by connected component
        components = {}
        for i in range(n):
            root = find(i)
            if root not in components:
                components[root] = []
            components[root].append(relevant_circles[i])
        
        # Check if any component blocks the path
        for component in components.values():
            if self._component_blocks(component, xCorner, yCorner):
                return False
        
        return True
    
    def _is_relevant(self, cx, cy, r, xCorner, yCorner):
        """
        Check if a circle is relevant - i.e., could affect whether we can reach the corner.
        A circle is relevant if it's close enough to the rectangle to potentially block.
        """
        # Find closest point on rectangle to circle center
        closest_x = max(0, min(cx, xCorner))
        closest_y = max(0, min(cy, yCorner))
        
        # Distance from circle center to closest point on rectangle
        dist = math.sqrt((cx - closest_x) ** 2 + (cy - closest_y) ** 2)
        
        # Circle is relevant if it intersects or touches the rectangle
        return dist <= r
    
    def _circles_overlap(self, circle1, circle2):
        """Check if two circles overlap or touch."""
        x1, y1, r1 = circle1
        x2, y2, r2 = circle2
        dist_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return dist_sq <= (r1 + r2) ** 2
    
    def _component_blocks(self, circles, xCorner, yCorner):
        """
        Check if a connected component of circles blocks the path from (0,0) to (xCorner, yCorner).
        
        A component blocks if it forms a barrier that separates the two corners.
        We use the approach of checking if the component spans from one edge to another
        in a way that blocks all paths.
        """
        
        if not circles:
            return False
        
        # Check 1: If either corner is inside a circle, that circle block the path immediately
        # (since the corner itself must be reachable)
        for cx, cy, r in circles:
            dist_to_origin = math.sqrt(cx ** 2 + cy ** 2)
            dist_to_corner = math.sqrt((xCorner - cx) ** 2 + (yCorner - cy) ** 2)
            
            # If origin is inside the circle, it blocks
            if dist_to_origin < r:
                # Actually, origin is at (0,0) which is a corner, so this can't happen in valid input
                # But corner (xCorner, yCorner) could be inside
                pass
            
            # If the target corner is inside this circle, we can't reach it
            if dist_to_corner < r:
                return True
        
        # Check 2: Compute the extent of the circle component
        # and check if it forms a barrier
        min_x = min(cx - r for cx, cy, r in circles)
        max_x = max(cx + r for cx, cy, r in circles)
        min_y = min(cy - r for cx, cy, r in circles)
        max_y = max(cy + r for cx, cy, r in circles)
        
        # Clamp to rectangle bounds for analysis
        min_x = max(0, min_x)
        max_x = min(xCorner, max_x)
        min_y = max(0, min_y)
        max_y = min(yCorner, max_y)
        
        # The component potentially blocks if it spans both horizontally and vertically
        # AND there's no clear gap
        
        # Check if circles extend across the entire rectangle width or height
        circles_touch_left = any(cx - r <= 0 for cx, cy, r in circles)
        circles_touch_right = any(cx + r >= xCorner for cx, cy, r in circles)
        circles_touch_bottom = any(cy - r <= 0 for cx, cy, r in circles)
        circles_touch_top = any(cy + r >= yCorner for cx, cy, r in circles)
        
        # Component blocks if it touches opposite sides completely
        if circles_touch_left and circles_touch_right and circles_touch_bottom and circles_touch_top:
            # Could still be a gap, need more detailed check
            return self._check_detailed_block(circles, xCorner, yCorner)
        
        if (circles_touch_left and circles_touch_right) or (circles_touch_bottom and circles_touch_top):
            # Might block, do detailed check
            return self._check_detailed_block(circles, xCorner, yCorner)
        
        return False
    
    def _check_detailed_block(self, circles, xCorner, yCorner):
        """
        Detailed check if circles form a barrier.
        Uses the concept of checking if we can find a path around the circles.
        """
        
        # Strategy: Check multiple potential paths and see if circles block all of them
        # We check: straight diagonal, path hugging bottom edge, path hugging right edge, etc.
        
        paths = [
            # Diagonal path
            [(t * xCorner, t * yCorner) for t in [0, 0.25, 0.5, 0.75, 1.0]],
            # Path along bottom then right
            [(t * xCorner, 0) for t in [0, 0.5, 1.0]] + [(xCorner, t * yCorner) for t in [0.25, 0.5, 0.75, 1.0]],
            # Path along left then top  
            [(0, t * yCorner) for t in [0, 0.5, 1.0]] + [(t * xCorner, yCorner) for t in [0.25, 0.5, 0.75, 1.0]],
        ]
        
        for path in paths:
            if self._path_is_clear(path, circles):
                return False
        
        # If we couldn't find a clear path, circles block
        return True
    
    def _path_is_clear(self, path_points, circles):
        """
        Check if a path (represented as points) is clear of all circles.
        For simplicity, we check if we can find a route through the intermediate points
        without colliding with circles.
        """
        
        # Check if any point on the path is inside any circle
        for px, py in path_points:
            inside_circle = False
            for cx, cy, r in circles:
                dist = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
                if dist < r:
                    inside_circle = True
                    break
            
            if inside_circle:
                return False
        
        # Also check if line segments between consecutive points intersect circles
        for i in range(len(path_points) - 1):
            p1 = path_points[i]
            p2 = path_points[i + 1]
            
            for cx, cy, r in circles:
                if self._line_segment_intersects_circle(p1, p2, (cx, cy), r):
                    return False
        
        return True
    
    def _line_segment_intersects_circle(self, p1, p2, circle_center, radius):
        """Check if a line segment intersects with a circle."""
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = circle_center
        
        # Vector from p1 to p2
        dx = x2 - x1
        dy = y2 - y1
        
        # Vector from p1 to circle center
        fx = x1 - cx
        fy = y1 - cy
        
        # Solve for closest point on line segment
        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - radius * radius
        
        # If segment has zero length
        if a == 0:
            return c <= 0
        
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False
        
        discriminant = math.sqrt(discriminant)
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)
        
        # Check if intersection occurs within segment [0, 1]
        if (0 <= t1 <= 1) or (0 <= t2 <= 1) or (t1 < 0 and t2 > 1):
            return True
        
        return False
