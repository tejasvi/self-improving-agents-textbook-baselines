import sys

def can_see_all_buildings(h, buildings):
    """
    Check if all buildings are visible from (0, h).
    A building i is visible if there's no building j < i that blocks it.
    """
    n = len(buildings)
    for i in range(n):
        x_i, h_i = buildings[i]
        blocked = False
        # Check if building i is blocked by any previous building j
        for j in range(i):
            x_j, h_j = buildings[j]
            # Height of line from (0, h) to top of building i at position x_j
            line_height = h + (h_i - h) * x_j / x_i
            if line_height >= h_j:
                # Building j blocks building i
                blocked = True
                break
        if blocked:
            return False
    return True

def find_blocking_height(i, j, buildings):
    """
    Find the height h such that building j just blocks building i.
    Returns the threshold height where j blocks i.
    At h >= threshold, building j blocks building i.
    """
    x_i, h_i = buildings[i]
    x_j, h_j = buildings[j]
    # h + (h_i - h) * x_j / x_i = h_j
    # h * (1 - x_j/x_i) + h_i * x_j / x_i = h_j
    # h * (x_i - x_j) / x_i = h_j - h_i * x_j / x_i
    # h = (h_j * x_i - h_i * x_j) / (x_i - x_j)
    threshold = (h_j * x_i - h_i * x_j) / (x_i - x_j)
    return threshold

def solve():
    n = int(input())
    buildings = []
    for _ in range(n):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # Check if all buildings are visible at h=0
    if can_see_all_buildings(0, buildings):
        print(-1)
        return
    
    # Find the maximum height at which not all buildings are visible
    # We need to find the minimum blocking height across all buildings
    max_blocking_height = 0
    
    for i in range(1, n):
        # For building i, find what's the maximum height at which it's still blocked
        # Building i can be blocked by any building j < i
        # Find the minimum threshold among all j that can block i
        min_threshold_for_i = float('inf')
        
        for j in range(i):
            threshold = find_blocking_height(i, j, buildings)
            if threshold >= 0:
                min_threshold_for_i = min(min_threshold_for_i, threshold)
        
        # The maximum height at which building i is blocked is just below min_threshold_for_i
        if min_threshold_for_i != float('inf'):
            max_blocking_height = max(max_blocking_height, min_threshold_for_i)
    
    print(max_blocking_height)

solve()
