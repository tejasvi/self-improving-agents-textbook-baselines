# Write your solution here. Read from stdin, write to stdout.

def max_kagamimochi(mochi):
    """
    Given a list of mochi sizes (already sorted), find the maximum number
    of kagamimochi that can be made.
    
    A pair (a, b) where a <= b can form a kagamimochi if a <= b/2.
    """
    n = len(mochi)
    if n < 2:
        return 0
    
    # Greedy approach: match smallest with smallest that satisfies condition
    # Use two pointers: left for smaller mochi, right for larger mochi
    left = 0
    right = n // 2
    count = 0
    
    while left < n // 2 and right < n:
        # Check if mochi[left] can be paired with mochi[right]
        # We need: mochi[left] <= mochi[right] / 2
        # Which is: 2 * mochi[left] <= mochi[right]
        if 2 * mochi[left] <= mochi[right]:
            # Can make a pair
            count += 1
            left += 1
            right += 1
        else:
            # mochi[right] is too small, try next larger one
            right += 1
    
    return count


# Read input
N = int(input())
A = list(map(int, input().split()))

Q = int(input())
for _ in range(Q):
    L, R = map(int, input().split())
    # Convert to 0-indexed
    L -= 1
    R -= 1
    
    # Extract the mochi in range [L, R]
    mochi_slice = A[L:R+1]
    
    # Find maximum kagamimochi
    result = max_kagamimochi(mochi_slice)
    print(result)
