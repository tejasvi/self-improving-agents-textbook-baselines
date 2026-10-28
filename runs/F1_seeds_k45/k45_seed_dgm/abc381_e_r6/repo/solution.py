def solve():
    N, Q = map(int, input().split())
    S = input().strip()
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        L -= 1
        R -= 1
        
        # Extract substring
        T = S[L:R+1]
        
        # Find the maximum length of 11/22 subsequence
        max_length = 0
        
        # Try each '/' as the middle character
        for mid_idx in range(len(T)):
            if T[mid_idx] == '/':
                # Count '1's before this '/'
                ones_before = sum(1 for i in range(mid_idx) if T[i] == '1')
                # Count '2's after this '/'
                twos_after = sum(1 for i in range(mid_idx + 1, len(T)) if T[i] == '2')
                
                # Length of 11/22 string is: ones + 1 + twos
                length = ones_before + 1 + twos_after
                max_length = max(max_length, length)
        
        print(max_length)

solve()
