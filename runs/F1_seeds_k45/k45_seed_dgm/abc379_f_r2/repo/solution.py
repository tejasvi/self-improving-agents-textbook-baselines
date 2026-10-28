def can_see_from(start, end, heights):
    """
    Find all buildings visible from building at index 'start' 
    to buildings at indices > start (up to end if specified)
    """
    n = len(heights)
    visible = set()
    
    for j in range(start + 1, n):
        # Check if building j can be seen from building start
        # It can be seen if no building between start and j is taller than heights[j]
        can_see = True
        for k in range(start + 1, j):
            if heights[k] > heights[j]:
                can_see = False
                break
        if can_see:
            visible.add(j)
    
    return visible

# Read input
n, q = map(int, input().split())
heights = [0] + list(map(int, input().split()))  # 1-indexed

# Process queries
for _ in range(q):
    l, r = map(int, input().split())
    
    # Find buildings visible from l
    visible_from_l = can_see_from(l, n, heights)
    
    # Find buildings visible from r
    visible_from_r = can_see_from(r, n, heights)
    
    # Find buildings to the east of r
    buildings_to_east = set(range(r + 1, n + 1))
    
    # Count buildings visible from both l and r, and to the east of r
    answer = len((visible_from_l & visible_from_r) & buildings_to_east)
    
    print(answer)
