def can_see_from(buildings, start, target):
    """
    Check if building at index 'target' can be seen from building at index 'start'.
    Buildings are 0-indexed.
    """
    if start >= target:
        return False
    
    target_height = buildings[target]
    # Check all buildings between start and target
    for i in range(start + 1, target):
        if buildings[i] > target_height:
            return False
    return True


def solve():
    n, q = map(int, input().split())
    heights = list(map(int, input().split()))
    
    for _ in range(q):
        l, r = map(int, input().split())
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        count = 0
        # Check all buildings to the east of r (indices from r+1 to n-1)
        for k in range(r + 1, n):
            # Check if building k can be seen from both l and r
            if can_see_from(heights, l, k) and can_see_from(heights, r, k):
                count += 1
        
        print(count)


if __name__ == "__main__":
    solve()
