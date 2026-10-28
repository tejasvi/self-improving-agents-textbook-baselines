# Write your solution here. Read from stdin, write to stdout.

def can_see_from(heights, i, j):
    """Check if building j can be seen from building i (i < j)"""
    if i >= j:
        return False
    # Check if there's no building taller than heights[j] between i and j
    for k in range(i + 1, j):
        if heights[k] > heights[j]:
            return False
    return True

def solve():
    # Read input
    n, q = map(int, input().split())
    heights = list(map(int, input().split()))
    
    # Process queries
    for _ in range(q):
        l, r = map(int, input().split())
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        count = 0
        # Check all buildings to the east of r
        for k in range(r + 1, n):
            # Check if building k can be seen from both l and r
            visible_from_l = can_see_from(heights, l, k)
            visible_from_r = can_see_from(heights, r, k)
            
            if visible_from_l and visible_from_r:
                count += 1
        
        print(count)

solve()
