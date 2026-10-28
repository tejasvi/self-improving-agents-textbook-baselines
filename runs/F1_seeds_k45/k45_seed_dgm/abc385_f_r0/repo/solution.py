import sys
from math import inf

def solve():
    n = int(input())
    buildings = []
    for _ in range(n):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # For each building i, find the maximum height from which it's not visible
    # A building i is blocked by building j if the line of sight from (0, h)
    # to any point on building i passes through building j
    
    # The critical insight: building i becomes visible at height h if the line
    # from (0, h) through the top of some blocking building j reaches above building i
    
    # For building i to be just visible (grazing building j):
    # The line from (0, h) through (X_j, H_j) should reach height H_i at X_i
    # h + (H_j - h) / X_j * X_i = H_i
    # Solving for h:
    # h + (H_j - h) * X_i / X_j = H_i
    # h * (1 - X_i/X_j) + H_j * X_i / X_j = H_i
    # h * (X_j - X_i) / X_j = H_i - H_j * X_i / X_j
    # h = (H_i * X_j - H_j * X_i) / (X_j - X_i)
    
    # Since X_j < X_i (buildings are sorted by position), denominator is negative
    # h = (H_i * X_j - H_j * X_i) / (X_j - X_i)
    
    max_blocked_height = 0.0
    
    for i in range(n):
        # For building i, find what blocks it
        target_x, target_h = buildings[i]
        
        # The maximum height at which building i is blocked
        critical_heights = []
        
        for j in range(i):
            block_x, block_h = buildings[j]
            # Height at which line through (block_x, block_h) reaches target
            h_critical = (target_h * block_x - block_h * target_x) / (block_x - target_x)
            critical_heights.append(h_critical)
        
        if critical_heights:
            # Building i is visible if we're above the maximum critical height
            # So it's blocked if we're at or below the maximum critical height
            h_blocked = max(critical_heights)
            if h_blocked > max_blocked_height:
                max_blocked_height = h_blocked
    
    # Check if all buildings are visible at height 0
    if max_blocked_height <= 0:
        print(-1)
    else:
        print(f"{max_blocked_height:.18f}")

solve()
