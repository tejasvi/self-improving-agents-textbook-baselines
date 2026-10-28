def solve():
    n = int(input())
    buildings = []
    for _ in range(n):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # Check if all buildings are visible from (0, 0)
    # A building is visible from (0, 0) if the line from (0, 0) to (x_i, h_i)
    # doesn't intersect the top of any previous building
    
    def is_visible_from_height(height):
        """Check if all buildings are visible from (0, height)"""
        # For each building, check if it's visible
        for i in range(n):
            x_i, h_i = buildings[i]
            visible = False
            
            # Check if there's any point on building i visible from (0, height)
            # The top of building i at (x_i, h_i) is definitely on the building
            # Check if the line from (0, height) to (x_i, h_i) hits any previous building
            
            # A point on building i is at (x_i, y) where 0 <= y <= h_i
            # The line from (0, height) to (x_i, y) has equation:
            # Y = height + (y - height) * X / x_i
            
            # For the top of the building (x_i, h_i):
            hit_something = False
            for j in range(i):
                x_j, h_j = buildings[j]
                # Check if line from (0, height) to (x_i, h_i) passes through or above (x_j, h_j)
                # At x = x_j, the line has height: height + (h_i - height) * x_j / x_i
                line_height_at_j = height + (h_i - height) * x_j / x_i
                if line_height_at_j < h_j:
                    hit_something = True
                    break
            
            if not hit_something:
                visible = True
            
            if not visible:
                return False
        
        return True
    
    if is_visible_from_height(0):
        print(-1)
        return
    
    # Binary search for the maximum height from which not all buildings are visible
    left, right = 0.0, 2e9
    
    for _ in range(100):  # Enough iterations for convergence
        mid = (left + right) / 2
        if is_visible_from_height(mid):
            right = mid
        else:
            left = mid
    
    print(f"{left:.18f}")

solve()
