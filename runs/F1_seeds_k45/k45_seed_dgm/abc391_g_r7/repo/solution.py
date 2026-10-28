MOD = 998244353

def solve():
    N, M = map(int, input().split())
    S = input().strip()
    
    from collections import defaultdict
    
    # dp[i] = dict mapping lcs_row -> count
    # lcs_row is a tuple of N+1 values: lcs(T[:i], S[:j]) for j in 0..N
    # where T is a string of length i we're building
    dp = [defaultdict(int) for _ in range(M + 1)]
    
    # Initially, empty string has lcs[0][j] = 0 for all j
    initial_row = tuple([0] * (N + 1))
    dp[0][initial_row] = 1
    
    # Build strings character by character
    for i in range(M):
        for lcs_row, count in dp[i].items():
            # Try adding each character
            for ch_code in range(26):
                ch = chr(ord('a') + ch_code)
                
                # Compute new lcs_row
                # lcs_row[j] = lcs(T[:i], S[:j])
                # We want new_row[j] = lcs(T[:i+1], S[:j])
                
                # The recurrence is:
                # lcs(T[:i+1], S[:j]) = max(lcs(T[:i], S[:j]), lcs(T[:i], S[:j-1]) + (ch == S[j-1]))
                
                new_row = [0] * (N + 1)
                for j in range(N + 1):
                    if j == 0:
                        new_row[j] = 0
                    elif ch == S[j - 1]:
                        new_row[j] = max(lcs_row[j], lcs_row[j - 1] + 1)
                    else:
                        new_row[j] = max(lcs_row[j], lcs_row[j - 1])
                
                new_row_tuple = tuple(new_row)
                dp[i + 1][new_row_tuple] = (dp[i + 1][new_row_tuple] + count) % MOD
    
    # Count strings by final LCS value
    result = [0] * (N + 1)
    for lcs_row, count in dp[M].items():
        lcs_value = lcs_row[N]  # LCS with entire S
        result[lcs_value] = (result[lcs_value] + count) % MOD
    
    print(' '.join(map(str, result)))

solve()
