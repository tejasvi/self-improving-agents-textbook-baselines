# Write your solution here. Read from stdin, write to stdout.

def solve_query(arr):
    """
    Given an array of mochi sizes, find the maximum number of kagamimochi pairs.
    A mochi of size a can be placed on top of mochi of size b if a <= b/2.
    """
    n = len(arr)
    
    # We need to pair mochi optimally
    # Strategy: split into two halves, try to match smaller with larger
    # Use greedy two-pointer approach
    
    # For maximum matching, we should try to pair the smallest mochi with larger ones
    # Start from middle and try to match left side with right side
    
    mid = n // 2
    left = arr[:mid]  # smaller mochi
    right = arr[mid:]  # larger mochi
    
    # Try to match greedily: for each mochi in left (smaller), find a mochi in right (larger)
    # that it can be placed on top of
    left_idx = 0
    right_idx = 0
    pairs = 0
    
    while left_idx < len(left) and right_idx < len(right):
        # Check if we can pair left[left_idx] with right[right_idx]
        if left[left_idx] * 2 <= right[right_idx]:
            # We can make a pair
            pairs += 1
            left_idx += 1
            right_idx += 1
        else:
            # Can't pair with this right element, try next one
            right_idx += 1
    
    return pairs


def main():
    N = int(input())
    A = list(map(int, input().split()))
    Q = int(input())
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        L -= 1
        R -= 1
        
        # Extract the subarray
        subarray = A[L:R+1]
        
        # Solve for this query
        result = solve_query(subarray)
        print(result)


if __name__ == "__main__":
    main()
