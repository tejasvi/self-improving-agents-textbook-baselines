# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, Q = map(int, input().split())
    S = input().strip()
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        L -= 1
        R -= 1
        
        # Get substring (L to R inclusive in 0-indexed)
        T = S[L:R+1]
        
        max_length = 0
        
        # Try each '/' as the middle character
        for j in range(len(T)):
            if T[j] == '/':
                # Count '1's before position j
                ones_before = sum(1 for i in range(j) if T[i] == '1')
                # Count '2's after position j
                twos_after = sum(1 for i in range(j+1, len(T)) if T[i] == '2')
                
                # Calculate the maximum length 11/22 string with '/' at position j
                k = min(ones_before, twos_after)
                length = 2 * k + 1
                
                max_length = max(max_length, length)
        
        print(max_length)

solve()
