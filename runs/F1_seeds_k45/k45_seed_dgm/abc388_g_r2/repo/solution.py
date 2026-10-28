def solve_query(mochi):
    """
    Find the maximum number of kagamimochi that can be made from the given mochi list.
    A pair (a, b) with a <= b forms a kagamimochi if 2*a <= b.
    """
    n = len(mochi)
    
    # Greedy two-pointer approach
    # We try to match mochi from the first half with the second half
    # The key insight: if we sort mochi and try to match first half with second half
    # we should match smallest with smallest possible that works
    
    left = 0  # pointer for smaller mochi
    right = (n + 1) // 2  # pointer for larger mochi, starting from middle
    pairs = 0
    
    while left < (n + 1) // 2 and right < n:
        # Try to match mochi[left] with mochi[right]
        if 2 * mochi[left] <= mochi[right]:
            # This pair works, take it
            pairs += 1
            left += 1
            right += 1
        else:
            # Current mochi[right] is too small for mochi[left]
            # Try next larger mochi
            right += 1
    
    return pairs

# Read input
n = int(input())
A = list(map(int, input().split()))

q = int(input())
for _ in range(q):
    l, r = map(int, input().split())
    # Convert to 0-indexed
    l -= 1
    r -= 1
    # Extract the subarray
    mochi_subset = A[l:r+1]
    # Solve and print result
    print(solve_query(mochi_subset))
