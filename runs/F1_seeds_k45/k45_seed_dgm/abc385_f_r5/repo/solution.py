# Write your solution here. Read from stdin, write to stdout.

def solve():
    N = int(input())
    buildings = []
    for _ in range(N):
        x, h = map(int, input().split())
        buildings.append((x, h))
    
    # Check if we can see all buildings from height 0
    max_height_blocked = -1
    
    # For each building, calculate the line from (0, h) through its top (x, H)
    # The slope of this line is (H - h) / x
    # At position x', the line has height: h + (H - h) * x' / x = h + (H - h) * x' / x
    
    # For building i, find the maximum height from which building i is not visible
    # Building i is blocked by some building j < i if the line through building i
    # intersects building j
    
    for i in range(N):
        x_i, h_i = buildings[i]
        
        # Find the maximum height at which building i is blocked by previous buildings
        max_blocking_height = -1
        
        for j in range(i):
            x_j, h_j = buildings[j]
            
            # Line from (0, h) through (x_i, h_i) has equation:
            # y = h + (h_i - h) * x / x_i
            
            # At position x_j, this line has height:
            # y_j = h + (h_i - h) * x_j / x_i
            
            # This line intersects building j (which has height h_j) if:
            # y_j < h_j
            # h + (h_i - h) * x_j / x_i < h_j
            # (h_i - h) * x_j / x_i < h_j - h
            # h_i * x_j / x_i - h * x_j / x_i < h_j - h
            # h_i * x_j / x_i - h_j < h * x_j / x_i - h
            # h_i * x_j / x_i - h_j < h * (x_j / x_i - 1)
            # h_i * x_j / x_i - h_j < h * (x_j - x_i) / x_i
            
            # If x_j < x_i (which is true since j < i):
            # h_i * x_j - h_j * x_i < h * (x_j - x_i)
            # Since x_j - x_i < 0:
            # h > (h_i * x_j - h_j * x_i) / (x_j - x_i)
            # h > (h_j * x_i - h_i * x_j) / (x_i - x_j)
            
            # So building i is blocked by building j when:
            # h > (h_j * x_i - h_i * x_j) / (x_i - x_j)
            
            # The maximum height at which i is blocked by j:
            h_critical = (h_j * x_i - h_i * x_j) / (x_i - x_j)
            
            # Building i is blocked by j if h <= h_critical and h_critical >= 0
            if h_critical >= 0:
                max_blocking_height = max(max_blocking_height, h_critical)
        
        if max_blocking_height >= 0:
            max_height_blocked = max(max_height_blocked, max_blocking_height)
    
    if max_height_blocked == -1:
        print(-1)
    else:
        print(max_height_blocked)

solve()
