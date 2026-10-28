# Write your solution here. Read from stdin, write to stdout.

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    Q = int(input())
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        L -= 1
        R -= 1
        
        # Extract the mochi in range [L, R]
        mochi = A[L:R+1]
        
        # The maximum number of pairs is len(mochi) // 2
        n = len(mochi)
        
        # Try to match mochi[0:n//2] with mochi[n//2:n]
        first_half = mochi[:n//2]
        second_half = mochi[n//2:]
        
        # Use greedy matching: for each mochi in first half (from smallest),
        # try to pair with the smallest available mochi in second half that satisfies constraint
        
        count = 0
        second_idx = 0
        
        for small_mochi in first_half:
            # Find the first mochi in second_half starting from second_idx that satisfies constraint
            found = False
            while second_idx < len(second_half):
                if 2 * small_mochi <= second_half[second_idx]:
                    # Can pair
                    count += 1
                    second_idx += 1
                    found = True
                    break
                second_idx += 1
            
            # If not found, we just move to the next small_mochi
        
        print(count)

solve()
