from typing import List

class Solution:
    def canReachCorner(self, xCorner: int, yCorner: int, circles: List[List[int]]) -> bool:
        """
        Check if we can reach the corner (xCorner, yCorner) from (0, 0)
        while avoiding circles.
        
        Key insight: A path exists if and only if there is no connected component
        of circles that forms a complete barrier from one side to another.
        
        A circle is relevant if it could potentially block the path - i.e., if
        removing it would make a difference. We use Union-Find to detect if
        circles form a barrier.
        """
        
        # Check if start or end is blocked
        for x, y, r in circles:
            # Check if origin (0, 0) is inside any circle
            if x*x + y*y < r*r:
                return False
            # Check if target is inside any circle
            if (x-xCorner)**2 + (y-yCorner)**2 < r*r:
                return False
        
        # Filter relevant circles using Union-Find approach
        # A circle is relevant if it might block the passage
        
        # Create a super-source and super-sink
        # super-source represents the origin area, super-sink represents target area
        # Circles that are "close to" origin are connected to source
        # Circles that are "close to" target are connected to sink
        # If a path exists from source to sink through circles, they block the way
        
        # Use Union-Find
        parent = {}
        
        def find(x):
            if x not in parent:
                parent[x] = x
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Initialize source and sink
        source = "source"
        sink = "sink"
        find(source)
        find(sink)
        
        # Maximum distance threshold - circles farther than this won't matter
        # The diagonal of the rectangle is the farthest we need to consider
        max_threshold = (xCorner**2 + yCorner**2)**0.5
        threshold = max_threshold + max(xCorner, yCorner)
        
        filtered_circles = []
        for x, y, r in circles:
            dist_to_origin = (x*x + y*y)**0.5
            dist_to_target = ((x-xCorner)**2 + (y-yCorner)**2)**0.5
            
            # A circle matters if it's reasonably close to the rectangle
            if dist_to_origin < r + threshold or dist_to_target < r + threshold:
                filtered_circles.append((x, y, r, len(filtered_circles)))
        
        # Check which circles are close to origin or target
        for x, y, r, idx in filtered_circles:
            dist_to_origin = (x*x + y*y)**0.5
            dist_to_target = ((x-xCorner)**2 + (y-yCorner)**2)**0.5
            
            # If circle is close to origin, connect it to source
            if dist_to_origin < r + threshold:
                union(source, idx)
            
            # If circle is close to target, connect it to sink
            if dist_to_target < r + threshold:
                union(idx, sink)
        
        # Connect circles that are close to each other
        for i in range(len(filtered_circles)):
            x1, y1, r1, idx1 = filtered_circles[i]
            for j in range(i + 1, len(filtered_circles)):
                x2, y2, r2, idx2 = filtered_circles[j]
                
                dist_between = ((x1-x2)**2 + (y1-y2)**2)**0.5
                # Circles are close if they overlap or are close enough to block together
                if dist_between <= r1 + r2:
                    union(idx1, idx2)
        
        # If source and sink are connected, circles form a barrier
        return find(source) != find(sink)
