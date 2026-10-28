from typing import List
from collections import deque
import math

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Check if there's a path from (0,0) to (xCorner, yCorner) that:
        1. Stays inside the rectangle
        2. Doesn't touch or enter any circle
        3. Only touches rectangle boundary at corners
        
        Key insight: A circle blocks the path if it touches/enters both:
        - The starting corner (0,0) - within distance r from origin
        - The target corner (xCorner, yCorner) - within distance r from target
        OR if it prevents going around it by being positioned strategically.
        
        We use a graph-based approach:
        - Each circle can potentially block the path
        - Two circles form a "blocking pair" if together they prevent passage
        - We check if all circles together form an insurmountable barrier
        """
        
        # Filter out circles that don't threaten the path
        # A circle threatens the path if it could potentially block passage
        relevant_circles = []
        
        for x, y, r in circles:
            # Check if circle is far enough that it cannot block any path
            # A circle can only block if it's close to the rectangle
            
            # Distance from circle center to the rectangle [0, xCorner] x [0, yCorner]
            # We need to check if circle could intersect with the rectangle interior
            
            # If circle center is outside rectangle and far from all edges, it can't block
            closest_x = max(0, min(x, xCorner))
            closest_y = max(0, min(y, yCorner))
            dist_to_rect = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)
            
            # Circle must be close enough to potentially block
            if dist_to_rect < r:
                relevant_circles.append((x, y, r))
        
        if not relevant_circles:
            return True
        
        # Key insight: A circle blocks the path completely if:
        # - It reaches the start point (0, 0): distance from center to (0,0) <= r
        # - AND it reaches the end point (xCorner, yCorner): distance from center to end <= r
        # OR if multiple circles form a blocking barrier
        
        # Use Union-Find or check if any circle completely separates the corners
        # A circle completely blocks if the diagonal path is cut off
        
        # Check each circle individually first
        for x, y, r in relevant_circles:
            dist_to_start = math.sqrt(x*x + y*y)
            dist_to_end = math.sqrt((x - xCorner)**2 + (y - yCorner)**2)
            
            # If a circle reaches both start and end, it blocks all paths
            if dist_to_start <= r and dist_to_end <= r:
                return False
        
        # For multiple circles, check if they form a blocking configuration
        # Use BFS to check connectivity through circles
        # Treat circles as blocking nodes and check if start and end are separated
        
        # Build adjacency between circles and corners
        def touches_start(x, y, r):
            return math.sqrt(x*x + y*y) <= r
        
        def touches_end(x, y, r):
            return math.sqrt((x - xCorner)**2 + (y - yCorner)**2) <= r
        
        def circles_touch(x1, y1, r1, x2, y2, r2):
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            return dist <= r1 + r2
        
        # Check if start is blocked (reached by all adjacent circles)
        circles_at_start = [i for i in range(len(relevant_circles)) 
                          if touches_start(relevant_circles[i][0], relevant_circles[i][1], relevant_circles[i][2])]
        
        circles_at_end = [i for i in range(len(relevant_circles))
                        if touches_end(relevant_circles[i][0], relevant_circles[i][1], relevant_circles[i][2])]
        
        # BFS to check if circles at start connect to circles at end
        if not circles_at_start or not circles_at_end:
            # If no circle reaches start or no circle reaches end, path exists
            return True
        
        # BFS from circles at start to see if we can reach circles at end
        visited = set(circles_at_start)
        queue = deque(circles_at_start)
        
        while queue:
            i = queue.popleft()
            if i in circles_at_end:
                # Connected path of circles from start to end
                return False
            
            x1, y1, r1 = relevant_circles[i]
            for j in range(len(relevant_circles)):
                if j not in visited:
                    x2, y2, r2 = relevant_circles[j]
                    if circles_touch(x1, y1, r1, x2, y2, r2):
                        visited.add(j)
                        queue.append(j)
                        if j in circles_at_end:
                            return False
        
        return True
