# Write your solution here. Read from stdin, write to stdout.

def solve_query(mochi):
    """
    Given a list of mochi sizes (already sorted in ascending order),
    find the maximum number of kagamimochi that can be made.
    
    A pair (a, b) with a <= b can form a kagamimochi if a <= b/2.
    
    Greedy approach: Match elements from the first half with elements from the second half.
    - left starts at the beginning of the first half
    - right starts at the middle
    - For each element in the first half, try to find an element in the second half
      that it can pair with
    - If current right element works, make the pair and move both pointers
    - If not, move right to the next element (we need a larger mochi)
    """
    n = len(mochi)
    if n < 2:
        return 0
    
    left = 0
    right = (n + 1) // 2
    count = 0
    
    while left < (n + 1) // 2 and right < n:
        # Check if mochi[left] can pair with mochi[right]
        if mochi[left] * 2 <= mochi[right]:
            # Can make a pair
            count += 1
            left += 1
            right += 1
        else:
            # Cannot pair with current right, try next larger mochi
            right += 1
    
    return count


def main():
    n = int(input())
    a = list(map(int, input().split()))
    q = int(input())
    
    for _ in range(q):
        l, r = map(int, input().split())
        # Convert to 0-indexed
        l -= 1
        r -= 1
        
        # Extract the subarray
        subarray = a[l:r+1]
        
        # Solve for this query
        result = solve_query(subarray)
        print(result)


if __name__ == "__main__":
    main()
