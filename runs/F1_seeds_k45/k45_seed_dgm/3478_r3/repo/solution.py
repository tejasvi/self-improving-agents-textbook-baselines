from typing import List
from collections import deque
import math

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Check if there's a path from (0,0) to (xCorner, yCorner) that:
        - Stays inside the rectangle [0,xCorner] x [0,yCorner]
        - Doesn't touch or enter any circles
        - Only touches the rectangle at the two corners
        
        Key insight: We use BFS to explore the space around circles.
        Two circles "block" each other if one can reach around them.
        We need to check if we can reach from start to end by going around circles.
        """
        
        # Filter out circles that are completely outside and far from the rectangle
        relevant_circles = []
        start = (0, 0)
        end = (xCorner, yCorner)
        
        for x, y, r in circles:
            # Check if circle could possibly block the path
            # It blocks if it's close to any part of the rectangle
            
            # Distance from circle center to the rectangle
            closest_x = max(0, min(x, xCorner))
            closest_y = max(0, min(y, yCorner))
            dist_to_rect = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)
            
            # If circle is far outside, it can't block
            if dist_to_rect >= r:
                # Also check if it blocks the straight line from start to end
                if not self.segment_intersects_circle(start, end, (x, y), r):
                    continue
            
            relevant_circles.append((x, y, r))
        
        # If no relevant circles, path always exists
        if not relevant_circles:
            return True
        
        # Check if start or end is inside any circle
        for x, y, r in relevant_circles:
            if math.sqrt(x*x + y*y) <= r:
                return False
            if math.sqrt((x-xCorner)**2 + (y-yCorner)**2) <= r:
                return False
        
        # Use Union-Find-like approach or BFS to check connectivity
        # Build a graph where we check if circles can be navigated around
        
        n = len(relevant_circles)
        
        # Key insight: Check if we can find a path from start to end
        # by potentially going around intermediate circles
        
        # Use BFS: start -> circles we can go around -> end
        visited = [False] * (n + 2)  # 0: start, 1..n: circles, n+1: end
        queue = deque()
        queue.append(0)  # Start from position 0 (start point)
        visited[0] = True
        
        while queue:
            node = queue.popleft()
            
            if node == n + 1:  # Reached end
                return True
            
            if node == 0:
                # From start, check what circles/end we can reach
                current_pos = start
                
                # Can we reach end directly?
                if self.can_reach_directly(current_pos, end, relevant_circles):
                    return True
                
                # Can we reach around any circle?
                for i in range(n):
                    if not visited[i + 1]:
                        if self.can_pass_around_circle(current_pos, relevant_circles[i]):
                            visited[i + 1] = True
                            queue.append(i + 1)
            
            else:
                # From circle i-1, check what we can reach
                circle_idx = node - 1
                current_circle = relevant_circles[circle_idx]
                current_pos = (current_circle[0], current_circle[1])
                
                # Can we reach end from this circle?
                if self.can_reach_directly(current_pos, end, relevant_circles):
                    return True
                
                # Can we reach other circles?
                for i in range(n):
                    if not visited[i + 1] and i != circle_idx:
                        if not self.circles_overlap_significantly(current_circle, relevant_circles[i]):
                            visited[i + 1] = True
                            queue.append(i + 1)
        
        return False
    
    def segment_intersects_circle(self, p1, p2, center, radius):
        """Check if line segment p1-p2 intersects with circle (with small tolerance)"""
        # Distance from center to line segment
        dist = self.distance_point_to_segment(center, p1, p2)
        # Use a small epsilon for tolerance
        return dist < radius
    
    def distance_point_to_segment(self, p, a, b):
        """Calculate distance from point p to line segment ab"""
        ax, ay = a
        bx, by = b
        px, py = p
        
        # Vector from a to b
        abx = bx - ax
        aby = by - ay
        
        # Vector from a to p
        apx = px - ax
        apy = py - ay
        
        # Project ap onto ab
        ab_sq = abx*abx + aby*aby
        if ab_sq == 0:
            # a and b are the same point
            return math.sqrt(apx*apx + apy*apy)
        
        t = max(0, min(1, (apx*abx + apy*aby) / ab_sq))
        
        # Closest point on segment
        closest_x = ax + t * abx
        closest_y = ay + t * aby
        
        # Distance
        return math.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    
    def can_reach_directly(self, start, end, circles):
        """Check if we can reach from start to end without intersecting any circle"""
        for x, y, r in circles:
            if self.segment_intersects_circle(start, end, (x, y), r):
                return False
        return True
    
    def can_pass_around_circle(self, pos, circle):
        """Check if we can pass around a circle from the given position"""
        x, y, r = circle
        # We can pass if we're far enough from the circle
        dist = math.sqrt((pos[0] - x)**2 + (pos[1] - y)**2)
        # Need to be at least at distance r to pass around
        return dist > r
    
    def circles_overlap_significantly(self, circle1, circle2):
        """Check if two circles overlap/block each other"""
        x1, y1, r1 = circle1
        x2, y2, r2 = circle2
        
        dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        # Circles block if they overlap
        return dist < r1 + r2
