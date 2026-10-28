def can_see(heights, from_idx, to_idx):
    """
    Check if building at to_idx can be seen from building at from_idx.
    from_idx < to_idx (0-indexed)
    """
    target_height = heights[to_idx]
    for i in range(from_idx + 1, to_idx):
        if heights[i] > target_height:
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
            if can_see(heights, l, k) and can_see(heights, r, k):
                count += 1
        
        print(count)


if __name__ == "__main__":
    solve()
