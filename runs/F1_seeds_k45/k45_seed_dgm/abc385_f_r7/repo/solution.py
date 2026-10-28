# Write your solution here. Read from stdin, write to stdout.

def is_building_visible(observer_h, building_idx, buildings):
    """Check if a building is visible from (0, observer_h)"""
    x_target, h_target = buildings[building_idx]
    
    # Check if any other building blocks the view
    for j, (x_j, h_j) in enumerate(buildings):
        if j == building_idx:
            continue
        
        # Line from (0, observer_h) to (x_target, h_target)
        # At position x_j, the line has height:
        # observer_h + (h_target - observer_h) * x_j / x_target
        
        line_height_at_j = observer_h + (h_target - observer_h) * x_j / x_target
        # Building j blocks if it reaches above the line
        if h_j > line_height_at_j:
            return False
    
    return True


def all_buildings_visible(observer_h, buildings):
    """Check if all buildings are visible from (0, observer_h)"""
    for i in range(len(buildings)):
        if not is_building_visible(observer_h, i, buildings):
            return False
    return True


def solve():
    n = int(input())
    buildings = []
    for _ in range(n):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # Check if all buildings are visible at height 0
    if all_buildings_visible(0, buildings):
        print(-1)
        return
    
    # Binary search for the maximum height where not all buildings are visible
    # At left, not all visible; at right, all visible
    left, right = 0.0, 10**10
    
    # Find the point where all_buildings_visible becomes True
    for _ in range(200):  # Binary search iterations
        mid = (left + right) / 2
        if all_buildings_visible(mid, buildings):
            # All buildings visible at mid, so answer is <= mid
            right = mid
        else:
            # Not all visible at mid, so answer is >= mid
            left = mid
    
    result = left
    print(f"{result:.18f}")


solve()
