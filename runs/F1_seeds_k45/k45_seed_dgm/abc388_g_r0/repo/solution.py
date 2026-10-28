def max_kagamimochi(mochi):
    """
    Find the maximum number of kagamimochi that can be made from given mochi.
    
    The key insight: use a greedy two-pointer approach.
    Split the mochi into two halves, and try to match each mochi from the first half
    with a mochi from the second half such that small * 2 <= large.
    """
    n = len(mochi)
    if n < 2:
        return 0
    
    # Sort the mochi
    sorted_mochi = sorted(mochi)
    
    # Use greedy approach: for each mochi in the first half,
    # try to pair it with a mochi in the second half
    # We want small * 2 <= large
    
    # Two pointer approach:
    # Start from the middle, try to match mochi from left with mochi from right
    left = 0  # pointer for smaller mochi
    right = n // 2  # pointer for larger mochi (start from middle)
    count = 0
    
    while left < n // 2 and right < n:
        if sorted_mochi[left] * 2 <= sorted_mochi[right]:
            # We can pair these two
            count += 1
            left += 1
            right += 1
        else:
            # We need a larger mochi for the current small one
            right += 1
    
    return count


def main():
    N = int(input())
    A = list(map(int, input().split()))
    Q = int(input())
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        L -= 1
        R -= 1
        
        # Extract the range of mochi
        mochi_range = A[L:R+1]
        
        # Find maximum kagamimochi
        result = max_kagamimochi(mochi_range)
        print(result)


if __name__ == "__main__":
    main()
