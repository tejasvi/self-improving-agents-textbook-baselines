def can_see_all_buildings(buildings, h):
    """Check if all buildings are visible from (0, h)"""
    n = len(buildings)
    
    for i in range(n):
        x_i, h_i = buildings[i]
        
        # For building i to be visible, we need to find a point Q on it
        # such that the line from (0, h) to Q doesn't intersect any building j < i
        
        # The minimum height required on building i to see it
        threshold = h
        
        for j in range(i):
            x_j, h_j = buildings[j]
            # Line from (0, h) to (x_i, q) at position x_j has height:
            # h + (q - h) * x_j / x_i
            # For this not to intersect building j: h + (q - h) * x_j / x_i > h_j
            # Solving for q: q > h + (h_j - h) * x_i / x_j
            min_q = h + (h_j - h) * x_i / x_j
            threshold = max(threshold, min_q)
        
        # Building i is visible iff there exists q in (threshold, h_i]
        # This is possible iff h_i > threshold
        if h_i <= threshold:
            return False
    
    return True


def solve():
    n = int(input())
    buildings = []
    for _ in range(n):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # Check if all buildings are visible at height 0
    if can_see_all_buildings(buildings, 0.0):
        print("-1")
        return
    
    # Binary search for the maximum height where not all buildings are visible
    # Invariant: left = height where not all are visible
    #           right = height where all are visible
    left = 0.0
    right = 2.0 * 10**9
    
    for _ in range(100):
        mid = (left + right) / 2.0
        if can_see_all_buildings(buildings, mid):
            # All buildings visible at mid, so answer is <= mid
            right = mid
        else:
            # Not all buildings visible at mid, so answer is >= mid
            left = mid
    
    # Answer is the boundary where not all visible transitions to all visible
    answer = (left + right) / 2.0
    print(f"{answer:.18f}")


solve()
