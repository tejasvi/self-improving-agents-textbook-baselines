# Write your solution here. Read from stdin, write to stdout.

def solve_query(mochi_list):
    """
    Find the maximum number of kagamimochi pairs.
    A pair (a, b) where a < b is valid if a <= b/2.
    
    Greedy approach: use two pointers.
    - For each smallest unmatched mochi, try to pair it with the largest 
      unmatched mochi that satisfies the constraint.
    """
    n = len(mochi_list)
    if n < 2:
        return 0
    
    # Sort the mochi (should already be sorted but let's be safe)
    mochi = sorted(mochi_list)
    
    # Two pointers approach
    left = 0  # pointer to smallest unmatched
    right = n - 1  # pointer to largest unmatched
    pairs = 0
    
    while left < right:
        # Check if mochi[left] can be placed on top of mochi[right]
        # Condition: mochi[left] <= mochi[right] / 2
        if mochi[left] * 2 <= mochi[right]:
            # We can make a pair
            pairs += 1
            left += 1
            right -= 1
        else:
            # Can't pair with the largest, try with smaller
            right -= 1
    
    return pairs


def main():
    n = int(input())
    A = list(map(int, input().split()))
    
    q = int(input())
    
    for _ in range(q):
        l, r = map(int, input().split())
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Extract the subarray
        subarray = A[l:r+1]
        
        # Solve for this query
        result = solve_query(subarray)
        print(result)


if __name__ == "__main__":
    main()
