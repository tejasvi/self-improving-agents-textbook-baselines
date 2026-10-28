MOD = 998244353

def solve():
    N, M = map(int, input().split())
    S = input().strip()
    
    # Algorithm Overview:
    # We count strings of length M by their LCS with S using dynamic programming.
    # 
    # Key Insight: The LCS between a string T (of length m) and S can be computed
    # row-by-row. After adding each character to T, we compute a new row of the
    # LCS DP table. We track all possible LCS row states and count how many strings
    # lead to each state.
    #
    # dp[lcs_row] = count of strings of length m that produce this LCS row
    # where lcs_row[j] = LCS(T[0:m], S[0:j]) for j = 0..N
    #
    # LCS Table Update Rule:
    # Given the previous row (LCS values after m characters), when we add character c:
    # - new_row[0] = 0 (LCS with empty S is always 0)
    # - For j >= 1:
    #   - if c == S[j-1]: new_row[j] = prev_row[j-1] + 1
    #   - else: new_row[j] = max(prev_row[j], new_row[j-1])
    
    # Initialize: empty string has LCS 0 with all prefixes of S
    prev_dp = {tuple([0] * (N + 1)): 1}
    
    # Process each position in the M-length string
    for m in range(M):
        curr_dp = {}
        
        for row, count in prev_dp.items():
            # row[j] = LCS(current_string[0:m], S[0:j])
            
            # Try adding each of 26 lowercase letters
            for c_idx in range(26):
                c = chr(ord('a') + c_idx)
                
                # Compute the new LCS row after adding character c
                new_row = [0] * (N + 1)
                
                for j in range(1, N + 1):
                    if c == S[j - 1]:
                        # Character matches S[j-1], can extend previous LCS
                        new_row[j] = row[j - 1] + 1
                    else:
                        # Character doesn't match, take max of alternatives
                        new_row[j] = max(row[j], new_row[j - 1])
                
                new_row_tuple = tuple(new_row)
                curr_dp[new_row_tuple] = (curr_dp.get(new_row_tuple, 0) + count) % MOD
        
        prev_dp = curr_dp
    
    # Extract results: count strings by their final LCS value (row[N])
    result = [0] * (N + 1)
    for row, count in prev_dp.items():
        lcs_value = row[N]
        result[lcs_value] = (result[lcs_value] + count) % MOD
    
    print(' '.join(map(str, result)))

solve()
