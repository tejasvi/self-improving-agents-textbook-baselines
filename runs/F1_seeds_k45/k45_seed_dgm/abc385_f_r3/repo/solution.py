def can_see_all_buildings(buildings, view_height):
    """
    Check if from height view_height at coordinate 0, all buildings are visible.
    buildings: list of (x, h) tuples sorted by x
    Returns True if all buildings are visible, False otherwise
    """
    n = len(buildings)
    if n == 0:
        return True
    
    # For each building, check if it's blocked by previous ones
    for i in range(n):
        x_i, h_i = buildings[i]
        
        # Check if building i can be seen
        # The top of building i is at (x_i, h_i)
        
        # Check if line from (0, view_height) to (x_i, h_i) clears all previous buildings
        is_blocked = False
        for j in range(i):
            x_j, h_j = buildings[j]
            # Height of line from (0, view_height) to (x_i, h_i) at position x_j
            line_height_at_j = view_height + (h_i - view_height) * x_j / x_i
            # If line is at or below the top of building j, it's blocked
            if line_height_at_j <= h_j:
                is_blocked = True
                break
        
        if is_blocked:
            return False
    
    return True


def find_max_height():
    """Find the maximum height from which not all buildings are visible."""
    n = int(input())
    buildings = []
    for _ in range(n):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # Check if at height 0, all buildings are visible
    if can_see_all_buildings(buildings, 0):
        print(-1)
        return
    
    # Binary search for the maximum height where at least one building is invisible
    # As height increases, more buildings become visible
    # We want the largest height where at least one building is NOT visible
    
    low = 0.0
    high = 2e9  # Upper bound
    
    # Binary search for the answer
    for _ in range(100):  # Sufficient iterations for precision
        mid = (low + high) / 2
        if can_see_all_buildings(buildings, mid):
            # At mid height, all buildings are visible
            # So the answer is below mid
            high = mid
        else:
            # At mid height, at least one building is not visible
            # So the answer is at or above mid
            low = mid
    
    answer = (low + high) / 2
    print(f"{answer:.18f}")


if __name__ == "__main__":
    find_max_height()
