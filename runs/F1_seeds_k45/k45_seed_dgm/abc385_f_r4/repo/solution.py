# Write your solution here. Read from stdin, write to stdout.

def main():
    n = int(input())
    buildings = []
    for _ in range(n):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # For each building, find the height at which it first becomes invisible
    # (i.e., the minimum height at which a blocking building's line of sight reaches it)
    
    max_blocking_height = -1
    
    for i in range(n):
        target_x, target_h = buildings[i]
        
        # Find the maximum blocking height from all buildings to the left
        max_block_h = -1
        
        for j in range(i):
            block_x, block_h = buildings[j]
            
            # Height at which line from (0, h) to (target_x, target_h) passes through (block_x, block_h)
            # h = (block_h * target_x - target_h * block_x) / (target_x - block_x)
            h_critical = (block_h * target_x - target_h * block_x) / (target_x - block_x)
            
            # Building i is blocked at heights where h <= h_critical
            # (at h=h_critical, the line passes exactly through the blocker's top)
            # (at h < h_critical, the line passes below the blocker's top, so the blocker blocks the view)
            
            if h_critical >= 0:
                max_block_h = max(max_block_h, h_critical)
        
        # Building i is not visible for heights h <= max_block_h
        # So if we want to find the maximum height where not all buildings are visible,
        # we need the maximum of all such max_block_h values
        if max_block_h >= 0:
            max_blocking_height = max(max_blocking_height, max_block_h)
    
    if max_blocking_height < 0:
        # This means all buildings are always visible at non-negative heights
        print(-1)
    else:
        print(f"{max_blocking_height:.18f}")

if __name__ == "__main__":
    main()
