def solve():
    N, Q = map(int, input().split())
    S = input().strip()
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        L -= 1
        R -= 1
        
        substring = S[L:R+1]
        
        # Find the maximum length 11/22 subsequence
        max_length = 0
        
        # Try each slash position in the substring
        for slash_pos in range(len(substring)):
            if substring[slash_pos] != '/':
                continue
            
            # Count 1's before this slash
            count_ones = 0
            for i in range(slash_pos):
                if substring[i] == '1':
                    count_ones += 1
            
            # Count 2's after this slash
            count_twos = 0
            for i in range(slash_pos + 1, len(substring)):
                if substring[i] == '2':
                    count_twos += 1
            
            # The length of the 11/22 string with k ones and k twos
            k = min(count_ones, count_twos)
            if k > 0 or (count_ones == 0 and count_twos == 0):
                # Length is 2*k + 1 (k ones + 1 slash + k twos)
                length = 2 * k + 1
                max_length = max(max_length, length)
        
        print(max_length)

solve()
