def can_see(heights, from_pos, to_pos):
    """Check if building at to_pos can be seen from from_pos"""
    if from_pos >= to_pos:
        return False
    
    target_height = heights[to_pos]
    # Check all buildings between from_pos and to_pos
    for k in range(from_pos + 1, to_pos):
        if heights[k] > target_height:
            return False
    return True


def solve():
    # Read input
    n, q = map(int, input().split())
    heights = list(map(int, input().split()))
    
    # Process each query
    for _ in range(q):
        l, r = map(int, input().split())
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        count = 0
        # Check all buildings to the east of r
        for k in range(r + 1, n):
            # Check if building k can be seen from both l and r
            if can_see(heights, l, k) and can_see(heights, r, k):
                count += 1
        
        print(count)


if __name__ == "__main__":
    solve()
