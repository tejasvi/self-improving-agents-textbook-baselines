# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read number of mochi
    N = int(input())
    A = list(map(int, input().split()))
    
    # Read number of queries
    Q = int(input())
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        L -= 1
        R -= 1
        
        # Get the mochi in the range
        mochi = A[L:R+1]
        
        # Find maximum number of kagamimochi pairs
        # Use greedy approach with two pointers
        # The array is already sorted
        
        used = [False] * len(mochi)
        pairs = 0
        
        # Try to match from smallest to largest
        # For each potential "top" mochi, find a "base" mochi
        for i in range(len(mochi)):
            if used[i]:
                continue
            
            # Try to find a base mochi for mochi[i]
            # We need mochi[j] such that mochi[i] <= mochi[j] / 2
            # Which means 2 * mochi[i] <= mochi[j]
            for j in range(i + 1, len(mochi)):
                if used[j]:
                    continue
                
                if 2 * mochi[i] <= mochi[j]:
                    # Found a match
                    used[i] = True
                    used[j] = True
                    pairs += 1
                    break
        
        print(pairs)

solve()
